<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let quizId = '';
  let currentUser;
  let submissions = [];
  let selectedSubmission = null;
  let detailedSubmission = null;
  let manualScore = 0;
  let feedback = '';

  $: page.subscribe(p => {
    quizId = p.params.id;
  });

  onMount(async () => {
    currentUser = JSON.parse(localStorage.getItem('user'));
    if (!currentUser || currentUser.role !== 'teacher') {
      return goto('/login');
    }

    await fetchSubmissions();
  });

  async function fetchSubmissions() {
    const res = await fetch(`${API_BASE}/quiz/${quizId}/submissions`);
    const data = await res.json();

    if (res.ok) {
      submissions = data;
    } else {
      alert(data.error || 'Failed to fetch submissions.');
    }
  }

  async function selectSubmission(sub) {
    selectedSubmission = sub;
    manualScore = sub.score;
    feedback = '';

    const res = await fetch(`${API_BASE}/quiz/${quizId}/submission/${sub.student_id}`);
    const data = await res.json();

    if (res.ok) {
        detailedSubmission = data;
    } else {
        alert(data.error || 'Failed to load detailed submission.');
    }
    }

  async function submitScore() {
    const res = await fetch(`${API_BASE}/quiz/${quizId}/score/${selectedSubmission.student_id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        score: manualScore,
        feedback
      })
    });

    const data = await res.json();

    if (res.ok) {
      alert('✅ Score updated successfully!');
      selectedSubmission.score = manualScore;
      selectedSubmission = null;
      await fetchSubmissions();
    } else {
      alert(data.error || 'Failed to update score.');
    }
  }
</script>

<div class="container mt-4">
  <h3>📋 Review Quiz Submissions</h3>

  {#if submissions.length === 0}
    <p class="text-warning">No submissions found for this quiz.</p>
  {:else}
    <table class="table table-bordered table-hover table-dark mt-3">
      <thead>
        <tr>
          <th>Student Name</th>
          <th>Submitted At</th>
          <th>Time Taken</th>
          <th>Score (%)</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {#each submissions as sub}
          <tr>
            <td>{sub.student_name}</td>
            <td>{sub.submitted_at}</td>
            <td>{sub.time_taken} sec</td>
            <td>{sub.score.toFixed(2)}</td>
            <td>
              <button class="btn btn-info btn-sm" on:click={() => selectSubmission(sub)}>Review</button>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}

  {#if selectedSubmission}
    <div class="card card-body mt-4 text-black">
      <h5>Reviewing Submission: {selectedSubmission.student_name}</h5>

      <p><strong>Submitted:</strong> {selectedSubmission.submitted_at}</p>
      <p><strong>Time Taken:</strong> {selectedSubmission.time_taken} seconds</p>

      {#if detailedSubmission}
  <div class="card card-body mt-4 text-black bg-light">
    <h5>📘 Answers Review</h5>

    <ol>
      {#each detailedSubmission.answers as ans, i}
        <li class="mb-3">
          <p><strong>Q{i + 1}: {ans.question}</strong></p>
          {#if ans.options}
            <ul>
              {#each ans.options as opt}
                <li style="color: {opt === ans.correct_answer ? 'green' : (opt === ans.student_answer ? 'red' : 'black')}">
                  {opt}
                  {#if opt === ans.correct_answer}
                    <strong> ✅ Correct</strong>
                  {:else if opt === ans.student_answer}
                    <strong> ❌ Selected</strong>
                  {/if}
                </li>
              {/each}
            </ul>
          {:else}
            <p><strong>Answer:</strong> {ans.student_answer}</p>
            <p><strong>Expected:</strong> {ans.correct_answer || 'N/A (manual grading)'}</p>
          {/if}
        </li>
      {/each}
    </ol>
  </div>
{/if}


      <label>Manual Score (%)</label>
      <input class="form-control mb-2" type="number" min="0" max="100" bind:value={manualScore} />

      <label>Feedback (optional)</label>
      <textarea class="form-control mb-2" bind:value={feedback} placeholder="Give feedback or comments..."></textarea>

      <button class="btn btn-success me-2" on:click={submitScore}>💾 Save Score</button>
      <button class="btn btn-secondary" on:click={() => (selectedSubmission = null)}>❌ Cancel</button>
    </div>
  {/if}
</div>
