#!/usr/bin/env python3

import os
import pandas as pd
from datetime import datetime

# Настройки
folder = "ОСТАТКИ СЮДА"
required_columns = [
    'SKU',
    'Название склада',
    'Артикул',
    'Название товара',
    'Товары в пути',
    'Доступный к продаже товар'
]

for file in os.listdir(folder):
    if file.startswith("остатки-") and file.endswith(".xlsx"):
        print(f"Пропускаем промаркированный файл: {file}")
        continue

    if not file.endswith(".xlsx"):
        continue

    try:
        file_path = os.path.join(folder, file)
        xls = pd.ExcelFile(file_path)
        
        if 'Товар-склад' not in xls.sheet_names:
            print(f"Лист 'Товар-склад' отсутствует в {file}")
            continue
            
        df = pd.read_excel(xls, sheet_name='Товар-склад', header=None)
        
        # Извлекаем дату из A1
        date_str = df.iloc[0, 0].split(": ")[-1].strip()
        try:
            date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            formatted_date = date_obj.strftime("%d.%m.%Y")
        except Exception as e:
            print(f"Ошибка формата даты в {file}: {e}")
            continue

        # Основная обработка данных
        df = df.drop([0, 1, 3]).reset_index(drop=True)  # Удаляем строки 1,2,4
        df.columns = df.iloc[0]  # Берем заголовки из первой строки
        df = df[1:].reset_index(drop=True)  # Удаляем строку с заголовками
        df['Товары в пути'] = df.iloc[:,7] + df.iloc[:,14] + df.iloc[:,15]
        df = df.rename(columns={
            'Доступно к продаже': 'Доступный к продаже товар',
            'Склад': 'Название склада',
            'Название': 'Название товара'
        })
        df = df[required_columns]

        # Формируем финальную структуру
        header = pd.DataFrame([df.columns.tolist()], columns=df.columns)  # Заголовки как данные
        blank_rows = pd.DataFrame([[None]*len(df.columns)]*3, columns=df.columns)  # 3 пустые строки
        final_df = pd.concat([
            blank_rows,    # 3 пустые строки
            header,        # Заголовки в 4-й строке
            df             # Основные данные
        ], ignore_index=True)

        # Сохраняем результат
        new_filename = f"остатки-{formatted_date}.xlsx"
        save_path = os.path.join(folder, new_filename)
        
        with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
            final_df.to_excel(writer, index=False, header=False, sheet_name='Товар-склад')
        
        print(f"Обработан: {file} -> {new_filename}")

    except Exception as e:
        print(f"Критическая ошибка в {file}: {str(e)}")

print("Все операции завершены!")
