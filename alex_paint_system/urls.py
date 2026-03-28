"""
URL configuration for alex_paint_system project.
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('Home.urls')),
    path('admin/', admin.site.urls),
    path('suppliers/', include('Suppliers.urls')),
    path('reports/', include('Reports.urls')),
    path('orders/', include('Order.urls')),
    path('phieu-xuat-kho/', TemplateView.as_view(template_name='delivery_note_list.html'), name='delivery-note-list'),
    path('don-giao-hang/tao-moi/', TemplateView.as_view(template_name='delivery_order_create.html'), name='delivery-order-create'),
    path('phieu-xuat-kho/tao-moi/', TemplateView.as_view(template_name='delivery_note_create.html'), name='delivery-note-create'),
    path('phieu-xuat-kho/sua/', TemplateView.as_view(template_name='delivery_note_edit.html'), name='delivery-note-edit'),
    path('phieu-xuat-kho/thong-tin/', TemplateView.as_view(template_name='delivery_note_detail.html'), name='delivery-note-detail'),
    path('don-dat-hang-khach-hang/', TemplateView.as_view(template_name='customer_order_list.html'), name='customer-order-list'),
    path('don-dat-hang-khach-hang/tao-moi/', TemplateView.as_view(template_name='customer_order_create.html'), name='customer-order-create'),
    path('don-dat-hang-khach-hang/xem-chi-tiet/', TemplateView.as_view(template_name='customer_order_detail.html'), name='customer-order-detail'),
    path('don-dat-hang-khach-hang/sua/', TemplateView.as_view(template_name='customer_order_edit.html'), name='customer-order-edit'),
    path('danh-muc-san-pham/', TemplateView.as_view(template_name='product_catalog.html'), name='product-catalog'),
    path('canh-bao-ton-kho/', TemplateView.as_view(template_name='inventory_alert.html'), name='inventory-alert'),
    path('canh-bao-han-su-dung/', TemplateView.as_view(template_name='expiry_alert.html'), name='expiry-alert'),
]
