#!/usr/bin/env python3

# Этот скрипт нормализует продажи товаров, вычисленные на предыдущем этапе, к ежедневному потреблению (например, товар А на складе Б рода 1 раз за 4 дня, значит потребление 0,25 в день.

import os
import pandas as pd
from datetime import datetime

# Constants
SALES_FOLDER = "ОТЧЁТЫ/ПРОДАНО ТОВАРОВ"
PAIR_FILE_TEMPLATE = "ОТЧЁТЫ/found-pairs-{date}.txt"
OUTPUT_FOLDER = "СТАТИСТИКА"
DATE_FORMAT = "%d.%m.%Y"

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to extract date from filename
def extract_date(filename):
    try:
        if filename.startswith("продано-товаров-") and filename.endswith(".xlsx"):
            date_part = filename[len("продано-товаров-"):-len(".xlsx")]
            return datetime.strptime(date_part, DATE_FORMAT)
    except Exception as e:
        print(f"Error extracting date from file '{filename}': {e}")
    return None

# Function to load days from found-pairs file
def load_days_between_reports(date):
    pair_file = PAIR_FILE_TEMPLATE.format(date=datetime.now().strftime(DATE_FORMAT))
    if not os.path.exists(pair_file):
        print(f"Файл с парами не найден: {pair_file}")
        return None

    try:
        with open(pair_file, "r", encoding="utf-8") as f:
            lines = f.readlines()[3:]  # Skip the first three lines
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    newer_report = parts[1].strip()
                    days = int(parts[2].strip())
                    if newer_report.endswith(date.strftime(DATE_FORMAT) + ".xlsx"):
                        return days
    except Exception as e:
        print(f"Ошибка чтения файла с парами: {e}")

    return None

# Process a single sales file
def process_sales_file(sales_file):
    print(f"Обрабатываем файл: {sales_file}")

    # Extract the date from the sales file
    date = extract_date(sales_file)
    if not date:
        print(f"Не удалось извлечь дату из файла {sales_file}")
        return

    # Find the number of days from the found-pairs file
    days_between = load_days_between_reports(date)
    if not days_between:
        print(f"Не удалось определить количество дней для файла {sales_file}")
        return

    # Load the sales data
    try:
        sales_data = pd.read_excel(os.path.join(SALES_FOLDER, sales_file))
    except Exception as e:
        print(f"Ошибка загрузки файла {sales_file}: {e}")
        return

    # Ensure required columns exist
    required_columns = ["SKU", "Название склада", "Артикул", "Название товара", "Продано товаров"]
    if not all(col in sales_data.columns for col in required_columns):
        print(f"Нет необходимых колонок в файле {sales_file}")
        return

    # Calculate daily consumption
    sales_data["Ежедневное потребление"] = sales_data["Продано товаров"] / days_between

    # Select relevant columns
    result = sales_data[[
        "SKU", "Название склада", "Артикул", "Название товара", "Ежедневное потребление"
    ]]

    # Save to Excel
    output_file = os.path.join(OUTPUT_FOLDER, f"нормализованное-потребление-{date.strftime(DATE_FORMAT)}.xlsx")
    result.to_excel(output_file, index=False)
    print(f"Отчёт сохранён: {output_file}")

# Main script
if __name__ == "__main__":
    # Get all sales files
    sales_files = [f for f in os.listdir(SALES_FOLDER) if f.startswith("продано-товаров-") and f.endswith(".xlsx")]
    sales_files = sorted(sales_files, key=extract_date)

    if not sales_files:
        print("Нет файлов в папке ПРОДАНО ТОВАРОВ.")
        exit()

    # Ask user to process all files or only the last one
    choice = input("Обработать все файлы (1) или только последний отчёт (2)? ").strip()
    if choice not in ["1", "2"]:
        print("Неверный выбор. Выход.")
        exit()

    # Process files
    if choice == "2":
        process_sales_file(sales_files[-1])
    elif choice == "1":
        for sales_file in sales_files:
            process_sales_file(sales_file)

