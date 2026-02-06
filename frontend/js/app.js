(function () {
  'use strict';

  // Backend API URL - change if your backend runs on a different port/host
  const API_BASE = 'http://localhost:5000';
  
  // Check backend health on load
  async function checkBackendHealth() {
    try {
      const res = await fetch(API_BASE + '/health');
      const data = await res.json();
      if (data.status === 'healthy') {
        console.log('✓ Backend is running');
      } else {
        console.warn('⚠ Backend health check failed:', data);
        toast('Backend database connection issue. Check backend logs.', 'error');
      }
    } catch (err) {
      console.error('Backend not reachable:', err);
      toast('Cannot connect to backend. Make sure it\'s running on port 5000.', 'error');
    }
  }
  
  // Check health when page loads
  checkBackendHealth();

  const $ = (sel, el = document) => el.querySelector(sel);
  const $$ = (sel, el = document) => el.querySelectorAll(sel);

  // --- Toast ---
  function toast(message, type = 'info') {
    const node = $('#toast');
    node.textContent = message;
    node.className = 'toast ' + type + ' show';
    clearTimeout(toast._t);
    toast._t = setTimeout(() => {
      node.classList.remove('show');
    }, 4000);
  }

  // --- Tabs ---
  $$('.tab').forEach((tab) => {
    tab.addEventListener('click', () => {
      const id = tab.dataset.tab;
      $$('.tab').forEach((t) => t.classList.remove('active'));
      $$('.panel').forEach((p) => p.classList.remove('active'));
      tab.classList.add('active');
      $('#' + id).classList.add('active');
      if (id === 'logs') loadLogs();
    });
  });

  // --- Register form ---
  const registerForm = $('#register-form');
  const registerBtn = $('#register-btn');
  const registerImage = $('#register-image');

  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = $('#name').value.trim();
    const email = $('#email').value.trim();
    const file = registerImage.files[0];
    if (!file) {
      toast('Please choose a face photo.', 'error');
      return;
    }
    registerBtn.disabled = true;
    const formData = new FormData();
    formData.append('name', name);
    formData.append('email', email);
    formData.append('image', file);
    try {
      const res = await fetch(API_BASE + '/register', {
        method: 'POST',
        body: formData
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok) {
        toast(data.message || 'Registered successfully!', 'success');
        registerForm.reset();
      } else {
        toast(data.error || 'Registration failed.', 'error');
      }
    } catch (err) {
      toast('Cannot reach server. Is the backend running on port 5000?', 'error');
    } finally {
      registerBtn.disabled = false;
    }
  });

  // --- Camera / Mark attendance ---
  const video = $('#camera-preview');
  const canvas = $('#capture-canvas');
  const startCameraBtn = $('#start-camera');
  const captureBtn = $('#capture-btn');
  const attendanceImageInput = $('#attendance-image');
  const submitAttendanceFileBtn = $('#submit-attendance-file');

  let stream = null;

  startCameraBtn.addEventListener('click', async () => {
    if (stream) {
      stream.getTracks().forEach((t) => t.stop());
      stream = null;
      video.srcObject = null;
      startCameraBtn.textContent = 'Start camera';
      captureBtn.disabled = true;
      return;
    }
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
      video.srcObject = stream;
      startCameraBtn.textContent = 'Stop camera';
      captureBtn.disabled = false;
    } catch (err) {
      toast('Could not access camera. Use "Upload image" instead.', 'error');
    }
  });

  function blobToFile(blob, name) {
    return new File([blob], name, { type: blob.type });
  }

  captureBtn.addEventListener('click', async () => {
    if (!stream || !video.videoWidth) return;
    const w = video.videoWidth;
    const h = video.videoHeight;
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    canvas.toBlob(async (blob) => {
      const file = blobToFile(blob, 'capture.jpg');
      await markAttendance(file);
    }, 'image/jpeg', 0.92);
  });

  attendanceImageInput.addEventListener('change', () => {
    submitAttendanceFileBtn.disabled = !attendanceImageInput.files.length;
  });

  submitAttendanceFileBtn.addEventListener('click', async () => {
    const file = attendanceImageInput.files[0];
    if (!file) return;
    await markAttendance(file);
  });

  async function markAttendance(file) {
    captureBtn.disabled = true;
    submitAttendanceFileBtn.disabled = true;
    const formData = new FormData();
    formData.append('image', file);
    try {
      const res = await fetch(API_BASE + '/mark_attendance', {
        method: 'POST',
        body: formData
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok) {
        toast(data.message || 'Attendance marked!', 'success');
        attendanceImageInput.value = '';
        submitAttendanceFileBtn.disabled = true;
      } else {
        toast(data.message || data.error || 'Check-in failed.', 'error');
      }
    } catch (err) {
      toast('Cannot reach server. Is the backend running on port 5000?', 'error');
    } finally {
      captureBtn.disabled = !stream;
      submitAttendanceFileBtn.disabled = !!attendanceImageInput.files.length;
    }
  }

  // --- Logs ---
  const logsBody = $('#logs-body');
  const refreshLogsBtn = $('#refresh-logs');

  async function loadLogs() {
    logsBody.innerHTML = '<tr><td colspan="2" class="empty">Loading…</td></tr>';
    try {
      const res = await fetch(API_BASE + '/logs');
      if (!res.ok) {
        const error = await res.json().catch(() => ({}));
        logsBody.innerHTML = `<tr><td colspan="2" class="empty">Error: ${error.error || 'Could not load logs'}</td></tr>`;
        return;
      }
      const list = await res.json().catch(() => []);
      if (!Array.isArray(list)) {
        logsBody.innerHTML = '<tr><td colspan="2" class="empty">Invalid response from server.</td></tr>';
        return;
      }
      if (list.length === 0) {
        logsBody.innerHTML = '<tr><td colspan="2" class="empty">No attendance records yet.</td></tr>';
        return;
      }
      logsBody.innerHTML = list
        .map((row) => `<tr><td>${escapeHtml(row.user || 'Unknown')}</td><td>${escapeHtml(row.time || 'N/A')}</td></tr>`)
        .join('');
    } catch (err) {
      logsBody.innerHTML = '<tr><td colspan="2" class="empty">Cannot reach server. Is the backend running?</td></tr>';
      toast('Failed to load logs. Check if backend is running.', 'error');
    }
  }

  function escapeHtml(s) {
    const div = document.createElement('div');
    div.textContent = s;
    return div.innerHTML;
  }

  refreshLogsBtn.addEventListener('click', loadLogs);

  // Load logs when Logs tab is first shown
  const logsTab = $('[data-tab="logs"]');
  logsTab.addEventListener('click', () => loadLogs(), { once: true });
})();
