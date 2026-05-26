async function createRequest(event) {
  event.preventDefault();

  const titleInput = document.getElementById("requestTitle");
  const contentInput = document.getElementById("requestContent");
  const errorBox = document.getElementById("requestError");

  errorBox.textContent = "";

  try {
    await apiRequest(API.requests, "/requests", {
      method: "POST",
      body: JSON.stringify({
        title: titleInput.value.trim(),
        content: contentInput.value.trim(),
      }),
    });

    titleInput.value = "";
    contentInput.value = "";

    await loadMyRequests();
    await loadNotifications();
  } catch (error) {
    errorBox.textContent = error.message || "Не удалось создать заявку";
  }
}

async function loadMyRequests() {
  const requestsList = document.getElementById("requestsList");

  if (!requestsList) {
    return;
  }

  requestsList.innerHTML = "Загрузка заявок...";

  try {
    const requests = await apiRequest(API.requests, "/requests/my", {
      method: "GET",
    });

    if (!requests || requests.length === 0) {
      requestsList.innerHTML = "<p>У вас пока нет заявок.</p>";
      return;
    }

    requestsList.innerHTML = requests
      .map((item) => {
        const status = item.status || "created";

        return `
          <article class="item">
            <div class="item-header">
              <h3>${escapeHtml(item.title || "Без заголовка")}</h3>
              <span class="status">${escapeHtml(getStatusText(status))}</span>
            </div>

            <p>${escapeHtml(item.content || item.description || "Без описания")}</p>

            <small>
              ID: ${item.id}
              · Создано: ${formatDate(item.created_at)}
              ${item.updated_at ? ` · Обновлено: ${formatDate(item.updated_at)}` : ""}
            </small>
          </article>
        `;
      })
      .join("");
  } catch (error) {
    requestsList.innerHTML = `<p class="error">${error.message}</p>`;
  }
}

function getStatusText(status) {
  const statuses = {
    created: "создана",
    in_progress: "в работе",
    done: "выполнена",
    rejected: "отклонена",
  };

  return statuses[status] || status;
}
