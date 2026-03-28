from django.db import models


class DonHang(models.Model):
    class TinhTrang(models.TextChoices):
        DANG_GIAO = "dang_giao_hang", "Đang giao hàng"
        DA_XUAT = "da_xuat", "Đã xuất"
        DA_GIAO = "da_giao_hang", "Đã giao hàng"
        HUY = "huy", "Hủy"
        HOAN_HANG = "hoan_hang", "Hoàn hàng"

    ma_don = models.CharField(max_length=30, unique=True)
    nguoi_nhan = models.CharField(max_length=100)
    gia_tri = models.DecimalField(max_digits=15, decimal_places=0)
    thoi_gian = models.DateTimeField()
    tinh_trang = models.CharField(max_length=20, choices=TinhTrang.choices, default=TinhTrang.DANG_GIAO)

    class Meta:
        ordering = ["-thoi_gian", "id"]
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"

    def __str__(self):
        return self.ma_don

    @property
    def status_css_class(self):
        return self.tinh_trang.replace("_", "-")
