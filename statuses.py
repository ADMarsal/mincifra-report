"""
Шаг 4. Статус каждого студента.

  "Подходит"     - вуз и направление есть в списке Минцифры;
  "На проверку"  - программа не может решить сама: вуза нет в словаре
                   или направление не заполнено (надо посмотреть глазами);
  "Не подходит"  - всё заполнено, но вуза или направления нет в списке.
"""

from config import STATUS_CHECK, STATUS_NOT_OK, STATUS_OK, UNKNOWN_UNIVERSITY
from universities import normalize


def get_status(student: dict) -> str:
    """Определить статус одного студента по результатам проверки."""
    if student["short_university"] == UNKNOWN_UNIVERSITY:
        return STATUS_CHECK
    if normalize(student["speciality"]) == "":
        return STATUS_CHECK
    if student["university_ok"] and student["speciality_ok"]:
        return STATUS_OK
    return STATUS_NOT_OK


def set_statuses(students: list[dict]) -> dict:
    """Записать статус каждому студенту и вернуть, сколько студентов с каждым статусом."""
    counts = {STATUS_OK: 0, STATUS_CHECK: 0, STATUS_NOT_OK: 0}
    for student in students:
        student["status"] = get_status(student)
        counts[student["status"]] += 1
    return counts
