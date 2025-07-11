<script>
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores/userStore.js';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let identifier = "";
  let password = "";
  let error = "";
  let success = "";
  let showPassword = false;

  async function handleLogin(event) {
    event.preventDefault();

    if (!identifier || !password) {
      error = "All fields are required.";
      return;
    }

    const data = {
      email: identifier,
      password
    };

    try {
      const res = await fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      const result = await res.json();

      if (res.ok) {
        success = "Login successful!";
        error = "";

        user.set(result.user);
        localStorage.setItem('user', JSON.stringify(result.user));

        setTimeout(() => goto("/dashboard"), 1000);
      } else {
        error = result.error || "Login failed.";
        success = "";
      }
    } catch (err) {
      console.error(err);
      error = "Something went wrong.";
      success = "";
    }
  }
</script>


<style>
  html, body {
    height: 100%;
    margin: 0;
    overflow: hidden;
    background-color: #121212;
  }

  * {
    box-sizing: border-box;
  }

  .login-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 98vh;
    position: relative;
    z-index: 1;
    padding: 20px;
    overflow: hidden;
  }

  .login-wrapper::before {
    content: "";
    position: absolute;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle at 30% 30%, rgba(0, 255, 255, 0.08), transparent 60%),
                radial-gradient(circle at 70% 70%, rgba(255, 0, 255, 0.08), transparent 60%);
    animation: moveGlow 30s infinite alternate ease-in-out;
    z-index: 0;
    top: -20%;
    left: -20%;
    filter: blur(80px);
  }

  @keyframes moveGlow {
    0% { transform: scale(1) translate(0, 0); }
    50% { transform: scale(1.2) translate(10%, 10%); }
    100% { transform: scale(1) translate(0, 0); }
  }

  .login-card {
    max-width: 450px;
    width: 100%;
    padding: 25px;
    border-radius: 14px;
    background: rgba(30, 30, 30, 0.6);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    z-index: 2;
  }

  label {
    font-weight: 500;
  }

  .form-control {
    background-color: #2a2a2a;
    color: white;
    border: 1px solid #444;
  }

  .form-control:focus {
    background-color: #2a2a2a;
    color: white;
    border-color: #28a745;
    box-shadow: none;
  }

  .toggle-password {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: #ccc;
    cursor: pointer;
  }

  .forgot-password {
    text-align: right;
    margin-top: -8px;
    margin-bottom: 12px;
  }

  .forgot-password a {
    color: #0dcaf0;
    font-size: 0.9rem;
    text-decoration: none;
  }

  .forgot-password a:hover {
    text-decoration: underline;
  }

  button.btn-success:hover {
    background-color: #218838;
  }
</style>



<svelte:head>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/remixicon/fonts/remixicon.css" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" defer></script>
</svelte:head>

<!-- Login Page Layout -->
<div class="login-wrapper">
  <div class="card text-white login-card shadow">
    <h2 class="text-center mb-4" style="font-family: 'Quintessential', cursive;">
      <i class="ri-login-circle-line me-2"></i>Login
    </h2>

    <form on:submit={handleLogin}>
      <div class="mb-3">
        <label>
          <i class="ri-user-line me-1"></i>Email or Name
        </label>
        <input type="text" class="form-control" bind:value={identifier} required />
      </div>

      <div class="mb-3 position-relative">
        <label>
          <i class="ri-lock-password-line me-1"></i>Password
        </label>
        <input
          type={showPassword ? "text" : "password"}
          class="form-control"
          bind:value={password}
          required
        />
        <i
          class="ri-eye-line toggle-password"
          on:click={() => (showPassword = !showPassword)}
          class:ri-eye-off-line={!showPassword}
         style="padding-top:26px"></i>
      </div>

      <button type="submit" class="btn btn-success w-100 mt-2">
        <i class="ri-login-box-line me-2"></i>Log In
      </button>
    </form>
  </div>
</div>


<!-- Error Toast -->
{#if error}
  <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 9999; margin-top: 70px;">
    <div class="toast show align-items-center text-white bg-danger border-0" role="alert">
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
    <div class="toast show align-items-center text-white bg-success border-0" role="alert">
      <div class="d-flex">
        <div class="toast-body">{success}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" on:click={() => success = ""}></button>
      </div>
    </div>
  </div>
{/if}
