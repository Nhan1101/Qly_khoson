document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.querySelector(".search-box");
  const searchInput = document.querySelector(".search-box input");
  if (!searchForm || !searchInput) {
    return;
  }

  searchInput.addEventListener("input", () => {
    searchInput.value = searchInput.value.replace(/[^\d]/g, "");
  });

  searchForm.addEventListener("submit", (event) => {
    if (!searchInput.value.trim()) {
      event.preventDefault();
      searchInput.focus();
    }
  });
});
