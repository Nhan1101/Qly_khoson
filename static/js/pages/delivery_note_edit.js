document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector(".delivery-edit-page");
  const listUrl = page?.dataset.listUrl || "#";
  const fallbackData = {
    nguonNhan: "Nguyễn Văn A",
    maDon: "XXXXX",
    soDienThoai: "0975260109",
    diaChi: "35 Tạ Hiện, Đà Nẵng",
    maPhieu: "XXXXXX",
    ngayXuat: "08/03/2026",
    duKienGiao: "15/3/2026",
    lyDoXuat: "Giao cho khách hàng",
    tongTien: "50.000.000 đ",
    items: [
      { tenHangHoa: "Sơn Alex - Màu EFG", maHang: "XXXXX", donViTinh: "Thùng", donGia: "30.000.000", soLuong: "10", thanhTien: "300.000.000" },
      { tenHangHoa: "Sơn Alex - Màu ABC", maHang: "XXXXX", donViTinh: "Thùng", donGia: "3.998.000", soLuong: "10", thanhTien: "39.980.000" },
      { tenHangHoa: "Sơn Alex - Màu ABC", maHang: "XXXXX", donViTinh: "Thùng", donGia: "40.000.000", soLuong: "5", thanhTien: "200.000.000" },
      { tenHangHoa: "Sơn Alex - Màu ABC", maHang: "XXXXX", donViTinh: "Thùng", donGia: "20.000.000", soLuong: "4", thanhTien: "80.000.000" },
      { tenHangHoa: "Sơn Alex - Màu ABC", maHang: "XXXXX", donViTinh: "Thùng", donGia: "790.000", soLuong: "55", thanhTien: "43.450.000" }
    ]
  };

  const selectedData = JSON.parse(localStorage.getItem("selectedDeliveryNote") || "null");
  const data = selectedData || fallbackData;

  const itemsBody = document.getElementById("delivery-edit-items");
  const totalEl = document.getElementById("delivery-edit-tong-tien");
  const modal = document.getElementById("delivery-save-modal");
  const addBtn = document.getElementById("delivery-edit-add-btn");
  const saveBtn = document.getElementById("delivery-edit-save-btn");

  const setValue = (id, value) => {
    const el = document.getElementById(id);
    if (el) {
      el.value = value || "";
    }
  };

  setValue("delivery-edit-nguon-nhan", data.nguonNhan);
  setValue("delivery-edit-ma-don", data.maDon);
  setValue("delivery-edit-so-dien-thoai", data.soDienThoai);
  setValue("delivery-edit-dia-chi", data.diaChi);
  setValue("delivery-edit-ma-phieu", data.maPhieu);
  setValue("delivery-edit-ngay-xuat", data.ngayXuat);
  setValue("delivery-edit-du-kien-giao", data.duKienGiao);
  setValue("delivery-edit-ly-do-xuat", data.lyDoXuat);

  const parseNumber = (value) => {
    const normalized = String(value || "").replace(/\./g, "").replace(/,/g, "").trim();
    const parsed = Number(normalized);
    return Number.isFinite(parsed) ? parsed : 0;
  };

  const formatNumber = (value) => value.toLocaleString("vi-VN");

  const recalculateTotals = () => {
    let total = 0;
    itemsBody.querySelectorAll("tr").forEach((row, index) => {
      const indexCell = row.querySelector("[data-role='index']");
      if (indexCell) {
        indexCell.textContent = index + 1;
      }

      const donGiaInput = row.querySelector("[data-role='don-gia']");
      const soLuongInput = row.querySelector("[data-role='so-luong']");
      const thanhTienInput = row.querySelector("[data-role='thanh-tien']");
      const thanhTien = parseNumber(donGiaInput?.value) * parseNumber(soLuongInput?.value);

      if (thanhTienInput) {
        thanhTienInput.value = thanhTien > 0 ? formatNumber(thanhTien) : "";
      }

      total += thanhTien;
    });

    totalEl.textContent = `${formatNumber(total)} đ`;
  };

  const attachRowEvents = (row) => {
    row.querySelector("[data-role='don-gia']")?.addEventListener("input", recalculateTotals);
    row.querySelector("[data-role='so-luong']")?.addEventListener("input", recalculateTotals);
    row.querySelector("[data-role='delete']")?.addEventListener("click", () => {
      row.remove();
      recalculateTotals();
    });
  };

  const renderRow = (item, index) => `
    <tr>
      <td data-role="index">${index + 1}</td>
      <td><input class="delivery-edit-row-input text-left" type="text" value="${item.tenHangHoa || ""}"></td>
      <td><input class="delivery-edit-row-input" type="text" value="${item.maHang || ""}"></td>
      <td><input class="delivery-edit-row-input" type="text" value="${item.donViTinh || ""}"></td>
      <td><input class="delivery-edit-row-input" data-role="don-gia" type="text" value="${item.donGia || ""}"></td>
      <td><input class="delivery-edit-row-input" data-role="so-luong" type="text" value="${item.soLuong || ""}"></td>
      <td><input class="delivery-edit-row-input" data-role="thanh-tien" type="text" value="${item.thanhTien || ""}" readonly></td>
      <td><button class="delivery-edit-delete-btn" data-role="delete" type="button"><i class="fa-solid fa-trash-can"></i></button></td>
    </tr>
  `;

  const items = Array.isArray(data.items) && data.items.length ? data.items : [
    { tenHangHoa: "", maHang: "", donViTinh: "", donGia: "", soLuong: "", thanhTien: "" }
  ];

  itemsBody.innerHTML = items.map((item, index) => renderRow(item, index)).join("");
  itemsBody.querySelectorAll("tr").forEach(attachRowEvents);
  recalculateTotals();

  addBtn?.addEventListener("click", () => {
    itemsBody.insertAdjacentHTML("beforeend", renderRow({}, itemsBody.querySelectorAll("tr").length));
    attachRowEvents(itemsBody.lastElementChild);
    recalculateTotals();
  });

  saveBtn?.addEventListener("click", () => {
    modal.classList.add("show");
    localStorage.setItem("deliveryNoteEdited", "true");
    setTimeout(() => {
      window.location.href = listUrl;
    }, 1200);
  });
});
