<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let courseId = $page.params.id;
  let title = "";
  let description = "";
  let youtubeLink = "";
  let thumbnail = null;
  let currentUser;
  let error = "";
  let success = "";
  let isLoading = true;

  onMount(async () => {
    currentUser = JSON.parse(localStorage.getItem("user"));
    if (!currentUser || currentUser.role !== 'teacher') return goto('/login');

    // Fetch course data without authorization check
    const res = await fetch(`${API_BASE}/course/${courseId}`);
    const data = await res.json();

    if (res.ok) {
      title = data.title;
      description = data.description;
      youtubeLink = data.youtube_link;
      isLoading = false;
    } else {
      error = "Course not found.";
      isLoading = false;
    }
  });

  async function handleUpdate(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);
    formData.append("youtube_link", youtubeLink);
    formData.append("teacher_id", currentUser.id);
    if (thumbnail) {
      formData.append("thumbnail", thumbnail);
    }

    const res = await fetch(`${API_BASE}/update-course/${courseId}`, {
      method: "PUT",
      body: formData
    });

    const result = await res.json();
    if (res.ok) {
      success = "Course updated successfully!";
      setTimeout(() => goto('/dashboard/teacher'), 3000);
    } else {
      error = result.error || "Update failed.";
    }
  }
</script>

<div class="container mt-4">
  {#if isLoading}
    <div class="d-flex justify-content-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  {:else if error}
    <div class="alert alert-danger">{error}</div>
  {:else}
    <h2 class="mb-3">Edit Course #{courseId}</h2>

    <form on:submit={handleUpdate}>
      <div class="mb-3">
        <label>Title</label>
        <input class="form-control" bind:value={title} required />
      </div>

      <div class="mb-3">
        <label>Description</label>
        <textarea class="form-control" bind:value={description} required></textarea>
      </div>

      <div class="mb-3">
        <label>YouTube Link</label>
        <input class="form-control" type="url" bind:value={youtubeLink} required />
      </div>

      <div class="mb-3">
        <label>Thumbnail (optional)</label>
        <input class="form-control" type="file" on:change={e => thumbnail = e.target.files[0]} />
      </div>

      <button class="btn btn-primary">Update</button>
    </form>

    {#if success}
      <div class="alert alert-success mt-3">{success}</div>
    {/if}
  {/if}
</div>
