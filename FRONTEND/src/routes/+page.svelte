<script>
  import { goto } from '$app/navigation';

  function goToLogin() {
    goto('/login');
  }

  function goToSignup() {
    goto('/register');
  }

  function goToContact() {
    goto('/contact');
  }
</script>

<style>
  @media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
}

.hero {
  min-height: 98vh;
  width: 100%;
  display: flex;
  justify-content: center;
  padding-top: 3vh;
  padding-left: 16px;
  padding-right: 16px;
  padding-bottom: 40px;
  background: linear-gradient(135deg, #0f2027, #2c5364, #1b1b2f, #3a3a52);
  background-size: 300% 300%;
  animation: darkColorPulse 20s ease infinite;
  box-sizing: border-box;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 4rem 2rem;
  overflow-y: auto;
  position: relative;
  z-index: 1;
}

@keyframes darkColorPulse {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}


  .hero h1 {
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }

  .hero p {
    font-size: 1.3rem;
    max-width: 700px;
    margin-bottom: 2rem;
    color: #ccc;
  }

  .buttons button {
    margin: 0.5rem;
    padding: 0.9rem 1.8rem;
    font-size: 1rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s ease;
  }

  .login-btn {
    background-color: #28a745;
    color: white;
  }

  .signup-btn {
    background-color: #007bff;
    color: white;
  }

  .contact-btn {
    background-color: transparent;
    border: 1px solid white;
    color: white;
  }

  .login-btn:hover {
    background-color: #218838;
  }

  .signup-btn:hover {
    background-color: #0056b3;
  }

  .contact-btn:hover {
    background-color: white;
    color: black;
  }

  .features {
  padding: 4rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #e3f2fd, #e1f5fe); /* light blue gradient */
  color: #333;
}

.features h2 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #0d47a1;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  justify-items: center;
}

.feature {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: left;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}


  .feature h3 {
    color: #007bff;
    margin-bottom: 0.5rem;
  }
</style>

<!-- Hero Section -->
<section class="hero">
  <h1>Mentoroid Education Platform</h1>
  <p>"Next-Gen Mentorship. Today." 🚀</p>
  <br>
  <small>
    A smart web app designed for students and teachers to manage online learning, quizzes, YouTube-based courses, and personalized dashboards – all in one place.
  </small>
</section>

<!-- Features Section -->
<section class="features">
  <h2>📚 What You Can Do With Our App</h2>
  <div class="feature-grid">
    <div class="feature">
      <h3>🎓 Role-based Access</h3>
      <p>Students and teachers have separate logins with personalized dashboards and features tailored to their needs.</p>
    </div>
    <div class="feature">
      <h3>📘 Smart Course Management</h3>
      <p>Students can enroll in trending courses and access course videos uploaded by teachers.</p>
    </div>
    <div class="feature">
      <h3>📝 Quiz System</h3>
      <p>Teachers can create quizzes, students can take them, and teachers can manually assign scores.</p>
    </div>
    <div class="feature">
      <h3>🔔 Notifications</h3>
      <p>Get notified instantly when quizzes, scores, or new course materials are posted or when you enroll in a course.</p>
    </div>
    <div class="feature">
      <h3>🎥 YouTube Integration</h3>
      <p>Courses can include educational YouTube videos with “Watch” and “Download” options for enhanced learning.</p>
    </div>
    </div>
</section>