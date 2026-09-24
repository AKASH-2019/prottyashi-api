from datetime import datetime
from schools.models import School
from feeding.models import Delivery
from feeding.services import calculate_school_demand_by_date


def generate_form_10(month):

    year, month_num = map(int, month.split("-"))

    schools = School.objects.filter(active=True)

    report_rows = []

    totals = {
        "bun_demand": 0,
        "bun_delivered": 0,
        "egg_demand": 0,
        "egg_delivered": 0,
        "banana_demand": 0,
        "banana_delivered": 0,
    }

    deliveries = Delivery.objects.filter(
        date__year=year,
        date__month=month_num
    )

    for school in schools:

        bun_demand = 0
        egg_demand = 0
        banana_demand = 0

        bun_delivered = 0
        egg_delivered = 0
        banana_delivered = 0

        school_deliveries = deliveries.filter(
            school=school
        )

        for delivery in school_deliveries:

            demand = calculate_school_demand_by_date(
                school,
                delivery.date
            )

            bun_demand += demand["bun_demand"]
            egg_demand += demand["egg_demand"]
            banana_demand += demand["banana_demand"]

            bun_delivered += delivery.bun_delivered
            egg_delivered += delivery.egg_delivered
            banana_delivered += delivery.banana_delivered

        report_rows.append({
            "school_code": school.school_code,
            "school_name": school.name_bn,

            "bun_demand": bun_demand,
            "bun_delivered": bun_delivered,
            "bun_shortfall": bun_demand - bun_delivered,

            "egg_demand": egg_demand,
            "egg_delivered": egg_delivered,
            "egg_shortfall": egg_demand - egg_delivered,

            "banana_demand": banana_demand,
            "banana_delivered": banana_delivered,
            "banana_shortfall": banana_demand - banana_delivered,
        })

        totals["bun_demand"] += bun_demand
        totals["bun_delivered"] += bun_delivered

        totals["egg_demand"] += egg_demand
        totals["egg_delivered"] += egg_delivered

        totals["banana_demand"] += banana_demand
        totals["banana_delivered"] += banana_delivered

    return {
        "report": "Form 10",
        "month": month,
        "schools": report_rows,
        "totals": totals,
    }

from datetime import datetime, timedelta
from schools.models import School
from feeding.models import Delivery
from feeding.services import calculate_school_demand_by_date


def generate_form_13(month):

    year, month_num = map(int, month.split("-"))

    deliveries = Delivery.objects.filter(
        date__year=year,
        date__month=month_num
    )

    daily_rows = []

    dates = deliveries.values_list(
        "date",
        flat=True
    ).distinct().order_by("date")

    for report_date in dates:

        bun_demand = 0
        egg_demand = 0
        banana_demand = 0

        bun_delivered = 0
        egg_delivered = 0
        banana_delivered = 0

        schools = School.objects.filter(active=True)

        for school in schools:

            demand = calculate_school_demand_by_date(
                school,
                report_date
            )

            bun_demand += demand["bun_demand"]
            egg_demand += demand["egg_demand"]
            banana_demand += demand["banana_demand"]

        day_deliveries = deliveries.filter(
            date=report_date
        )

        for d in day_deliveries:

            bun_delivered += d.bun_delivered
            egg_delivered += d.egg_delivered
            banana_delivered += d.banana_delivered

        daily_rows.append({
            "date": report_date,

            "bun_demand": bun_demand,
            "bun_delivered": bun_delivered,
            "bun_shortfall": bun_demand - bun_delivered,

            "egg_demand": egg_demand,
            "egg_delivered": egg_delivered,
            "egg_shortfall": egg_demand - egg_delivered,

            "banana_demand": banana_demand,
            "banana_delivered": banana_delivered,
            "banana_shortfall": banana_demand - banana_delivered,
        })

    return {
        "report": "Form 13",
        "month": month,
        "rows": daily_rows,
    }


from schools.models import School
from feeding.models import Delivery
from feeding.services import calculate_school_demand_by_date


def generate_form_7(month):

    year, month_num = map(int, month.split("-"))

    schools = School.objects.filter(active=True)

    total_students = schools.count()

    deliveries = Delivery.objects.filter(
        date__year=year,
        date__month=month_num
    )

    total_bun = 0
    total_egg = 0
    total_banana = 0

    for delivery in deliveries:

        total_bun += delivery.bun_delivered
        total_egg += delivery.egg_delivered
        total_banana += delivery.banana_delivered

    return {
        "report": "Form 7",
        "month": month,

        "school_count": schools.count(),

        "total_bun": total_bun,
        "total_egg": total_egg,
        "total_banana": total_banana,
    }


from schools.models import School
from feeding.models import Delivery


def generate_form_12(month):

    year, month_num = map(int, month.split("-"))

    schools = School.objects.filter(active=True)

    report_pages = []

    for school in schools:

        deliveries = Delivery.objects.filter(
            school=school,
            date__year=year,
            date__month=month_num
        ).order_by("date")

        report_pages.append({
            "school_id": school.id,
            "school_code": school.school_code,
            "school_name": school.name_bn,
            "student_count": school.student_count,
            "deliveries": [
                {
                    "date": d.date,
                    "bun_delivered": d.bun_delivered,
                    "egg_delivered": d.egg_delivered,
                    "banana_delivered": d.banana_delivered,
                    "chalan_photo": (
                        d.chalan_photo.url
                        if d.chalan_photo
                        else None
                    ),
                }
                for d in deliveries
            ]
        })

    return {
        "report": "Form 12",
        "month": month,
        "pages": report_pages,
    }


from schools.models import School
from feeding.models import Delivery


def generate_form_4(month):

    year, month_num = map(int, month.split("-"))

    schools = School.objects.filter(active=True)

    report_pages = []

    for school in schools:

        deliveries = Delivery.objects.filter(
            school=school,
            date__year=year,
            date__month=month_num
        ).order_by("date")

        report_pages.append({
            "school_id": school.id,
            "school_code": school.school_code,
            "school_name": school.name_bn,
            "student_count": school.student_count,
            "deliveries": [
                {
                    "date": d.date,
                    "bun_delivered": d.bun_delivered,
                    "egg_delivered": d.egg_delivered,
                    "banana_delivered": d.banana_delivered,
                    "chalan_photo": (
                        d.chalan_photo.url
                        if d.chalan_photo
                        else None
                    ),
                }
                for d in deliveries
            ]
        })

    return {
        "report": "Form 4",
        "month": month,
        "pages": report_pages,
    }