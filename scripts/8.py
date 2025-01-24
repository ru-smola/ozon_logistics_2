#!/usr/bin/env python3

# скрипт копирует усреднённое потребление, полученное на предыдущем этапе, и создаёт "гипотезы" для отсутствующих товаров.

import os
import pandas as pd
from datetime import datetime

# Константы
STATS_FOLDER = "СТАТИСТИКА"
ARCHIVE_FOLDER = os.path.join(STATS_FOLDER, "Архив статистики")
SOURCE_FILE = os.path.join(STATS_FOLDER, "00-Усреднённое-14-дней.xlsx")
TARGET_FILE = os.path.join(STATS_FOLDER, "00-Гипотетическое.xlsx")
DATE_FORMAT = "%Y%m%d%H%M%S"

# Убедимся, что папки существуют
os.makedirs(STATS_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

# Проверяем наличие исходного файла
if not os.path.exists(SOURCE_FILE):
    print(f"Исходный файл {SOURCE_FILE} не найден.")
    exit()

# Шаг 1: Перемещение существующего файла 00-Гипотетическое.xlsx в архив
if os.path.exists(TARGET_FILE):
    timestamp = datetime.now().strftime(DATE_FORMAT)
    archived_file = os.path.join(ARCHIVE_FOLDER, f"00-Гипотетическое-{timestamp}.xlsx")
    os.rename(TARGET_FILE, archived_file)
    print(f"Старый файл {TARGET_FILE} перемещён в архив как {archived_file}.")

# Шаг 2: Чтение исходного файла
try:
    df = pd.read_excel(SOURCE_FILE)
    print(f"Файл {SOURCE_FILE} успешно прочитан.")
except Exception as e:
    print(f"Ошибка чтения файла {SOURCE_FILE}: {e}")
    exit()

# Добавляем колонку "Статус" со значением "Статистика"
df["Статус"] = "Статистика"

# Шаг 3: Дополнение отсутствующими парами склад-товар
# Получаем уникальные склады и товары
unique_warehouses = df["Название склада"].unique()
unique_items = df["Артикул"].unique()

# Создаем DataFrame с уникальными комбинациями складов и товаров
warehouse_item_combinations = pd.DataFrame(
    [(warehouse, item) for warehouse in unique_warehouses for item in unique_items],
    columns=["Название склада", "Артикул"]
)

# Объединяем с исходным DataFrame по складу и артикулу
merged_df = warehouse_item_combinations.merge(
    df,
    on=["Название склада", "Артикул"],
    how="left"
)

# Заполняем отсутствующие строки
missing_rows = merged_df[merged_df["Название товара"].isna()].copy()

# Вычисляем среднее значение потребления для каждого артикула (по всем складам)
item_mean_consumption = df.groupby("Артикул")["Усредненное ежедневное потребление"].mean()

# Добавляем недостающие данные в строки с гипотезами
missing_rows["Название товара"] = missing_rows["Артикул"].map(
    df.drop_duplicates("Артикул").set_index("Артикул")["Название товара"]
)
missing_rows["Усредненное ежедневное потребление"] = missing_rows["Артикул"].map(item_mean_consumption)
missing_rows["Статус"] = "Гипотеза"

# Объединяем исходные данные с дополненными строками
final_df = pd.concat([df, missing_rows], ignore_index=True)

# Сохраняем результат в новый файл
try:
    final_df.to_excel(TARGET_FILE, index=False)
    print(f"Файл успешно сохранён как {TARGET_FILE}.")
except Exception as e:
    print(f"Ошибка сохранения файла {TARGET_FILE}: {e}")

