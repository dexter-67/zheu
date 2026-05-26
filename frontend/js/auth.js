async function login(event) {
  event.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const errorBox = document.getElementById("error");

  errorBox.textContent = "";

  try {
    const data = await apiRequest(API.core, "/auth/login", {
      method: "POST",
      body: JSON.stringify({
        email,
        password,
      }),
    });

    saveAuthData(data);

    const me = await apiRequest(API.core, "/users/me", {
      method: "GET",
    });

    localStorage.setItem("user_id", me.id);
    localStorage.setItem("email", me.email);
    localStorage.setItem("username", me.username);
    localStorage.setItem("role", me.role);

    if (me.role === "admin") {
      window.location.href = "/admin";
    } else {
      window.location.href = "/dashboard";
    }
  } catch (error) {
    errorBox.textContent = error.message || "Неверный email или пароль";
  }
}

async function register(event) {
  event.preventDefault();

  const email = document.getElementById("email").value.trim();
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;
  const errorBox = document.getElementById("error");

  errorBox.textContent = "";

  try {
    await apiRequest(API.core, "/auth/register", {
      method: "POST",
      body: JSON.stringify({
        email,
        username,
        password,
      }),
    });

    window.location.href = "/login";
  } catch (error) {
    errorBox.textContent = error.message || "Ошибка регистрации";
  }
}