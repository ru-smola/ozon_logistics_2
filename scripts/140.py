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

    # Sort by "Доля в рейтинге" and split into priority and secondary groups
    df.sort_values(by="Доля в рейтинге", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)

    priority_group = df.iloc[:11]  # Top 11 warehouses
    secondary_group = df.iloc[11:]  # Remaining warehouses

    # Define shipments allocation
    TOTAL_SHIPMENTS = 40
    PRIORITY_SHIPMENTS = 30
    SECONDARY_SHIPMENTS = 10

    # Calculate shipments per month for priority group
    priority_total_rating = priority_group["Рейтинг склада"].sum()
    priority_group["Поставок в месяц"] = (
        PRIORITY_SHIPMENTS * priority_group["Рейтинг склада"] / priority_total_rating
    ).apply(lambda x: math.ceil(x) if x > 0 else 0)

    # Calculate shipments per month for secondary group
    secondary_total_rating = secondary_group["Рейтинг склада"].sum()
    secondary_group["Поставок в месяц"] = (
        SECONDARY_SHIPMENTS * secondary_group["Рейтинг склада"] / secondary_total_rating
    ).apply(lambda x: math.ceil(x) if x > 0 else 0)

    # Combine the groups back into one DataFrame
    df = pd.concat([priority_group, secondary_group], ignore_index=True)

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

