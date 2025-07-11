<script>
  import { user } from '$lib/stores/userStore.js';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import Navbar from '$lib/components/Navbar.svelte';


  onMount(() => {
    if (browser) {
      const stored = localStorage.getItem('user');
      if (stored) user.set(JSON.parse(stored));
    }
  });

  function logout() {
    localStorage.removeItem('user');
    user.set(null);
    goto('/login');
  }
</script>


<svelte:head>
  <title>Mentoriod</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/remixicon@2.5.0/fonts/remixicon.css" rel="stylesheet" />

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Quintessential&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Playpen+Sans+Thai:wght@100..800&display=swap" rel="stylesheet">

  <!-- Global CSS -->
  <link rel="stylesheet" href="/styles/global.css" />
</svelte:head>

<!--navbar-->
<Navbar />

<div class="main-content">
  <slot />
  <footer class="footer">
    <p>&copy; 2025 AI Education Portal. All rights reserved.</p>
  </footer>

</div>

<style>
  .main-content {
    padding-top: 58px;
    display: flex;
    flex-direction: column;
    min-height: 102vh;

}

.footer {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 1rem;
    margin-top: auto;
  }
</style>
