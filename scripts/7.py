#!/usr/bin/env python3

# Этот скрипт вычисляет среднее за 14 дней потребление исходя из нормализованных цифр, полученных на предыдущем этапе

import os
import pandas as pd
from datetime import datetime

# Constants
STATS_FOLDER = "СТАТИСТИКА"
ARCHIVE_FOLDER = os.path.join(STATS_FOLDER, "Архив статистики")
DATE_FORMAT = "%d.%m.%Y"
DAYS = 14  # Анализируемый период в днях
OUTPUT_FILE = os.path.join(STATS_FOLDER, "00-Усреднённое-14-дней.xlsx")

# Ensure output and archive folders exist
os.makedirs(STATS_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

# Step 1: Collect the latest reports
files = [
    f for f in os.listdir(STATS_FOLDER)
    if f.startswith("нормализованное-потребление-") and f.endswith(".xlsx")
]
files.sort(
    key=lambda x: datetime.strptime(x.replace("нормализованное-потребление-", "").replace(".xlsx", ""), DATE_FORMAT),
    reverse=True
)
latest_files = files[:DAYS]

# Warn user if fewer than the required reports are available
if len(latest_files) < DAYS:
    print(f"Отчётов менее {DAYS}, статистика может быть ненадёжной.")

if not latest_files:
    print("Нет доступных отчётов для обработки.")
    exit()

# Step 2: Combine data and calculate averages
all_data = []
for file in latest_files:
    file_path = os.path.join(STATS_FOLDER, file)
    try:
        df = pd.read_excel(file_path)
        if not {"SKU", "Название склада", "Артикул", "Название товара", "Ежедневное потребление"}.issubset(df.columns):
            print(f"Пропущен файл из-за отсутствия необходимых колонок: {file}")
            continue
        all_data.append(df)
    except Exception as e:
        print(f"Ошибка чтения файла {file}: {e}")

if not all_data:
    print("Нет данных для обработки.")
    exit()

# Concatenate all data and calculate the average consumption
combined_df = pd.concat(all_data, ignore_index=True)
average_df = combined_df.groupby([
    "SKU", "Название склада", "Артикул", "Название товара"
], as_index=False).agg({
    "Ежедневное потребление": "mean"
})
average_df.rename(columns={"Ежедневное потребление": "Усредненное ежедневное потребление"}, inplace=True)

# Sort by "Название склада"
average_df.sort_values(by="Название склада", inplace=True)

# Step 3: Handle existing file in the stats folder
if os.path.exists(OUTPUT_FILE):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_file = os.path.join(ARCHIVE_FOLDER, os.path.basename(OUTPUT_FILE).replace(".xlsx", f"-{timestamp}.xlsx"))
    os.rename(OUTPUT_FILE, archive_file)
    print(f"Старый отчёт перемещён в архив: {archive_file}")

# Step 4: Save the new averaged report
try:
    average_df.to_excel(OUTPUT_FILE, index=False)
    print(f"Усреднённый отчёт сохранён: {OUTPUT_FILE}")
except Exception as e:
    print(f"Ошибка сохранения отчёта: {e}")

