#!/usr/bin/env python3

# Это основной отчёт: количество проданных товаров. На входе "остатки-..." из папки "ОСТАТКИ СЮДА", поступившие товары из "ОТЧЁТЫ/ПРИБЫЛО ТОВАРОВ" и пары из "ОТЧЁТЫ/found-pairs-{date}.txt". Считаем сколько товара продано с учётом поставленного И ПУСТЫХ СТРОК (то есть если в более новом отчёте товар не значится, то мы считаем что он кончился и вычисляем продажи между старым и новым отчётами, считая значение в новом отчёте за 0, например, 5 - 0 = 5

import os
import pandas as pd
from datetime import datetime
import warnings
from openpyxl.styles.stylesheet import Stylesheet

# Suppress the specific warning about "no default style"
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Constants
STOCK_FOLDER = "ОСТАТКИ СЮДА"
SUPPLIED_FOLDER = "ОТЧЁТЫ/ПРИБЫЛО ТОВАРОВ"
REPORT_FOLDER = "ОТЧЁТЫ/ПРОДАНО ТОВАРОВ"
PAIR_FILE_TEMPLATE = "ОТЧЁТЫ/found-pairs-{date}.txt"
DATE_FORMAT = "%d.%m.%Y"

# Ensure output folder exists
os.makedirs(REPORT_FOLDER, exist_ok=True)

# Function to extract date from filename
def extract_date(filename):
    try:
        if filename.startswith("остатки-") and filename.endswith(".xlsx"):
            date_part = filename[len("остатки-"):-len(".xlsx")]
            return datetime.strptime(date_part, DATE_FORMAT)
    except Exception as e:
        print(f"Error extracting date from file '{filename}': {e}")
    return None

# Load supplied goods for a specific date
def load_supplied_goods(date_newer):
    supplied_file = os.path.join(SUPPLIED_FOLDER, f"прибыло-товаров-{date_newer.strftime(DATE_FORMAT)}.xlsx")
    if not os.path.exists(supplied_file):
        print(f"No supplied goods report found for {date_newer.strftime(DATE_FORMAT)}. Assuming no supplies.")
        return pd.DataFrame(columns=["SKU", "Название склада", "Артикул", "Название товара", "Прибыло товаров"])
    try:
        return pd.read_excel(supplied_file)
    except Exception as e:
        print(f"Error loading supplied goods file: {e}")
        return pd.DataFrame(columns=["SKU", "Название склада", "Артикул", "Название товара", "Прибыло товаров"])

# Process a single pair of files
def process_file_pair(file1, file2):
    print(f"Processing pair: {file1} and {file2}")

    # Extract the date of the newer file
    date_newer = extract_date(file2)
    if not date_newer:
        print(f"Error extracting date from {file2}")
        return

    # Load data, skipping the first 3 rows
    try:
        df1 = pd.read_excel(os.path.join(STOCK_FOLDER, file1), skiprows=3)
        df2 = pd.read_excel(os.path.join(STOCK_FOLDER, file2), skiprows=3)
    except Exception as e:
        print(f"Error loading files {file1} or {file2}: {e}")
        return

    # Ensure required columns exist
    required_columns = ["SKU", "Название склада", "Артикул", "Название товара", "Доступный к продаже товар"]
    if not all(col in df1.columns and col in df2.columns for col in required_columns):
        print(f"Missing required columns in one of the files: {file1}, {file2}")
        return

    # Load supplied goods for the date of the newer file
    supplied_goods = load_supplied_goods(date_newer)

    # Ensure all pairs from the old file are present in the new file
    df2 = pd.merge(
        df1[["SKU", "Название склада", "Артикул", "Название товара"]],
        df2,
        on=["SKU", "Название склада", "Артикул", "Название товара"],
        how="left"
    )

    # Fill missing values in "Доступный к продаже товар" with 0
    df2["Доступный к продаже товар"] = df2["Доступный к продаже товар"].fillna(0)

    # Merge data on SKU and warehouse
    merged = pd.merge(
        df1, df2,
        on=["SKU", "Название склада", "Артикул", "Название товара"],
        suffixes=("_old", "_new")
    )

    # Merge with supplied goods to get the number of items supplied for the newer date
    merged = pd.merge(
        merged,
        supplied_goods,
        on=["SKU", "Название склада", "Артикул", "Название товара"],
        how="left"
    )

    # Fill missing "Прибыло товаров" with 0
    merged["Прибыло товаров"] = merged["Прибыло товаров"].fillna(0)

    # Calculate the number of sold goods
    merged["Продано товаров"] = merged["Доступный к продаже товар_old"] - (
        merged["Доступный к продаже товар_new"] - merged["Прибыло товаров"]
    )

    # Filter out rows where the number of sold goods is <= 0
    result = merged[merged["Продано товаров"] > 0]

    # Select relevant columns
    result = result[[
        "SKU", "Название склада", "Артикул", "Название товара", "Продано товаров"
    ]]

    # Save to Excel
    output_file = os.path.join(REPORT_FOLDER, f"продано-товаров-{date_newer.strftime(DATE_FORMAT)}.xlsx")
    result.to_excel(output_file, index=False)
    print(f"Report saved to {output_file}")

# Main script
if __name__ == "__main__":
    # Get today's date
    today = datetime.now().strftime(DATE_FORMAT)

    # Determine pair file name
    pair_file = PAIR_FILE_TEMPLATE.format(date=today)
    if not os.path.exists(pair_file):
        print(f"Pair file not found: {pair_file}")
        exit()

    # Read pair file and skip the first three lines
    try:
        with open(pair_file, "r", encoding="utf-8") as f:
            lines = f.readlines()[3:]  # Skip first 3 lines
            pairs = [line.strip().split(",")[:2] for line in lines if "," in line]
    except Exception as e:
        print(f"Error reading pair file: {e}")
        exit()

    if not pairs:
        print("No pairs found in the pair file.")
        exit()

    # Ask user to process all pairs or only the last one
    choice = input("Обработать все файлы (1) или только последнюю пару (2)? ").strip()
    if choice not in ["1", "2"]:
        print("Invalid choice. Exiting.")
        exit()

    # Process pairs
    if choice == "2":
        process_file_pair(pairs[-1][0], pairs[-1][1])
    elif choice == "1":
        for pair in pairs:
            process_file_pair(pair[0], pair[1])

