from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import AccountForm
from .models import ChiTietPhieuKiemKe, NhaCungCap, NguoiDung, PhieuKiemKe, SanPham, TonKho


def apply_ticket_display_state(ticket):
    ticket.display_code = f"KK{ticket.pk:05d}"
    details = list(ticket.chitietphieukiemke_set.all())
    has_difference = any(detail.chenh_lech != 0 for detail in details)
    if ticket.trang_thai == "draft" and not details:
        ticket.display_status = "Đang làm"
        ticket.display_status_class = "status-draft"
    elif has_difference:
        ticket.display_status = "Chênh lệch"
        ticket.display_status_class = "status-diff"
    else:
        ticket.display_status = "Khớp"
        ticket.display_status_class = "status-match"


def build_ticket_detail_rows(ticket, data=None):
    stock_items = list(
        TonKho.objects.select_related("san_pham").order_by("san_pham__ten_son", "san_pham__id")
    )
    existing_details = {
        detail.san_pham_id: detail
        for detail in ticket.chitietphieukiemke_set.select_related("san_pham")
    }

    rows = []
    errors = []

    for index, stock in enumerate(stock_items, start=1):
        detail = existing_details.get(stock.san_pham_id)
        actual_key = f"actual_{stock.san_pham_id}"
        reason_key = f"reason_{stock.san_pham_id}"

        if data is None:
            actual_raw = "" if detail is None else str(detail.so_luong_thuc_te)
            reason_raw = "" if detail is None or not detail.ly_do else detail.ly_do
        else:
            actual_raw = data.get(actual_key, "").strip()
            reason_raw = data.get(reason_key, "").strip()

        actual_value = None
        difference = ""
        actual_error = ""
        reason_error = ""

        if actual_raw:
            try:
                actual_value = int(actual_raw)
                if actual_value < 0:
                    actual_error = "Tồn thực tế phải lớn hơn hoặc bằng 0."
                else:
                    difference = actual_value - stock.so_luong_ton
                    if actual_value < stock.so_luong_ton and not reason_raw:
                        reason_error = "Vui lòng nhập lý do khi tồn thực tế nhỏ hơn hệ thống."
            except ValueError:
                actual_error = "Tồn thực tế phải là số nguyên."

        if actual_error or reason_error:
            errors.append(stock.san_pham_id)

        rows.append(
            {
                "index": index,
                "stock": stock,
                "actual_name": actual_key,
                "reason_name": reason_key,
                "actual_raw": actual_raw,
                "reason_raw": reason_raw,
                "difference": difference,
                "actual_error": actual_error,
                "reason_error": reason_error,
            }
        )

    return rows, errors


@method_decorator(ensure_csrf_cookie, name="dispatch")
class SupplierListView(ListView):
    model = NhaCungCap
    template_name = "suppliers/index.html"
    context_object_name = "suppliers"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        ma = self.request.GET.get("ma", "").strip()
        ten_ncc = self.request.GET.get("ten_ncc", "").strip()
        email = self.request.GET.get("email", "").strip()
        so_dien_thoai = self.request.GET.get("so_dien_thoai", "").strip()
        dia_chi = self.request.GET.get("dia_chi", "").strip()

        if ma:
            normalized = ma.upper().replace("NCC_", "").replace("NCC", "").strip()
            if normalized.isdigit():
                queryset = queryset.filter(id=int(normalized))
            else:
                queryset = queryset.filter(id__icontains=normalized)

        if ten_ncc:
            queryset = queryset.filter(ten_ncc__icontains=ten_ncc)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if so_dien_thoai:
            queryset = queryset.filter(so_dien_thoai__icontains=so_dien_thoai)
        if dia_chi:
            queryset = queryset.filter(dia_chi__icontains=dia_chi)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_success"] = self.request.GET.get("deleted") == "1"
        last_id = NhaCungCap.objects.order_by("-id").values_list("id", flat=True).first() or 0
        context["next_code"] = f"NCC_{last_id + 1:02d}"
        return context


