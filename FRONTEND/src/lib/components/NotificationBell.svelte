<script>
  import { onMount } from 'svelte';
  import { user } from '$lib/stores/userStore.js';
  import { goto } from '$app/navigation';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let notifications = [];
  let showDropdown = false;

  async function fetchNotifications() {
    const localUser = JSON.parse(localStorage.getItem('user'));
    const res = await fetch(`${API_BASE}/notifications/${localUser.id}`);
    notifications = await res.json();
  }

  function toggleDropdown() {
    showDropdown = !showDropdown;
  }

  function unreadCount() {
    const count = notifications.filter(n => !n.is_read).length;
    return count > 9 ? '9+' : count;
  }

  async function markAllAsRead() {
    const localUser = JSON.parse(localStorage.getItem('user'));
    await fetch(`${API_BASE}/notifications/mark-read/${localUser.id}`, { method: 'POST' });
    fetchNotifications();
  }

  onMount(fetchNotifications);
</script>

<style>
  .notif-dropdown {
    position: absolute;
    right: 20px;
    top: 60px;
    width: 300px;
    z-index: 999;
  }
</style>

<div class="position-relative">
  <button class="btn btn-dark position-relative" on:click={toggleDropdown}>
    <i class="ri-notification-line"></i>
    {#if unreadCount() > 0}
      <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
        {unreadCount()}
      </span>
    {/if}
  </button>

  {#if showDropdown}
    <div class="card notif-dropdown p-2 bg-dark text-white">
      <div class="d-flex justify-content-between align-items-center">
        <strong>Notifications</strong>
        <button class="btn btn-sm btn-light" on:click={markAllAsRead}>Mark All Read</button>
      </div>
      <hr />
      {#each notifications as notif}
        <div class="mb-2 small">{notif.message}</div>
        <hr>
      {:else}
        <p class="text-muted">No notifications</p>
      {/each}
    </div>
  {/if}
</div>
