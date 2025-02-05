#!/usr/bin/env python3

# скрипт составляет сводный рейтинг "рейтинг склада" * "рейтинг товара", что позволяет сгладить аберрации

import pandas as pd

def calculate_combined_rating():
    # Пути к файлам
    warehouses_file = "warehouses.xlsx"
    product_ratings_file = "Рейтинг-товаров.xlsx"
    output_file = "Сводный-рейтинг.xlsx"

    # Шаг 1: Читаем данные из файла warehouses.xlsx
    try:
        warehouses_df = pd.read_excel(warehouses_file)
        if 'Название склада' not in warehouses_df.columns or 'Рейтинг склада' not in warehouses_df.columns:
            raise ValueError("Файл 'warehouses.xlsx' должен содержать колонки 'Название склада' и 'Рейтинг'.")
    except Exception as e:
        print(f"Ошибка при чтении файла '{warehouses_file}': {e}")
        return

    # Шаг 2: Читаем данные из файла Рейтинг-товаров.xlsx
    try:
        product_ratings_df = pd.read_excel(product_ratings_file)
        if 'Название склада' not in product_ratings_df.columns or \
           'Артикул' not in product_ratings_df.columns or \
           'Рейтинг товара' not in product_ratings_df.columns:
            raise ValueError("Файл 'Рейтинг-товаров.xlsx' должен содержать колонки 'Название склада', 'Артикул' и 'Рейтинг товара'.")
    except Exception as e:
        print(f"Ошибка при чтении файла '{product_ratings_file}': {e}")
        return

    # Шаг 3: Объединяем данные по колонке "Название склада"
    merged_df = pd.merge(product_ratings_df, warehouses_df, on="Название склада", how="left")

    # Проверяем наличие пропущенных значений в колонке "Рейтинг" (склады без рейтинга)
    if merged_df['Рейтинг склада'].isnull().any():
        print("Внимание: Некоторые склады не имеют данных о рейтинге!")

    # Шаг 4: Вычисляем сводный рейтинг
    merged_df['Сводный рейтинг'] = merged_df['Рейтинг товара'] * merged_df['Рейтинг склада'] / 100

    # Шаг 5: Сортируем по колонке "Сводный рейтинг" от большего к меньшему
    sorted_df = merged_df.sort_values(by="Сводный рейтинг", ascending=False)

    # Шаг 6: Сохраняем результат в новый файл
    sorted_df.to_excel(output_file, index=False)
    print(f"Файл '{output_file}' успешно создан.")

# Основная функция
if __name__ == '__main__':
    try:
        calculate_combined_rating()
        print("Скрипт выполнен успешно.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