@method_decorator(ensure_csrf_cookie, name="dispatch")
class ProductListView(ListView):
    model = SanPham
    template_name = "products/index.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        ma_son = self.request.GET.get("ma_son", "").strip()
        ten_son = self.request.GET.get("ten_son", "").strip()
        loai_son = self.request.GET.get("loai_son", "").strip()
        mau_sac = self.request.GET.get("mau_sac", "").strip()
        don_vi_tinh = self.request.GET.get("don_vi_tinh", "").strip()

        if ma_son:
            queryset = queryset.filter(ma_son__icontains=ma_son)
        if ten_son:
            queryset = queryset.filter(ten_son__icontains=ten_son)
        if loai_son:
            queryset = queryset.filter(loai_son__icontains=loai_son)
        if mau_sac:
            queryset = queryset.filter(mau_sac__icontains=mau_sac)
        if don_vi_tinh:
            queryset = queryset.filter(don_vi_tinh__icontains=don_vi_tinh)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_success"] = self.request.GET.get("deleted") == "1"
        last_id = SanPham.objects.order_by("-id").values_list("id", flat=True).first() or 0
        context["next_code"] = f"SP_{last_id + 1:02d}"
        return context


class AccountListView(ListView):
    model = NguoiDung
    template_name = "accounts/index.html"
    context_object_name = "accounts"
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-ngay_tao", "-id")
        full_name = self.request.GET.get("full_name", "").strip()
        username = self.request.GET.get("username", "").strip()
        role = self.request.GET.get("role", "").strip()

        if full_name:
            queryset = queryset.filter(
                Q(first_name__icontains=full_name) | Q(last_name__icontains=full_name)
            )

        if username:
            queryset = queryset.filter(username__icontains=username)

        if role:
            queryset = queryset.filter(vai_tro=role)

        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filters"] = {
            "full_name": self.request.GET.get("full_name", ""),
            "username": self.request.GET.get("username", ""),
            "role": self.request.GET.get("role", ""),
        }
        params = self.request.GET.copy()
        params.pop("page", None)
        query_string = params.urlencode()
        ctx["query_suffix"] = f"&{query_string}" if query_string else ""
        edit_url = reverse("account_edit", args=[0])
        ctx["edit_url_template"] = edit_url.replace("/0/", "/{id}/", 1)
        return ctx


class KiemKeListView(ListView):
    model = PhieuKiemKe
    template_name = "kiemke/index.html"
    context_object_name = "tickets"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("nguoi_dung")
            .prefetch_related("chitietphieukiemke_set")
            .order_by("-ngay_tao", "-id")
        )
        ma_phieu = self.request.GET.get("ma_phieu", "").strip().upper()
        ngay_tao = self.request.GET.get("ngay_tao", "").strip()
        nguoi_thuc_hien = self.request.GET.get("nguoi_thuc_hien", "").strip()

        if ma_phieu:
            normalized_code = ma_phieu.replace("KK", "", 1) if ma_phieu.startswith("KK") else ma_phieu
            digits = "".join(ch for ch in normalized_code if ch.isdigit())
            if digits:
                queryset = queryset.filter(pk=int(digits))
            else:
                queryset = queryset.none()

        if ngay_tao:
            queryset = queryset.filter(ngay_tao__date=ngay_tao)

        if nguoi_thuc_hien:
            queryset = queryset.filter(
                Q(nguoi_dung__username__icontains=nguoi_thuc_hien)
                | Q(nguoi_dung__first_name__icontains=nguoi_thuc_hien)
                | Q(nguoi_dung__last_name__icontains=nguoi_thuc_hien)
            )

        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        start_index = ctx["page_obj"].start_index() if ctx.get("page_obj") else 0
        for offset, ticket in enumerate(ctx["object_list"], start=start_index):
            ticket.display_index = offset
            apply_ticket_display_state(ticket)

        ctx["filters"] = {
            "ma_phieu": self.request.GET.get("ma_phieu", ""),
            "ngay_tao": self.request.GET.get("ngay_tao", ""),
            "nguoi_thuc_hien": self.request.GET.get("nguoi_thuc_hien", ""),
        }
        ctx["updated_at"] = timezone.now()
        ctx["performers"] = NguoiDung.objects.filter(dang_hoat_dong=True).order_by(
            "first_name", "last_name", "username"
        )
        next_ticket_id = (
            PhieuKiemKe.objects.order_by("-id").values_list("id", flat=True).first() or 0
        ) + 1
        ctx["next_ticket_code"] = f"KK{next_ticket_id:05d}"
        params = self.request.GET.copy()
        params.pop("page", None)
        query_string = params.urlencode()
        ctx["query_suffix"] = f"&{query_string}" if query_string else ""
        return ctx


