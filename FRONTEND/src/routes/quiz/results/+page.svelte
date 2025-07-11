<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { toast } from '@zerodevx/svelte-toast'; 

  const API_BASE = import.meta.env.VITE_API_BASE;

  let currentUser, quizResults = [], loading = true, error = '';
  let detail = null, detailLoading = false, detailError = '';

  onMount(async () => {
    currentUser = JSON.parse(localStorage.getItem('user'));
    if (!currentUser || currentUser.role !== 'student') goto('/login');

    try {
      const res = await fetch(`${API_BASE}/student/${currentUser.id}/submissions`);
      const data = await res.json();
      quizResults = res.ok ? data : (error = data.error || 'Failed to load.');
    } catch {
      error = 'Server error.';
    } finally {
      loading = false;
    }
  });

  function viewLeaderboard(qid, score) {
    if (score == null) {
      toast.push('❌ This quiz has not been reviewed by the teacher yet.');
      return;
    }
    goto(`/quiz/leaderboard/${qid}`);
  }

  async function viewAnswers(qid) {
    detailLoading = true;
    detailError = '';
    detail = null;

    try {
      const res = await fetch(`${API_BASE}/student/${currentUser.id}/submission/${qid}`);
      const data = await res.json();
      if (res.ok) detail = data;
      else detailError = data.error;
    } catch {
      detailError = 'Fetch error.';
    } finally {
      detailLoading = false;
    }
  }
</script>

<style>
  body {
  background: linear-gradient(135deg, #1e1e1e, #222831, #1b262c);
  color: #e0e0e0;
  font-family: 'Playpen Sans Thai', cursive;
}

h2 {
  font-family: 'Quintessential', cursive;
  font-size: 2rem;
  margin-bottom: 20px;
  color: #d6e6ff;
}

.table {
  border-radius: 10px;
  overflow: hidden;
}

.table th {
  background-color: #2d2f34;
  color: #ffd369;
  font-weight: 600;
  border: none;
}

.table td {
  background-color: rgba(38, 42, 48, 0.9);
  color: #f1f1f1;
  border: none;
}

.table td:first-child {
  font-weight: 600;
  color: #00adb5;
}

.table td:last-child {
  display: flex;
  gap: 0.5rem;
}

.btn-outline-success,
.btn-outline-info {
  font-size: 0.85rem;
  padding: 4px 10px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-outline-success:hover {
  background-color: #00c897;
  color: #000;
}

.btn-outline-info:hover {
  background-color: #00bcd4;
  color: #000;
}

/* Quiz Detail Card */
.card.detail {
  background: rgba(36, 41, 52, 0.9); /* dark smoky blue */
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  color: #ffffff;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
}



.card h4 {
  font-size: 1.5rem;
  color: #fbd46d;
}

.card p, .card strong {
  font-size: 0.95rem;
  line-height: 1.6;
}

.card ul {
  padding-left: 18px;
}

.card li {
  margin-bottom: 5px;
  font-weight: 500;
}


</style>


<div class="container mt-4">
  <h2 class="text-white mb-4">📊 Your Quiz Results</h2>

  {#if loading}
    <p class="text-light">Loading...</p>
  {:else if error}
    <div class="alert alert-danger">{error}</div>
  {:else if quizResults.length === 0}
    <p class="text-warning">You haven't submitted any quizzes yet.</p>
  {:else}
    <table class="table table-bordered table-dark table-hover">
      <thead>
        <tr>
          <th>Quiz Title</th>
          <th>Submitted At</th>
          <th>Time Taken</th>
          <th>Score (%)</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {#each quizResults as quiz}
          <tr>
            <td>{quiz.title}</td>
            <td>{quiz.submitted_at}</td>
            <td>{quiz.time_taken} sec</td>
            <td>{quiz.score == null ? 'Not reviewed yet' : `${quiz.score.toFixed(2)}%`}</td>
            <td>
                <button class="btn btn-sm btn-outline-success me-1" on:click={() => viewLeaderboard(quiz.quiz_id, quiz.score)}>
                📊 Leaderboard
                </button>
                <button class="btn btn-sm btn-outline-info" on:click={() => viewAnswers(quiz.quiz_id)}>
                📄 View My Answers
                </button>
            </td>
        </tr>
        {/each}
      </tbody>
    </table>
  {/if}

  {#if detailLoading}
  <p>Loading...</p>
{:else if detailError}
  <div class="alert alert-danger">{detailError}</div>
{:else if detail}
  <div class="card detail text-dark p-3 mt-4 text-white " style="margin-bottom: 20px">
    <h4>Your Quiz Answers</h4>
    <p><em>Submitted at: {detail.submitted_at}</em></p>
    <p>Time Taken: {detail.time_taken} sec</p>
    {#each detail.answers as a,i}
      <div class="mb-3">
        <strong>Q{i+1}:</strong> {a.question}
        {#if a.options}
          <ul>
            {#each a.options as opt}
              <li style="color: {opt === a.correct_answer ? 'green' : (opt === a.student_answer ? 'red' : 'black')}">
                {opt} {opt === a.correct_answer ? ' ✅' : opt === a.student_answer ? ' 🔴' : ''}
              </li>
            {/each}
          </ul>
        {:else}
          <p><b><u>Your answer:</u></b> {a.student_answer}</p>
          <p><b><u>Expected:</u></b> {a.correct_answer || '—'}</p>
        {/if}
      </div>
    {/each}
    <p><strong>Score:</strong> {detail.score != null ? `${detail.score.toFixed(2)}%` : 'Not reviewed'}</p>
  </div>
{/if}

</div>

