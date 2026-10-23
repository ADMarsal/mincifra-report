"""
Точка запуска.

    python3 main.py                      - прочитать пример data/example_students.xlsx
    python3 main.py путь/к/таблице.xlsx  - прочитать свою таблицу
"""

import sys
import zipfile

from openpyxl.utils.exceptions import InvalidFileException

from config import DEFAULT_STUDENTS_FILE, PREVIEW_ROWS
from reader import read_students


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


def main() -> None:
    path = get_file_path(sys.argv)
    try:
        students = read_students(path)
    except FileNotFoundError:
        print(f"Ошибка: файл не найден: {path}")
        sys.exit(1)
    except (zipfile.BadZipFile, InvalidFileException):
        print(f"Ошибка: файл не похож на Excel (.xlsx): {path}")
        sys.exit(1)
    except PermissionError:
        print(f"Ошибка: нет доступа к файлу (возможно, он открыт в Excel): {path}")
        sys.exit(1)
    except ValueError as error:
        print(f"Ошибка в структуре таблицы: {error}")
        sys.exit(1)

    print(f"Файл: {path}")
    print(f"Прочитано студентов: {len(students)}")
    print(f"Всего часов: {total_hours(students)}")
    print(f"\nПервые {PREVIEW_ROWS}:")
    for student in students[:PREVIEW_ROWS]:
        print(f"  {student['name']} | {student['university']} | {student['hours']} ч")


if __name__ == "__main__":
    main()
