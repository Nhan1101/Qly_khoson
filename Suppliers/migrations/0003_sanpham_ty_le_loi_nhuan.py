from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("suppliers", "0002_alter_chitietphieukiemke_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sanpham",
            name="ty_le_loi_nhuan",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
