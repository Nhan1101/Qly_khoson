from decimal import Decimal

from django.db import migrations, models
from django.utils import timezone


def seed_orders(apps, schema_editor):
    DonHang = apps.get_model("Order", "DonHang")
    sample_rows = [
        ("XXXXXX1", "Nguyễn Văn A", Decimal("50000000"), timezone.datetime(2022, 11, 13, 15, 30), "dang_giao_hang"),
        ("XXXXXX2", "Nguyễn Văn B", Decimal("50000000"), timezone.datetime(2022, 11, 13, 11, 9), "da_xuat"),
        ("XXXXXX3", "Nguyễn Văn C", Decimal("50000000"), timezone.datetime(2022, 11, 12, 14, 30), "dang_giao_hang"),
        ("XXXXXX4", "Nguyễn Văn A", Decimal("50000000"), timezone.datetime(2022, 11, 12, 12, 30), "huy"),
        ("XXXXXX5", "Nguyễn Văn D", Decimal("50000000"), timezone.datetime(2022, 11, 12, 9, 30), "da_giao_hang"),
        ("XXXXXX6", "Nguyễn Văn B", Decimal("50000000"), timezone.datetime(2022, 11, 11, 15, 30), "da_giao_hang"),
        ("XXXXXX7", "Nguyễn Văn A", Decimal("50000000"), timezone.datetime(2022, 11, 10, 16, 8), "da_xuat"),
        ("XXXXXX8", "Nguyễn Văn E", Decimal("50000000"), timezone.datetime(2022, 11, 10, 15, 5), "da_giao_hang"),
        ("XXXXXX9", "Nguyễn Văn E", Decimal("50000000"), timezone.datetime(2022, 11, 10, 9, 55), "huy"),
        ("XXXXXX10", "Nguyễn Văn A", Decimal("50000000"), timezone.datetime(2022, 11, 10, 8, 30), "da_xuat"),
        ("XXXXXX11", "Nguyễn Văn A", Decimal("50000000"), timezone.datetime(2022, 11, 9, 17, 27), "da_xuat"),
        ("XXXXXX12", "Nguyễn Văn C", Decimal("50000000"), timezone.datetime(2022, 11, 9, 7, 30), "hoan_hang"),
        ("XXXXXX13", "Nguyễn Văn F", Decimal("50000000"), timezone.datetime(2022, 11, 8, 15, 30), "da_xuat"),
        ("XXXXXX14", "Nguyễn Văn B", Decimal("50000000"), timezone.datetime(2022, 11, 8, 12, 6), "da_xuat"),
    ]
    for ma_don, nguoi_nhan, gia_tri, thoi_gian, tinh_trang in sample_rows:
        DonHang.objects.create(
            ma_don=ma_don,
            nguoi_nhan=nguoi_nhan,
            gia_tri=gia_tri,
            thoi_gian=timezone.make_aware(thoi_gian),
            tinh_trang=tinh_trang,
        )


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DonHang",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ma_don", models.CharField(max_length=30, unique=True)),
                ("nguoi_nhan", models.CharField(max_length=100)),
                ("gia_tri", models.DecimalField(decimal_places=0, max_digits=15)),
                ("thoi_gian", models.DateTimeField()),
                (
                    "tinh_trang",
                    models.CharField(
                        choices=[
                            ("dang_giao_hang", "Đang giao hàng"),
                            ("da_xuat", "Đã xuất"),
                            ("da_giao_hang", "Đã giao hàng"),
                            ("huy", "Hủy"),
                            ("hoan_hang", "Hoàn hàng"),
                        ],
                        default="dang_giao_hang",
                        max_length=20,
                    ),
                ),
            ],
            options={
                "verbose_name": "Đơn hàng",
                "verbose_name_plural": "Đơn hàng",
                "ordering": ["-thoi_gian", "id"],
            },
        ),
        migrations.RunPython(seed_orders, migrations.RunPython.noop),
    ]
