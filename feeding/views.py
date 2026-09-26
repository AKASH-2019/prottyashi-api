from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Holiday, RationSetting, Delivery
from schools.models import School
from django.db.models import Sum, Count, Q
from rest_framework.filters import SearchFilter
from .serializers import DeliverySerializer
from collections import defaultdict
from decimal import Decimal

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


class Form07ReportView(APIView):

    def get(self, request):

        month = request.GET.get("month")
        year = request.GET.get("year")

        rows = []

        schools = School.objects.all().order_by("name_bn")

        sl = 1

        for school in schools:

            deliveries = Delivery.objects.filter(
                school=school,
                date__month=month,
                date__year=year
            )

            rows.append({
                "sl": sl,
                "school_name": school.name_bn,
                "emis_code": school.emis_code,

                "bun_chalan_count":
                    deliveries.exclude(
                        bun_chalan_no__isnull=True
                    ).exclude(
                        bun_chalan_no=""
                    ).count(),

                "bun_total":
                    deliveries.aggregate(
                        total=Sum("bun_delivered")
                    )["total"] or 0,

                "egg_chalan_count":
                    deliveries.exclude(
                        egg_chalan_no__isnull=True
                    ).exclude(
                        egg_chalan_no=""
                    ).count(),

                "egg_total":
                    deliveries.aggregate(
                        total=Sum("egg_delivered")
                    )["total"] or 0,

                "banana_chalan_count":
                    deliveries.exclude(
                        banana_chalan_no__isnull=True
                    ).exclude(
                        banana_chalan_no=""
                    ).count(),

                "banana_total":
                    deliveries.aggregate(
                        total=Sum("banana_delivered")
                    )["total"] or 0,
            })

            sl += 1

        return Response({
            "month": int(month),
            "year": int(year),
            "rows": rows
        })


class Form10ReportView(APIView):

    def get(self, request):

        month = request.GET.get("month")
        year = request.GET.get("year")

        BUN_PRICE = Decimal("22.883")
        EGG_PRICE = Decimal("13.543")
        BANANA_PRICE = Decimal("9.807")

        schools_data = []

        overall_total = Decimal("0")

        schools = School.objects.all().order_by("name_bn")

        for school in schools:

            deliveries = Delivery.objects.filter(
                school=school,
                date__month=month,
                date__year=year
            )

            bun_qty = deliveries.aggregate(
                total=Sum("bun_delivered")
            )["total"] or 0

            egg_qty = deliveries.aggregate(
                total=Sum("egg_delivered")
            )["total"] or 0

            banana_qty = deliveries.aggregate(
                total=Sum("banana_delivered")
            )["total"] or 0

            bun_total = round(
                Decimal(bun_qty) * BUN_PRICE, 2
            )

            egg_total = round(
                Decimal(egg_qty) * EGG_PRICE, 2
            )

            banana_total = round(
                Decimal(banana_qty) * BANANA_PRICE, 2
            )

            school_total = (
                bun_total +
                egg_total +
                banana_total
            )

            overall_total += school_total

            schools_data.append({

                "school_id": school.id,

                "school_name": school.name_bn,

                "emis_code": school.emis_code,

                "items": [

                    {
                        "food_name": "বনরুটি",

                        "quantity": bun_qty,

                        "unit_price": float(BUN_PRICE),

                        "food_total": float(bun_total),

                        "service_unit_price": 0,

                        "service_total": 0,

                        "grand_total": float(
                            bun_total
                        ),
                    },

                    {
                        "food_name": "সিদ্ধ ডিম",

                        "quantity": egg_qty,

                        "unit_price": float(EGG_PRICE),

                        "food_total": float(egg_total),

                        "service_unit_price": 0,

                        "service_total": 0,

                        "grand_total": float(
                            egg_total
                        ),
                    },

                    {
                        "food_name": "কলা",

                        "quantity": banana_qty,

                        "unit_price": float(
                            BANANA_PRICE
                        ),

                        "food_total": float(
                            banana_total
                        ),

                        "service_unit_price": 0,

                        "service_total": 0,

                        "grand_total": float(
                            banana_total
                        ),
                    },

                ],

                "school_total": float(
                    school_total
                ),
            })

        return Response({

            "month": int(month),

            "year": int(year),

            "schools": schools_data,

            "overall_total": float(
                overall_total
            ),
        })

class Form12And13ReportView(APIView):

    def get(self, request):

        month = request.GET.get("month")
        year = request.GET.get("year")

        rows = []

        schools = School.objects.all().order_by("name_bn")

        sl = 1

        for school in schools:

            deliveries = Delivery.objects.filter(
                school=school,
                date__month=month,
                date__year=year
            )

            bun_received = (
                deliveries.aggregate(
                    total=Sum("bun_delivered")
                )["total"] or 0
            )

            egg_received = (
                deliveries.aggregate(
                    total=Sum("egg_delivered")
                )["total"] or 0
            )

            banana_received = (
                deliveries.aggregate(
                    total=Sum("banana_delivered")
                )["total"] or 0
            )

            bun_distributed = bun_received
            egg_distributed = egg_received
            banana_distributed = banana_received

            bun_balance = (
                bun_received -
                bun_distributed
            )

            egg_balance = (
                egg_received -
                egg_distributed
            )

            banana_balance = (
                banana_received -
                banana_distributed
            )

            total_received = (
                bun_received +
                egg_received +
                banana_received
            )

            total_distributed = (
                bun_distributed +
                egg_distributed +
                banana_distributed
            )

            total_balance = (
                bun_balance +
                egg_balance +
                banana_balance
            )

            rows.append({

                "sl": sl,

                "school_id": school.id,

                "school_name": school.name_bn,

                "emis_code": school.emis_code,

                "bun": {
                    "received": bun_received,
                    "distributed": bun_distributed,
                    "balance": bun_balance,
                },

                "egg": {
                    "received": egg_received,
                    "distributed": egg_distributed,
                    "balance": egg_balance,
                },

                "banana": {
                    "received": banana_received,
                    "distributed": banana_distributed,
                    "balance": banana_balance,
                },

                "total": {
                    "received": total_received,
                    "distributed": total_distributed,
                    "balance": total_balance,
                },
            })

            sl += 1

        return Response({

            "month": int(month),

            "year": int(year),

            "schools": rows
        })