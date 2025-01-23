#!/usr/bin/env python3
#this scripts sorts and renames xlsx files

import os
import pandas as pd

# Define the folder containing the files
folder = "ОСТАТКИ СЮДА"

# Process each file in the folder
for i, file in enumerate(os.listdir(folder), start=1):
    # Skip files that are already correctly named
    if file.startswith("остатки-") and file.endswith(".xlsx"):
        print(f"Уже промаркированные файлы ({i}): {file}")
        continue

    file_path = os.path.join(folder, file)

    # Only process .xlsx files
    if file.endswith(".xlsx"):
        try:
            # Read the file using pandas
            excel_data = pd.read_excel(file_path, header=None)  # Read without assuming column headers

            # Extract the date from cell B2
            date_str = excel_data.iloc[1, 1]  # B2 corresponds to row 1, column 1 (0-based index)

            # Ensure the date is in the expected format dd/mm/yyyy
            try:
                date = pd.to_datetime(date_str, format="%d/%m/%Y").strftime("%d.%m.%Y")
            except ValueError:
                print(f"Формат даты в файле не соответствует {file}: {date_str}. Проверьте файл.")
                continue

            # Rename the file
            new_file_name = f"остатки-{date}.xlsx"
            new_file_path = os.path.join(folder, new_file_name)
            os.rename(file_path, new_file_path)
            print(f"Переименовано: {file} -> {new_file_name}")

        except Exception as e:
            print(f"Ошибки обработки {file}: {e}")

print("Сортировка по дате и маркировка выполнена.")
