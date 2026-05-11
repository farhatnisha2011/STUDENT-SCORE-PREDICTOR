<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Student Score Predictor</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css"/>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Space Grotesk', sans-serif;
      background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }

    .wrap {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 100%;
      max-width: 460px;
    }

    .logo { font-size: 36px; margin-bottom: 6px; }

    .title {
      color: #00FFD1;
      font-size: 26px;
      font-weight: 700;
      text-align: center;
      letter-spacing: -0.5px;
      margin-bottom: 4px;
    }

    .subtitle {
      color: #a0bcc8;
      font-size: 13px;
      text-align: center;
      margin-bottom: 1.5rem;
    }

    /* Role buttons */
    .role-row {
      display: flex;
      gap: 10px;
      width: 100%;
      margin-bottom: 1rem;
    }

    .role-btn {
      flex: 1;
      padding: 10px 0;
      border-radius: 10px;
      border: 1.5px solid #2a4a5a;
      background: #1a2f3a;
      color: #a0bcc8;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      font-family: inherit;
    }

    .role-btn.active {
      background: #00FFD1;
      color: #0a2030;
      border-color: #00FFD1;
      font-weight: 700;
    }

    .role-btn:hover:not(.active) {
      border-color: #00FFD1;
      color: #00FFD1;
    }

    /* Badge */
    .badge {
      background: #00FFD1;
      color: #0a2030;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 18px;
      border-radius: 20px;
      letter-spacing: 1px;
      margin-bottom: 1.2rem;
      display: inline-block;
    }

    /* Card */
    .card {
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid #00FFD1;
      border-radius: 18px;
      padding: 1.8rem 1.6rem;
      width: 100%;
    }

    .card-title {
      color: #00FFD1;
      font-size: 18px;
      font-weight: 700;
      text-align: center;
      margin-bottom: 1.2rem;
    }

    /* Autofill note */
    .autofill-note {
      background: rgba(0, 255, 209, 0.08);
      border: 1px solid rgba(0, 255, 209, 0.3);
      border-radius: 8px;
      padding: 8px 12px;
      color: #00FFD1;
      font-size: 11px;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Fields */
    .field { margin-bottom: 1rem; }

    .field label {
      display: block;
      color: #a0bcc8;
      font-size: 12px;
      font-weight: 500;
      margin-bottom: 5px;
      letter-spacing: 0.4px;
    }

    .field input {
      width: 100%;
      background: #111827;
      border: 1px solid #00FFD1;
      border-radius: 8px;
      padding: 10px 14px;
      color: #fff;
      font-size: 14px;
      font-family: inherit;
      outline: none;
      transition: box-shadow 0.15s;
    }

    .field input:focus {
      box-shadow: 0 0 0 2px rgba(0, 255, 209, 0.25);
    }

    /* Password wrapper */
    .pw-wrap { position: relative; }
    .pw-wrap input { padding-right: 40px; }

    .eye-btn {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      cursor: pointer;
      color: #a0bcc8;
      font-size: 18px;
      line-height: 1;
      padding: 0;
    }

    .eye-btn:hover { color: #00FFD1; }

    /* Buttons */
    .btn-row {
      display: flex;
      gap: 10px;
      margin-top: 0.5rem;
    }

    .btn-login {
      flex: 1;
      background: linear-gradient(135deg, #00C9FF, #92FE9D);
      color: #0a2030;
      font-weight: 700;
      font-size: 14px;
      padding: 11px;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      font-family: inherit;
      transition: opacity 0.15s;
    }

    .btn-login:hover { opacity: 0.88; }

    .btn-guest {
      flex: 1;
      background: transparent;
      color: #a0bcc8;
      font-weight: 500;
      font-size: 13px;
      padding: 11px;
      border: 1px solid #2a4a5a;
      border-radius: 10px;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s;
    }

    .btn-guest:hover { border-color: #00FFD1; color: #00FFD1; }

    .btn-create {
      width: 100%;
      background: transparent;
      color: #00FFD1;
      font-weight: 600;
      font-size: 13px;
      padding: 11px;
      border: 1px solid rgba(0, 255, 209, 0.35);
      border-radius: 10px;
      cursor: pointer;
      font-family: inherit;
      margin-top: 10px;
      transition: all 0.15s;
    }

    .btn-create:hover { background: rgba(0, 255, 209, 0.07); }

    /* Messages */
    .success-msg {
      background: rgba(0, 255, 209, 0.12);
      border: 1px solid rgba(0, 255, 209, 0.4);
      border-radius: 8px;
      color: #00FFD1;
      font-size: 13px;
      padding: 10px 14px;
      text-align: center;
      margin-top: 10px;
      animation: fadein 0.3s ease;
    }

    .error-msg {
      background: rgba(255, 80, 80, 0.1);
      border: 1px solid rgba(255, 80, 80, 0.3);
      border-radius: 8px;
      color: #ff7070;
      font-size: 13px;
      padding: 10px 14px;
      text-align: center;
      margin-top: 10px;
    }

    @keyframes fadein {
      from { opacity: 0; transform: translateY(-4px); }
      to   { opacity: 1; transform: none; }
    }
  </style>
</head>
<body>

<div class="wrap">
  <div class="logo">🎓</div>
  <div class="title">Student Score Predictor</div>
  <div class="subtitle">Predict &amp; track your academic performance</div>

  <!-- Role buttons -->
  <div class="role-row">
    <button class="role-btn active" onclick="selectRole('student', this)">🎓 Student</button>
    <button class="role-btn"        onclick="selectRole('teacher', this)">👨‍🏫 Teacher</button>
    <button class="role-btn"        onclick="selectRole('parent',  this)">👨‍👩‍👧 Parent</button>
  </div>

  <div class="badge" id="selectedBadge">✓ SELECTED: STUDENT</div>

  <!-- Login card -->
  <div class="card">
    <div class="card-title" id="cardTitle">🎓 Student Login</div>

    <div class="autofill-note" id="autofillNote">
      ✅ Credentials auto-filled for Student
    </div>

    <div class="field">
      <label for="usernameInput">Username</label>
      <input type="text" id="usernameInput" placeholder="Enter your username" value="student1" />
    </div>

    <div class="field">
      <label for="passwordInput">Password</label>
      <div class="pw-wrap">
        <input type="password" id="passwordInput" placeholder="Enter your password" value="pass123" />
        <button class="eye-btn" onclick="togglePw()" aria-label="Toggle password visibility">
          👁️
        </button>
      </div>
    </div>

    <div class="btn-row">
      <button class="btn-login" onclick="doLogin()">🔐 LOGIN</button>
      <button class="btn-guest" onclick="doGuest()">👤 Guest Mode</button>
    </div>

    <div id="msgBox"></div>
  </div>

  <button class="btn-create" onclick="showCreate()">📝 CREATE NEW ACCOUNT</button>
</div>

<script>
  const USERS = {
    student1: { password: 'pass123',   name: 'John Doe',       role: 'student' },
    teacher1: { password: 'teach123',  name: 'Ms. Smith',      role: 'teacher' },
    parent1:  { password: 'parent123', name: 'Robert Johnson', role: 'parent'  },
    parent2:  { password: 'mom123',    name: 'Sarah Williams', role: 'parent'  }
  };

  const AUTO = {
    student: { user: 'student1', pw: 'pass123',   emoji: '🎓',       title: 'Student Login' },
    teacher: { user: 'teacher1', pw: 'teach123',  emoji: '👨‍🏫',  title: 'Teacher Login' },
    parent:  { user: 'parent1',  pw: 'parent123', emoji: '👨‍👩‍👧', title: 'Parent Login'  }
  };

  let currentRole = 'student';
  let pwVisible   = false;

  function selectRole(role, btn) {
    currentRole = role;
    document.querySelectorAll('.role-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const d = AUTO[role];
    document.getElementById('selectedBadge').textContent  = '✓ SELECTED: ' + role.toUpperCase();
    document.getElementById('cardTitle').textContent       = d.emoji + ' ' + d.title;
    document.getElementById('usernameInput').value         = d.user;
    document.getElementById('passwordInput').value         = d.pw;
    document.getElementById('autofillNote').textContent    =
      '✅ Credentials auto-filled for ' + role.charAt(0).toUpperCase() + role.slice(1);
    document.getElementById('msgBox').innerHTML = '';

    // Reset password visibility
    pwVisible = false;
    document.getElementById('passwordInput').type = 'password';
  }

  function togglePw() {
    const inp = document.getElementById('passwordInput');
    pwVisible = !pwVisible;
    inp.type  = pwVisible ? 'text' : 'password';
  }

  function doLogin() {
    const u   = document.getElementById('usernameInput').value.trim();
    const p   = document.getElementById('passwordInput').value;
    const box = document.getElementById('msgBox');

    if (!u || !p) {
      box.innerHTML = '<div class="error-msg">⚠️ Please enter username and password!</div>';
      return;
    }
    if (!USERS[u]) {
      box.innerHTML = '<div class="error-msg">❌ Username not found!</div>';
      return;
    }
    if (USERS[u].password !== p) {
      box.innerHTML = '<div class="error-msg">❌ Incorrect password!</div>';
      return;
    }
    if (USERS[u].role !== currentRole) {
      box.innerHTML = `<div class="error-msg">❌ This account is for "${USERS[u].role}" role only!</div>`;
      return;
    }
    box.innerHTML = `<div class="success-msg">✅ Welcome, ${USERS[u].name}! Redirecting...</div>`;
  }

  function doGuest() {
    document.getElementById('msgBox').innerHTML =
      '<div class="success-msg">✅ Logged in as Guest User!</div>';
  }

  function showCreate() {
    document.getElementById('msgBox').innerHTML =
      '<div class="success-msg">📝 Registration form would open here.</div>';
  }
</script>

</body>
</html>
