<script>
  import { user } from '$lib/stores/userStore.js';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import NotificationBell from './NotificationBell.svelte';

  const logout = () => {
    user.set(null);
    localStorage.removeItem('user');
    window.location.href = "/login";
  };
</script>

<style>
  .fixed-navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1050;
    background: rgba(0, 0, 0, 0.6); /* semi-transparent */
    backdrop-filter: blur(20px);    /* frosted glass effect */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
  }

  .navbar a.navbar-brand {
    font-family: 'Playpen Sans Thai', cursive;
    letter-spacing: 1px;
  }

  body {
    padding-top: 70px; /* space below fixed navbar */
  }

  .btn-outline-light.mt-3 {
    margin-left: 0.5rem;
  }

  /* Optional: smoother nav links for unauthenticated users */
  .nav-link {
    color: white !important;
    font-weight: 500;
  }

  .nav-link:hover {
    text-decoration: none;
  }
</style>

<nav class="navbar navbar-expand-lg fixed-navbar navbar-dark small-navbar">
  <div class="container-fluid px-4">
    {#if browser && $user}
      <a
        class="navbar-brand"
        href={$user.role === 'teacher' ? '/dashboard/teacher' : '/dashboard/student'}
      >
        <i class="ri-graduation-cap-line me-2"></i>Mentoroid
      </a>
    {:else}
      <a class="navbar-brand" href="/login">
        <i class="ri-graduation-cap-line me-2"></i>Mentoroid
      </a>
    {/if}

    <div class="collapse navbar-collapse justify-content-end">
      <ul class="navbar-nav align-items-center gap-2">
        {#if browser && $user}
          <li class="nav-item d-flex align-items-center text-white me-3">
            <span class="me-2">
              Hello, {$user.name} ({$user.role})
            </span>
            <img
              src={$user.image || 'https://via.placeholder.com/32'}
              alt="profile"
              width="32"
              height="32"
              class="rounded-circle"
            />
          </li>

          <li class="nav-item position-relative me-2">
            <NotificationBell />
          </li>

          <li class="nav-item d-flex flex-column flex-md-row align-items-start align-items-md-center gap-2">
            <button class="btn btn-outline-light" on:click={logout}>Logout</button>
            <button class="btn btn-outline-light">
              <a href="mailto:priyankadafda.sdmify@gmail.com">📩 Contact Us</a>
            </button>
          </li>
        {:else}
          <li class="nav-item"><a class="nav-link" href="/signup">📝Register</a></li>
          <li class="nav-item"><a class="nav-link" href="/login">🔐Login</a></li>
          <a href="mailto:priyankadafda.sdmify@gmail.com" class="btn btn-outline-light ms-2">📩 Contact Us</a>
        {/if}
      </ul>
    </div>
  </div>
</nav>
