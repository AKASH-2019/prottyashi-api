from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Holiday, RationSetting
from .serializers import (
    HolidaySerializer,
    RationSettingSerializer,
    DeliverySerializer,
)
from .permissions import HolidayPermission

from .services import (
    get_dashboard_data
)


class HolidayViewSet(
    viewsets.ModelViewSet
):

    queryset = Holiday.objects.all().order_by(
        "date"
    )

    serializer_class = HolidaySerializer

    permission_classes = [
        HolidayPermission
    ]

class RationSettingViewSet(viewsets.ModelViewSet):

    queryset = RationSetting.objects.all().order_by(
        "-effective_date"
    )

    serializer_class = RationSettingSerializer

    permission_classes = [
        HolidayPermission
    ]

from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from .models import Delivery
from .serializers import DeliverySerializer


class DeliveryViewSet(viewsets.ModelViewSet):

    queryset = Delivery.objects.all().order_by("-date")

    serializer_class = DeliverySerializer

    filter_backends = [SearchFilter]

    search_fields = [
        "school__school_code",
        "school__name_bn",
    ]

    def perform_create(self, serializer):

        serializer.save(
            entered_by=self.request.user
        )

class DashboardAPIView(
    APIView
):

    def get(
        self,
        request
    ):

        data = get_dashboard_data()

        return Response(data)