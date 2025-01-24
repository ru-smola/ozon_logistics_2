#!/usr/bin/env python3

# Этот скрипт формирует рекомендованную поставку на основании "точки поставки", "среднего потребления" и фактических остатков.

import os
import pandas as pd
from datetime import datetime
import math

# Константы
STOCK_FOLDER = "ОСТАТКИ СЮДА"
SUPPLY_POINTS_FILE = "точки-поставки.xlsx"
OUTPUT_FILE_TEMPLATE = "Черновик поставки-{date}.xlsx"
DATE_FORMAT = "%d.%m.%Y"

# Функция для извлечения даты из имени файла
def extract_date(filename):
    try:
        if filename.startswith("остатки-") and filename.endswith(".xlsx"):
            date_part = filename[len("остатки-"):-len(".xlsx")]
            return datetime.strptime(date_part, DATE_FORMAT)
    except Exception as e:
        print(f"Ошибка извлечения даты из файла '{filename}': {e}")
    return None

# Шаг 1: Найти самый новый файл остатков
stock_files = [f for f in os.listdir(STOCK_FOLDER) if f.startswith("остатки-") and f.endswith(".xlsx")]
if not stock_files:
    print("Нет файлов остатков в папке 'ОСТАТКИ СЮДА'.")
    exit()

stock_files.sort(key=lambda x: extract_date(x), reverse=True)
latest_stock_file = stock_files[0]
print(f"Последний файл остатков: {latest_stock_file}")

# Шаг 2: Загрузка данных из файлов
if not os.path.exists(SUPPLY_POINTS_FILE):
    print(f"Файл с точками поставки не найден: {SUPPLY_POINTS_FILE}")
    exit()

try:
    supply_points_df = pd.read_excel(SUPPLY_POINTS_FILE)
    if not {"Название склада", "Артикул", "Название товара", "Рекомендованная точка поставки", "Усредненное ежедневное потребление", "Срок поставки"}.issubset(supply_points_df.columns):
        print("Некорректный формат файла точек поставки.")
        exit()

    stock_df = pd.read_excel(os.path.join(STOCK_FOLDER, latest_stock_file), skiprows=3)
    if not {"Название склада", "Артикул", "Название товара", "Доступный к продаже товар"}.issubset(stock_df.columns):
        print("Некорректный формат файла остатков.")
        exit()
except Exception as e:
    print(f"Ошибка загрузки данных: {e}")
    exit()

# Шаг 3: Объединение данных
merged_df = pd.merge(supply_points_df, stock_df, on=["Название склада", "Артикул", "Название товара"], how="left")
merged_df["Доступный к продаже товар"] = merged_df["Доступный к продаже товар"].fillna(0)

# Отбросить товары с оборачиваемостью менее 0,3
merged_df = merged_df[merged_df["Усредненное ежедневное потребление"] >= 0.3]

# Рассчитать количество "ПОСТАВИТЬ"
merged_df["ПОСТАВИТЬ"] = (merged_df["Срок поставки"] + 2) * merged_df["Усредненное ежедневное потребление"] - merged_df["Доступный к продаже товар"]
merged_df["ПОСТАВИТЬ"] = merged_df["ПОСТАВИТЬ"].apply(lambda x: math.ceil(x) if x > 0 else 0)

# Шаг 4: Сохранение по складам
output_file = OUTPUT_FILE_TEMPLATE.format(date=datetime.now().strftime(DATE_FORMAT))
archive_folder = "АРХИВ ПОСТАВОК"
os.makedirs(archive_folder, exist_ok=True)
if os.path.exists(output_file):
    archive_path = os.path.join(archive_folder, os.path.basename(output_file))
    os.rename(output_file, archive_path)

try:
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for i, (warehouse, group) in enumerate(merged_df.groupby("Название склада"), start=1):
            sheet_name = f"{i:02d} - {warehouse}"
            group = group[["Артикул", "Название товара", "Доступный к продаже товар", "Рекомендованная точка поставки", "Усредненное ежедневное потребление", "Срок поставки", "ПОСТАВИТЬ"]]
            group.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Черновик поставки сохранён в файл: {output_file}")
except Exception as e:
    print(f"Ошибка сохранения файла черновика поставки: {e}")

