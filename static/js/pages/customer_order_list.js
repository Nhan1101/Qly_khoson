const customerOrderRows = [
  {
    stt: 1,
    ma: "DH0001",
    ten: "Nguyễn Văn A",
    gia: "50.000.000",
    time: "13/11/2022 15:30",
    st: "Chờ xử lý",
    detail: {
      tenKhachHang: "Nguyễn Văn A",
      maDon: "DH0001",
      soDienThoai: "0975260109",
      diaChi: "35 Tạ Hiện, Đà Nẵng",
      maPhieu: "",
      ngayDatHang: "13-11-2022",
      ghiChu: "Giao 5 thùng vào ngày 10/3/2026, còn lại giao vào ngày 15/3/2026",
      tongTien: "50.000.000 đ",
      items: [
        { tenHangHoa: "Sơn Alex - Màu ABC", maHang: "SP001", donViTinh: "Thùng", donGia: "5.000.000", soLuong: "10", thanhTien: "50.000.000" }
      ]
    }
  },
  { stt: 2, ma: "DH0002", ten: "Nguyễn Văn A", gia: "50.000.000", time: "13/11/2022 11:09", st: "Đã xuất 1 phần" },
  { stt: 3, ma: "DH0003", ten: "Nguyễn Văn A", gia: "50.000.000", time: "12/11/2022 14:30", st: "Chờ xử lý" },
  { stt: 4, ma: "DH0004", ten: "Nguyễn Văn A", gia: "50.000.000", time: "12/11/2022 12:30", st: "Đã hủy" },
  { stt: 5, ma: "DH0005", ten: "Nguyễn Văn A", gia: "50.000.000", time: "12/11/2022 09:30", st: "Đã hủy" },
  { stt: 7, ma: "DH0007", ten: "Nguyễn Văn A", gia: "50.000.000", time: "10/11/2022 16:08", st: "Đã xuất" },
  { stt: 8, ma: "DH0008", ten: "Nguyễn Văn A", gia: "50.000.000", time: "10/11/2022 15:05", st: "Đã xuất 1 phần" },
  { stt: 9, ma: "DH0009", ten: "Nguyễn Văn A", gia: "50.000.000", time: "10/11/2022 09:55", st: "Đã hủy" },
  { stt: 10, ma: "DH0010", ten: "Nguyễn Văn A", gia: "50.000.000", time: "10/11/2022 08:30", st: "Đã xuất" },
  { stt: 11, ma: "DH0011", ten: "Nguyễn Văn A", gia: "50.000.000", time: "09/11/2022 17:27", st: "Đã xuất 1 phần" },
  { stt: 12, ma: "DH0012", ten: "Nguyễn Văn A", gia: "50.000.000", time: "09/11/2022 07:30", st: "Đã xuất 1 phần" }
];

function customerOrderBadgeClass(status) {
  if (status === "Chờ xử lý") {
    return "order-badge-waiting";
  }
  if (status === "Đã xuất 1 phần") {
    return "order-badge-partial";
  }
  if (status === "Đã hủy") {
    return "order-badge-cancelled";
  }
  if (status === "Đã xuất") {
    return "order-badge-exported";
  }
  return "order-badge-waiting";
}

document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector(".order-page");
  const tableBody = document.getElementById("customer-order-table-body");
  const exportModal = document.getElementById("order-export-modal");
  const exportClose = document.getElementById("order-export-close");
  const exportCancel = document.getElementById("order-export-cancel");
  const deleteModal = document.getElementById("order-delete-modal");
  const deleteConfirm = document.getElementById("order-delete-confirm");
  const deleteCancel = document.getElementById("order-delete-cancel");
  const detailUrl = page?.dataset.detailUrl || "#";
  const editUrl = page?.dataset.editUrl || "#";
  const deliveryCreateUrl = page?.dataset.deliveryCreateUrl || "#";
  let selectedOrder = null;
  let pendingDeleteIndex = null;

  if (!tableBody || !page) {
    return;
  }

  const closeExportModal = () => {
    exportModal?.classList.remove("show");
    selectedOrder = null;
  };

  const closeDeleteModal = () => {
    deleteModal?.classList.remove("show");
    pendingDeleteIndex = null;
  };

  const renderTable = () => {
    tableBody.innerHTML = customerOrderRows.map((row, index) => `
      <tr>
        <td>${row.stt}</td>
        <td>${row.ma}</td>
        <td>${row.ten}</td>
        <td class="order-td-value">${row.gia}</td>
        <td>${row.time}</td>
        <td><span class="order-badge ${customerOrderBadgeClass(row.st)}">${row.st}</span></td>
        <td>
          <div class="order-actions">
            <a class="order-act-icon" href="${detailUrl}"><i class="fa-regular fa-eye" style="color: #555;"></i></a>
            <a class="order-act-icon" href="${editUrl}"><i class="fa-solid fa-pen" style="color: #555;"></i></a>
            <button class="order-act-icon order-open-delete" type="button" data-index="${index}">
              <i class="fa-solid fa-trash-can" style="color: #e53c2b;"></i>
            </button>
            <button class="order-act-icon order-open-export" type="button" data-index="${index}">
              <i class="fa-regular fa-square-plus" style="color: #27ae60;"></i>
            </button>
          </div>
        </td>
      </tr>
    `).join("");

    tableBody.querySelectorAll(".order-open-export").forEach((button) => {
      button.addEventListener("click", () => {
        const index = Number(button.dataset.index);
        selectedOrder = customerOrderRows[index] || null;
        exportModal?.classList.add("show");
      });
    });

    tableBody.querySelectorAll(".order-open-delete").forEach((button) => {
      button.addEventListener("click", () => {
        pendingDeleteIndex = Number(button.dataset.index);
        deleteModal?.classList.add("show");
      });
    });
  };

  renderTable();

  exportClose?.addEventListener("click", closeExportModal);
  exportCancel?.addEventListener("click", closeExportModal);

  exportModal?.addEventListener("click", (event) => {
    if (event.target === exportModal) {
      closeExportModal();
    }
  });

  document.querySelectorAll("[data-export-type]").forEach((button) => {
    button.addEventListener("click", () => {
      if (!selectedOrder) {
        return;
      }

      const exportType = button.dataset.exportType;
      const payload = selectedOrder.detail || {
        tenKhachHang: selectedOrder.ten,
        maDon: selectedOrder.ma,
        soDienThoai: "0975260109",
        diaChi: "35 Tạ Hiện, Đà Nẵng",
        maPhieu: "",
        ngayDatHang: "13-11-2022",
        ghiChu: "",
        tongTien: `${selectedOrder.gia} đ`,
        items: [
          {
            tenHangHoa: "Sơn Alex - Màu ABC",
            maHang: "XXXXX",
            donViTinh: "Thùng",
            donGia: "5.000.000",
            soLuong: "10",
            thanhTien: selectedOrder.gia
          }
        ]
      };

      localStorage.setItem("customerOrderExportDraft", JSON.stringify(payload));
      localStorage.setItem("customerOrderExportType", exportType);
      localStorage.setItem("deliveryNoteSource", "customer-order");
      window.location.href = deliveryCreateUrl;
    });
  });

  deleteConfirm?.addEventListener("click", () => {
    if (pendingDeleteIndex === null) {
      return;
    }

    customerOrderRows.splice(pendingDeleteIndex, 1);
    closeDeleteModal();
    renderTable();
  });

  deleteCancel?.addEventListener("click", closeDeleteModal);

  deleteModal?.addEventListener("click", (event) => {
    if (event.target === deleteModal) {
      closeDeleteModal();
    }
  });
});
