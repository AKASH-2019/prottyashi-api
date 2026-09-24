from django.http import HttpResponse
from .pdf import generate_daily_report_pdf
from rest_framework.views import APIView
from rest_framework.response import Response

from .excel import (
    generate_daily_report_excel
)

from feeding.services import (
    get_daily_delivery_report
)

from .services import (
    generate_form_10,
    generate_form_13,
    generate_form_7,
    generate_form_12,
    generate_form_4,
)


class DailyReportExcelAPIView(
    APIView
):

    def get(
        self,
        request
    ):

        report_date = request.GET.get(
            "date"
        )

        report_data = (
            get_daily_delivery_report(
                report_date
            )
        )

        excel_file = (
            generate_daily_report_excel(
                report_data
            )
        )

        response = HttpResponse(
            excel_file,
            content_type=
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        response[
            "Content-Disposition"
        ] = (
            f'attachment; '
            f'filename="daily_report_{report_date}.xlsx"'
        )

        return response

class DailyReportPDFAPIView(
    APIView
):

    def get(
        self,
        request
    ):

        report_date = request.GET.get(
            "date"
        )

        report_data = (
            get_daily_delivery_report(
                report_date
            )
        )

        pdf_file = (
            generate_daily_report_pdf(
                report_data
            )
        )

        response = HttpResponse(
            pdf_file,
            content_type="application/pdf"
        )

        response[
            "Content-Disposition"
        ] = (
            f'attachment; '
            f'filename="daily_report_{report_date}.pdf"'
        )

        return response

class ReportGeneratorAPIView(APIView):

    REPORT_MAP = {
        "form10": generate_form_10,
        "form13": generate_form_13,
        "form7": generate_form_7,
        "form12": generate_form_12,
        "form4": generate_form_4,
    }

    def get(self, request):

        report_type = request.GET.get("report")
        month = request.GET.get("month")

        if not report_type:
            return Response(
                {"error": "report parameter required"},
                status=400
            )

        if not month:
            return Response(
                {"error": "month parameter required"},
                status=400
            )

        generator = self.REPORT_MAP.get(
            report_type
        )

        if not generator:
            return Response(
                {"error": "invalid report type"},
                status=400
            )

        data = generator(month)

        return Response(data)