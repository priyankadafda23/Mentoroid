<script>
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  let quiz = [], score = 0;

  const API_BASE = import.meta.env.VITE_API_BASE;

  onMount(async () => {
    const id = $page.params.id;
    const res = await fetch(`${API_BASE}/quiz/${id}`);
    quiz = await res.json();
  });

  function submit() {
    alert(`Score: ${score} / ${quiz.length}`);
  }
</script>

<h2>Quiz</h2>
{#each quiz as q, i}
  <div>
    <p>{q.question}</p>
    {#each q.options as opt}
      <input type="radio" name={`q${i}`} value={opt} on:change={() => { if (opt == q.answer) score += 1 }} /> {opt}<br>
    {/each}
  </div>
{/each}

<button on:click={submit}>Submit Quiz</button>