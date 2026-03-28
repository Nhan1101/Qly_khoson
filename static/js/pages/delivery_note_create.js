document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector(".delivery-create-page");
  const customerOrderListUrl = page?.dataset.customerOrderListUrl || "#";
  const deliveryDetailUrl = page?.dataset.deliveryDetailUrl || "#";
  const source = localStorage.getItem("deliveryNoteSource") || "";
  const exportType = localStorage.getItem("customerOrderExportType") || "";
  const exportDraft = JSON.parse(localStorage.getItem("customerOrderExportDraft") || "null");
  const draftData = JSON.parse(localStorage.getItem("deliveryNoteDraft") || "null");

  const initialData = exportDraft ? {
    nguonNhan: exportDraft.tenKhachHang || "",
    maDon: exportDraft.maDon || "",
    soDienThoai: exportDraft.soDienThoai || "",
    diaChi: exportDraft.diaChi || "",
    maPhieu: "",
    ngayXuat: "",
    duKienGiao: "",
    lyDoXuat: exportType === "partial" ? "Xuất kho một phần cho khách hàng" : "Xuất kho toàn phần cho khách hàng",
    tongTien: exportDraft.tongTien || "0 đ",
    items: Array.isArray(exportDraft.items) ? exportDraft.items : []
  } : (draftData || {
    nguonNhan: "",
    maDon: "",
    soDienThoai: "",
    diaChi: "",
    maPhieu: "",
    ngayXuat: "",
    duKienGiao: "",
    lyDoXuat: "",
    tongTien: "0 đ",
    items: []
  });

  const itemsBody = document.getElementById("delivery-create-items");
  const totalEl = document.getElementById("delivery-create-tong-tien");
  const saveBtn = document.getElementById("delivery-create-save-btn");
  const addBtn = document.getElementById("delivery-create-add-btn");
  const successModal = document.getElementById("delivery-success-modal");
  const exportBadge = document.getElementById("delivery-create-export-badge");

  const setValue = (id, value) => {
    const el = document.getElementById(id);
    if (el) {
      el.value = value || "";
    }
  };

  setValue("delivery-create-nguon-nhan", initialData.nguonNhan);
  setValue("delivery-create-ma-don", initialData.maDon);
  setValue("delivery-create-so-dien-thoai", initialData.soDienThoai);
  setValue("delivery-create-dia-chi", initialData.diaChi);
  setValue("delivery-create-ma-phieu", initialData.maPhieu);
  setValue("delivery-create-ngay-xuat", initialData.ngayXuat);
  setValue("delivery-create-du-kien-giao", initialData.duKienGiao);
  setValue("delivery-create-ly-do-xuat", initialData.lyDoXuat);

  if (source === "customer-order" && exportBadge) {
    exportBadge.style.display = "inline-flex";
    exportBadge.textContent = exportType === "partial" ? "Xuất kho một phần" : "Xuất kho toàn phần";
  }

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
      <td><input class="delivery-create-row-input text-left" type="text" value="${item.tenHangHoa || ""}"></td>
      <td><input class="delivery-create-row-input" type="text" value="${item.maHang || ""}"></td>
      <td><input class="delivery-create-row-input" type="text" value="${item.donViTinh || ""}"></td>
      <td><input class="delivery-create-row-input" data-role="don-gia" type="text" value="${item.donGia || ""}"></td>
      <td><input class="delivery-create-row-input" data-role="so-luong" type="text" value="${item.soLuong || ""}"></td>
      <td><input class="delivery-create-row-input readonly" data-role="thanh-tien" type="text" value="${item.thanhTien || ""}" readonly></td>
      <td><button class="delivery-create-delete-btn" data-role="delete" type="button"><i class="fa-solid fa-trash-can"></i></button></td>
    </tr>
  `;

  const items = Array.isArray(initialData.items) && initialData.items.length ? initialData.items : [
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
    const getValue = (id) => document.getElementById(id)?.value.trim() || "";
    const items = Array.from(itemsBody.querySelectorAll("tr")).map((row) => ({
      tenHangHoa: row.children[1].querySelector("input")?.value.trim() || "",
      maHang: row.children[2].querySelector("input")?.value.trim() || "",
      donViTinh: row.children[3].querySelector("input")?.value.trim() || "",
      donGia: row.querySelector("[data-role='don-gia']")?.value.trim() || "",
      soLuong: row.querySelector("[data-role='so-luong']")?.value.trim() || "",
      thanhTien: row.querySelector("[data-role='thanh-tien']")?.value.trim() || ""
    })).filter((item) => Object.values(item).some(Boolean));

    const draft = {
      nguonNhan: getValue("delivery-create-nguon-nhan"),
      maDon: getValue("delivery-create-ma-don"),
      soDienThoai: getValue("delivery-create-so-dien-thoai"),
      diaChi: getValue("delivery-create-dia-chi"),
      maPhieu: getValue("delivery-create-ma-phieu"),
      ngayXuat: getValue("delivery-create-ngay-xuat"),
      duKienGiao: getValue("delivery-create-du-kien-giao"),
      lyDoXuat: getValue("delivery-create-ly-do-xuat"),
      tongTien: totalEl.textContent.trim(),
      items
    };

    localStorage.setItem("deliveryNoteDraft", JSON.stringify(draft));

    if (source === "customer-order") {
      successModal.classList.add("show");
      localStorage.removeItem("customerOrderExportDraft");
      localStorage.removeItem("customerOrderExportType");
      localStorage.removeItem("deliveryNoteSource");
      setTimeout(() => {
        window.location.href = customerOrderListUrl;
      }, 1200);
      return;
    }

    window.location.href = deliveryDetailUrl;
  });
});
