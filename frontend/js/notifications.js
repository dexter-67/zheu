function updateNotificationsBadgeByData(notifications) {
  const badge = document.getElementById("notificationsBadge");

  if (!badge) {
    return;
  }

  const unreadCount = notifications.filter((item) => !item.is_read).length;

  if (unreadCount > 0) {
    badge.textContent = unreadCount;
    badge.classList.remove("hidden");
  } else {
    badge.textContent = "0";
    badge.classList.add("hidden");
  }
}

async function loadNotifications() {
  const notificationsList = document.getElementById("notificationsList");

  if (!notificationsList) {
    return;
  }

  notificationsList.innerHTML = "Загрузка уведомлений...";

  try {
    const notifications = await apiRequest(
      API.notifications,
      "/notifications/my",
      {
        method: "GET",
      }
    );

    if (!notifications || notifications.length === 0) {
      updateNotificationsBadgeByData([]);
      notificationsList.innerHTML = "<p>Уведомлений пока нет.</p>";
      return;
    }

    updateNotificationsBadgeByData(notifications);

    notificationsList.innerHTML = notifications
      .map((item) => {
        const readClass = item.is_read ? "" : "unread";

        const title = item.title || item.event_type || "Уведомление";
        const message = item.message || "Нет текста уведомления";
        const eventType = item.event_type || "event";

        return `
          <article class="item ${readClass}" data-is-read="${item.is_read}">
            <div class="item-header">
              <h3>${escapeHtml(title)}</h3>
              <span>${escapeHtml(eventType)}</span>
            </div>

            <p>${escapeHtml(message)}</p>

            <small>${formatDate(item.created_at)}</small>

            ${
              item.is_read
                ? ""
                : `<button class="small-button" onclick="markNotificationAsRead(${item.id})">
                    Прочитать
                  </button>`
            }
          </article>
        `;
      })
      .join("");
  } catch (error) {
    notificationsList.innerHTML = `<p class="error">${error.message}</p>`;
  }
}

async function markNotificationAsRead(id) {
  try {
    await apiRequest(API.notifications, `/notifications/${id}/read`, {
      method: "PATCH",
    });

    await loadNotifications();
  } catch (error) {
    showToast(
      "Ошибка",
      error.message || "Не удалось отметить уведомление прочитанным"
    );
  }
}
