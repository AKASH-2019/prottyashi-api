from .models import Holiday, RationSetting, Delivery
from schools.models import School

from datetime import date

# from .services import calculate_school_demand_by_date


def is_working_day(date):

    holiday_exists = Holiday.objects.filter(
        date=date
    ).exists()

    return not holiday_exists

# def get_current_ration():
#     return (
#         RationSetting.objects
#         .order_by("-effective_date")
#         .first()
#     )
def get_current_ration():

    ration = (
        RationSetting.objects
        .order_by("-effective_date")
        .first()
    )

    print("RATION COUNT =", RationSetting.objects.count())
    print("RATION OBJ =", ration)

    return ration

def calculate_demand(school):

    ration = get_current_ration()
    print("RATION =", ration)

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
    print("RATION INSIDE DEMAND =", ration)


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


from datetime import date

def get_dashboard_data(report_date=None):

    if report_date is None:
        report_date = date.today()

    schools = School.objects.filter(
        active=True
    )

    total_students = 0

    total_bun = 0
    total_egg = 0
    total_banana = 0

    total_food_delivered = 0
    total_shortfall = 0

    schools_data = []
    shortfall_schools = []

    for school in schools:

        student_count = (
            school.student_count or 0
        )

        delivery = Delivery.objects.filter(
            school=school,
            date=report_date
        ).first()

        bun = (
            delivery.bun_delivered
            if delivery else 0
        )

        egg = (
            delivery.egg_delivered
            if delivery else 0
        )

        banana = (
            delivery.banana_delivered
            if delivery else 0
        )

        food_delivered = (
            bun +
            egg +
            banana
        )

        school_shortfall = max(
            0,
            student_count -
            food_delivered
        )

        total_students += (
            student_count
        )

        total_bun += bun
        total_egg += egg
        total_banana += banana

        total_food_delivered += (
            food_delivered
        )

        total_shortfall += (
            school_shortfall
        )

        school_data = {

            "school_id":
                school.id,

            "school_name":
                school.name_bn,

            "school_code":
                school.school_code,

            "emis_code":
                school.emis_code,

            "student_count":
                student_count,

            "bun_delivered":
                bun,

            "egg_delivered":
                egg,

            "banana_delivered":
                banana,

            "food_delivered":
                food_delivered,

            "shortfall":
                school_shortfall,
        }

        schools_data.append(
            school_data
        )

        if school_shortfall > 0:

            shortfall_schools.append(
                school_data
            )

    return {

        "date":
            report_date,

        "total_students":
            total_students,

        "total_food_delivered":
            total_food_delivered,

        "total_shortfall":
            total_shortfall,

        "total_bun":
            total_bun,

        "total_egg":
            total_egg,

        "total_banana":
            total_banana,

        "schools":
            schools_data,

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


from datetime import date

from feeding.models import Delivery


def get_staff_dashboard_data(
    staff,
    report_date=None
):

    if report_date is None:
        report_date = date.today()

    deliveries = (
        Delivery.objects
        .filter(
            entered_by=staff,
            date=report_date
        )
        .select_related("school")
        .order_by("school__name_bn")
    )

    overall_schools = School.objects.filter(
        active=True
    ).count()

    total_bun = 0
    total_egg = 0
    total_banana = 0

    school_list = []

    for delivery in deliveries:

        bun = delivery.bun_delivered or 0
        egg = delivery.egg_delivered or 0
        banana = delivery.banana_delivered or 0

        total_bun += bun
        total_egg += egg
        total_banana += banana

        school_list.append({
            "school_id": delivery.school.id,
            "school_name": delivery.school.name_bn,
            "school_code": delivery.school.school_code,
            "emis_code": delivery.school.emis_code,
            "student_count": delivery.school.student_count,

            "bun_delivered": bun,
            "egg_delivered": egg,
            "banana_delivered": banana,

            "total_food": bun + egg + banana,

            "bun_chalan_no": delivery.bun_chalan_no,
            "bun_chalan_date": delivery.bun_chalan_date,
            "bun_chalan_image": (
                delivery.bun_chalan_image.url
                if delivery.bun_chalan_image
                else None
            ),

            "egg_chalan_no": delivery.egg_chalan_no,
            "egg_chalan_date": delivery.egg_chalan_date,
            "egg_chalan_image": (
                delivery.egg_chalan_image.url
                if delivery.egg_chalan_image
                else None
            ),

            "banana_chalan_no": delivery.banana_chalan_no,
            "banana_chalan_date": delivery.banana_chalan_date,
            "banana_chalan_image": (
                delivery.banana_chalan_image.url
                if delivery.banana_chalan_image
                else None
            ),
        })

    return {
        "date": report_date,

        "staff_id": staff.id,

        "staff_name": (
            staff.get_full_name()
            or staff.username
        ),

        "total_schools": len(school_list),
        "overall_schools": overall_schools,

        "total_bun": total_bun,
        "total_egg": total_egg,
        "total_banana": total_banana,

        "total_food": (
            total_bun +
            total_egg +
            total_banana
        ),

        "schools": school_list,
    }