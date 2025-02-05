#!/usr/bin/env python3

# Этот скрипт вычисляет приоритет для каждого склада на основе суммарного дефицита и рейтинга склада.

import os
import pandas as pd

# Constants
WAREHOUSES_FILE = "warehouses.xlsx"
DEFICITS_FILE = "Дефициты.xlsx"
OUTPUT_FILE = "Приоритет.xlsx"

# Step 1: Load data
if not os.path.exists(WAREHOUSES_FILE):
    raise FileNotFoundError(f"Файл {WAREHOUSES_FILE} не найден.")
if not os.path.exists(DEFICITS_FILE):
    raise FileNotFoundError(f"Файл {DEFICITS_FILE} не найден.")

warehouses_df = pd.read_excel(WAREHOUSES_FILE)
deficits_df = pd.read_excel(DEFICITS_FILE)

# Ensure necessary columns exist
if not {"Название склада", "Рейтинг склада"}.issubset(warehouses_df.columns):
    raise ValueError("Файл warehouses.xlsx должен содержать колонки 'Название склада' и 'Рейтинг склада'.")
if not {"Название склада", "Суммарный дефицит"}.issubset(deficits_df.columns):
    raise ValueError("Файл Дефициты.xlsx должен содержать колонки 'Название склада' и 'Суммарный дефицит'.")

# Step 2: Merge data
merged_df = pd.merge(
    deficits_df, warehouses_df, on="Название склада", how="left"
)

# Ensure no missing values in "Рейтинг склада"
merged_df["Рейтинг склада"] = merged_df["Рейтинг склада"].fillna(0)

# Step 3: Calculate priority
merged_df["Приоритет"] = (
    (merged_df["Суммарный дефицит"] * 1.5 + merged_df["Рейтинг склада"]) / 10000
)

# Step 4: Select necessary columns and sort
priority_df = merged_df[["Название склада", "Приоритет"]]
priority_df = priority_df.sort_values(by="Приоритет", ascending=False)

# Step 5: Save to Excel
try:
    priority_df.to_excel(OUTPUT_FILE, index=False)
    print(f"Файл 'Приоритет.xlsx' успешно сформирован и сохранён по пути: {OUTPUT_FILE}")
except Exception as e:
    print(f"Ошибка сохранения файла: {e}")

