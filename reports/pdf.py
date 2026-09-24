# GET /api/reports/daily-report/pdf/?date=2026-09-24

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_daily_report_pdf(report_data):
    buffer = BytesIO()
    
    # Use landscape or set explicit tight margins to fit 11 columns on A4
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15,
        leftMargin=15,
        topMargin=20,
        bottomMargin=20
    )
    elements = []
    styles = getSampleStyleSheet()

    # Create custom typography styles for table content wrapping
    normal_style = ParagraphStyle(name='TableText', parent=styles['Normal'], fontSize=7, leading=9)
    bold_style = ParagraphStyle(name='TableTextBold', parent=styles['Normal'], fontSize=7, leading=9, fontName='Helvetica-Bold')
    title_style = styles["Title"]

    # Document Header
    title = Paragraph(f"Daily Delivery Report - {report_data.get('date', '')}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Define Header Titles
    headers = [
        "School Code", "School Name",
        "Bun D", "Bun Del", "Bun SF",
        "Egg D", "Egg Del", "Egg SF",
        "Banana D", "Banana Del", "Banana SF"
    ]
    
    # Wrap headers in Paragraphs so they format correctly
    data = [[Paragraph(h, bold_style) for h in headers]]

    # 1. Append School Rows
    for row in report_data["schools"]:
        data.append([
            Paragraph(str(row["school_code"]), normal_style),
            Paragraph(row["school_name"], normal_style), # Long names wrap safely now
            Paragraph(str(row["bun_demand"]), normal_style),
            Paragraph(str(row["bun_delivered"]), normal_style),
            Paragraph(str(row["bun_shortfall"]), normal_style),
            Paragraph(str(row["egg_demand"]), normal_style),
            Paragraph(str(row["egg_delivered"]), normal_style),
            Paragraph(str(row["egg_shortfall"]), normal_style),
            Paragraph(str(row["banana_demand"]), normal_style),
            Paragraph(str(row["banana_delivered"]), normal_style),
            Paragraph(str(row["banana_shortfall"]), normal_style),
        ])

    # 2. FIXED: Totals execution pulled out of the loop
    totals = report_data["totals"]
    data.append([
        Paragraph("", bold_style),
        Paragraph("UPAZILA TOTAL", bold_style),
        Paragraph(str(totals["bun_demand"]), bold_style),
        Paragraph(str(totals["bun_delivered"]), bold_style),
        Paragraph(str(totals["bun_shortfall"]), bold_style),
        Paragraph(str(totals["egg_demand"]), bold_style),
        Paragraph(str(totals["egg_delivered"]), bold_style),
        Paragraph(str(totals["egg_shortfall"]), bold_style),
        Paragraph(str(totals["banana_demand"]), bold_style),
        Paragraph(str(totals["banana_delivered"]), bold_style),
        Paragraph(str(totals["banana_shortfall"]), bold_style),
    ])

    # 3. Define Column Widths explicitly (Total A4 printable width is ~565 points)
    # School Code and Name take more space; numeric metrics are packed tightly
    col_widths = [50, 115, 40, 40, 40, 40, 40, 40, 40, 40, 40]
    
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BACKGROUND", (0, -1), (-1, -1), colors.whitesmoke), # Distinct color for totals
        ])
    )

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer



# from io import BytesIO

# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4

# from reportlab.platypus import (
#     SimpleDocTemplate,
#     Table,
#     TableStyle,
#     Paragraph,
#     Spacer,
# )

# from reportlab.lib.styles import getSampleStyleSheet

# def generate_daily_report_pdf(report_data):

#     buffer = BytesIO()

#     doc = SimpleDocTemplate(
#         buffer,
#         pagesize=A4
#     )

#     elements = []

#     styles = getSampleStyleSheet()

#     title = Paragraph(
#         f"Daily Delivery Report - {report_data['date']}",
#         styles["Title"]
#     )

#     elements.append(title)
#     elements.append(Spacer(1, 12))

#     data = [

#         [
#             "School Code",
#             "School Name",

#             "Bun D",
#             "Bun Del",
#             "Bun SF",

#             "Egg D",
#             "Egg Del",
#             "Egg SF",

#             "Banana D",
#             "Banana Del",
#             "Banana SF",
#         ]
#     ]

#     for row in report_data["schools"]:

#         data.append([

#             row["school_code"],
#             row["school_name"],

#             row["bun_demand"],
#             row["bun_delivered"],
#             row["bun_shortfall"],

#             row["egg_demand"],
#             row["egg_delivered"],
#             row["egg_shortfall"],

#             row["banana_demand"],
#             row["banana_delivered"],
#             row["banana_shortfall"],
#         ])

#         totals = report_data["totals"]

#     data.append([

#         "",
#         "UPAZILA TOTAL",

#         totals["bun_demand"],
#         totals["bun_delivered"],
#         totals["bun_shortfall"],

#         totals["egg_demand"],
#         totals["egg_delivered"],
#         totals["egg_shortfall"],

#         totals["banana_demand"],
#         totals["banana_delivered"],
#         totals["banana_shortfall"],
#     ])

#     table = Table(data)

#     table.setStyle(

#         TableStyle([

#             ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

#             ("GRID", (0, 0), (-1, -1), 1, colors.black),

#             ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

#             ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
#         ])
#     )

#     elements.append(table)

#     doc.build(elements)

#     buffer.seek(0)

#     return buffer