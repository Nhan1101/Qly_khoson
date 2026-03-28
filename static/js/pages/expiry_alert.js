const expiryRows = [
    { stt: 1, ten: "Sơn nước Alex A", han: "09/01/2026", muc: "10 ngày", tt: "Còn hạn" },
    { stt: 2, ten: "Sơn nước Alex B", han: "22/12/2026", muc: "30 ngày", tt: "Còn hạn" },
    { stt: 3, ten: "Sơn nước Alex C", han: "10/11/2025", muc: "15 ngày", tt: "Sắp hết" },
    { stt: 4, ten: "Sơn nước Alex E", han: "22/12/2026", muc: "25 ngày", tt: "Còn hạn" },
    { stt: 5, ten: "Sơn nước Alex F", han: "10/2/2026", muc: "10 ngày", tt: "Sắp hết" },
    { stt: 6, ten: "Sơn nước Alex G", han: "7/12/2026", muc: "30 ngày", tt: "Còn hạn" },
    { stt: 7, ten: "Sơn nước Alex H", han: "15/12/2026", muc: "9 ngày", tt: "Sắp hết" },
    { stt: 8, ten: "Sơn nước Alex I", han: "31/03/2026", muc: "2 ngày", tt: "Sắp hết" },
    { stt: 9, ten: "Sơn nước Alex K", han: "10/11/2026", muc: "12 ngày", tt: "Sắp hết" },
    { stt: 10, ten: "Sơn nước Alex L", han: "9/12/2026", muc: "15 ngày", tt: "Còn hạn" },
    { stt: 11, ten: "Sơn nước Alex M", han: "17/11/2026", muc: "40 ngày", tt: "Còn hạn" },
    { stt: 12, ten: "Sơn nước Alex N", han: "20/04/2026", muc: "9 ngày", tt: "Sắp hết" }
  ];

document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.getElementById("expiry-table-body");

  tableBody.innerHTML = expiryRows.map(row => `
    <tr>
      <td>${row.stt}</td>
      <td title="${row.ten}">${row.ten}</td>
      <td>${row.han}</td>
      <td>${row.muc}</td>
      <td>
        <span class="expiry-badge ${row.tt === "Còn hạn" ? "expiry-badge-ok" : "expiry-badge-warn"}">
          ${row.tt}
        </span>
      </td>
    </tr>
  `).join("");
});

