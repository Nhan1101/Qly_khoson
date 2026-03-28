from decimal import Decimal

from django.test import TestCase

from Suppliers.models import (
    ChiTietPhieuNhap,
    ChiTietPhieuXuat,
    DoiTuongNhan,
    NguoiDung,
    NhaCungCap,
    PhieuNhap,
    PhieuXuat,
    SanPham,
    TonKho,
)


class ReportsSmokeTest(TestCase):
    def setUp(self):
        self.user = NguoiDung.objects.create_user(
            username="report-user",
            password="123456",
            vai_tro="Admin",
        )
        self.receiver = DoiTuongNhan.objects.create(ten_nguoi_nhan="Nguyen Van A")
        self.supplier = NhaCungCap.objects.create(ten_ncc="Nha cung cap A", so_dien_thoai="0123456789")
        self.product = SanPham.objects.create(
            ma_son="SP001",
            ten_son="Son noi that",
            loai_son="Noi that",
            don_vi_tinh="Thung",
            gia_ban=Decimal("100000.00"),
            gia_nhap=Decimal("80000.00"),
        )
        TonKho.objects.create(san_pham=self.product, so_luong_ton=50, muc_toi_thieu=5)
        self.receipt = PhieuXuat.objects.create(doi_tuong_nhan=self.receiver, nguoi_dung=self.user)
        ChiTietPhieuXuat.objects.create(phieu_xuat=self.receipt, san_pham=self.product, so_luong=5)
        self.import_receipt = PhieuNhap.objects.create(nha_cung_cap=self.supplier, nguoi_dung=self.user)
        ChiTietPhieuNhap.objects.create(phieu_nhap=self.import_receipt, san_pham=self.product, so_luong=6)

    def test_export_report_page_loads(self):
        response = self.client.get("/reports/export/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PX001")
        self.assertContains(response, "Nguyen Van A")
        self.assertContains(response, "500000")

    def test_import_report_page_loads(self):
        response = self.client.get("/reports/import/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PN001")
        self.assertContains(response, "Nha cung cap A")
        self.assertContains(response, "480000")

    def test_revenue_report_page_loads(self):
        response = self.client.get("/reports/revenue/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.receipt.ngay_xuat.strftime("%d/%m/%Y"))
        self.assertContains(response, "500000")
        self.assertContains(response, "5")
