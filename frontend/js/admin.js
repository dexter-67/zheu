document.addEventListener("DOMContentLoaded", async () => {
  await loadAdminUser();
  await loadAdminNews();
  await loadAllRequests();

  connectAdminNotificationsWebSocket();
});

async function loadAdminUser() {
  const token = localStorage.getItem("access_token");

  if (!token) {
    window.location.href = "/login";
    return;
  }

  try {
    const user = await apiRequest(API.core, "/users/me", {
      method: "GET",
    });

    if (user.role !== "admin") {
      window.location.href = "/dashboard";
      return;
    }

    localStorage.setItem("user_id", user.id);
    localStorage.setItem("email", user.email);
    localStorage.setItem("username", user.username);
    localStorage.setItem("role", user.role);

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

async function createNews(event) {
  event.preventDefault();

  const titleInput = document.getElementById("newsTitle");
  const contentInput = document.getElementById("newsContent");
  const publishedInput = document.getElementById("newsPublished");
  const errorBox = document.getElementById("newsError");

  errorBox.textContent = "";

  try {
    await apiRequest(API.news, "/news/", {
      method: "POST",
      body: JSON.stringify({
        title: titleInput.value.trim(),
        content: contentInput.value.trim(),
        is_published: publishedInput.checked,
      }),
    });

    titleInput.value = "";
    contentInput.value = "";
    publishedInput.checked = true;

    await loadAdminNews();
  } catch (error) {
    errorBox.textContent = error.message || "Не удалось создать новость";
  }
}

async function loadAdminNews() {
  const newsList = document.getElementById("adminNewsList");

  newsList.innerHTML = "Загрузка новостей...";

  try {
    const news = await apiRequest(API.news, "/news/", {
      method: "GET",
    });

    if (!news || news.length === 0) {
      newsList.innerHTML = "<p>Новостей пока нет.</p>";
      return;
    }

    newsList.innerHTML = news
      .map((item) => {
        return `
          <article class="item">
            <div class="item-header">
              <h3>${escapeHtml(item.title)}</h3>

              <button
                class="danger-button"
                onclick="deleteNews(${item.id})"
              >
                Удалить
              </button>
            </div>

            <p>${escapeHtml(item.content)}</p>

            <small>
              ID: ${item.id}
              · ${formatDate(item.created_at)}
              · published: ${item.is_published}
            </small>

            <div class="edit-box">
              <label>
                Новый заголовок

                <input
                  id="editNewsTitle-${item.id}"
                  type="text"
                  value="${escapeHtml(item.title)}"
                />
              </label>

              <label>
                Новый текст

                <textarea id="editNewsContent-${item.id}">${escapeHtml(item.content)}</textarea>
              </label>

              <label class="checkbox-label">
                <input
                  id="editNewsPublished-${item.id}"
                  type="checkbox"
                  ${item.is_published ? "checked" : ""}
                />

                Опубликована
              </label>

              <button
                class="small-button"
                onclick="updateNews(${item.id})"
              >
                Сохранить изменения
              </button>
            </div>
          </article>
        `;
      })
      .join("");
  } catch (error) {
    newsList.innerHTML = `
      <p class="error">
        ${error.message}
      </p>
    `;
  }
}

async function updateNews(id) {
  const titleInput = document.getElementById(`editNewsTitle-${id}`);
  const contentInput = document.getElementById(`editNewsContent-${id}`);
  const publishedInput = document.getElementById(`editNewsPublished-${id}`);

  try {
    await apiRequest(API.news, `/news/${id}`, {
      method: "PATCH",
      body: JSON.stringify({
        title: titleInput.value.trim(),
        content: contentInput.value.trim(),
        is_published: publishedInput.checked,
      }),
    });

    await loadAdminNews();
  } catch (error) {
    showToast("Ошибка", error.message || "Не удалось обновить новость");
  }
}

async function deleteNews(id) {
  const confirmed = confirm("Удалить эту новость?");

  if (!confirmed) {
    return;
  }

  try {
    await apiRequest(API.news, `/news/${id}`, {
      method: "DELETE",
    });

    await loadAdminNews();
  } catch (error) {
    showToast("Ошибка", error.message || "Не удалось удалить новость");
  }
}

async function loadAllRequests() {
  const requestsList = document.getElementById("adminRequestsList");

  requestsList.innerHTML = "Загрузка заявок...";

  try {
    const requests = await apiRequest(API.requests, "/requests/", {
      method: "GET",
    });

    if (!requests || requests.length === 0) {
      requestsList.innerHTML = "<p>Заявок пока нет.</p>";
      return;
    }

    requestsList.innerHTML = requests
      .map((item) => {
        return `
          <article class="item">
            <div class="item-header">
              <h3>${escapeHtml(item.title)}</h3>

              <span class="status">
                ${escapeHtml(getRequestStatusText(item.status))}
              </span>
            </div>

            <p>${escapeHtml(item.content)}</p>

            <small>
              ID: ${item.id}
              · author_id: ${item.author_id}
              · Создано: ${formatDate(item.created_at)}
              ${
                item.updated_at
                  ? ` · Обновлено: ${formatDate(item.updated_at)}`
                  : ""
              }
            </small>

            <div class="actions">
              <button
                class="small-button"
                onclick="updateRequestStatus(${item.id}, 'created')"
              >
                создана
              </button>

              <button
                class="small-button"
                onclick="updateRequestStatus(${item.id}, 'in_progress')"
              >
                в работе
              </button>

              <button
                class="small-button"
                onclick="updateRequestStatus(${item.id}, 'done')"
              >
                выполнена
              </button>

              <button
                class="small-button"
                onclick="updateRequestStatus(${item.id}, 'rejected')"
              >
                отклонена
              </button>
            </div>
          </article>
        `;
      })
      .join("");
  } catch (error) {
    requestsList.innerHTML = `
      <p class="error">
        ${error.message}
      </p>
    `;
  }
}

async function updateRequestStatus(id, status) {
  try {
    await apiRequest(API.requests, `/requests/${id}`, {
      method: "PATCH",
      body: JSON.stringify({
        status,
      }),
    });

    await loadAllRequests();
  } catch (error) {
    showToast("Ошибка", error.message || "Не удалось изменить статус заявки");
  }
}

function getRequestStatusText(status) {
  const statuses = {
    created: "создана",
    in_progress: "в работе",
    done: "выполнена",
    rejected: "отклонена",
  };

  return statuses[status] || status;
}

function showToast(title, message) {
  const container = document.getElementById("toastContainer");

  if (!container) {
    return;
  }

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

function connectAdminNotificationsWebSocket() {
  const token = localStorage.getItem("access_token");

  if (!token) {
    return;
  }

  window.ws = new WebSocket(
    `ws://${window.location.hostname}:8004/ws/notifications?token=${token}`
  );

  window.ws.onmessage = async (event) => {
    const notification = JSON.parse(event.data);

    showToast(notification.title, notification.message);

    await loadAllRequests();
  };

  window.ws.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
}