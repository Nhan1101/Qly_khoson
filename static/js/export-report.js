document.addEventListener("DOMContentLoaded", () => {
  const pathName = window.location.pathname;
  const activeLink = Array.from(document.querySelectorAll(".menu-items a")).find((link) => {
    const href = link.getAttribute("href");
    return href && pathName.startsWith(href);
  });

  if (activeLink) {
    activeLink.classList.add("is-active");
  }

  const values = Array.from(document.querySelectorAll("[data-count]"));
  values.forEach((element) => {
    const target = Number(element.dataset.count || "0");
    element.textContent = new Intl.NumberFormat("vi-VN").format(target);
  });

  const startDate = document.getElementById("start-date");
  const endDate = document.getElementById("end-date");

  if (startDate && endDate) {
    const syncDates = () => {
      if (startDate.value && endDate.value && startDate.value > endDate.value) {
        endDate.value = startDate.value;
      }
    };

    startDate.addEventListener("change", syncDates);
    endDate.addEventListener("change", syncDates);
  }
});