class KiemKeCreateView(View):
    def post(self, request, *args, **kwargs):
        performer_id = request.POST.get("nguoi_dung_id")
        next_url = request.POST.get("next") or reverse("kiemke_list")

        if not performer_id:
            messages.error(request, "Vui lòng chọn người thực hiện.")
            return redirect(next_url)

        performer = get_object_or_404(NguoiDung, pk=performer_id, dang_hoat_dong=True)
        PhieuKiemKe.objects.create(nguoi_dung=performer, trang_thai="draft")
        messages.success(request, "Đã tạo phiếu kiểm kê mới.")
        return redirect(next_url)


class KiemKeDetailView(View):
    template_name = "kiemke/detail.html"

    def get_ticket(self, pk):
        return get_object_or_404(
            PhieuKiemKe.objects.select_related("nguoi_dung").prefetch_related("chitietphieukiemke_set"),
            pk=pk,
        )

    def build_context(self, ticket, rows):
        apply_ticket_display_state(ticket)
        return {
            "ticket": ticket,
            "rows": rows,
            "is_readonly": ticket.trang_thai == "completed",
        }

    def get(self, request, pk, *args, **kwargs):
        ticket = self.get_ticket(pk)
        rows, _ = build_ticket_detail_rows(ticket)
        return render(request, self.template_name, self.build_context(ticket, rows))

    def post(self, request, pk, *args, **kwargs):
        ticket = self.get_ticket(pk)
        if ticket.trang_thai == "completed":
            messages.error(request, "Phiếu đã hoàn thành, không thể chỉnh sửa.")
            return redirect("kiemke_detail", pk=ticket.pk)

        rows, errors = build_ticket_detail_rows(ticket, request.POST)
        if errors:
            context = self.build_context(ticket, rows)
            context["form_error"] = "Vui lòng kiểm tra lại các dòng dữ liệu chưa hợp lệ."
            return render(request, self.template_name, context, status=400)

        existing_details = {
            detail.san_pham_id: detail for detail in ticket.chitietphieukiemke_set.all()
        }
        with transaction.atomic():
            for row in rows:
                stock = row["stock"]
                actual_raw = row["actual_raw"]
                reason_raw = row["reason_raw"] or None
                detail = existing_details.get(stock.san_pham_id)

                if not actual_raw:
                    if detail is not None:
                        detail.delete()
                    continue

                actual_value = int(actual_raw)
                ChiTietPhieuKiemKe.objects.update_or_create(
                    phieu_kiem_ke=ticket,
                    san_pham=stock.san_pham,
                    defaults={
                        "so_luong_he_thong": stock.so_luong_ton,
                        "so_luong_thuc_te": actual_value,
                        "chenh_lech": actual_value - stock.so_luong_ton,
                        "ly_do": reason_raw,
                    },
                )

        messages.success(request, "Đã lưu chi tiết phiếu kiểm kê.")
        return redirect("kiemke_detail", pk=ticket.pk)


class AccountCreateView(View):
    def post(self, request, *args, **kwargs):
        form = AccountForm(request.POST, require_password=True)
        next_url = request.POST.get("next") or reverse("accounts_list")
        if form.is_valid():
            form.save()
            messages.success(request, "Đã tạo tài khoản.")
        else:
            messages.error(request, "Không thể tạo tài khoản, kiểm tra dữ liệu.")
        return redirect(next_url)


class AccountUpdateView(View):
    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(NguoiDung, pk=pk)
        form = AccountForm(request.POST, instance=user)
        next_url = request.POST.get("next") or reverse("accounts_list")
        if form.is_valid():
            form.save()
            messages.success(request, "Đã cập nhật tài khoản.")
        else:
            messages.error(request, "Không thể cập nhật tài khoản, kiểm tra dữ liệu.")
        return redirect(next_url)


class AccountDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(NguoiDung, pk=pk)
        next_url = request.POST.get("next") or reverse("accounts_list")
        user.delete()
        messages.success(request, "Đã xoá tài khoản.")
        return redirect(next_url)


def _parse_decimal(value):
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError):
        return Decimal("0")


