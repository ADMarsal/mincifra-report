"""
Шаг 5. Итоговый отчёт в Excel (output/report.xlsx).

Листы:
  "Студенты"        - все студенты со статусом;
  "Сводная по вузам" - по каждому вузу: сколько подходит, часы и деньги;
  "На проверку"     - кого надо проверить вручную.
"""

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

from config import MONEY_PER_HOUR, STATUS_CHECK, STATUS_OK

STUDENT_HEADERS = ["Сотрудник", "Вуз", "Вуз (полностью)", "Направление", "Часы", "Статус"]
SUMMARY_HEADERS = ["Вуз", "Подходит, чел.", "Часы", "Деньги, руб."]


def hours_of(student: dict) -> float:
    """Часы студента числом (пусто или текст -> 0)."""
    hours = student["hours"]
    return hours if isinstance(hours, (int, float)) else 0


def build_summary(students: list[dict]) -> dict:
    """Сводная по вузам только для подходящих студентов: вуз -> {"count", "hours"}."""
    summary = {}
    for student in students:
        if student["status"] != STATUS_OK:
            continue
        row = summary.setdefault(student["short_university"], {"count": 0, "hours": 0})
        row["count"] += 1
        row["hours"] += hours_of(student)
    return summary


def add_sheet(workbook: Workbook, title: str, headers: list, rows: list) -> None:
    """Добавить лист: жирные заголовки, потом строки."""
    sheet = workbook.create_sheet(title)
    sheet.append(headers)
    for cell in sheet[1]:
        cell.font = Font(bold=True)
    for row in rows:
        sheet.append(row)


def student_row(student: dict) -> list:
    return [student["name"], student["short_university"], student["university"],
            student["speciality"], student["hours"], student["status"]]


def save_report(students: list[dict], path: str) -> dict:
    """Собрать отчёт и сохранить в файл. Возвращает сводную (для вывода на экран)."""
    workbook = Workbook()
    workbook.remove(workbook.active)       # убираем пустой лист "Sheet"

    add_sheet(workbook, "Студенты", STUDENT_HEADERS, [student_row(s) for s in students])

    summary = build_summary(students)
    summary_rows = []
    for name in sorted(summary):
        hours = summary[name]["hours"]
        summary_rows.append([name, summary[name]["count"], hours, round(hours * MONEY_PER_HOUR, 2)])
    total_hours = sum(row[2] for row in summary_rows)
    summary_rows.append(["Итого", sum(row[1] for row in summary_rows), total_hours,
                         round(total_hours * MONEY_PER_HOUR, 2)])
    add_sheet(workbook, "Сводная по вузам", SUMMARY_HEADERS, summary_rows)

    to_check = [student_row(s) for s in students if s["status"] == STATUS_CHECK]
    add_sheet(workbook, "На проверку", STUDENT_HEADERS, to_check)

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)
    return summary
