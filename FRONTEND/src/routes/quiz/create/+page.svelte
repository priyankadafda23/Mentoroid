<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let currentUser;
  let selectedCourse = '';
  let courses = [];
  let newQuestion = {
    question: '',
    type: 'short',
    options: [],
    answer: ''
  };
  let newOption = '';
  let questions = [];
  let instructions = '';
  let error = '';
  let toast = '';
  let title='';

  onMount(async () => {
    currentUser = JSON.parse(localStorage.getItem('user'));
    if (!currentUser || currentUser.role !== 'teacher') {
      return goto('/login');
    }

    const res = await fetch(`${API_BASE}/dashboard/teacher?id=${currentUser.id}`);
    const data = await res.json();
    courses = data.my_courses || [];
  });

  function addOption() {
    if (newOption.trim()) {
      newQuestion.options.push(newOption.trim());
      newOption = '';
    }
  }

  function addQuestion() {
    error = '';

    if (!newQuestion.question || !newQuestion.type) {
      error = 'Please provide question and type.';
      return;
    }

    if (newQuestion.type === 'mcq' && newQuestion.options.length < 2) {
      error = 'MCQ requires at least 2 options.';
      return;
    }

    const questionToAdd = {
      text: newQuestion.question,
      type: newQuestion.type,
      options: newQuestion.type === 'mcq' ? [...newQuestion.options] : null,
      correct_option: newQuestion.answer
};

    questions = [...questions, questionToAdd];

    newQuestion = { question: '', type: 'short', options: [], answer: '' };
    newOption = '';
    toast = '✅ Question added successfully!';
    setTimeout(() => (toast = ''), 3000);
  }

  async function submitQuiz() {
    error = '';
    toast = '';

    // ✅ Only validate course, instructions, and questions
    if (!selectedCourse || !instructions.trim() || questions.length === 0) {
      error = 'Please select a course, write instructions, and add at least one question.';
      return;
    }

    const payload = {
      course_id: selectedCourse,
      teacher_id: currentUser.id,
      instructions,
      questions,
      title
    };

    try {
      const res = await fetch('${API_BASE}/quiz/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const result = await res.json();
      if (res.ok) {
        toast = '✅ Quiz created!';
        setTimeout(() => goto('/dashboard/teacher'), 2000);
      } else {
        error = result.error || 'Something went wrong.';
      }
    } catch (err) {
      console.error(err);
      error = 'Error submitting quiz.';
    }
  }
</script>


<div class="container mt-4">
  <h2 class="mb-4" style="font-family: Caveat, cursive;">Create Quiz</h2>

  <!-- Course Selector -->
  <div class="mb-3">
    <label>Select Course</label>
    <select class="form-control" bind:value={selectedCourse}>
      <option value="">-- Select Course --</option>
      {#each courses as course}
        <option value={course.id}>{course.title}</option>
      {/each}
    </select>
  </div>

  <!-- Instructions -->
  <div class="mb-3">
    <label>Quiz Title</label>
    <input class="form-control" type="text" bind:value={title} placeholder="Enter quiz title" required/>
</div>

  <div class="mb-3">
    <label>Quiz Instructions</label>
    <textarea class="form-control" rows="2" bind:value={instructions} placeholder="Write brief instructions..."></textarea>
  </div>

  <!-- Question Builder -->
  <div class="card card-body bg-light text-black">
    <h5 style="font-family: Caveat, cursive;">Add Question</h5>

    <div class="mb-2">
      <label>Question</label>
      <input class="form-control" bind:value={newQuestion.question} />
    </div>

    <div class="mb-2">
      <label>Type</label>
      <select class="form-control" bind:value={newQuestion.type}>
        <option value="short">Short Answer</option>
        <option value="long">Long Answer</option>
        <option value="number">Number Only</option>
        <option value="mcq">Multiple Choice</option>
      </select>
    </div>

    {#if newQuestion.type === 'mcq'}
      <div class="mb-2">
        <label>Options</label>
        <div class="input-group">
          <input class="form-control" placeholder="Enter option" bind:value={newOption} />
          <button class="btn btn-outline-secondary" on:click={addOption}>Add</button>
        </div>
        {#each newQuestion.options as opt, i}
          <div class="text-black small">Option {i + 1}: {opt}</div>
        {/each}
      </div>
    {/if}

    <div class="mb-2">
      <label>Answer</label>
      <input class="form-control" bind:value={newQuestion.answer} />
    </div>

    <button class="btn btn-warning w-100" on:click={addQuestion}>
      ➕ Add Question
    </button>
  </div>

  {#if questions.length > 0}
    <div class="card card-body bg-dark text-white mt-4">
      <h5 class="mb-3" style="font-family: Caveat, cursive;">Quiz Preview</h5>

      <ol>
        {#each questions as q, i}
          <li class="mb-2">
            <strong>{q.question}</strong> ({q.type})
            {#if q.type === 'mcq'}
              <ul>
                {#each q.options as opt}
                  <li>{opt}</li>
                {/each}
              </ul>
            {/if}
            <div class="text-muted small">Answer: {q.answer}</div>
          </li>
        {/each}
      </ol>

      <button class="btn btn-success mt-3" on:click={submitQuiz}>🚀 Submit Quiz</button>
    </div>
  {/if}

  {#if error}
    <div class="alert alert-danger mt-3">{error}</div>
  {/if}

  {#if toast}
    <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index:9999;">
      <div class="toast show align-items-center text-white bg-success border-0" role="alert">
        <div class="d-flex">
          <div class="toast-body">{toast}</div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" on:click={() => (toast = '')}></button>
        </div>
      </div>
    </div>
  {/if}
</div>
