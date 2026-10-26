"""
Шаг 3. Проверка по списку Минцифры.

В файле data/mincifra_list.csv перечислены пары "вуз;направление",
которые засчитываются для отчёта:
    ВШЭ;Прикладная информатика
    ИТМО;Программная инженерия

Студент подходит, если:
  1) его вуз есть в списке;
  2) его направление есть в списке ИМЕННО для этого вуза.
"""

import csv

from config import CSV_DELIMITER
from universities import normalize


def load_mincifra_list(path: str) -> dict:
    """Прочитать список Минцифры: короткое название вуза -> множество направлений."""
    allowed = {}
    with open(path, encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=CSV_DELIMITER)
        next(reader)                       # пропускаем строку с заголовками
        for line_number, row in enumerate(reader, start=2):
            if not row:
                continue
            if len(row) != 2:
                raise ValueError(f"{path}, строка {line_number}: нужно 2 значения через «{CSV_DELIMITER}»")
            university, speciality = row
            allowed.setdefault(university.strip(), set()).add(normalize(speciality))
    return allowed


def is_university_in_list(short_university: str, allowed: dict) -> bool:
    """Есть ли вуз в списке Минцифры."""
    return short_university in allowed


def is_speciality_allowed(short_university: str, speciality, allowed: dict) -> bool:
    """
    Засчитывается ли направление для этого вуза.
    Направление может быть записано с кодом ("09.03.03 Прикладная информатика"),
    поэтому ищем название из списка ВНУТРИ текста, а не точное совпадение.
    """
    text = normalize(speciality)
    if text == "":
        return False
    for allowed_speciality in allowed.get(short_university, set()):
        if allowed_speciality in text:
            return True
    return False


def check_students(students: list[dict], allowed: dict) -> dict:
    """
    Проверить всех студентов. Каждому добавляются два поля:
    "university_ok" и "speciality_ok" (True/False).
    Возвращает итоги: сколько прошли каждую проверку.
    """
    totals = {"university_ok": 0, "both_ok": 0}
    for student in students:
        university = student["short_university"]
        student["university_ok"] = is_university_in_list(university, allowed)
        student["speciality_ok"] = is_speciality_allowed(university, student["speciality"], allowed)
        if student["university_ok"]:
            totals["university_ok"] += 1
        if student["university_ok"] and student["speciality_ok"]:
            totals["both_ok"] += 1
    return totals
