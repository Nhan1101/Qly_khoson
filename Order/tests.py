from django.test import TestCase
from django.urls import reverse

from .models import DonHang


class OrderViewTest(TestCase):
    def test_order_list_page_loads(self):
        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Trạng thái giao hàng")
        self.assertContains(response, "XXXXXX1")

    def test_order_update_persists_changes(self):
        order = DonHang.objects.get(ma_don="XXXXXX1")

        response = self.client.post(
            reverse("order-update", args=[order.pk]),
            {
                "ma_don": "HD0001",
                "nguoi_nhan": "Khách Hàng Mới",
                "gia_tri": "75000000",
                "thoi_gian": "2022-11-13T16:45",
                "tinh_trang": DonHang.TinhTrang.DA_GIAO,
            },
        )

        self.assertRedirects(response, reverse("order-list") + f"?updated={order.pk}")
        order.refresh_from_db()
        self.assertEqual(order.ma_don, "HD0001")
        self.assertEqual(order.nguoi_nhan, "Khách Hàng Mới")
        self.assertEqual(order.tinh_trang, DonHang.TinhTrang.DA_GIAO)
