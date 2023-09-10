import io

import xlsxwriter

from add_hours.application.dto.response.activity import GetActivitiesResponse
from add_hours.domain.models.student.student import Student


async def create_xlsx(
    student: Student, get_activities: GetActivitiesResponse, activities: dict
):
    output_xlsx = io.BytesIO()
    workbook = xlsxwriter.Workbook(output_xlsx)
    worksheet = workbook.add_worksheet()

    total_activities = get_activities.total_activities

    for i in range(0, 7):
        worksheet.set_column(0, i, 23)

    for i in range(1, 5):
        worksheet.merge_range(f"A{i}:G{i}", "")

    center = workbook.add_format(
        {"align": "center", "valign": "vcenter", "text_wrap": True}
    )
    for i in range(4):
        [worksheet.write(i, j, "", center) for j in range(7)]

    # worksheet.set_row(4, 35)
    column_format = workbook.add_format(
        {
            "bg_color": "#D9D9D9", "border": 1, "align": "center",
            "valign": "vcenter", "text_wrap": True, "bold": True
        }
    )
    [worksheet.write(4, i, "", column_format) for i in range(0, 7)]

    cell_default_format = workbook.add_format(
        {"border": 1, "align": "center", "valign": "vcenter", "text_wrap": True}
    )
    for i in range(5, 6 + total_activities):
        [worksheet.write(i, j, "", cell_default_format) for j in range(7)]

    worksheet.write(0, 0, "HORAS COMPLEMENTARES", center)

    worksheet.write(
        2, 0, f"Aluno(a): {student.name} ({student.enrollment})", center
    )

    worksheet.write(4, 0, "ATIVIDADE", column_format)
    worksheet.write(4, 1, "INSTITUIÇÃO", column_format)
    worksheet.write(4, 2, "CATEGORIA", column_format)
    worksheet.write(4, 3, "ATUAÇÃO", column_format)
    worksheet.write(4, 4, "DATA", column_format)
    worksheet.write(4, 5, "CARGA HORÁRIA A LANÇAR", column_format)
    worksheet.write(4, 6, "CARGA HORÁRIA CUMPRIDA", column_format)

    worksheet.write(
        5 + total_activities, 4, "TOTAL DE HORAS", cell_default_format
    )

    j = 0
    for activity in get_activities.activities:
        index = 5 + j

        category_to_write = (
            f"{activities.get(activity.category).id_and_dimension} - "
            f"{activities.get(activity.category).activity_type}"
        )

        worksheet.write(index, 0, activity.activity, cell_default_format)
        worksheet.write(index, 1, activity.institution, cell_default_format)
        worksheet.write(index, 2, category_to_write, cell_default_format)
        worksheet.write(index, 3, activity.area, cell_default_format)
        worksheet.write(
            index, 4, f"{activity.start_date} a {activity.end_date}",
            cell_default_format
        )
        worksheet.write(index, 5, activity.posted_workload, cell_default_format)
        worksheet.write(
            index, 6, activity.accomplished_workload, cell_default_format
        )

        j += 1

    worksheet.write(
        5 + total_activities, 5, get_activities.total_posted_workload,
        cell_default_format
    )
    worksheet.write(
        5 + total_activities, 6, get_activities.total_accomplished_workload,
        cell_default_format
    )

    workbook.close()

    return output_xlsx
