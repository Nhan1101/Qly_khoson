from django.urls import path

from .views import export_report_view, import_report_view, revenue_report_view

urlpatterns = [
    path("import/", import_report_view, name="import-report"),
    path("export/", export_report_view, name="export-report"),
    path("revenue/", revenue_report_view, name="revenue-report"),
]
