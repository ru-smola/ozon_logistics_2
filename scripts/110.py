#!/usr/bin/env python3

# Скрипт рассчитывает рейтинг склада: оборачиваемость товаров / срок поставки * 100

import pandas as pd
from tabulate import tabulate

# Шаг 1: Загрузка данных из файла warehouses.xlsx
file_path = "warehouses.xlsx"
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Файл {file_path} не найден. Проверьте, что файл находится в корневой папке проекта.")
    exit()

# Шаг 2: Проверка наличия необходимых столбцов
required_columns = ["Название склада", "Оборачиваемость склада", "Срок поставки"]
for col in required_columns:
    if col not in df.columns:
        print(f"В файле отсутствует необходимый столбец: {col}")
        exit()

# Шаг 3: Расчет рейтинга склада
df["Рейтинг склада"] = (df["Оборачиваемость склада"] / df["Срок поставки"]) * 100

# Шаг 4: Сортировка по рейтингу склада (от большего к меньшему)
df = df.sort_values(by="Рейтинг склада", ascending=False)

# Шаг 5: Отображение результата в консоли
output_columns = ["Название склада", "Рейтинг склада"]
result = df[output_columns]
print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))

# Шаг 6: Сохранение результата в файл warehouses.xlsx
try:
    df.to_excel(file_path, index=False)
    print(f"\nДанные успешно сохранены в файл {file_path}.")
except Exception as e:
    print(f"Ошибка при сохранении файла: {e}")

