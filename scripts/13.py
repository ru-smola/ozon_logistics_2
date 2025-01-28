#!/usr/bin/env python3

# Этот скрипт вычисляет интервал между поставками, основываясь на доле каждого склада в выручке и сроке доставки до него.

import os
import pandas as pd
import math

# Constants
WAREHOUSES_FILE = "warehouses.xlsx"

# Check if file exists
if not os.path.exists(WAREHOUSES_FILE):
    print(f"Файл {WAREHOUSES_FILE} не найден.")
    exit()

try:
    # Load data from the file
    df = pd.read_excel(WAREHOUSES_FILE)

    # Ensure required columns exist
    if not {"Название склада", "Рейтинг склада"}.issubset(df.columns):
        print("Файл должен содержать колонки 'Название склада' и 'Рейтинг склада'.")
        exit()

    # Calculate total rating
    total_rating = df["Рейтинг склада"].sum()

    # Add "Суммарный рейтинг" column
    df["Суммарный рейтинг"] = ""
    if total_rating > 0:
        df.loc[0, "Суммарный рейтинг"] = total_rating

    # Add "Доля в рейтинге" column
    df["Доля в рейтинге"] = df["Рейтинг склада"] / total_rating

    # Define the total number of shipments per month
    TOTAL_SHIPMENTS_PER_MONTH = 35

    # Add "Поставок в месяц" column
    df["Поставок в месяц"] = (TOTAL_SHIPMENTS_PER_MONTH * df["Доля в рейтинге"]).apply(lambda x: math.ceil(x) if x > 0 else 0)

    # Define the average number of working days in a month
    WORKING_DAYS_PER_MONTH = 20.65

    # Add "Рабочих дней между поставками" column
    df["Рабочих дней между поставками"] = df["Поставок в месяц"].apply(
        lambda x: math.ceil(WORKING_DAYS_PER_MONTH / x) if x > 0 else 0
    )

    # Add "Календарных дней между поставками" column
    CALENDAR_DAYS_PER_MONTH = 30
    df["Календарных дней между поставками"] = df["Поставок в месяц"].apply(
        lambda x: math.ceil(CALENDAR_DAYS_PER_MONTH / x) if x > 0 else 0
    )

    # Save updated data back to the same file
    df.to_excel(WAREHOUSES_FILE, index=False)
    print(f"Файл {WAREHOUSES_FILE} обновлён.")

except Exception as e:
    print(f"Ошибка обработки файла: {e}")

