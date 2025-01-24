#!/usr/bin/env python3

# Этот скрипт вычисляет точку поставки, то есть ПРИ КАКОМ ОСТАТКЕ пора поставлять товар

import os
import pandas as pd
from datetime import datetime

# Constants
WAREHOUSES_FILE = "warehouses.xlsx"
AVERAGE_FILE = "СТАТИСТИКА/00-Усреднённое-14-дней.xlsx"
OUTPUT_FILE = "точки-поставки.xlsx"

# Step 1: Load warehouse delivery times
if not os.path.exists(WAREHOUSES_FILE):
    print(f"Файл со сроками поставки не найден: {WAREHOUSES_FILE}")
    exit()

try:
    warehouses_df = pd.read_excel(WAREHOUSES_FILE)
    if not {"Название склада", "Срок поставки"}.issubset(warehouses_df.columns):
        print("Отсутствуют необходимые колонки в файле warehouses.xlsx. Требуются: 'Название склада', 'Срок поставки'.")
        exit()
except Exception as e:
    print(f"Ошибка чтения файла warehouses.xlsx: {e}")
    exit()

# Step 2: Load average daily consumption
if not os.path.exists(AVERAGE_FILE):
    print(f"Файл с усреднённым потреблением не найден: {AVERAGE_FILE}")
    exit()

try:
    average_df = pd.read_excel(AVERAGE_FILE)
    if not {"SKU", "Название склада", "Артикул", "Название товара", "Усредненное ежедневное потребление"}.issubset(average_df.columns):
        print("Отсутствуют необходимые колонки в файле с усреднённым потреблением. Требуются: 'SKU', 'Название склада', 'Артикул', 'Название товара', 'Усредненное ежедневное потребление'.")
        exit()
except Exception as e:
    print(f"Ошибка чтения файла с усреднённым потреблением: {e}")
    exit()

# Step 3: Merge data
merged_df = pd.merge(average_df, warehouses_df, on="Название склада", how="left")

if merged_df["Срок поставки"].isnull().any():
    print("Некоторые склады из усреднённого отчёта отсутствуют в файле warehouses.xlsx. Проверьте данные.")

# Step 4: Calculate supply points
merged_df["Рекомендованная точка поставки"] = merged_df["Усредненное ежедневное потребление"] * merged_df["Срок поставки"] + 2

# Step 5: Save the result
try:
    merged_df = merged_df[[
        "SKU", "Название склада", "Артикул", "Название товара", 
        "Усредненное ежедневное потребление", "Срок поставки", "Рекомендованная точка поставки"
    ]]
    merged_df.to_excel(OUTPUT_FILE, index=False)
    print(f"Рекомендованные точки поставки сохранены в файл: {OUTPUT_FILE}")
except Exception as e:
    print(f"Ошибка сохранения файла с точками поставки: {e}")

