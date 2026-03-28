const inventoryRows = [
    { stt: 1, ten: "Sơn nước Alex A", ton: 12, min: 15, tt: "Thiếu nhẹ" },
    { stt: 2, ten: "Sơn nước Alex B", ton: 10, min: 15, tt: "Thiếu nhẹ" },
    { stt: 3, ten: "Sơn nước Alex C", ton: 5, min: 15, tt: "Nguy cấp" },
    { stt: 4, ten: "Sơn nước Alex E", ton: 10, min: 15, tt: "Thiếu nhẹ" },
    { stt: 5, ten: "Sơn nước Alex F", ton: 3, min: 15, tt: "Nguy cấp" },
    { stt: 6, ten: "Sơn nước Alex G", ton: 5, min: 15, tt: "Nguy cấp" },
    { stt: 7, ten: "Sơn nước Alex H", ton: 3, min: 15, tt: "Nguy cấp" },
    { stt: 8, ten: "Sơn nước Alex I", ton: 5, min: 15, tt: "Nguy cấp" },
    { stt: 9, ten: "Sơn nước Alex K", ton: 6, min: 15, tt: "Nguy cấp" },
    { stt: 10, ten: "Sơn nước Alex L", ton: 4, min: 15, tt: "Nguy cấp" },
    { stt: 11, ten: "Sơn nước Alex M", ton: 5, min: 15, tt: "Nguy cấp" },
    { stt: 12, ten: "Sơn nước Alex N", ton: 5, min: 15, tt: "Nguy cấp" }
  ];

  document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.getElementById("inventory-table-body");
    if (!tableBody) {
      return;
    }

    tableBody.innerHTML = inventoryRows.map((row) => `
      <tr>
        <td>${row.stt}</td>
        <td>${row.ten}</td>
        <td>${row.ton}</td>
        <td>${row.min}</td>
        <td>
          <span class="inventory-badge ${row.tt === "Thiếu nhẹ" ? "inventory-badge-mild" : "inventory-badge-critical"}">${row.tt}</span>
        </td>
      </tr>
    `).join("");
  });

