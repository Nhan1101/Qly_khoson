from django.urls import path

from .views import (
    AccountCreateView,
    AccountDeleteView,
    AccountListView,
    AccountUpdateView,
    KiemKeCreateView,
    KiemKeDetailView,
    KiemKeListView,
    SupplierListView,
    supplier_create,
    supplier_delete,
    supplier_update,
)

urlpatterns = [
    path("", SupplierListView.as_view(), name="suppliers_list"),
    path("create/", supplier_create, name="suppliers_create"),
    path("update/<int:pk>/", supplier_update, name="suppliers_update"),
    path("delete/<int:pk>/", supplier_delete, name="suppliers_delete"),
    path("accounts/", AccountListView.as_view(), name="accounts_list"),
    path("accounts/create/", AccountCreateView.as_view(), name="account_create"),
    path("accounts/<int:pk>/edit/", AccountUpdateView.as_view(), name="account_edit"),
    path("accounts/<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"),
    path("kiem-ke/", KiemKeListView.as_view(), name="kiemke_list"),
    path("kiem-ke/create/", KiemKeCreateView.as_view(), name="kiemke_create"),
    path("kiem-ke/<int:pk>/", KiemKeDetailView.as_view(), name="kiemke_detail"),
]