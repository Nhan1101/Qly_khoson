from django.views.generic import ListView

from .models import NhaCungCap


class SupplierListView(ListView):
    model = NhaCungCap
    template_name = "suppliers/index.html"
    context_object_name = "suppliers"
    paginate_by = 10
