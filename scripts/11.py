#!/usr/bin/env python3

# скрипт рассчитывает рейтинг товаров: оборачиваемость (усреднённое ежедневное потребление) из файла 00-Гипотетическое.xlsx * прибыльность из таблицы по ссылке https://docs.google.com/spreadsheets/d/1Ed3zc8mtVR4YodxuVYG1o_SaSR0T-dbKkaBE9vsUVOI/edit?gid=0#gid=0

import pandas as pd
import os

# 1. Создаем или перезаписываем файл Рейтинг-товаров.xlsx из файла СТАТИСТИКА/00-Гипотетическое.xlsx
def create_rating_file():
    # Путь к исходному файлу
    input_file_path = 'СТАТИСТИКА/00-Гипотетическое.xlsx'
    output_file_path = 'Рейтинг-товаров.xlsx'

    # Читаем данные из исходного файла
    df = pd.read_excel(input_file_path)

    # Выбираем только нужные колонки
    df = df[['Название склада', 'Артикул', 'Усредненное ежедневное потребление', 'Статус']]

    # Сохраняем в новый файл
    df.to_excel(output_file_path, index=False)
    print(f"Файл '{output_file_path}' успешно создан.")

# 2. Получаем данные о прибыльности из Google Sheets
def fetch_profitability_data():
    # URL для экспорта Google Sheets в CSV (заменяем /edit на /export?format=csv)
    sheet_url = "https://docs.google.com/spreadsheets/d/1Ed3zc8mtVR4YodxuVYG1o_SaSR0T-dbKkaBE9vsUVOI/export?format=csv&gid=0"
    
    # Загружаем данные в pandas DataFrame
    profitability_df = pd.read_csv(sheet_url)
    
    # Проверяем, что колонка с артикулом и прибыльностью существует
    if 'Артикул' not in profitability_df.columns or 'Прибыльность' not in profitability_df.columns:
        raise ValueError("В таблице Google Sheets отсутствуют необходимые колонки: 'Артикул' и 'Прибыльность'")
    
    return profitability_df

# 3. Объединяем данные и считаем рейтинг товара
def calculate_and_sort_rating():
    # Открываем файл Рейтинг-товаров.xlsx
    rating_file_path = 'Рейтинг-товаров.xlsx'
    df = pd.read_excel(rating_file_path)

    # Получаем данные о прибыльности из Google Sheets
    profitability_df = fetch_profitability_data()

    # Объединяем таблицы по колонке "Артикул"
    merged_df = pd.merge(df, profitability_df, on='Артикул', how='left')

    # Проверяем наличие пропущенных значений в колонке "Прибыльность"
    if merged_df['Прибыльность'].isnull().any():
        print("Внимание: Некоторые артикулы не имеют данных о прибыльности!")

    # Удаляем товары с усреднённым ежедневным потреблением < 0.25
    filtered_df = merged_df[merged_df['Усредненное ежедневное потребление'] >= 0.25].copy()

    # Добавляем колонку "Рейтинг товара" (перемножаем "Усредненное ежедневное потребление" и "Прибыльность")
    filtered_df['Рейтинг товара'] = filtered_df['Усредненное ежедневное потребление'] * filtered_df['Прибыльность']

    # Если "Статус" == "Гипотеза", делим рейтинг пополам
    # Пояснение: Это подход из теории игр. Грубо говоря, при недостатке данных рассматриваем вероятность как ход противника: Гипотеза может полностью подтвердиться (1) или полностью провалиться (0). Таким образом, коэффициент составляет 0.5. При накоплении данных пара товар-склад переходит из статуса "Гипотеза"в статус "Статистика", и отсюда пропадает
    filtered_df.loc[filtered_df['Статус'] == 'Гипотеза', 'Рейтинг товара'] /= 2

    # Сортируем товары по рейтингу от большего к меньшему
    sorted_df = filtered_df.sort_values(by='Рейтинг товара', ascending=False)

    # Сохраняем обратно в файл Рейтинг-товаров.xlsx
    sorted_df.to_excel(rating_file_path, index=False)
    print(f"Файл '{rating_file_path}' успешно обновлен и отсортирован.")

# Основная функция
if __name__ == '__main__':
    try:
        create_rating_file()
        calculate_and_sort_rating()
        print("Скрипт выполнен успешно.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

