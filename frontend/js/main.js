document.addEventListener("DOMContentLoaded", async () => {
  await loadCurrentUser();
  await loadNews();
  await loadMyRequests();
  await loadNotifications();
});

async function loadCurrentUser() {
  const token = localStorage.getItem("access_token");

  if (!token) {
    window.location.href = "/login";
    return;
  }

  try {
    const user = await apiRequest(API.core, "/users/me", {
      method: "GET",
    });

    localStorage.setItem("user_id", user.id);
    localStorage.setItem("email", user.email);
    localStorage.setItem("username", user.username);
    localStorage.setItem("role", user.role);

    if (user.role === "admin") {
      window.location.href = "/admin";
      return;
    }

    document.getElementById("currentUser").textContent = user.username;
    document.getElementById("currentRole").textContent = user.role;

    document.getElementById("profileEmail").textContent = user.email;
    document.getElementById("profileUsername").textContent = user.username;
    document.getElementById("profileRole").textContent = user.role;
  } catch (error) {
    console.error(error);
    logout();
  }
}
