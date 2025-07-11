<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let currentUser = null;
  let courses = [];
  let courseIdToEdit = "";
  let error = "";

  onMount(async () => {
    currentUser = JSON.parse(localStorage.getItem('user'));
    if (!currentUser || currentUser.role !== 'teacher') {
      goto('/login');
      return;
    }

    const res = await fetch(`${API_BASE}/dashboard/teacher?id=${currentUser.id}`);
    const data = await res.json();
    courses = data.my_courses || [];
  });

  async function handleEditSubmit(e) {
    e.preventDefault();
    error = "";

    if (!courseIdToEdit) return;

    // Check if the entered course ID exists in the teacher's course list
    const courseExists = courses.some(course => course.id === parseInt(courseIdToEdit));
    
    if (courseExists) {
      goto(`/courses/edit/${courseIdToEdit}`);
    } else {
      error = "You are not authorized to edit this course.";
    }
  }
</script>

<div class="container mt-4">
  <h2 class="mb-3">Update Existing Course</h2>

  <div class="mb-4">
    <h5>Your Courses:</h5>
    <ul class="list-group">
      {#each courses as course}
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <span>{course.title}</span>
          <span class="badge bg-primary">ID: {course.id}</span>
        </li>
      {/each}
    </ul>
  </div>

  <form on:submit={handleEditSubmit} class="mb-3">
    <div class="mb-3">
      <label>Enter Course ID to Edit:</label>
      <input type="number" class="form-control" bind:value={courseIdToEdit} required />
    </div>
    <button class="btn btn-success">Continue to Edit</button>
  </form>

  <!-- 🔔 Toast for Unauthorized Access -->
  {#if error}
    <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 9999; margin-top: 70px;">
      <div class="toast show align-items-center text-white bg-danger border-0" role="alert" aria-live="assertive" aria-since="true">
        <div class="d-flex">
          <div class="toast-body">{error}</div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" on:click={() => error = ""}></button>
        </div>
      </div>
    </div>
  {/if}
</div>