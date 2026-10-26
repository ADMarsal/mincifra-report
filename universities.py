"""
Шаг 2. Короткие названия вузов.

В общей таблице вузы записаны полностью и по-разному:
    ФГБОУ ВО "Российский экономический университет имени Г.В.Плеханова"
Программе нужно короткое название, например "РЭУ".

Словарь лежит в файле data/universities.csv:
    ключевые слова;короткое название
    плеханова;РЭУ
Если ключевые слова встречаются в полном названии - это тот самый вуз.
"""

import csv

from config import CSV_DELIMITER, UNKNOWN_UNIVERSITY


def normalize(text) -> str:
    """Привести текст к единому виду: строка, маленькие буквы, ё -> е, без пробелов по краям."""
    if text is None:
        return ""
    return str(text).strip().lower().replace("ё", "е")


def load_university_names(path: str) -> dict:
    """Прочитать словарь вузов: ключевые слова -> короткое название."""
    names = {}
    with open(path, encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=CSV_DELIMITER)
        next(reader)                       # пропускаем строку с заголовками
        for line_number, row in enumerate(reader, start=2):
            if not row:
                continue                   # пустая строка в конце файла
            if len(row) != 2:
                raise ValueError(f"{path}, строка {line_number}: нужно 2 значения через «{CSV_DELIMITER}»")
            keywords, short_name = row
            names[normalize(keywords)] = short_name.strip()
    return names


def short_university_name(full_name, names: dict) -> str:
    """Найти короткое название вуза по полному. Если вуз не найден - UNKNOWN_UNIVERSITY."""
    text = normalize(full_name)
    for keywords, short_name in names.items():
        if keywords in text:
            return short_name
    return UNKNOWN_UNIVERSITY


def count_by_university(students: list[dict]) -> dict:
    """Сколько студентов из каждого вуза: короткое название -> количество."""
    counts = {}
    for student in students:
        name = student["short_university"]
        counts[name] = counts.get(name, 0) + 1
    return counts
