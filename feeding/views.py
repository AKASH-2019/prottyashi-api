from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Holiday, RationSetting, Delivery
from django.db.models import Q
from rest_framework.filters import SearchFilter
from .serializers import DeliverySerializer
from collections import defaultdict

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

class Form4ReportAPIView(APIView):

    def get(self, request):

        month = request.GET.get("month")
        year = request.GET.get("year")

        deliveries = (
            Delivery.objects
            .select_related("school")
            .filter(
                date__month=month,
                date__year=year
            )
            .order_by(
                "school__name_bn",
                "date"
            )
        )

        schools_data = defaultdict(list)

        for delivery in deliveries:

            chalan_no = (
                delivery.bun_chalan_no
                or delivery.egg_chalan_no
                or delivery.banana_chalan_no
                or "-"
            )

            chalan_date = (
                delivery.bun_chalan_date
                or delivery.egg_chalan_date
                or delivery.banana_chalan_date
                or delivery.date
            )

            schools_data[delivery.school.id].append({
                "food_receive_date": delivery.date,
                "chalan_no": chalan_no,
                "chalan_date": chalan_date,
                "bun": delivery.bun_delivered,
                "egg": delivery.egg_delivered,
                "banana": delivery.banana_delivered,
            })

        schools = []

        for school_id, rows in schools_data.items():

            school = deliveries.filter(
                school_id=school_id
            ).first().school

            formatted_rows = []

            for idx, row in enumerate(rows, start=1):

                row["sl"] = idx

                formatted_rows.append(row)

            schools.append({
                "school_id": school.id,
                "school_name": school.name_bn,
                "emis_code": school.emis_code,
                "rows": formatted_rows,
            })

        return Response({
            "month": int(month),
            "year": int(year),
            "schools": schools,
        })