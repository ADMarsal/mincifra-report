"""
Точка запуска.

    python3 main.py                      - прочитать пример data/example_students.xlsx
    python3 main.py путь/к/таблице.xlsx  - прочитать свою таблицу
"""

import sys
import zipfile

from openpyxl.utils.exceptions import InvalidFileException

from config import DEFAULT_STUDENTS_FILE, MINCIFRA_FILE, OUTPUT_FILE, UNIVERSITIES_FILE
from mincifra import check_students, load_mincifra_list
from reader import read_students
from report import save_report
from statuses import set_statuses
from universities import count_by_university, load_university_names, short_university_name


def get_file_path(arguments: list[str]) -> str:
    """Взять путь к файлу из команды запуска, а если его нет - файл-пример."""
    if len(arguments) > 1:
        return arguments[1]
    return DEFAULT_STUDENTS_FILE


def total_hours(students: list[dict]) -> int:
    """Сложить часы всех студентов. Пустые и нечисловые ячейки пропускаются."""
    total = 0
    for student in students:
        if isinstance(student["hours"], (int, float)):
            total += student["hours"]
    return total


def load_data(path: str) -> tuple[list[dict], dict, dict]:
    """Прочитать все файлы. При ошибке - понятное сообщение и выход из программы."""
    try:
        students = read_students(path)
        university_names = load_university_names(UNIVERSITIES_FILE)
        allowed = load_mincifra_list(MINCIFRA_FILE)
    except FileNotFoundError as error:
        print(f"Ошибка: файл не найден: {error.filename}")
        sys.exit(1)
    except (zipfile.BadZipFile, InvalidFileException):
        print(f"Ошибка: файл не похож на Excel (.xlsx): {path}")
        sys.exit(1)
    except PermissionError as error:
        print(f"Ошибка: нет доступа к файлу (возможно, он открыт в Excel): {error.filename}")
        sys.exit(1)
    except ValueError as error:
        print(f"Ошибка в структуре файла: {error}")
        sys.exit(1)
    return students, university_names, allowed


def main() -> None:
    path = get_file_path(sys.argv)
    students, university_names, allowed = load_data(path)

    for student in students:
        student["short_university"] = short_university_name(student["university"], university_names)

    print(f"Файл: {path}")
    print(f"Прочитано студентов: {len(students)}")
    print(f"Всего часов: {total_hours(students)}")

    print("\nСтудентов по вузам:")
    counts = count_by_university(students)
    for name in sorted(counts):
        print(f"  {name}: {counts[name]}")

    totals = check_students(students, allowed)
    print("\nПроверка по списку Минцифры:")
    print(f"  Вуз есть в списке: {totals['university_ok']} из {len(students)}")
    print(f"  Вуз и направление подходят: {totals['both_ok']} из {len(students)}")

    print("\nСтатусы:")
    for status, count in set_statuses(students).items():
        print(f"  {status}: {count}")

    try:
        save_report(students, OUTPUT_FILE)
    except PermissionError:
        print(f"\nОшибка: не удалось сохранить отчёт - закройте {OUTPUT_FILE} в Excel и запустите снова.")
        sys.exit(1)
    print(f"\nОтчёт сохранён: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
