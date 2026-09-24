from django.contrib import admin
from .models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):

    list_display = [
        "school_code",
        "emis_code",
        "name_bn",
        "student_count",
        "active",
    ]

    search_fields = [
        "school_code",
        "emis_code",
        "name_bn",
    ]
