#!/usr/bin/env python3

import pandas as pd
from datetime import datetime, timedelta
import os

# Constants
WAREHOUSES_FILE = "warehouses.xlsx"
OUTPUT_HTML = "supply_calendar.html"

# Check if the warehouses file exists
if not os.path.exists(WAREHOUSES_FILE):
    print(f"Файл {WAREHOUSES_FILE} не найден.")
    exit()

# Load the warehouse data
try:
    warehouses_df = pd.read_excel(WAREHOUSES_FILE)
except Exception as e:
    print(f"Ошибка чтения файла {WAREHOUSES_FILE}: {e}")
    exit()

# Ensure the required columns exist
required_columns = {"Название склада", "Календарных дней между поставками"}
if not required_columns.issubset(warehouses_df.columns):
    print(f"Файл должен содержать колонки: {', '.join(required_columns)}.")
    exit()

# HTML calendar template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Supply Calendar</title>
    <style>
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid black; padding: 8px; text-align: center; }}
        th {{ background-color: #f2f2f2; }}
        .weekend {{ background-color: #f9c2c2; }} /* Highlight weekends in light red */
        .empty {{ background-color: #e0e0e0; }} /* Highlight non-existent dates in gray */
    </style>
</head>
<body>
    <h1>Календарь поставок</h1>
    <table>
        <thead>
            <tr>
                <th>День</th>
                <th>День недели</th>
                <th>Январь</th>
                <th>Февраль</th>
                <th>Март</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
</body>
</html>
"""

# Prepare calendar data structure
calendar_data = {month: {} for month in range(1, 4)}  # For January, February, March
start_date = datetime(datetime.now().year, 1, 1)
end_date = datetime(datetime.now().year, 3, 31)

current_date = start_date
while current_date <= end_date:
    month = current_date.month
    day = current_date.day
    calendar_data[month][day] = {"day_name": current_date.strftime("%A"), "warehouses": []}
    current_date += timedelta(days=1)

# Assign warehouses to calendar days
for _, row in warehouses_df.iterrows():
    warehouse = row["Название склада"]
    interval_days = row.get("Календарных дней между поставками", 0)

    # Validate interval_days
    if pd.isna(interval_days) or interval_days <= 0:
        print(f"Некорректный интервал дней для склада '{warehouse}': {interval_days}. Пропуск.")
        continue

    interval_days = int(interval_days)
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() >= 5:  # Skip weekends
            current_date += timedelta(days=1)
            continue

        month = current_date.month
        day = current_date.day

        # Add warehouse to the calendar if space is available
        if len(calendar_data[month][day]["warehouses"]) < 2:
            calendar_data[month][day]["warehouses"].append(warehouse)

        # Move to the next scheduled date for this warehouse
        current_date += timedelta(days=interval_days)

# Generate HTML rows for the calendar
rows = ""
for day in range(1, 32):  # Maximum possible days in a month
    row = f"<tr><td>{day}</td><td></td>"
    for month in range(1, 4):  # For January, February, March
        if day in calendar_data[month]:
            day_data = calendar_data[month][day]
            day_name = day_data["day_name"]
            warehouses = ", ".join(day_data["warehouses"])
            class_attr = "weekend" if day_name in ["Saturday", "Sunday"] else ""
            row += f'<td class="{class_attr}">{warehouses}</td>'
        else:
            row += '<td class="empty"></td>'  # Non-existent dates
    row += "</tr>"
    rows += row

# Insert rows into the HTML template
html_content = html_template.format(rows=rows)

# Save the HTML to file
try:
    with open(OUTPUT_HTML, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"Календарь поставок успешно сохранён: {OUTPUT_HTML}")
except Exception as e:
    print(f"Ошибка сохранения HTML файла: {e}")

