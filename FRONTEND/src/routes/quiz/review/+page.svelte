<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  const API_BASE = import.meta.env.VITE_API_BASE;
  
  let quizzes = [];
  let loading = true;
  let error = null;
  
  // Function to fetch quizzes from backend
  async function fetchQuizzes() {
    try {
      console.log('Fetching quizzes...');
      const response = await fetch(`${API_BASE}/quizzes`);
      console.log('Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Fetched data:', data);
        quizzes = data;
        error = null;
      } else {
        const errorData = await response.json();
        error = errorData.error || 'Failed to fetch quizzes';
        console.error('Error response:', errorData);
      }
    } catch (err) {
      console.error('Fetch error:', err);
      error = 'Unable to connect to server';
    } finally {
      loading = false;
    }
  }
  
  // Load quizzes when component mounts
  onMount(() => {
    fetchQuizzes();
  });
  
  // Navigate to specific quiz leaderboard
  function viewLeaderboard(quizId) {
    goto(`/quiz/review/${quizId}`);
  }
  
  // Refresh quizzes
  function refresh() {
    loading = true;
    fetchQuizzes();
  }
</script>

<div class="container">
  <div class="header">
    <h1 class="text-white">Quiz Leaderboards</h1>
    <button class="refresh-btn" on:click={refresh} disabled={loading}>
      {#if loading}
        Loading...
      {:else}
        Refresh
      {/if}
    </button>
  </div>
  
  {#if error}
    <div class="error">
      <h3>Error</h3>
      <p>{error}</p>
      <button on:click={refresh}>Try Again</button>
    </div>
  {/if}
  
  {#if loading}
    <div class="loading">
      <p>Loading quizzes...</p>
    </div>
  {/if}
  
  {#if !loading && !error}
    {#if quizzes.length === 0}
      <div class="no-quizzes">
        <h3>No Quizzes Found</h3>
        <p>There are no quizzes available at the moment.</p>
      </div>
    {:else}
      <div class="quiz-grid">
        {#each quizzes as quiz}
          <div class="quiz-card">
            <h3>{quiz.title}</h3>
            {#if quiz.instructions}
              <p class="instructions">{quiz.instructions.substring(0, 100)}...</p>
            {/if}
            <p class="date">Created: {quiz.created_at}</p>
            <button 
              class="view-btn" 
              on:click={() => viewLeaderboard(quiz.id)}
            >
              Assign Marks
            </button>
          </div>
        {/each}
      </div>
    {/if}
  {/if}
</div>

<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
  }
  
  .header h1 {
    color: #333;
    margin: 0;
  }
  
  .refresh-btn {
    background: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .refresh-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
  }
  
  .error {
    background: #f8d7da;
    color: #721c24;
    padding: 20px;
    border-radius: 5px;
    margin-bottom: 20px;
  }
  
  .loading {
    text-align: center;
    padding: 40px;
    color: #666;
  }
  
  .no-quizzes {
    text-align: center;
    padding: 40px;
    color: #666;
  }
  
  .quiz-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .quiz-card {
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s;
  }
  
  .quiz-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  }
  
  .quiz-card h3 {
    color: #333;
    margin-bottom: 10px;
  }
  
  .instructions {
    color: #666;
    font-size: 14px;
    margin-bottom: 10px;
  }
  
  .date {
    color: #999;
    font-size: 12px;
    margin-bottom: 15px;
  }
  
  .view-btn {
    background: #28a745;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    width: 100%;
  }
  
  .view-btn:hover {
    background: #218838;
  }
</style>