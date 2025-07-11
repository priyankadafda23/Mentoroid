<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let dashboardData = {};
  let currentUser = null;

  async function fetchDashboard() {
    const res = await fetch(`${API_BASE}/dashboard/teacher?id=${currentUser.id}`);
    dashboardData = await res.json();
  }

  onMount(async () => {
    currentUser = JSON.parse(localStorage.getItem('user'));
    if (!currentUser || currentUser.role !== 'teacher') return goto('/login');
    await fetchDashboard();
  });
</script>

<style>
  .card-glass {
    background: rgba(36, 41, 52, 0.9);
    border-radius: 16px;
    color: #e0e0e0;
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .card-glass:hover {
    transform: translateY(-6px);
    box-shadow: 0 0 20px rgba(0, 174, 255, 0.3);
  }

  h4, h5 {
    font-family: 'Quintessential', cursive;
  }

  .bg-glass-container {
    padding: 2rem;
    border-radius: 20px;
    background: linear-gradient(135deg, #1a1f2b, #2a2f3a);
  }
</style>


<div class="container-fluid bg-glass-container">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h4 class="text-white">🧑‍🏫 My Courses</h4>
    <button class="btn btn-outline-info btn-sm" on:click={fetchDashboard}>🔄 Refresh</button>
  </div>

  <div class="row">
    {#each dashboardData.my_courses ?? [] as course}
      <div class="col-md-3 mb-4">
        <div class="card-glass p-3">
          {#if course.thumbnail}
            <img src={course.thumbnail} alt="thumbnail" class="img-fluid rounded" />
          {/if}
          <h5 class="mt-3">{course.title}</h5>
          <p>👨‍🎓 Enrolled Students: {course.students}</p>
        </div>
      </div>
    {/each}
  </div>

  <h4 class="mt-5 text-white">📚 Actions</h4>
  <div class="row">
    {#each dashboardData.actions ?? [] as action}
      <div class="col-md-4 mb-4">
        <a href={action.link} class="card-glass p-3 d-block text-white text-decoration-none">
          <h5>{action.title}</h5>
        </a>
      </div>
    {/each}
  </div>
</div>
