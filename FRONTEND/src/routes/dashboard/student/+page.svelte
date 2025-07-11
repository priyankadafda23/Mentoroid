<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  const API_BASE = import.meta.env.VITE_API_BASE;

  let dashboardData = {
    courses: [],
    my_enrolled: [],
    enrolled: []
  };

  let enrolledCourses = [];
  let currentUser = null;
  let loadingId = null;
  
  let courseQuizzes = {};

let notifications = [];

onMount(async () => {
  currentUser = JSON.parse(localStorage.getItem('user'));
  if (!currentUser || currentUser.role !== 'student') {
    return goto('/login');
  }

  const res = await fetch(`${API_BASE}/quiz/student?student_id=${currentUser.id}`); 
  const data = await res.json();
  courseQuizzes = data;

  const dashRes = await fetch(`${API_BASE}/dashboard/student?student_id=${currentUser.id}`);
  dashboardData = await dashRes.json();
  enrolledCourses = dashboardData.enrolled ?? [];

  // ✅ Fetch notifications
  const notifRes = await fetch(`${API_BASE}/notifications/${currentUser.id}`);
  notifications = await notifRes.json();

  let quizResults = [];

async function fetchStudentQuizResults() {
  const res = await fetch(`${API_BASE}/student/${currentUser.id}/submissions`);
  const data = await res.json();
  if (res.ok) {
    quizResults = data;
  } else {
    console.error('Failed to fetch quiz results');
  }
}

fetchStudentQuizResults();


});


  async function enroll(courseId) {
    loadingId = courseId;

    const res = await fetch(`${API_BASE}/enroll/${courseId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: currentUser.id })
    });

    const data = await res.json();
    loadingId = null;

    if (res.ok) {
      // Update enrolled ID list
      enrolledCourses.push(courseId);

      // Get the course object
      const course = dashboardData.courses.find(c => c.id === courseId);

      if (course) {
        // Push to enrolled section (only if not already there)
        if (!dashboardData.my_enrolled.some(c => c.id === courseId)) {
          dashboardData.my_enrolled.push(course);
        }
      }

      alert(data.message);
    } else {
      alert(data.error);
    }
  }

  function isEnrolled(courseId) {
    return enrolledCourses.includes(courseId);
  }

  function truncate(text, max = 50) {
    return text?.length > max ? text.substring(0, max) + '...' : text;
  }
</script>

<style>
/* Background & Global */
body {
  background: linear-gradient(135deg, #1e1e1e, #2b2b2b, #252c35);
  color: #fff;
  font-family: 'Playpen Sans Thai', cursive;
  padding-bottom: 80px;
}

/* Enrolled Course Cards */
.enrolled-card {
  background: rgba(40, 40, 40, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  padding: 15px;
  color: #f1f1f1;
}

.enrolled-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 0 24px rgba(0, 174, 255, 0.35); /* soft cyan glow */
}

/* Section Headings */
h2 {
  font-family: 'Quintessential', cursive;
  font-size: 1.6rem;
  margin-top: 20px;
  margin-bottom: 14px;
  color: #d6e6ff;
}

/* Quiz Button */
.take-quiz-btn {
  background-color: #1e88e5;
  border: none;
  color: #fff;
  padding: 6px 14px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.take-quiz-btn:hover {
  background-color: #0d6efd;
}

/* Available course cards */
.available-card {
  background-color: #f0f0f0;
  color: #222;
  padding: 15px;
  border-radius: 10px;
  transition: transform 0.3s;
}

.available-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 12px rgba(255, 255, 255, 0.1);
}

/* Footer */
footer {
  background-color: #101010;
  color: #aaa;
  padding: 12px 0;
  font-size: 0.85rem;
  text-align: center;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

</style>


<div class="container mt-4">
  <h4 class="mt-5 ">My Enrolled Courses</h4>
  <div class="row mt-4">
    {#each dashboardData.my_enrolled ?? [] as course}
      <div class="col-md-4 mb-3">
        <a href={`/course/${course.id}`} class="card card-body enrolled-card bg-dark text-white text-decoration-none">
          <h5>{course.title}</h5>
          <p>{truncate(course.description)}</p>
        </a>
        {#if courseQuizzes[course.id]?.length}
  <div class="mt-2 me-5">
    <h6>Available Quizzes:</h6>
    <div class="row">
      {#each courseQuizzes[course.id] as quiz}
        <div class="col card bg-secondary text-white p-2 mb-2">
          <div class="d-flex justify-content-between">
            <strong>{course.title}</strong>
            <a class="btn btn-sm btn-primary " href={`/take-quiz/${quiz.id}`}>Take Quiz</a>
          </div>
        </div>
    {/each}
    </div>
  </div>
{/if}

      </div>
    {/each}
  </div>

  <div class="mb-3 text-end">
  <button class="btn btn-info take-quiz-btn" on:click={() => goto('/quiz/results')}>
    📊 View Quiz Results
  </button>
</div>


  <h4 class="mt-4">Available Courses</h4>
  <div class="row">
    {#each dashboardData.courses ?? [] as course}
      <div class="col-md-4 mb-3">
        <div class="card card-body bg-light text-black available-card">
          {#if course.thumbnail}
            <img 
              src={course.thumbnail} 
              alt="thumbnail">
          {/if}
          <h5 class="mt-3">{course.title}</h5>
          <p>{truncate(course.description)}</p>

          {#if isEnrolled(course.id)}
            <a class="btn btn-secondary disabled">Enrolled</a>
          {:else}
            <button
              class="btn btn-primary"
              on:click={() => enroll(course.id)}
              disabled={loadingId === course.id}
            >
              {#if loadingId === course.id}
                <span class="spinner-border spinner-border-sm"></span> Enrolling...
              {:else}
                Enroll Now
              {/if}
            </button>
          {/if}
        </div>
      </div>
    {/each}
  </div>

</div>
