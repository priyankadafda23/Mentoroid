<script>
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let title = "";
  let description = "";
  let thumbnail = null;
  let youtubeLink = "";
  let success = "";
  let error = "";

  let currentUser;

  onMount(() => {
    currentUser = JSON.parse(localStorage.getItem("user"));
    if (!currentUser || currentUser.role !== 'teacher') {
      goto('/login');
    }
  });

  async function handleSubmit(e) {
    e.preventDefault();

    if (!title || !description || !youtubeLink) {
      error = "All fields except Thumbnail Image are required!";
      return;
    }

    const formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);
    formData.append("thumbnail", thumbnail);
    formData.append("teacher_id", currentUser?.id);
    formData.append("youtube_link", youtubeLink);

    try {
      const res = await fetch(`${API_BASE}/create-course`, {
        method: "POST",
        body: formData
      });

      const result = await res.json();

      if (res.ok) {
        success = "Course created successfully!";
        error = "";
        setTimeout(() => goto('/dashboard/teacher'), 5000);
      } else {
        error = result.error || "Failed to create course.";
        success = "";
      }
    } catch (err) {
      console.error(err);
      error = "Something went wrong.";
    }
  }
</script>

<div class="container mt-4">
  <h2 class="mb-4">Create New Course</h2>

  <form on:submit={handleSubmit}>
    <div class="mb-3">
      <label>Course Title</label>
      <input type="text" class="form-control" bind:value={title} required />
    </div>

    <div class="mb-3">
      <label>Description</label>
      <textarea class="form-control" bind:value={description} required></textarea>
    </div>

    <div class="mb-3">
      <label>Thumbnail</label>
      <input type="file" class="form-control" on:change={e => thumbnail = e.target.files[0]} />
    </div>

    <div class="mb-3">
      <label>YouTube Video URL</label>
      <input type="url" class="form-control" bind:value={youtubeLink} placeholder="https://youtube.com/..."  required />
    </div>

    <button class="btn btn-success">Create Course</button>
  </form>
  </div>

<!-- Error Toast -->
{#if error}
  <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 9999; margin-top: 70px;">
    <div class="toast show align-items-center text-white bg-danger border-0" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body">{error}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" on:click={() => error = ""}></button>
      </div>
    </div>
  </div>
{/if}

<!-- Success Toast -->
{#if success}
  <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 9999; margin-top: 70px;">
    <div class="toast show align-items-center text-white bg-success border-0" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body">{success}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" on:click={() => success = ""}></button>
      </div>
    </div>
  </div>
{/if}

