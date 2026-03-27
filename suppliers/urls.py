from django.urls import path

from .views import (
    AccountCreateView,
    AccountDeleteView,
    AccountListView,
    KiemKeCreateView,
    KiemKeDetailView,
    AccountUpdateView,
    KiemKeListView,
    SupplierListView,
)

urlpatterns = [
    path("", SupplierListView.as_view(), name="suppliers_list"),
    path("accounts/", AccountListView.as_view(), name="accounts_list"),
    path("accounts/create/", AccountCreateView.as_view(), name="account_create"),
    path("accounts/<int:pk>/edit/", AccountUpdateView.as_view(), name="account_edit"),
    path("accounts/<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"),
    path("kiem-ke/", KiemKeListView.as_view(), name="kiemke_list"),
    path("kiem-ke/create/", KiemKeCreateView.as_view(), name="kiemke_create"),
    path("kiem-ke/<int:pk>/", KiemKeDetailView.as_view(), name="kiemke_detail"),
]
