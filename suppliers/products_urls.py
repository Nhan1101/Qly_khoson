from django.urls import path

from .views import (
    ProductListView,
    product_create,
    product_delete,
    product_update,
)

urlpatterns = [
    path("", ProductListView.as_view(), name="products_list"),
    path("create/", product_create, name="products_create"),
    path("update/<int:pk>/", product_update, name="products_update"),
    path("delete/<int:pk>/", product_delete, name="products_delete"),
]