@require_POST
def supplier_create(request):
    ten_ncc = request.POST.get("ten_ncc", "").strip()
    so_dien_thoai = request.POST.get("so_dien_thoai", "").strip()
    email = request.POST.get("email", "").strip() or None
    dia_chi = request.POST.get("dia_chi", "").strip() or None

    if ten_ncc and so_dien_thoai:
        NhaCungCap.objects.create(
            ten_ncc=ten_ncc,
            so_dien_thoai=so_dien_thoai,
            email=email,
            dia_chi=dia_chi,
        )

    return redirect("suppliers_list")


@require_POST
def supplier_update(request, pk):
    supplier = get_object_or_404(NhaCungCap, pk=pk)

    ten_ncc = request.POST.get("ten_ncc", "").strip()
    so_dien_thoai = request.POST.get("so_dien_thoai", "").strip()
    email = request.POST.get("email", "").strip() or None
    dia_chi = request.POST.get("dia_chi", "").strip() or None

    if ten_ncc and so_dien_thoai:
        supplier.ten_ncc = ten_ncc
        supplier.so_dien_thoai = so_dien_thoai
        supplier.email = email
        supplier.dia_chi = dia_chi
        supplier.save()

    return redirect("suppliers_list")


@require_POST
def supplier_delete(request, pk):
    supplier = get_object_or_404(NhaCungCap, pk=pk)
    supplier.delete()
    url = reverse("suppliers_list")
    return redirect(f"{url}?{urlencode({'deleted': 1})}")


@require_POST
def product_create(request):
    ma_son = request.POST.get("ma_son", "").strip()
    ten_son = request.POST.get("ten_son", "").strip()
    loai_son = request.POST.get("loai_son", "").strip()
    mau_sac = request.POST.get("mau_sac", "").strip() or None
    don_vi_tinh = request.POST.get("don_vi_tinh", "").strip()
    gia_nhap = _parse_decimal(request.POST.get("gia_nhap", "0"))
    ty_le_loi_nhuan = _parse_decimal(request.POST.get("ty_le_loi_nhuan", "0"))
    muc_toi_thieu = request.POST.get("muc_toi_thieu", "").strip()

    try:
        muc_toi_thieu_value = int(muc_toi_thieu) if muc_toi_thieu else 0
    except ValueError:
        muc_toi_thieu_value = 0

    if ma_son and ten_son and loai_son and don_vi_tinh:
        product = SanPham.objects.create(
            ma_son=ma_son,
            ten_son=ten_son,
            loai_son=loai_son,
            mau_sac=mau_sac,
            don_vi_tinh=don_vi_tinh,
            gia_nhap=gia_nhap,
            ty_le_loi_nhuan=ty_le_loi_nhuan,
        )
        TonKho.objects.get_or_create(
            san_pham=product,
            defaults={"muc_toi_thieu": muc_toi_thieu_value},
        )

    return redirect("products_list")


@require_POST
def product_update(request, pk):
    product = get_object_or_404(SanPham, pk=pk)

    ma_son = request.POST.get("ma_son", "").strip()
    ten_son = request.POST.get("ten_son", "").strip()
    loai_son = request.POST.get("loai_son", "").strip()
    mau_sac = request.POST.get("mau_sac", "").strip() or None
    don_vi_tinh = request.POST.get("don_vi_tinh", "").strip()
    gia_nhap = _parse_decimal(request.POST.get("gia_nhap", "0"))
    ty_le_loi_nhuan = _parse_decimal(request.POST.get("ty_le_loi_nhuan", "0"))
    muc_toi_thieu = request.POST.get("muc_toi_thieu", "").strip()

    try:
        muc_toi_thieu_value = int(muc_toi_thieu) if muc_toi_thieu else 0
    except ValueError:
        muc_toi_thieu_value = 0

    if ma_son and ten_son and loai_son and don_vi_tinh:
        product.ma_son = ma_son
        product.ten_son = ten_son
        product.loai_son = loai_son
        product.mau_sac = mau_sac
        product.don_vi_tinh = don_vi_tinh
        product.gia_nhap = gia_nhap
        product.ty_le_loi_nhuan = ty_le_loi_nhuan
        product.save()

        ton_kho, _ = TonKho.objects.get_or_create(san_pham=product)
        ton_kho.muc_toi_thieu = muc_toi_thieu_value
        ton_kho.save()

    return redirect("products_list")


@require_POST
def product_delete(request, pk):
    product = get_object_or_404(SanPham, pk=pk)
    product.delete()
    url = reverse("products_list")
    return redirect(f"{url}?{urlencode({'deleted': 1})}")