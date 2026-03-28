document.addEventListener("DOMContentLoaded", () => {
  const backdrop = document.querySelector("[data-order-modal]");
  if (!backdrop) {
    return;
  }

  const closeButtons = backdrop.querySelectorAll("[data-close-modal]");
  const openButtons = document.querySelectorAll("[data-open-modal]");
  const form = backdrop.querySelector("form");
  const maDonInput = backdrop.querySelector("#id_ma_don");
  const nguoiNhanInput = backdrop.querySelector("#id_nguoi_nhan");
  const giaTriInput = backdrop.querySelector("#id_gia_tri");
  const thoiGianInput = backdrop.querySelector("#id_thoi_gian");
  const tinhTrangInput = backdrop.querySelector("#id_tinh_trang");
  const statusClasses = [
    "is-dang-giao-hang",
    "is-da-xuat",
    "is-da-giao-hang",
    "is-huy",
    "is-hoan-hang",
  ];

  const syncStatusColor = () => {
    if (!tinhTrangInput) {
      return;
    }
    tinhTrangInput.classList.remove(...statusClasses);
    const statusClass = `is-${tinhTrangInput.value.replaceAll("_", "-")}`;
    tinhTrangInput.classList.add(statusClass);
  };

  const openModal = () => backdrop.classList.add("is-open");
  const closeModal = () => backdrop.classList.remove("is-open");

  openButtons.forEach((button) => {
    button.addEventListener("click", () => {
      form.action = button.dataset.action;
      maDonInput.value = button.dataset.maDon;
      nguoiNhanInput.value = button.dataset.nguoiNhan;
      giaTriInput.value = button.dataset.giaTri;
      thoiGianInput.value = button.dataset.thoiGian;
      tinhTrangInput.value = button.dataset.tinhTrang;
      syncStatusColor();
      openModal();
    });
  });

  closeButtons.forEach((button) => {
    button.addEventListener("click", closeModal);
  });

  backdrop.addEventListener("click", (event) => {
    if (event.target === backdrop) {
      closeModal();
    }
  });

  if (backdrop.dataset.openOnLoad === "true") {
    openModal();
  }

  if (tinhTrangInput) {
    tinhTrangInput.addEventListener("change", syncStatusColor);
    syncStatusColor();
  }
});
