#!/usr/bin/env python3

import os
from datetime import datetime

# Constants
STOCK_FOLDER = "ОСТАТКИ СЮДА"
REPORT_FOLDER = "ОТЧЁТЫ"
DATE_FORMAT = "%d.%m.%Y"

# Ensure output folder exists
os.makedirs(REPORT_FOLDER, exist_ok=True)

# Function to extract date from filename
def extract_date(filename):
    try:
        # Split filename to extract date part correctly
        # Example filename: "остатки-13.12.2024.xlsx"
        base_name = filename.split(".xlsx")[0]  # Remove the extension
        date_part = base_name.split("-")[1]  # Extract the date part after "остатки-"
        return datetime.strptime(date_part, DATE_FORMAT)  # Parse the date
    except Exception as e:
        print(f"Ошибка извлечения даты из файла '{filename}': {e}")
        return None

# Function to find and print file pairs
def find_pairs():
    # Get all valid files
    files = [f for f in os.listdir(STOCK_FOLDER) if f.startswith("остатки-") and f.endswith(".xlsx")]
    print(f"Найденные файлы: {files}")  # Debug: print found files

    # Extract dates from filenames
    files_with_dates = []
    for f in files:
        date = extract_date(f)
        if date is not None:
            files_with_dates.append((f, date))
        else:
            print(f"Файл пропущен из-за ошибки извлечения даты: {f}")

    # Sort files by date
    files_with_dates.sort(key=lambda x: x[1])

    # Debug: Print extracted dates
    print("Файлы с извлечёнными датами:")
    for f, date in files_with_dates:
        print(f"{f}: {date.strftime(DATE_FORMAT)}")

    # If less than 2 files, no pairs can be formed
    if len(files_with_dates) < 2:
        print("Недостаточно файлов для формирования пар.")
        return

    # Form pairs
    pairs = []
    for i in range(len(files_with_dates) - 1):
        pairs.append(f"{files_with_dates[i][0]} И {files_with_dates[i + 1][0]}")

    # Print oldest date and all pairs
    print(f"Самая старая дата: {files_with_dates[0][1].strftime(DATE_FORMAT)}")
    print("\nНайденные пары файлов:")
    for pair in pairs:
        print(pair)

    # Save pairs to a file
    current_date = datetime.now().strftime(DATE_FORMAT)
    output_file = os.path.join(REPORT_FOLDER, f"found-pairs-{current_date}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Самая старая дата: {files_with_dates[0][1].strftime(DATE_FORMAT)}\n\n")
        f.write("Найденные пары файлов:\n")
        for pair in pairs:
            f.write(pair.replace(" И ", ",") + "\n")

    print(f"\nПары сохранены в файл: {output_file}")

# Main script
if __name__ == "__main__":
    find_pairs()
