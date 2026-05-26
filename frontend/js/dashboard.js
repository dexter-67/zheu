function showToast(title, message) {
  const container = document.getElementById("toastContainer");

  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "alert alert-info shadow-lg max-w-sm";

  toast.innerHTML = `
    <div>
      <h3 class="font-bold">${escapeHtml(title)}</h3>
      <div class="text-sm">${escapeHtml(message)}</div>
    </div>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 5000);
}

function connectNotificationsWebSocket() {
  const token = localStorage.getItem("access_token");

  if (!token) return;

  window.ws = new WebSocket(
    `ws://${window.location.hostname}:8004/ws/notifications?token=${token}`
  );

  window.ws.onmessage = async (event) => {
    const notification = JSON.parse(event.data);

    await loadNotifications();

    showToast(notification.title, notification.message);
  };

  window.ws.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
}

document.addEventListener("DOMContentLoaded", () => {
  connectNotificationsWebSocket();
});