from django.test import TestCase


class HomeSmokeTest(TestCase):
    def test_landing_page_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sơn Alex sơn để Thành Công")
        self.assertContains(response, "HOTLINE: 1900 98 89 67 / 0961 662 268")
        self.assertContains(response, "/login/")

    def test_landing_page_shows_tracking_result_for_known_phone(self):
        response = self.client.get("/", {"phone": "093245135"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thông tin đơn hàng")
        self.assertContains(response, "0324135564")
        self.assertContains(response, "Giao thành công")

    def test_landing_page_shows_not_found_message_for_unknown_phone(self):
        response = self.client.get("/", {"phone": "0900000000"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Không tìm thấy đơn hàng")
        self.assertContains(response, "0900000000")

    def test_login_page_loads(self):
        response = self.client.get("/login/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ĐĂNG NHẬP VÀO TÀI KHOẢN")
        self.assertContains(response, "Tên đăng nhập")
