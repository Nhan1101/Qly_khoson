from django import forms

from .models import DonHang


class DonHangForm(forms.ModelForm):
    thoi_gian = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M", "%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    tinh_trang = forms.ChoiceField(
        choices=DonHang.TinhTrang.choices,
        widget=forms.Select(attrs={"class": "status-select"}),
    )

    class Meta:
        model = DonHang
        fields = ["ma_don", "nguoi_nhan", "gia_tri", "thoi_gian", "tinh_trang"]
