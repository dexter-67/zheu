async function loadNews() {
  const newsList = document.getElementById("newsList");

  if (!newsList) {
    return;
  }

  newsList.innerHTML = "Загрузка новостей...";

  try {
    const news = await apiRequest(window.API.gateway, "/news", {
      method: "GET",
    });

    if (!Array.isArray(news) || news.length === 0) {
      newsList.innerHTML = "<p>Новостей пока нет.</p>";
      return;
    }

    newsList.innerHTML = news
      .map((item) => {
        return `
          <article class="item">
            <h3>${escapeHtml(item.title)}</h3>
            <p>${escapeHtml(item.content)}</p>
            <small>${formatDate(item.created_at)}</small>
          </article>
        `;
      })
      .join("");
  } catch (error) {
    console.error("Ошибка загрузки новостей:", error);
    newsList.innerHTML = `<p class="error">${escapeHtml(
      error.message || "Не удалось загрузить новости"
    )}</p>`;
  }
}
