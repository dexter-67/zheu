const HOST = window.location.hostname;
const API_GATEWAY = `http://${HOST}:8080`;

window.API = {
  gateway: API_GATEWAY,
  core: API_GATEWAY,
  news: API_GATEWAY,
  requests: API_GATEWAY,
  notifications: API_GATEWAY,
};

function getToken() {
  return localStorage.getItem("access_token");
}

function saveAuthData(data) {
  localStorage.setItem("access_token", data.access_token);
  localStorage.setItem("refresh_token", data.refresh_token);

  if (data.role) {
    localStorage.setItem("role", data.role);
  }

  if (data.user_id) {
    localStorage.setItem("user_id", data.user_id);
  }
}

function logout() {
  localStorage.clear();
  window.location.href = "/login";
}

async function apiRequest(baseUrl, path, options = {}) {
  if (!baseUrl) {
    throw new Error(`Не указан baseUrl для запроса ${path}`);
  }

  const token = getToken();

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  let response;

  try {
    response = await fetch(`${baseUrl}${path}`, {
      ...options,
      headers,
    });
  } catch {
    throw new Error("Не удалось подключиться к серверу");
  }

  if (response.status === 401) {
    logout();
    return;
  }

  if (response.status === 204) {
    return null;
  }

  let data = null;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    let message = `Ошибка сервера: ${response.status}`;

    if (typeof data?.detail === "string") {
      message = data.detail;
    } else if (Array.isArray(data?.detail)) {
      message = data.detail.map((item) => item.msg || JSON.stringify(item)).join("; ");
    } else if (typeof data?.message === "string") {
      message = data.message;
    }

    throw new Error(message);
  }

  return data;
}

function formatDate(value) {
  if (!value) {
    return "-";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleString("ru-RU");
}

function escapeHtml(value) {
  if (value === null || value === undefined) {
    return "";
  }

  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
