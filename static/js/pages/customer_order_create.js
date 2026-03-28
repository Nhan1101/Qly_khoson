document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector(".order-create-page");
  const listUrl = page?.dataset.listUrl || "#";
  const donGiaInput = document.getElementById("order-create-don-gia");
  const soLuongInput = document.getElementById("order-create-so-luong");
  const thanhTienInput = document.getElementById("order-create-thanh-tien");
  const totalEl = document.getElementById("order-create-total");
  const saveBtn = document.getElementById("order-create-save-btn");

  const parseNumber = (value) => {
    const normalized = String(value || "").replace(/\./g, "").replace(/,/g, "").trim();
    const parsed = Number(normalized);
    return Number.isFinite(parsed) ? parsed : 0;
  };

  const formatNumber = (value) => value.toLocaleString("vi-VN");

  const recalculate = () => {
    const donGia = parseNumber(donGiaInput?.value);
    const soLuong = parseNumber(soLuongInput?.value);
    const thanhTien = donGia * soLuong;

    if (thanhTienInput) {
      thanhTienInput.value = thanhTien > 0 ? formatNumber(thanhTien) : "";
    }

    if (totalEl) {
      totalEl.textContent = `${formatNumber(thanhTien)} đ`;
    }
  };

  donGiaInput?.addEventListener("input", recalculate);
  soLuongInput?.addEventListener("input", recalculate);
  recalculate();

  saveBtn?.addEventListener("click", () => {
    window.location.href = listUrl;
  });
});
