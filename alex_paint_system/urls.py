from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="base.html"), name="home"),
    path("nhap-kho/", TemplateView.as_view(template_name="nhap_kho.html"), name="nhap_kho"),
    path("tao-phieu-nhap/", TemplateView.as_view(template_name="tao_phieu_nhap.html"), name="tao_phieu_nhap"),
    path("sua-phieu-nhap/", TemplateView.as_view(template_name="sua_phieu_nhap.html"), name="sua_phieu_nhap"),
    path("xem-phieu/", TemplateView.as_view(template_name="xem_chi_tiet_phieu.html"), name="xem_phieu"),
    path(
        "ds-don-dat-hang-ncc/",
        TemplateView.as_view(template_name="ds_don_dat_hang_ncc.html"),
        name="ds_don_dat_hang_ncc",
    ),
    path("tao-don-dat-hang/", TemplateView.as_view(template_name="tao_don_dat_hang.html"), name="tao_don_dat_hang"),
    path("chi-tiet-don-hang/", TemplateView.as_view(template_name="chi_tiet_don_hang.html"), name="chi_tiet_don_hang"),
    path("danh-sach-ncc/", TemplateView.as_view(template_name="dsncc.html"), name="danh_sach_ncc"),
    path("suppliers/", include("Suppliers.urls")),
    path("products/", include("Suppliers.products_urls")),
    path("admin/", admin.site.urls),
]
