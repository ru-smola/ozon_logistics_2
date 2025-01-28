#!/usr/bin/env python3

# Этот скрипт оценивает дефицит пар склад-товар для топ-11 складов на основе требуемой поставки и рейтинга товара.

import os
import pandas as pd

# Constants
WAREHOUSES_FILE = "warehouses.xlsx"
ITEM_RATINGS_FILE = "Рейтинг-товаров.xlsx"
REQUIRED_SUPPLY_FILE = "Можно-поставить.xlsx"
OUTPUT_FILE = "Дефициты.xlsx"

# Step 1: Load data
if not os.path.exists(WAREHOUSES_FILE):
    raise FileNotFoundError(f"Файл {WAREHOUSES_FILE} не найден.")
if not os.path.exists(ITEM_RATINGS_FILE):
    raise FileNotFoundError(f"Файл {ITEM_RATINGS_FILE} не найден.")
if not os.path.exists(REQUIRED_SUPPLY_FILE):
    raise FileNotFoundError(f"Файл {REQUIRED_SUPPLY_FILE} не найден.")

warehouses_df = pd.read_excel(WAREHOUSES_FILE)
item_ratings_df = pd.read_excel(ITEM_RATINGS_FILE)
required_supply_df = pd.read_excel(REQUIRED_SUPPLY_FILE)

# Ensure necessary columns exist
if not {"Название склада", "Рейтинг склада"}.issubset(warehouses_df.columns):
    raise ValueError("Файл warehouses.xlsx должен содержать колонки 'Название склада' и 'Рейтинг склада'.")
if not {"Артикул", "Рейтинг товара"}.issubset(item_ratings_df.columns):
    raise ValueError("Файл Рейтинг-товаров.xlsx должен содержать колонки 'Артикул' и 'Рейтинг товара'.")
if not {"Название склада", "Артикул", "Требуется поставить"}.issubset(required_supply_df.columns):
    raise ValueError("Файл Черновик поставки.xlsx должен содержать колонки 'Название склада', 'Артикул' и 'Требуется поставить'.")

# Step 2: Select top 11 warehouses
warehouses_df.sort_values(by="Рейтинг склада", ascending=False, inplace=True)
top_warehouses = warehouses_df.iloc[:11]

# Step 3: Filter required supply for top warehouses
top_supply_df = required_supply_df[required_supply_df["Название склада"].isin(top_warehouses["Название склада"])]

# Step 4: Merge data with item ratings
top_supply_with_ratings = pd.merge(
    top_supply_df,
    item_ratings_df,
    on="Артикул",
    how="left",
    suffixes=("", "_item")  # Избегаем дублирования
)

# Ensure no missing values in "Рейтинг товара"
top_supply_with_ratings["Рейтинг товара"] = top_supply_with_ratings["Рейтинг товара"].fillna(0)

# Step 5: Calculate "Дефицит пары"
top_supply_with_ratings["Дефицит пары"] = (
    top_supply_with_ratings["Требуется поставить"] * top_supply_with_ratings["Рейтинг товара"]
)

# Step 6: Calculate total deficit per warehouse
if "Название склада" not in top_supply_with_ratings.columns:
    print("Ошибка: колонка 'Название склада' отсутствует в объединённой таблице.")
    exit()

warehouse_deficits = top_supply_with_ratings.groupby("Название склада")["Дефицит пары"].sum().reset_index()
warehouse_deficits.rename(columns={"Дефицит пары": "Суммарный дефицит"}, inplace=True)

# Step 7: Save result to Excel
output_columns = ["Название склада", "Суммарный дефицит"]
warehouse_deficits = warehouse_deficits[output_columns]

try:
    warehouse_deficits.to_excel(OUTPUT_FILE, index=False)
    print(f"Файл 'Дефициты.xlsx' успешно сформирован и сохранён по пути: {OUTPUT_FILE}")
except Exception as e:
    print(f"Ошибка сохранения файла: {e}")

