from rest_framework import serializers
from django.utils import timezone

from .models import Holiday, RationSetting, Delivery
from .services import is_working_day


class HolidaySerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Holiday
        fields = "__all__"


class RationSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = RationSetting
        fields = "__all__"

class DeliverySerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Delivery
        fields = "__all__"

    def validate(self, data):

        date = data["date"]

        if date > timezone.now().date():
            raise serializers.ValidationError(
                "Future date not allowed."
            )

        if not is_working_day(date):
            raise serializers.ValidationError(
                "Holiday delivery not allowed."
            )

        return data


    from rest_framework import serializers


class DashboardSerializer(
    serializers.Serializer
):

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


class DeliverySerializer(serializers.ModelSerializer):

    def validate(self, attrs):

        date = attrs.get("date")

        if Holiday.objects.filter(date=date).exists():
            raise serializers.ValidationError(
                "This date is a holiday. Delivery entry is not allowed."
            )

        return attrs