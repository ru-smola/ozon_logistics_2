#!/usr/bin/env python3

# Этот скрипт обновляет черновик поставки с учётом товаров в пути

import os
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook

# Константы
STOCK_FOLDER = "ОСТАТКИ СЮДА"
DRAFT_FILE_TEMPLATE = "Черновик поставки-{date}.xlsx"
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

# Найти самый новый файл остатков
stock_files = [f for f in os.listdir(STOCK_FOLDER) if f.startswith("остатки-") and f.endswith(".xlsx")]
if not stock_files:
    print("Нет файлов остатков в папке 'ОСТАТКИ СЮДА'.")
    exit()

stock_files.sort(key=lambda x: extract_date(x), reverse=True)
latest_stock_file = stock_files[0]
print(f"Последний файл остатков: {latest_stock_file}")

# Загрузить данные из файла остатков
try:
    stock_df = pd.read_excel(os.path.join(STOCK_FOLDER, latest_stock_file), skiprows=3)
    if not {"Название склада", "Артикул", "Название товара", "Товары в пути"}.issubset(stock_df.columns):
        print("Некорректный формат файла остатков.")
        exit()
except Exception as e:
    print(f"Ошибка загрузки файла остатков: {e}")
    exit()

# Загрузить черновик поставки
today = datetime.now().strftime(DATE_FORMAT)
draft_file = DRAFT_FILE_TEMPLATE.format(date=today)

if not os.path.exists(draft_file):
    print(f"Файл 'Черновик поставки' не найден: {draft_file}")
    exit()

try:
    draft_excel = pd.ExcelFile(draft_file)
    sheet_names = draft_excel.sheet_names
except Exception as e:
    print(f"Ошибка загрузки черновика поставки: {e}")
    exit()

# Обработать каждый лист
try:
    with pd.ExcelWriter(draft_file, mode="w", engine="openpyxl") as writer:
        for sheet_name in sheet_names:
            # Извлечь название склада из имени листа
            warehouse_name = sheet_name.split(" - ", 1)[-1].strip()
            print(f"Обрабатываем склад: {warehouse_name}")

            try:
                draft_df = draft_excel.parse(sheet_name)
            except Exception as e:
                print(f"Ошибка чтения листа '{sheet_name}': {e}")
                continue

            # Проверить, что нужные колонки есть в черновике
            if not {"Артикул", "Название товара", "ПОСТАВИТЬ"}.issubset(draft_df.columns):
                print(f"Некорректный формат на листе '{sheet_name}'. Пропускаем.")
                continue

            # Найти товары в пути для текущего склада
            stock_filtered = stock_df[stock_df["Название склада"] == warehouse_name]

            # Объединить данные
            merged_df = pd.merge(
                draft_df,
                stock_filtered[["Артикул", "Название товара", "Товары в пути"]],
                on=["Артикул", "Название товара"],
                how="left"
            )
            merged_df["Товары в пути"] = merged_df["Товары в пути"].fillna(0)

            # Пересчитать колонку "ПОСТАВИТЬ"
            merged_df["ПОСТАВИТЬ"] = merged_df["ПОСТАВИТЬ"] - merged_df["Товары в пути"]
            merged_df["ПОСТАВИТЬ"] = merged_df["ПОСТАВИТЬ"].apply(lambda x: max(x, 0)).apply(lambda x: int(round(x)))

            # Добавить "Товары в пути" перед "ПОСТАВИТЬ"
            columns = list(merged_df.columns)
            columns.insert(columns.index("ПОСТАВИТЬ"), "Товары в пути")
            merged_df = merged_df[columns]

            # Сохранить лист с обновлёнными данными
            merged_df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Убедиться, что все листы видимы
        writer.book.active = 0  # Первый лист будет активным
        for sheet in writer.book.sheetnames:
            writer.book[sheet].sheet_state = 'visible'

    print(f"Файл 'Черновик поставки' обновлён: {draft_file}")

except Exception as e:
    print(f"Ошибка обработки черновика поставки: {e}")

