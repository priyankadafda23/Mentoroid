<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let course = {};
  let videos = [];
  let loading = true;
  let isGridView = true;

  $: courseId = $page.params.id;

  onMount(async () => {
  const courseRes = await fetch(`${API_BASE}/course/${courseId}`);
  course = await courseRes.json();

  if (course.youtube_link) {
    if (course.youtube_link.includes("list=")) {
      const playlistRes = await fetch(`${API_BASE}/fetch-playlist?url=${encodeURIComponent(course.youtube_link)}`);
      videos = await playlistRes.json();
    } else if (course.youtube_link.includes("youtu.be/")) {
       const videoId = course.youtube_link.split("youtu.be/")[1].split("?")[0];
      if (videoId) {
        const videoRes = await fetch(`${API_BASE}/fetch-video-details?videoId=${videoId}`);
        const videoData = await videoRes.json();
        if ( videoData && !videoData.error && videoData.videoId && videoData.thumbnail && videoData.title) {
          videos = [videoData];
        } else {
          console.error("Invalid video data:", videoData);
        }
      }
    }
  }

  loading = false;
});

</script>

<style>
  /* Your existing styles remain */
  .video-description {
    color: #fff;
    font-size: 0.95rem;
    margin-top: 5px;
    white-space: normal;
    overflow-wrap: break-word;
  }

  .video-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    background-color: #f8f9fa;
    border-radius: 10px;
    transition: 0.5s ease;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  }

  .video-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
  }

  .grid-mode {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .grid-mode:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  }

  .list-mode {
    background-color: transparent !important;
    box-shadow: none !important;
    flex-direction: row;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem 0;
  }

  .video-card img {
    max-width: 150px;
    border-radius: 6px;
  }

  .video-text {
    flex: 1;
    color: white;
  }

  .toggle-buttons {
    display: flex;
    gap: 0.5rem;
  }
</style>

{#if loading}
  <div class="text-center mt-5">
    <div class="spinner-border" role="status"></div>
    <p>Loading course...</p>
  </div>
{:else}
  <div class="container mt-4">
    <h1>{course.title}</h1>
    <p class="text-white">{course.description}</p>


    {#if videos.length > 0}
      <div class="d-flex justify-content-between text-black align-items-center mt-4 mb-3">
        <h5 class="mb-0 text-white">Playlist/Video</h5> <div class="toggle-buttons">
          <button class="btn btn-outline-light btn-sm" on:click={() => isGridView = true}>
            🔲 Grid
          </button>
          <button class="btn btn-outline-light btn-sm" on:click={() => isGridView = false}>
            📄 List
          </button>
        </div>
      </div>

      <div class={isGridView ? 'row justify-content-center' : 'd-flex flex-column'}>
        {#each videos as video}
          <div class={isGridView ? 'col-md-3 mb-3 d-flex justify-content-center' : 'mb-3'}>
            <div class={`video-card ${isGridView ? 'grid-mode' : 'list-mode'}`}>
              <img src={video.thumbnail} alt={video.title} />
              <div class="video-text mt-2">
                <div class="video-description {isGridView ? 'text-black' : 'text-white'}">{video.title}</div>
                <div class="d-flex gap-2 mt-2">
                  <a href={`https://www.youtube.com/watch?v=${video.videoId}`} target="_blank" class="btn btn-success btn-sm">Watch</a>
                  <a href={`https://www.y2mate.com/youtube/${video.videoId}`} target="_blank" class="btn btn-outline-primary btn-sm">Download</a>
                </div>
              </div>
            </div>
          </div>
        {/each}
      </div>
      
    {:else}
      <p class="mt-3 text-light">This course does not have valid video content or a playlist link.</p>
    {/if}
  </div>
{/if}