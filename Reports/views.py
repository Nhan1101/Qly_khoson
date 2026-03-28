from datetime import date
from decimal import Decimal

from django.core.paginator import Paginator
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils.dateparse import parse_date

from Suppliers.models import ChiTietPhieuNhap, ChiTietPhieuXuat, PhieuNhap, PhieuXuat


def _resolve_date_range(values_queryset, start_param, end_param):
    start_date = parse_date(start_param or "")
    end_date = parse_date(end_param or "")

    default_start = values_queryset.first() or date.today()
    default_end = values_queryset.last() or default_start

    if start_date is None:
        start_date = default_start
    if end_date is None:
        end_date = default_end
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    return start_date, end_date


def import_report_view(request):
    start_date, end_date = _resolve_date_range(
        PhieuNhap.objects.order_by("ngay_nhap").values_list("ngay_nhap", flat=True),
        request.GET.get("start_date"),
        request.GET.get("end_date"),
    )

    receipts = (
        PhieuNhap.objects.filter(ngay_nhap__range=(start_date, end_date))
        .select_related("nha_cung_cap")
        .order_by("-ngay_nhap", "-id")
    )

    line_total = ExpressionWrapper(
        F("chitietphieunhap__so_luong") * F("chitietphieunhap__san_pham__gia_nhap"),
        output_field=DecimalField(max_digits=18, decimal_places=2),
    )
    receipt_total = Coalesce(
        Sum(line_total),
        Value(Decimal("0.00")),
        output_field=DecimalField(max_digits=18, decimal_places=2),
    )
    receipts = receipts.annotate(total_value=receipt_total)

    detail_queryset = ChiTietPhieuNhap.objects.filter(
        phieu_nhap__ngay_nhap__range=(start_date, end_date)
    ).select_related("san_pham", "phieu_nhap")

    total_import_quantity = detail_queryset.aggregate(total=Coalesce(Sum("so_luong"), 0))["total"] or 0
    total_receipts = receipts.count()
    page_obj = Paginator(receipts, 10).get_page(request.GET.get("page"))

    context = {
        "report_type": "import",
        "start_date": start_date,
        "end_date": end_date,
        "total_receipts": total_receipts,
        "total_import_quantity": total_import_quantity,
        "page_obj": page_obj,
    }
    return render(request, "reports/import_report.html", context)


def export_report_view(request):
    start_date, end_date = _resolve_date_range(
        PhieuXuat.objects.order_by("ngay_xuat").values_list("ngay_xuat", flat=True),
        request.GET.get("start_date"),
        request.GET.get("end_date"),
    )

    receipts = (
        PhieuXuat.objects.filter(ngay_xuat__range=(start_date, end_date))
        .select_related("doi_tuong_nhan")
        .order_by("-ngay_xuat", "-id")
    )

    line_total = ExpressionWrapper(
        F("chitietphieuxuat__so_luong") * F("chitietphieuxuat__san_pham__gia_ban"),
        output_field=DecimalField(max_digits=18, decimal_places=2),
    )
    receipt_total = Coalesce(Sum(line_total), Value(Decimal("0.00")), output_field=DecimalField(max_digits=18, decimal_places=2))

    receipts = receipts.annotate(total_value=receipt_total)

    detail_queryset = ChiTietPhieuXuat.objects.filter(
        phieu_xuat__ngay_xuat__range=(start_date, end_date)
    ).select_related("san_pham", "phieu_xuat")

    total_export_quantity = detail_queryset.aggregate(total=Coalesce(Sum("so_luong"), 0))["total"] or 0
    total_receipts = receipts.count()

    page_obj = Paginator(receipts, 10).get_page(request.GET.get("page"))

    context = {
        "report_type": "export",
        "start_date": start_date,
        "end_date": end_date,
        "total_receipts": total_receipts,
        "total_export_quantity": total_export_quantity,
        "page_obj": page_obj,
    }
    return render(request, "reports/export_report.html", context)


def revenue_report_view(request):
    start_date, end_date = _resolve_date_range(
        PhieuXuat.objects.order_by("ngay_xuat").values_list("ngay_xuat", flat=True),
        request.GET.get("start_date"),
        request.GET.get("end_date"),
    )

    detail_queryset = ChiTietPhieuXuat.objects.filter(
        phieu_xuat__ngay_xuat__range=(start_date, end_date)
    ).select_related("san_pham", "phieu_xuat")

    line_total = ExpressionWrapper(
        F("so_luong") * F("san_pham__gia_ban"),
        output_field=DecimalField(max_digits=18, decimal_places=2),
    )

    daily_rows = (
        detail_queryset.values("phieu_xuat__ngay_xuat")
        .annotate(
            completed_orders=Count("phieu_xuat", distinct=True),
            product_quantity=Coalesce(Sum("so_luong"), 0),
            revenue=Coalesce(
                Sum(line_total),
                Value(Decimal("0.00")),
                output_field=DecimalField(max_digits=18, decimal_places=2),
            ),
        )
        .order_by("-phieu_xuat__ngay_xuat")
    )

    page_obj = Paginator(daily_rows, 10).get_page(request.GET.get("page"))
    total_completed_orders = sum(row["completed_orders"] for row in daily_rows)
    total_revenue = sum((row["revenue"] for row in daily_rows), Decimal("0.00"))

    chart_rows = list(reversed(list(daily_rows[:10])))
    chart_max = max((row["revenue"] for row in chart_rows), default=Decimal("0.00"))
    chart_data = []
    for row in chart_rows:
        height_ratio = 0 if chart_max == 0 else float(row["revenue"] / chart_max)
        chart_data.append(
            {
                "label": row["phieu_xuat__ngay_xuat"].strftime("%d/%m"),
                "height_percent": max(12, round(height_ratio * 100)) if row["revenue"] else 0,
                "revenue": row["revenue"],
            }
        )

    context = {
        "report_type": "revenue",
        "start_date": start_date,
        "end_date": end_date,
        "total_completed_orders": total_completed_orders,
        "total_revenue": total_revenue,
        "chart_data": chart_data,
        "page_obj": page_obj,
    }
    return render(request, "reports/revenue_report.html", context)
