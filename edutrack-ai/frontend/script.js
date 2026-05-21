// EduTrack AI - Frontend API Client + UX Core
const API_BASE = 'http://localhost:5000/api';
const chartInstances = {};

// -------------------- Core Fetch --------------------
const parseApiError = async (response) => {
  try {
    const data = await response.json();
    if (data?.error) return data.error;
    return `Erro HTTP ${response.status}`;
  } catch {
    return response.status === 401
      ? 'Sessão expirada. Faça login novamente.'
      : response.status === 404
      ? 'Recurso não encontrado.'
      : response.status >= 500
      ? 'Erro interno no servidor. Tente novamente.'
      : `Erro HTTP ${response.status}`;
  }
};

const apiFetch = async (endpoint, options = {}) => {
  const token = localStorage.getItem('token');
  const config = {
    headers: { 'Content-Type': 'application/json' },
    ...options
  };

  if (token) config.headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API_BASE}${endpoint}`, config);

  if (!response.ok) {
    const message = await parseApiError(response);
    throw new Error(message);
  }

  if (response.status === 204) return {};
  return response.json();
};

// -------------------- Theme --------------------
window.applyTheme = (theme) => {
  const root = document.documentElement;
  root.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
};

window.toggleTheme = () => {
  const current = localStorage.getItem('theme') || 'dark';
  const next = current === 'dark' ? 'light' : 'dark';
  window.applyTheme(next);

  const icon = document.getElementById('theme-toggle-icon');
  if (icon) icon.innerHTML = themeIconSvg(next);
};

window.initTheme = () => {
  const saved = localStorage.getItem('theme') || 'dark';
  window.applyTheme(saved);
  const icon = document.getElementById('theme-toggle-icon');
  if (icon) icon.innerHTML = themeIconSvg(saved);
};

function themeIconSvg(theme) {
  if (theme === 'light') {
    // ícone "sol" para indicar que ao clicar volta para escuro
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>';
  }
  // ícone "lua" para indicar que ao clicar vai para claro
  return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
}
window.themeIconSvg = themeIconSvg;

// -------------------- Helpers --------------------
window.formatDate = (value) => {
  if (!value) return '-';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString('pt-BR');
};

window.normalizeStatus = (status = '') => {
  if (status === 'concluida') return 'Concluída';
  if (status === 'pendente') return 'Pendente';
  return status;
};

window.getStatusClass = (status = '') =>
  status === 'concluida' ? 'status-pill status-pill--done' : 'status-pill status-pill--pending';

// -------------------- Toast + Loader --------------------
window.showMessage = (message, type = 'success') => {
  let stack = document.getElementById('toast-stack');
  if (!stack) {
    stack = document.createElement('div');
    stack.id = 'toast-stack';
    stack.className = 'toast-stack';
    document.body.appendChild(stack);
  }

  const toast = document.createElement('div');
  const variant = type === 'error' ? 'error' : type === 'info' ? 'info' : 'success';
  toast.className = `toast toast--${variant}`;
  toast.textContent = message;
  stack.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-6px)';
    setTimeout(() => toast.remove(), 200);
  }, 3500);
};

const ensureLoader = () => {
  let loader = document.getElementById('global-loader');
  if (loader) return loader;

  loader = document.createElement('div');
  loader.id = 'global-loader';
  loader.className = 'global-loader';
  loader.innerHTML = '<div class="loader-ring"></div>';
  document.body.appendChild(loader);
  return loader;
};

window.showLoader = (show = true) => {
  const loader = ensureLoader();
  loader.style.display = show ? 'flex' : 'none';
};

// -------------------- AUTH --------------------
window.register = async (email, password) =>
  apiFetch('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  });

window.login = async (email, password) => {
  const data = await apiFetch('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  });

  if (data.access_token) {
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user_id', data.user_id);
  }
  return data;
};

window.logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user_id');
  window.location.href = 'login.html';
};

// -------------------- SUBJECTS --------------------
window.getSubjects = () => apiFetch('/subjects');
window.createSubject = (payload) =>
  apiFetch('/subjects', { method: 'POST', body: JSON.stringify(payload) });
window.updateSubject = (id, payload) =>
  apiFetch(`/subjects/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
window.deleteSubject = (id) => apiFetch(`/subjects/${id}`, { method: 'DELETE' });

// -------------------- TASKS --------------------
window.getTasks = (subjectId) => apiFetch(`/tasks/${subjectId}`);
window.createTask = (subjectId, payload) =>
  apiFetch(`/tasks/${subjectId}`, { method: 'POST', body: JSON.stringify(payload) });
window.updateTask = (taskId, payload) =>
  apiFetch(`/tasks/${taskId}`, { method: 'PUT', body: JSON.stringify(payload) });
window.deleteTask = (taskId) =>
  apiFetch(`/tasks/${taskId}`, { method: 'DELETE' });

// -------------------- DASHBOARD --------------------
window.getDashboard = () => apiFetch('/dashboard');

// -------------------- CHART --------------------
window.initCharts = (canvasId, data, type = 'doughnut') => {
  const ctx = document.getElementById(canvasId);
  if (!ctx || typeof Chart === 'undefined') return;

  if (chartInstances[canvasId]) chartInstances[canvasId].destroy();

  chartInstances[canvasId] = new Chart(ctx, {
    type,
    data: {
      labels: data.labels || [],
      datasets: [
        {
          data: data.values || [],
          backgroundColor: ['#7c8cff', '#22c55e', '#f59e0b', '#ef4444', '#06b6d4', '#a855f7'],
          borderWidth: 0
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom', labels: { color: getComputedStyle(document.documentElement).getPropertyValue('--text') } }
      }
    }
  });
};

// -------------------- Navigation --------------------
window.navigate = (page) => {
  window.location.href = page;
};

// -------------------- Auth Guard + Theme Init --------------------
document.addEventListener('DOMContentLoaded', () => {
  window.initTheme();

  const token = localStorage.getItem('token');
  const protectedPages = ['index.html', 'subjects.html', 'tasks.html'];
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';

  if (protectedPages.includes(currentPage) && !token) {
    window.location.href = 'login.html';
  }
});
