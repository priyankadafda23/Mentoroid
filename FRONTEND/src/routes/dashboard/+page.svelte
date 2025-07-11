<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores/userStore.js';

  onMount(() => {
    const currentUser = JSON.parse(localStorage.getItem('user'));

    if (!currentUser) {
      goto('/login');
    } else {
      if (currentUser.role === 'student') {
        goto('/dashboard/student');
      } else if (currentUser.role === 'teacher') {
        goto('/dashboard/teacher');
      } else {
        goto('/login');
      }
    }
  });
</script>

<p>Redirecting based on your role...</p>
