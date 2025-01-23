#!/usr/bin/env python3

import os
from datetime import datetime

# Constants
PAIR_FILE_TEMPLATE = "ОТЧЁТЫ/found-pairs-{date}.txt"
DATE_FORMAT = "%d.%m.%Y"

# Function to extract date from filename
def extract_date(filename):
    try:
        # Correctly split and extract the date part between "остатки-" and ".xlsx"
        if filename.startswith("остатки-") and filename.endswith(".xlsx"):
            date_part = filename[len("остатки-"):-len(".xlsx")]
            return datetime.strptime(date_part, DATE_FORMAT)
    except Exception as e:
        print(f"Не удалось прочитать дату в названии файла '{filename}': {e}")
    return None

# Main script
if __name__ == "__main__":
    # Get today's date
    today = datetime.now().strftime(DATE_FORMAT)

    # Determine pair file name
    pair_file = PAIR_FILE_TEMPLATE.format(date=today)
    if not os.path.exists(pair_file):
        print(f"Пара не найдена: {pair_file}")
        exit()

    # Read pairs from the file
    try:
        with open(pair_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Не удалось прочитать пару: {e}")
        exit()

    # Skip the first three lines
    header_lines = lines[:3]
    pair_lines = lines[3:]

    # Process pairs and calculate day differences
    updated_pairs = []
    for line in pair_lines:
        if "," not in line.strip():
            continue
        file1, file2 = line.strip().split(",")
        date1 = extract_date(file1)
        date2 = extract_date(file2)
        if date1 and date2:
            day_difference = (date2 - date1).days
            updated_pairs.append(f"{file1},{file2},{day_difference}")
        else:
            print(f"Не удалось прочитать дату в названии пары: {line.strip()}")
            continue

    # Rewrite the file with the updated pairs
    try:
        with open(pair_file, "w", encoding="utf-8") as f:
            # Write back the header
            f.writelines(header_lines)
            # Write the updated pairs
            for pair in updated_pairs:
                f.write(pair + "\n")
    except Exception as e:
        print(f"Не удалось записать: {e}")
        exit()

    print(f"\nВ файл с перечнем пар отчётов добавлена вычисленная разница в днях: {pair_file}")
