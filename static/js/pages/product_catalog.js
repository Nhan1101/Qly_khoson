const productCatalogRows = [
  { stt: 1, ten: "Sơn Alex - Màu ABC", ma: "XXXXX", loai: "Sơn nội thất", dvt: "Thùng", ton: 20, giaBan: "3.000.000", giaVon: "2.000.000" },
  { stt: 2, ten: "Sơn Alex - Màu ABC", ma: "XXXXX", loai: "Sơn ngoại thất", dvt: "Thùng", ton: 17, giaBan: "2.000.000", giaVon: "1.000.000" },
  { stt: 3, ten: "Sơn Alex - Màu ABC", ma: "XXXXX", loai: "Sơn chuyên dụng", dvt: "Thùng", ton: 10, giaBan: "1.000.000", giaVon: "500.000" },
  { stt: 4, ten: "Sơn Alex - Màu ABC", ma: "XXXXX", loai: "Sơn nội thất", dvt: "Thùng", ton: 12, giaBan: "3.000.000", giaVon: "2.000.000" },
  { stt: 5, ten: "Sơn Alex - Màu ABC", ma: "XXXXX", loai: "Sơn nội thất", dvt: "Thùng", ton: 50, giaBan: "3.000.000", giaVon: "2.000.000" },
  { stt: 6, ten: "Sơn Alex - Màu ABC", ma: "XXXXX", loai: "Sơn nội thất", dvt: "Thùng", ton: 30, giaBan: "5.000.000", giaVon: "3.000.000" },
  { stt: 7, ten: "Sơn Alex - Màu ABC", ma: "XXXXX", loai: "Sơn nội thất", dvt: "Thùng", ton: 5, giaBan: "6.000.000", giaVon: "4.000.000" },
  { stt: 8, ten: "Sơn Alex - Màu ABC", ma: "XXXXX", loai: "Sơn ngoại thất", dvt: "Thùng", ton: 15, giaBan: "7.000.000", giaVon: "6.000.000" },
  { stt: 9, ten: "Sơn Alex - Màu ABC", ma: "XXXXX", loai: "Sơn ngoại thất", dvt: "Thùng", ton: 70, giaBan: "2.000.000", giaVon: "1.000.000" },
  { stt: 10, ten: "Sơn Alex - Màu ABC", ma: "XXXXX", loai: "Sơn ngoại thất", dvt: "Thùng", ton: 30, giaBan: "1.000.000", giaVon: "800.000" },
  { stt: 11, ten: "Sơn Alex - Màu ABC", ma: "XXXXX", loai: "Sơn chuyên dụng", dvt: "Thùng", ton: 5, giaBan: "2.000.000", giaVon: "1.000.000" },
  { stt: 12, ten: "Sơn Alex - Màu ABC", ma: "XXXXX", loai: "Sơn chuyên dụng", dvt: "Thùng", ton: 8, giaBan: "2.000.000", giaVon: "1.000.000" }
];

document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.getElementById("product-catalog-table-body");
  if (!tableBody) {
    return;
  }

  tableBody.innerHTML = productCatalogRows.map((row) => `
    <tr>
      <td>${row.stt}</td>
      <td class="product-name-cell">${row.ten}</td>
      <td>${row.ma}</td>
      <td>${row.loai}</td>
      <td>${row.dvt}</td>
      <td>${row.ton}</td>
      <td class="product-money-cell">${row.giaBan}</td>
      <td class="product-money-cell">${row.giaVon}</td>
      <td>
        <div class="product-actions-cell">
          <button class="product-icon-btn edit" type="button" title="Chỉnh sửa" aria-label="Chỉnh sửa">
            <i class="fa-solid fa-pen"></i>
          </button>
          <button class="product-icon-btn delete" type="button" title="Xóa" aria-label="Xóa">
            <i class="fa-solid fa-trash"></i>
          </button>
        </div>
      </td>
    </tr>
  `).join("");
});
