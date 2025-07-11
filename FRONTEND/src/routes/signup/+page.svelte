<script>
  import { goto } from '$app/navigation';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let role = "student";
  let name = "";
  let email = "";
  let password = "";
  let roll_no = "";
  let image = null;
  let error = "";
  let success = "";
  let showPassword = false;

  const emailRegex = /.+@(gmail|yahoo|outlook)\.com$/;
  const passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[{(!@#$%^&*)}]).{8,}$/;

  function handleSubmit(event) {
    console.log("Submit clicked");
    event.preventDefault();

    if (!emailRegex.test(email)) {
      error = "Only Gmail, Yahoo, or Outlook emails allowed.";
      return;
    }

    if (!passwordRegex.test(password)) {
      error = "Password must be 8+ characters with uppercase, lowercase, number & symbol.";
      return;
    }

    const formData = new FormData();
    formData.append("role", role);
    formData.append("name", name);
    formData.append("email", email);
    formData.append("password", password);

    if (role === "student") {
      formData.append("roll_no", roll_no);
    }

    if (image) {
      formData.append("image", image);
    }

    fetch(`${API_BASE}/signup`, {
      method: "POST",
      body: formData
    })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) {
          error = data.error || "Signup failed";
          success = "";
          throw new Error(error);
        }
        success = "Signup successful!";
        error = "";
        
        setTimeout(() => goto("/login"), 1500);
      })

      .catch((err) => {
        console.error("Signup failed", err);
        if (!error) error = "Signup failed due to server error.";
      });
  }
</script>

<svelte:head>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/remixicon/fonts/remixicon.css" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" defer></script>
</svelte:head>

<style>
  .center-wrapper {
  position: relative;
  min-height: calc(100vh - 70px);
  padding: 4vh 16px 40px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  background-color: #14141c;
  overflow: hidden;
  z-index: 1;
}

.center-wrapper::before {
  content: "";
  position: absolute;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle at 30% 30%, rgba(0, 255, 255, 0.08), transparent 60%),
              radial-gradient(circle at 70% 70%, rgba(255, 0, 255, 0.08), transparent 60%);
  animation: moveGlow 10s infinite alternate ease-in-out;
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

.toggle-password {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: #ccc;
    cursor: pointer;
  }
</style>


<div class="center-wrapper">
  <div class="auth-card">
    <h2><i class="ri-user-add-line"></i>Register</h2>

    <form on:submit={handleSubmit} enctype="multipart/form-data" class="form-wrapper">
      <div class="form-group">
        <label><i class="ri-user-settings-line me-1"></i>Select Role</label>
        <select bind:value={role}>
          <option value="student">Student</option>
          <option value="teacher">Teacher</option>
        </select>
      </div>

      <div class="form-group">
        <label><i class="ri-user-line me-1"></i>Name</label>
        <input type="text" name="name" bind:value={name} required />
      </div>

      <div class="form-group">
        <label><i class="ri-mail-line me-1"></i>Email</label>
        <input type="email" name="email" bind:value={email} required />
      </div>

      <div class="form-group position-relative">
        <label><i class="ri-lock-password-line me-1"></i>Password</label>
        <input
          type={showPassword ? "text" : "password"}
          name="password"
          class="form-control"
          bind:value={password}
          required  />
          <i
            class={`toggle-password ri-eye-line ${!showPassword ? 'ri-eye-off-line' : ''}`}
            on:click={() => showPassword = !showPassword}
          ></i>
</div>

      <div class="form-group">
        <label><i class="ri-image-add-line me-1"></i>Profile Image</label>
        <input type="file" name="image" on:change={(e) => image = e.target.files[0]} />
      </div>

      <button type="submit" class="btn btn-success w-100 mt-3">
        <i class="ri-user-add-line me-2"></i>Register
      </button>
    </form>

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

  </div>
</div>
