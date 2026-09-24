from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import HolidayViewSet, RationSettingViewSet, DeliveryViewSet, DashboardAPIView

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
]