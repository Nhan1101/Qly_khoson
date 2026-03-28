from django.urls import path

from .views import order_list_view, order_update_view

urlpatterns = [
    path("", order_list_view, name="order-list"),
    path("<int:pk>/edit/", order_update_view, name="order-update"),
]
