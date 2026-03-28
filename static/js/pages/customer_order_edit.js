document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector(".order-edit-page");
  const listUrl = page?.dataset.listUrl || "#";
  const saveBtn = document.querySelector(".order-edit-save-btn");
  const closeBtn = document.querySelector(".order-edit-close");
  const modal = document.getElementById("order-edit-success-modal");

  closeBtn?.addEventListener("click", () => {
    window.location.href = listUrl;
  });

  saveBtn?.addEventListener("click", () => {
    modal?.classList.add("show");
    setTimeout(() => {
      window.location.href = listUrl;
    }, 1200);
  });
});
