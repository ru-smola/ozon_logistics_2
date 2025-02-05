#!/usr/bin/env python3

import os
import pandas as pd
import numpy as np

# Constants
RATING_FILE = "Сводный-рейтинг.xlsx"
OUTPUT_FILE = "ОЖЗ.xlsx"

# Step 1: Load data
if not os.path.exists(RATING_FILE):
    raise FileNotFoundError(f"Файл с рейтингом не найден: {RATING_FILE}")

rating_df = pd.read_excel(RATING_FILE)

# Ensure necessary columns are present
required_columns = {
    "Название склада", "Артикул", "Усредненное ежедневное потребление", 
    "Календарных дней между поставками", "Статус", "Рейтинг склада"
}

if not required_columns.issubset(rating_df.columns):
    raise ValueError(f"Файл {RATING_FILE} должен содержать колонки: {required_columns}")

# Step 2: Calculate ТЗ (Текущий запас)
rating_df["Текущий запас"] = (
    rating_df["Усредненное ежедневное потребление"] * rating_df["Календарных дней между поставками"]
)

# Step 3: Calculate СЗ (Страховой запас)
def calculate_safety_stock(daily_consumption, lead_time_days):
    return daily_consumption * np.sqrt(lead_time_days) * 0.85

rating_df["Страховой запас"] = rating_df.apply(
    lambda row: calculate_safety_stock(row["Усредненное ежедневное потребление"], row["Календарных дней между поставками"]),
    axis=1
)

# Step 4: Calculate ОЖЗ (Общий желаемый запас)
rating_df["Общий желаемый запас"] = (
    rating_df["Текущий запас"]# + rating_df["Страховой запас"]
).round(0)

print("Страховой запас сейчас отключен, так как есть дефицит товара")

# Step 5: Save result to Excel
output_columns = [
    "Название склада", "Артикул", "Усредненное ежедневное потребление", 
    "Календарных дней между поставками", "Текущий запас", "Страховой запас", "Общий желаемый запас",
    "Статус", "Рейтинг склада"
]

result_df = rating_df[output_columns]

# Sort by warehouse rating
result_df.sort_values(by="Рейтинг склада", ascending=False, inplace=True)

try:
    result_df.to_excel(OUTPUT_FILE, index=False)
    print(f"Файл 'ОЖЗ.xlsx' успешно сформирован и сохранён по пути: {OUTPUT_FILE}")
except Exception as e:
    print(f"Ошибка сохранения файла: {e}")

