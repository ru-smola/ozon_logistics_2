#!/usr/bin/env python3

# скрипт рассчитывает оборачиваемость склада на основании усреднённых данных о продажах всех товаров для этого склада из данных статистики

import pandas as pd

def calculate_turnover():
    # Путь к файлу с данными об оборачиваемости
    stats_file = "СТАТИСТИКА/00-Усреднённое-14-дней.xlsx"
    warehouses_file = "warehouses.xlsx"

    # Чтение данных из файла статистики
    stats_df = pd.read_excel(stats_file)

    # Проверяем, что нужные колонки существуют
    required_columns_stats = ["Название склада", "Усредненное ежедневное потребление"]
    if not all(col in stats_df.columns for col in required_columns_stats):
        raise ValueError("В файле статистики отсутствуют необходимые колонки.")

    # Вычисляем среднюю оборачиваемость для каждого склада
    turnover_data = stats_df.groupby("Название склада")["Усредненное ежедневное потребление"].mean().reset_index()
    turnover_data.rename(columns={"Усредненное ежедневное потребление": "Оборачиваемость склада"}, inplace=True)

    # Чтение данных из файла складов
    try:
        warehouses_df = pd.read_excel(warehouses_file)
    except FileNotFoundError:
        # Если файл не найден, создаем новый DataFrame
        warehouses_df = pd.DataFrame(columns=["Название склада", "Оборачиваемость склада"])

    # Проверяем, что в файле складов есть нужные колонки
    if "Название склада" not in warehouses_df.columns:
        warehouses_df["Название склада"] = []
    if "Оборачиваемость склада" not in warehouses_df.columns:
        warehouses_df["Оборачиваемость склада"] = 0

    # Обновляем данные об оборачиваемости складов
    for _, row in turnover_data.iterrows():
        warehouse_name = row["Название склада"]
        turnover_value = row["Оборачиваемость склада"]

        # Если склад уже есть в таблице, обновляем значение
        if warehouse_name in warehouses_df["Название склада"].values:
            warehouses_df.loc[warehouses_df["Название склада"] == warehouse_name, "Оборачиваемость склада"] = turnover_value
        else:
            # Если склада нет, добавляем новую строку
            warehouses_df = pd.concat([
                warehouses_df,
                pd.DataFrame({"Название склада": [warehouse_name], "Оборачиваемость склада": [turnover_value]})
            ], ignore_index=True)

    # Заполняем нулями оборачиваемость для складов, которые не рассчитаны
    warehouses_df["Оборачиваемость склада"] = warehouses_df["Оборачиваемость склада"].fillna(0)

    # Сохраняем обновленный файл складов
    warehouses_df.to_excel(warehouses_file, index=False)
    print(f"Файл {warehouses_file} успешно обновлен.")

# Запуск функции
if __name__ == "__main__":
    calculate_turnover()

