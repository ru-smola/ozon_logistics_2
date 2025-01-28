#!/usr/bin/env python3

# Этот скрипт вычисляет скользящее среднее за 10 дней потребления

import os
import pandas as pd
from datetime import datetime

# Constants
STATS_FOLDER = "СТАТИСТИКА"
ARCHIVE_FOLDER = os.path.join(STATS_FOLDER, "Архив статистики")
DATE_FORMAT = "%d.%m.%Y"
WINDOW_SIZE = 10  # Размер окна для скользящего среднего
OUTPUT_FILE = os.path.join(STATS_FOLDER, "00-Скользящее-среднее-10-дней.xlsx")

# Ensure output and archive folders exist
os.makedirs(STATS_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

# Step 1: Collect historical reports
files = [
    f for f in os.listdir(STATS_FOLDER)
    if f.startswith("нормализованное-потребление-") and f.endswith(".xlsx")
]

# Sort files by date
files.sort(
    key=lambda x: datetime.strptime(x.replace("нормализованное-потребление-", "").replace(".xlsx", ""), DATE_FORMAT)
)

# Step 2: Prepare data for MA calculation
all_data = []
for file in files:
    file_path = os.path.join(STATS_FOLDER, file)
    try:
        df = pd.read_excel(file_path)
        if not {"SKU", "Название склада", "Артикул", "Название товара", "Ежедневное потребление"}.issubset(df.columns):
            continue
        
        # Extract date from filename
        date_str = file.replace("нормализованное-потребление-", "").replace(".xlsx", "")
        df["Дата"] = datetime.strptime(date_str, DATE_FORMAT)
        
        all_data.append(df)
    except Exception as e:
        print(f"Ошибка чтения файла {file}: {e}")

if not all_data:
    print("Нет данных для обработки.")
    exit()

# Combine all data
combined_df = pd.concat(all_data, ignore_index=True)

# Step 3: Calculate rolling average
def calculate_ma(group):
    group = group.sort_values('Дата')
    group["Усредненное ежедневное потребление"] = (
        group['Ежедневное потребление']
        .rolling(window=WINDOW_SIZE, min_periods=1)
        .mean()
    )
    return group

# Group and calculate rolling average
result_df = combined_df.groupby(
    ["SKU", "Название склада", "Артикул", "Название товара"],
    as_index=False,
).apply(calculate_ma).reset_index(drop=True)

# Drop duplicates and keep only the last date's rolling average for each group
result_df = result_df.sort_values("Дата").drop_duplicates(
    subset=["SKU", "Название склада", "Артикул", "Название товара"],
    keep="last"
)

# Keep only relevant columns
result_df = result_df[
    ["SKU", "Название склада", "Артикул", "Название товара", "Усредненное ежедневное потребление"]
]

# Sort by warehouse name
result_df.sort_values(by="Название склада", inplace=True)

# Step 4: Handle existing file
if os.path.exists(OUTPUT_FILE):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_file = os.path.join(ARCHIVE_FOLDER, os.path.basename(OUTPUT_FILE).replace(".xlsx", f"-{timestamp}.xlsx"))
    os.rename(OUTPUT_FILE, archive_file)
    print(f"Старый отчёт перемещён в архив: {archive_file}")

# Step 5: Save new report
try:
    result_df.to_excel(OUTPUT_FILE, index=False)
    print(f"Отчёт со скользящим средним сохранён: {OUTPUT_FILE}")
except Exception as e:
    print(f"Ошибка сохранения отчёта: {e}")

