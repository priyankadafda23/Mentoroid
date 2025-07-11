<script>
  import { toast } from '@zerodevx/svelte-toast';
  let name = '', email = '', mobile = '', subject = '', message = '';

  const API_BASE = import.meta.env.VITE_API_BASE;

  async function submitForm() {
    if (!name || !email || !mobile || !subject || !message) {
      toast.push('❌ All fields are required!');
      return;
    }

    const res = await fetch(`${API_BASE}/contact`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, mobile, subject, message })
    });

    const data = await res.json();
    if (res.ok) {
      toast.push('✅ Form submitted successfully!');
      name = email = mobile = subject = message = '';
    } else {
      toast.push(`❌ ${data.error}`);
    }
  }
</script>

<style>
  .container {
    max-width: 600px;
    margin: auto;
    padding: 2rem;
  }

  h2 {
    color: #ffffff;
    text-align: center;
    margin-bottom: 1.5rem;
    font-size: 2rem;
    font-weight: bold;
  }

  form {
    background: #1e1e2f;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
  }

  label {
    display: block;
    margin-bottom: 0.4rem;
    font-weight: 500;
    color: #ccc;
  }

  input,
  textarea {
    width: 100%;
    padding: 0.75rem;
    background: #2c2c3e;
    border: 1px solid #444;
    border-radius: 8px;
    color: #f1f1f1;
    font-size: 1rem;
    transition: 0.3s ease;
    text:white;
  }

  input:focus,
  textarea:focus {
    outline: none;
    border-color: #28a745;
    background: #ffffff;
    
  }

  textarea {
    resize: none;
  }

  .btn {
    width: 100%;
    padding: 0.8rem;
    font-size: 1rem;
    font-weight: 600;
    background: linear-gradient(to right, #28a745, #218838);
    border: none;
    color: white;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s ease;
    margin-top: 1rem;
  }

  .btn:hover {
    background: linear-gradient(to right, #218838, #1e7e34);
  }

  .mb-3 {
    margin-bottom: 1.2rem;
  }

html, body {
  overflow-x: hidden;
  overflow-y: auto;
  max-width: 100vw;
  height: 100%;
  margin: 0;
  padding: 0;
}

body {
  position: relative;
}

* {
  box-sizing: border-box;
}

</style>



<div class="container">
  <h2 class="text-white mb-4">📩 Contact Us</h2>

  <form on:submit|preventDefault={submitForm} class="bg-dark text-light p-4 rounded shadow">
    <div class="mb-3">
      <label class="form-label">Name</label>
      <input class="form-control" bind:value={name} required />
    </div>
    <div class="mb-3">
      <label class="form-label">Email</label>
      <input type="email" class="form-control" bind:value={email} required />
    </div>
    <div class="mb-3">
      <label class="form-label">Mobile</label>
      <input type="tel" class="form-control" bind:value={mobile} required />
    </div>
    <div class="mb-3">
      <label class="form-label">Subject</label>
      <input class="form-control" bind:value={subject} required />
    </div>
    <div class="mb-3">
      <label class="form-label">Message</label>
      <textarea class="form-control" rows="4" bind:value={message} required></textarea>
    </div>
    <button type="submit" class="btn btn-success">Submit</button>
  </form>
</div>
