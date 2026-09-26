from rest_framework import serializers
from django.utils import timezone

from .models import (
    Holiday,
    RationSetting,
    Delivery,
)
from .services import is_working_day


class HolidaySerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Holiday
        fields = "__all__"


class RationSettingSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = RationSetting
        fields = "__all__"


class DeliverySerializer(
    serializers.ModelSerializer
):

    school_name = serializers.CharField(
        source="school.name_bn",
        read_only=True
    )

    entered_by_name = serializers.CharField(
        source="entered_by.username",
        read_only=True
    )

    class Meta:
        model = Delivery
        fields = "__all__"

    def validate(self, attrs):

        date = attrs.get("date")

        if date > timezone.now().date():
            raise serializers.ValidationError(
                "Future date not allowed."
            )

        if Holiday.objects.filter(
            date=date
        ).exists():
            raise serializers.ValidationError(
                "Holiday delivery not allowed."
            )

        return attrs


class DashboardSerializer(serializers.Serializer):
    date = serializers.DateField()

    bun_demand = serializers.IntegerField()
    bun_delivered = serializers.IntegerField()
    bun_shortfall = serializers.IntegerField()

    egg_demand = serializers.IntegerField()
    egg_delivered = serializers.IntegerField()
    egg_shortfall = serializers.IntegerField()

    banana_demand = serializers.IntegerField()
    banana_delivered = serializers.IntegerField()
    banana_shortfall = serializers.IntegerField()

    shortfall_schools = serializers.ListField()



class Form4Serializer(serializers.Serializer):

    sl = serializers.IntegerField()

    food_receive_date = serializers.DateField()

    chalan_no = serializers.CharField()

    chalan_date = serializers.DateField()

    bun = serializers.IntegerField()

    egg = serializers.IntegerField()

    banana = serializers.IntegerField()


class Form07RowSerializer(serializers.Serializer):
    sl = serializers.IntegerField()

    school_name = serializers.CharField()

    emis_code = serializers.CharField()

    bun_chalan_count = serializers.IntegerField()

    bun_total = serializers.IntegerField()

    egg_chalan_count = serializers.IntegerField()

    egg_total = serializers.IntegerField()

    banana_chalan_count = serializers.IntegerField()

    banana_total = serializers.IntegerField()


class Form10Serializer(serializers.Serializer):

    food_name = serializers.CharField()

    quantity = serializers.IntegerField()

    unit_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    food_total = serializers.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    service_unit_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    service_total = serializers.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    grand_total = serializers.DecimalField(
        max_digits=15,
        decimal_places=2
    )