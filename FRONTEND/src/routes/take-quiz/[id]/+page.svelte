<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { toast } from '@zerodevx/svelte-toast';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let quizId = '';
  let quiz = { questions: [] };
  let answers = {};
  let startTime = null;
  let timer = 0;
  let interval;
  let currentUser;
  let quizStarted = false;

  $: page.subscribe(p => {
    quizId = p.params.id;
  });

  onMount(async () => {
    currentUser = JSON.parse(localStorage.getItem('user'));

    if (!currentUser || currentUser.role !== 'student') {
      return goto('/login');
    }

    const res = await fetch(`${API_BASE}/quiz/${quizId}`);
    const data = await res.json();

    if (!res.ok || !data || !data.questions) {
      alert("Quiz not found!");
      return goto('/dashboard/student');
    }

    quiz = data;
    console.log('✅ Quiz Loaded:', quiz);
    console.log("🎯 Quiz questions loaded:", quiz.questions);


  });

  function startQuiz() {
    quizStarted = true;
    startTime = new Date();
    interval = setInterval(() => {
      timer += 1;
    }, 1000);
  }

  function allQuestionsAnswered() {
    return quiz.questions.every(q => answers[q.id] !== undefined && answers[q.id] !== '');
  }

  async function submitQuiz() {
    clearInterval(interval);
    const endTime = new Date();

    const answerList = Object.entries(answers).map(([question_id, answer]) => ({
      question_id: parseInt(question_id),
      answer
    }));

    const timeTaken = Math.floor((endTime - startTime) / 1000); 

    const payload = {
      student_id: currentUser.id,
      answers: answerList,
      time_taken: timeTaken,
      score : score
    };


    const res = await fetch(`${API_BASE}/submit-quiz/${quizId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });


    const result = await res.json();
    if (res.ok) {
      toast.push(`✅ Quiz submitted successfully! You scored ${result.score}`);
      setTimeout(() => {
        goto(`/quiz/leaderboard/${quizId}`);
      }, 5000);
    } else {
      alert(result.error || '❌ Submission failed');
    }
  }
</script>

<div class="container mt-4">
  <h3 class="mb-3">{quiz.title || "Quiz"}</h3>
  <p>{quiz.instructions}</p>

  {#if !quizStarted}
    <button class="btn btn-primary" on:click={startQuiz}>🚀 Start Quiz</button>
  {:else if quiz.questions.length > 0}
    <div>
      <div class="text-end text-danger fw-bold">⏱ Time: {timer} sec</div>

      {#each quiz.questions as q, i}
        <div class="card mb-3 p-3">
          <h5>Q{i + 1}: {q.text}</h5>

          {#if q.type === 'short'}
            <input class="form-control" on:input={e => answers[q.id] = e.target.value} required />
          {:else if q.type === 'long'}
            <textarea class="form-control" on:input={e => answers[q.id] = e.target.value} required></textarea>
          {:else if q.type === 'number'}
            <input type="number" class="form-control" on:input={e => answers[q.id] = e.target.value} required />
          {:else if q.type === 'mcq'}
            {#each q.options as opt}
              <div>
                <input type="radio" bind:group={answers[q.id]} value={opt} required/> {opt}
              </div>
            {/each}
          {/if}
        </div>
      {/each}

      <button class="btn btn-success mt-3" on:click={submitQuiz}>
        ✅ Submit Quiz
      </button>
    </div>
    {:else if quizStarted && (!quiz.questions || quiz.questions.length === 0)}
      <p class="text-warning">⚠️ No questions found for this quiz.</p>

    {:else}
  <p class="text-warning">⚠️ Loading quiz questions...</p>
{/if}
</div>
