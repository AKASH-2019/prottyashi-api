from django.urls import path

from .views import (
    DailyReportExcelAPIView, DailyReportPDFAPIView, ReportGeneratorAPIView
)

urlpatterns = [

    path(
        "daily-report/excel/",
        DailyReportExcelAPIView.as_view(),
        name="daily-report-excel"
    ),

    path(
    "daily-report/pdf/",
    DailyReportPDFAPIView.as_view(),
    name="daily-report-pdf"),

    path(
        "generate/",
        ReportGeneratorAPIView.as_view(),
        name="report-generator",
    ),
]