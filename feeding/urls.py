from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import HolidayViewSet, RationSettingViewSet, DeliveryViewSet, DashboardAPIView, Form4ReportAPIView, Form07ReportView, Form10ReportView, Form12And13ReportView

router = DefaultRouter()

router.register(
    "holidays",
    HolidayViewSet,
    basename="holidays"
)

# 2. Register your new ViewSet
router.register(
    "ration-settings",             
    RationSettingViewSet,
    basename="ration-settings"      
)

router.register(
    "deliveries",
    DeliveryViewSet,
    basename="deliveries"
)


urlpatterns = router.urls

urlpatterns += [
    path(
        "dashboard/",
        DashboardAPIView.as_view(),
        name="dashboard"
    ),
    path(
        "reports/form4/",
        Form4ReportAPIView.as_view(),
        name="form4-report",
    ),
    path(
        "reports/form07/",
        Form07ReportView.as_view(),
        name="form07-report"
    ),
    path(
        "reports/form10/",
        Form10ReportView.as_view(),
        name="form10-report"
    ),
    path(
        "reports/form12-13/",
        Form12And13ReportView.as_view(),
        name="form12-13-report"
    ),
]