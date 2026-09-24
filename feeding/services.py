from .models import Holiday, RationSetting, Delivery
from schools.models import School

from datetime import date

# from .services import calculate_school_demand_by_date


def is_working_day(date):

    holiday_exists = Holiday.objects.filter(
        date=date
    ).exists()

    return not holiday_exists

def get_current_ration():
    return (
        RationSetting.objects
        .order_by("-effective_date")
        .first()
    )

def calculate_demand(school):

    ration = get_current_ration()

    return {
        "bun":
            school.student_count *
            ration.bun_per_student,

        "egg":
            school.student_count *
            ration.egg_per_student,

        "banana":
            school.student_count *
            ration.banana_per_student,
    }

# calculate demand for one school
def calculate_school_demand(school):

    ration = get_current_ration()

    if not ration:
        raise Exception(
            "Ration setting not found."
        )

    return {
        "school_id": school.id,
        "school_code": school.school_code,
        "school_name": school.name_bn,

        "bun_demand":
            school.student_count *
            ration.bun_per_student,

        "egg_demand":
            school.student_count *
            ration.egg_per_student,

        "banana_demand":
            school.student_count *
            ration.banana_per_student,
    }

# calculate demand by date
def calculate_school_demand_by_date(
    school,
    date
):

    if not is_working_day(date):

        return {
            "bun_demand": 0,
            "egg_demand": 0,
            "banana_demand": 0,
        }

    return calculate_school_demand(
        school
    )

# upazila total demand

def calculate_upazila_demand(
    date
):

    schools = School.objects.filter(
        active=True
    )

    total_bun = 0
    total_egg = 0
    total_banana = 0

    for school in schools:

        demand = (
            calculate_school_demand_by_date(
                school,
                date
            )
        )

        total_bun += demand["bun_demand"]
        total_egg += demand["egg_demand"]
        total_banana += demand["banana_demand"]

    return {
        "bun_demand": total_bun,
        "egg_demand": total_egg,
        "banana_demand": total_banana,
    }

def get_queryset(self):

    queryset = Delivery.objects.all()

    school_id = self.request.query_params.get(
        "school"
    )

    date = self.request.query_params.get(
        "date"
    )

    if school_id:
        queryset = queryset.filter(
            school_id=school_id
        )

    if date:
        queryset = queryset.filter(
            date=date
        )

    return queryset.order_by("-date")


# def get_dashboard_data(
#     report_date=None
# ):

#     if report_date is None:
#         report_date = date.today()

#     schools = School.objects.filter(
#         active=True
#     )

#     bun_demand = 0
#     egg_demand = 0
#     banana_demand = 0

#     bun_delivered = 0
#     egg_delivered = 0
#     banana_delivered = 0

#     shortfall_schools = []


def get_dashboard_data(
    report_date=None
):

    if report_date is None:
        report_date = date.today()

    schools = School.objects.filter(
        active=True
    )

    bun_demand = 0
    egg_demand = 0
    banana_demand = 0

    bun_delivered = 0
    egg_delivered = 0
    banana_delivered = 0

    shortfall_schools = []

    for school in schools:

        demand = (
            calculate_school_demand_by_date(
                school,
                report_date
            )
        )

        delivery = Delivery.objects.filter(
            school=school,
            date=report_date
        ).first()

        bun_demand += demand[
            "bun_demand"
        ]

        egg_demand += demand[
            "egg_demand"
        ]

        banana_demand += demand[
            "banana_demand"
        ]

        if delivery:

            bun_delivered += (
                delivery.bun_delivered
            )

            egg_delivered += (
                delivery.egg_delivered
            )

            banana_delivered += (
                delivery.banana_delivered
            )

        if delivery:

            bun_delivered += (
                delivery.bun_delivered
            )

            egg_delivered += (
                delivery.egg_delivered
            )

            banana_delivered += (
                delivery.banana_delivered
            )

        return {

            "date": report_date,

            "bun_demand":
                bun_demand,

            "bun_delivered":
                bun_delivered,

            "bun_shortfall":
                bun_demand -
                bun_delivered,

            "egg_demand":
                egg_demand,

            "egg_delivered":
                egg_delivered,

            "egg_shortfall":
                egg_demand -
                egg_delivered,

            "banana_demand":
                banana_demand,

            "banana_delivered":
                banana_delivered,

            "banana_shortfall":
                banana_demand -
                banana_delivered,

            "shortfall_schools":
                shortfall_schools,
        }

def get_daily_delivery_report(report_date):

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

    for school in schools:

        demand = calculate_school_demand_by_date(
            school=school,
            date=report_date
        )

        delivery = Delivery.objects.filter(
            school=school,
            date=report_date
        ).first()

        bun_delivered = (
            delivery.bun_delivered
            if delivery else 0
        )

        egg_delivered = (
            delivery.egg_delivered
            if delivery else 0
        )

        banana_delivered = (
            delivery.banana_delivered
            if delivery else 0
        )

        row = {

            "school_id": school.id,
            "school_code": school.school_code,
            "school_name": school.name_bn,

            "bun_demand": demand["bun_demand"],
            "bun_delivered": bun_delivered,
            "bun_shortfall":
                demand["bun_demand"] - bun_delivered,

            "egg_demand": demand["egg_demand"],
            "egg_delivered": egg_delivered,
            "egg_shortfall":
                demand["egg_demand"] - egg_delivered,

            "banana_demand": demand["banana_demand"],
            "banana_delivered": banana_delivered,
            "banana_shortfall":
                demand["banana_demand"] - banana_delivered,
        }

        report_rows.append(row)

        totals["bun_demand"] += demand["bun_demand"]
        totals["bun_delivered"] += bun_delivered

        totals["egg_demand"] += demand["egg_demand"]
        totals["egg_delivered"] += egg_delivered

        totals["banana_demand"] += demand["banana_demand"]
        totals["banana_delivered"] += banana_delivered

    totals["bun_shortfall"] = (
        totals["bun_demand"] -
        totals["bun_delivered"]
    )

    totals["egg_shortfall"] = (
        totals["egg_demand"] -
        totals["egg_delivered"]
    )

    totals["banana_shortfall"] = (
        totals["banana_demand"] -
        totals["banana_delivered"]
    )

    return {
        "date": report_date,
        "schools": report_rows,
        "totals": totals,
    }