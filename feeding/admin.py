from django.contrib import admin
from .models import Holiday, RationSetting, Delivery


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ["date", "title"]
    search_fields = ["title"]
    ordering = ["date"]

@admin.register(RationSetting)
class RationSettingAdmin(admin.ModelAdmin):

    list_display = [
        "effective_date",
        "bun_per_student",
        "egg_per_student",
        "banana_per_student",
    ]

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):

    list_display = [
        "school",
        "date",
        "bun_delivered",
        "egg_delivered",
        "banana_delivered",
        "entered_by",
    ]

    list_filter = [
        "date",
        "school",
    ]

    search_fields = [
        "school__school_code",
        "school__name_bn",
    ]