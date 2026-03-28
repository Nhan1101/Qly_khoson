from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import DonHangForm
from .models import DonHang


def order_list_view(request):
    page_obj = Paginator(DonHang.objects.all(), 14).get_page(request.GET.get("page"))
    order_form = DonHangForm()

    context = {
        "page_obj": page_obj,
        "order_form": order_form,
        "active_menu": "order-status",
        "active_order_id": request.GET.get("editing"),
        "status_options": DonHang.TinhTrang.choices,
    }
    return render(request, "order/order_list.html", context)


def order_update_view(request, pk):
    order = get_object_or_404(DonHang, pk=pk)
    if request.method == "POST":
        form = DonHangForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('order-list')}?updated={order.pk}")

        page_obj = Paginator(DonHang.objects.all(), 14).get_page(request.GET.get("page"))
        context = {
            "page_obj": page_obj,
            "order_form": form,
            "active_menu": "order-status",
            "active_order_id": str(order.pk),
            "editing_order": order,
            "status_options": DonHang.TinhTrang.choices,
            "open_modal_on_load": True,
        }
        return render(request, "order/order_list.html", context, status=400)

    return redirect("order-list")
