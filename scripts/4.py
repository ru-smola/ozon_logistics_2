#!/usr/bin/env python3


# Этот скрипт вычисляет количество поступивших товаров, чтобы избежать арифметической ошибки при расчёте проданных товаров (на входе -- файлы "остатки-..." из папки "ОСТАТКИ СЮДА"), и сохраняет в ОТЧЁТЫ/ПРИБЫЛО ТОВАРОВ в виде xlsx.

import os
import pandas as pd
from datetime import datetime
import warnings
from openpyxl.styles.stylesheet import Stylesheet

# Suppress the specific warning about "no default style"
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Constants
STOCK_FOLDER = "ОСТАТКИ СЮДА"
REPORT_FOLDER = "ОТЧЁТЫ/ПРИБЫЛО ТОВАРОВ"
PAIR_FILE_TEMPLATE = "ОТЧЁТЫ/found-pairs-{date}.txt"
DATE_FORMAT = "%d.%m.%Y"

# Ensure output folder exists
os.makedirs(REPORT_FOLDER, exist_ok=True)

# Function to extract date from filename
def extract_date(filename):
    try:
        # Extract date part between "остатки-" and ".xlsx"
        if filename.startswith("остатки-") and filename.endswith(".xlsx"):
            date_part = filename[len("остатки-"):-len(".xlsx")]
            return datetime.strptime(date_part, DATE_FORMAT)
    except Exception as e:
        print(f"Не удалось прочитать дату в названии пары '{filename}': {e}")
    return None

# Process a single pair of files
def process_file_pair(file1, file2):
    print(f"Обрабатываем пару: {file1} and {file2}")

    # Extract the date of the newer file
    date_newer = extract_date(file2)
    if not date_newer:
        print(f"Не удалось прочитать дату в названии {file2}")
        return

    # Load data, skipping the first 3 rows
    try:
        df1 = pd.read_excel(os.path.join(STOCK_FOLDER, file1), skiprows=3)
        df2 = pd.read_excel(os.path.join(STOCK_FOLDER, file2), skiprows=3)
    except Exception as e:
        print(f"Не удалось загрузить {file1} или {file2}: {e}")
        return

    # Ensure required columns exist
    required_columns = ["SKU", "Название склада", "Артикул", "Название товара", "Товары в пути"]
    if not all(col in df1.columns and col in df2.columns for col in required_columns):
        print(f"Нет необходимых колонок в файлах : {file1}, {file2} — требуется SKU, Название склада, Артикул, Название товара, товары в пути")
        return

    # Merge data on SKU and warehouse
    merged = pd.merge(
        df1, df2,
        on=["SKU", "Название склада", "Артикул", "Название товара"],
        suffixes=("_old", "_new")
    )

    # Calculate the difference in "Товары в пути"
    merged["Прибыло товаров"] = merged["Товары в пути_old"] - merged["Товары в пути_new"]

    # Filter out rows where the difference is <= 0
    result = merged[merged["Прибыло товаров"] > 0]

    # Select relevant columns
    result = result[[
        "SKU", "Название склада", "Артикул", "Название товара", "Прибыло товаров"
    ]]

    # Save to Excel
    output_file = os.path.join(REPORT_FOLDER, f"прибыло-товаров-{date_newer.strftime(DATE_FORMAT)}.xlsx")
    result.to_excel(output_file, index=False)
    print(f"Отчёт сохранён {output_file}")

# Main script
if __name__ == "__main__":
    # Get today's date
    today = datetime.now().strftime(DATE_FORMAT)

    # Determine pair file name
    pair_file = PAIR_FILE_TEMPLATE.format(date=today)
    if not os.path.exists(pair_file):
        print(f"Пара не найдена: {pair_file}")
        exit()

    # Read pair file and skip the first three lines
    try:
        with open(pair_file, "r", encoding="utf-8") as f:
            lines = f.readlines()[3:]  # Skip first 3 lines
            # Process only the first two columns (skip the third column)
            pairs = [line.strip().split(",")[:2] for line in lines if "," in line]
    except Exception as e:
        print(f"Не удалось прочитать пару файлов: {e}")
        exit()

    if not pairs:
        print("Пары не найдены.")
        exit()

    # Ask user to process all pairs or only the last one
    choice = input("Обработать все файлы (1) или только последнюю пару (2)? ").strip()
    if choice not in ["1", "2"]:
        print("Значение не равно 1 или 2, сброс.")
        exit()

    # Process pairs
    if choice == "2":
        process_file_pair(pairs[-1][0], pairs[-1][1])
    elif choice == "1":
        for pair in pairs:
            process_file_pair(pair[0], pair[1])
