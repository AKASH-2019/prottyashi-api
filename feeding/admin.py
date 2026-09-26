from django.contrib import admin
from .models import (
    Holiday,
    RationSetting,
    Delivery,
    FoodPrice
)

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "date",
        "title",
        "created_at",
    )

    search_fields = (
        "title",
    )


@admin.register(RationSetting)
class RationSettingAdmin(
    admin.ModelAdmin
):

    list_display = (
        "id",
        "bun_per_student",
        "egg_per_student",
        "banana_per_student",
    )


@admin.register(Delivery)
class DeliveryAdmin(
    admin.ModelAdmin
):

    list_display = (
        "id",
        "school",
        "date",
        "bun_delivered",
        "egg_delivered",
        "banana_delivered",
        "entered_by",
        "created_at",
    )

    list_filter = (
        "date",
        "school",
    )

    search_fields = (
        "school__name_bn",
        "school__school_code",
        "school__emis_code",
    )





@admin.register(FoodPrice)
class FoodPriceAdmin(admin.ModelAdmin):

    list_display = (
        "bun_unit_price",
        "egg_unit_price",
        "banana_unit_price",
        "updated_at",
    )

    readonly_fields = (
        "updated_at",
    )