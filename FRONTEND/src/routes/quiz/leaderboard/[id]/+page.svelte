<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let quizId = '';
  let leaderboardData = [];
  let loading = true;
  let error = null;
  let currentUserScore = null;
  let studentId = null;

  // Get current user from localStorage or session
  onMount(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      const user = JSON.parse(userData);
      studentId = user.id;
      userRole = user.role;
    }
  });

  $: page.subscribe(p => {
    quizId = p.params.id;
    // Get score from URL params if available
    const urlParams = new URLSearchParams(p.url.searchParams);
    currentUserScore = urlParams.get('score');
    
    // Load leaderboard when quiz ID changes
    if (quizId) {
      loadLeaderboard();
    }
  });

  async function loadLeaderboard() {
    if (!quizId) return;

    try {
        loading = true;
        error = null;
        
        console.log(`Fetching leaderboard for quiz ${quizId}`);
        
        const response = await fetch(`${API_BASE}/leaderboard/${quizId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch leaderboard: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Leaderboard data:', data);
        
        // Transform data to match expected format
        leaderboardData = data.map(item => ({
            student_id: item.student_id,
            student_name: item.student_name,
            time_taken: item.time_taken,
            score: item.score,
            submitted_at: item.submitted_at
        }));
        
        loading = false;
        
    } catch (err) {
        console.error('Error loading leaderboard:', err);
        error = err.message;
        loading = false;
    }
}

  // Refresh leaderboard manually
  async function refreshLeaderboard() {
    await loadLeaderboard();
  }

  // Format time helper function
  function formatTime(seconds) {
    if (!seconds || isNaN(seconds)) return 'N/A';

    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
  }

  // Format date helper function (improved robustness)
  function formatDate(dateString) {
    if (!dateString) return 'N/A';

    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        return 'Invalid Date';
      }
      return date.toLocaleString();
    } catch {
      return 'Invalid Date';
    }
  }

  // Get rank emoji
  function getRankEmoji(index) {
    switch(index) {
      case 0: return '🥇';
      case 1: return '🥈';
      case 2: return '🥉';
      default: return `${index + 1}`;
    }
  }

  // Get score color based on percentage
  function getScoreColor(score) {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'danger';
  }

  // Check if current user
  function isCurrentUser(submission) {
    return studentId && submission.student_id === studentId;
  }

  // Get user's rank
  function getUserRank() {
    if (!studentId) return null;
    
    const userSubmission = leaderboardData.find(sub => sub.student_id === studentId);
    if (!userSubmission) return null;
    
    return leaderboardData.indexOf(userSubmission) + 1;
  }

  function goToDashboard() {
  const userData = localStorage.getItem('user');
  if (userData) {
    const user = JSON.parse(userData);
    if (user.role === 'teacher') {
      goto('/dashboard/teacher');
    } else {
      goto('/dashboard/student');
    }
  } else {
    // Fallback if user not found (optional)
    goto('/login');
  }
}

</script>

<div class="container mt-4">
  <div class="row">
    <div class="col-lg-10 mx-auto">
      <div class="card shadow-lg">
        <div class="card-header bg-primary text-white">
          <div class="d-flex justify-content-between align-items-center">
            <h3 class="mb-0">
              🏆 Leaderboard for Quiz {quizId}
            </h3>
          </div>
        </div>

        <div class="card-body">
          <!-- Current User Score Display -->
          {#if currentUserScore !== null && userRole === 'student'}
            <div class="alert alert-success mb-2">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h5 class="alert-heading">🎉 Quiz Completed!</h5>
                  <p class="mb-0">Your Score: <strong>{currentUserScore}%</strong></p>
                </div>
                {#if getUserRank()}
                  <div class="text-end">
                    <small class="text-muted">Your Rank: #{getUserRank()}</small>
                  </div>
                {/if}
              </div>
            </div>
          {/if}


          <!-- Loading State -->
          {#if loading}
            <div class="text-center py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="mt-3 text-muted">Loading leaderboard...</p>
            </div>

          <!-- Error State -->
          {:else if error}
            <div class="alert alert-danger">
              <h5 class="alert-heading">❌ Error</h5>
              <p class="mb-3">{error}</p>
              <button class="btn btn-danger btn-sm" on:click={refreshLeaderboard}>
                Try Again
              </button>
            </div>

          <!-- Empty State -->
          {:else if leaderboardData.length === 0}
            <div class="text-center py-5">
              <div class="mb-3">
                <i class="fas fa-clipboard-list fa-3x text-muted"></i>
              </div>
              <h5 class="text-muted">No submissions yet</h5>
              <p class="text-muted">Be the first to take this quiz!</p>
              <button class="btn btn-primary" on:click={() => goto(`/quiz/${quizId}`)}>
                Take Quiz
              </button>
            </div>

          <!-- Leaderboard Table -->
          {:else}
            <div class="mb-3">
              <p class="text-muted mb-0">
                <i class="fas fa-users me-1"></i>
                Total Submissions: <strong>{leaderboardData.length}</strong>
              </p>
            </div>

            <div class="table-responsive">
              <table class="table table-hover">
                <thead class="table-dark">
                  <tr>
                    <th scope="col" class="text-center">Rank</th>
                    <th scope="col">Student</th>
                    <th scope="col" class="text-center">Score</th>
                    <th scope="col" class="text-center">Time</th>
                    <th scope="col" class="text-center">Submitted</th>
                  </tr>
                </thead>
                <tbody>
                  {#each leaderboardData as submission, index}
                    <tr class="align-middle {isCurrentUser(submission) ? 'table-info' : ''}">
                      <!-- Rank -->
                      <td class="text-center">
                        <span class="fs-4 fw-bold">
                          {getRankEmoji(index)}
                        </span>
                      </td>
                      
                      <!-- Student Name -->
                      <td>
                        <div class="d-flex align-items-center">
                          <div class="avatar bg-primary text-white rounded-circle me-3 d-flex align-items-center justify-content-center" 
                               style="width: 40px; height: 40px; font-size: 16px;">
                            {submission.student_name.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <strong class="d-block">{submission.student_name}</strong>
                            {#if isCurrentUser(submission)}
                              <small class="text-primary">👤 You</small>
                            {/if}
                          </div>
                        </div>
                      </td>
                      
                      <!-- Score -->
                      <td class="text-center">
                        <span class="badge bg-{getScoreColor(submission.score)} fs-6 px-3 py-2">
                          {submission.score}%
                        </span>
                      </td>
                      
                      <!-- Time Taken -->
                      <td class="text-center">
                        <span class="text-muted fw-medium">
                          <i class="fas fa-clock me-1"></i>
                          {formatTime(submission.time_taken)}
                        </span>
                      </td>
                      
                      <!-- Submitted At -->
                      <td class="text-center">
                        <small class="text-muted">
                          {formatDate(submission.submitted_at)}
                        </small>
                      </td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>

            <!-- Statistics -->
            <div class="row mt-4">
              <div class="col-md-4">
                <div class="card bg-light">
                  <div class="card-body text-center">
                    <h5 class="card-title text-primary">Highest Score</h5>
                    <h3 class="text-success">{leaderboardData[0]?.score || 0}%</h3>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="card bg-light">
                  <div class="card-body text-center">
                    <h5 class="card-title text-primary">Average Score</h5>
                    <h3 class="text-info">
                      {leaderboardData.length > 0 ? 
                        Math.round(leaderboardData.reduce((sum, sub) => sum + sub.score, 0) / leaderboardData.length) : 0}%
                    </h3>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="card bg-light">
                  <div class="card-body text-center">
                    <h5 class="card-title text-primary">Fastest Time</h5>
                    <h3 class="text-warning">
                      {formatTime(Math.min(...leaderboardData.map(sub => sub.time_taken)))}
                    </h3>
                  </div>
                </div>
              </div>
            </div>
          {/if}
        </div>

        <!-- Footer -->
        <div class="card-footer bg-light">
          <div class="d-flex justify-content-between align-items-center">
            <button class="btn btn-outline-primary" on:click={goToDashboard}>
              <i class="fas fa-arrow-left me-1"></i>
              Back to Dashboard
            </button>
              
              {#if leaderboardData.length > 0}
                <button class="btn btn-outline-secondary" on:click={refreshLeaderboard}>
                  <i class="fas fa-sync-alt me-1"></i>
                  Refresh
                </button>
              {/if}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

<style>
  .avatar {
    min-width: 40px;
    min-height: 40px;
  }

  .table th {
    border-top: none;
    font-weight: 600;
  }

  .card {
    border-radius: 15px;
    border: none;
  }

  .card-header {
    border-radius: 15px 15px 0 0;
    padding: 1.5rem;
  }

  .table-responsive {
    border-radius: 10px;
  }

  .table-info {
    background-color: rgba(13, 202, 240, 0.1);
  }

  .badge {
    font-size: 0.9rem;
  }

  .card-body {
    padding: 1rem;
  }

  .card-footer {
    border-radius: 0 0 15px 15px;
  }

  .btn {
    border-radius: 8px;
  }

  .alert {
    border-radius: 10px;
  }

  .spinner-border {
    width: 3rem;
    height: 3rem;
  }
</style>