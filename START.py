#!/usr/bin/env python3

import os
import time
import subprocess

# Define the PROJECT root folder
project_root = os.path.abspath(os.path.dirname(__file__))

# Задаём пути к скриптам

# 00 подготовка перед работой: проверяем стабильность интеренет-соединения. Если соединения нет, скрипт ждёт пока появится и не запускает следующие.
script00_path = os.path.join(project_root, "scripts", "00.py")

# 10 - скачивание файла
# этот скрипт скачивает файл остатков с озона. Эмулирует запрос от пользователя через бразуер с помощью куки. Если (когда) кука просрочится, перестанет работать: надо иногда менять
script10_path = os.path.join(project_root, "scripts", "10.py")

# 20 - сортировка и переименование. 
# Этот скрипт сортирует и переименовывает файлы xlsx в папке ОСТАТКИ СЮДА, при этом не трогает уже промаркированные файлы (начинаются с "остатки"), любые другие обрабатывает и ищет в ячейке B2 у них дату для переименования. Сохраняет там же, без перемещений.
script20_path = os.path.join(project_root, "scripts", "20.py")

# 30 - идентифицируем и сохраняем пары.
# Этот скрипт сопоставляет пары файлов, используя даты в названиях файлов, и составляет список таких пар для дальнейшего анализа. На входе: файлы "остатки-..." из папки "ОСТАТКИ СЮДА", на выходе файл found-pairs-дата.txt в папке ОТЧЁТЫ
script30_path = os.path.join(project_root, "scripts", "30.py")

# 40 - считаем дни между парами
# Этот скрипт вычисляет разницу в днях между парами файлов, сопоставленными на предыдущем этапе, и дописывает в found-pairs-дата.txt в папке ОТЧЁТЫ.
script40_path = os.path.join(project_root, "scripts", "40.py")

# 50 - считаем сколько товара прибыло
# Этот скрипт вычисляет количество поступивших товаров, чтобы избежать арифметической ошибки при расчёте проданных товаров (на входе -- файлы "остатки-..." из папки "ОСТАТКИ СЮДА"), и сохраняет в ОТЧЁТЫ/ПРИБЫЛО ТОВАРОВ в виде xlsx.
script50_path = os.path.join(project_root, "scripts", "50.py")

# 60 - считаем сколько товара продано с учётом поставленного И ПУСТЫХ СТРОК (то есть если в более новом отчёте товар не значится, то мы считаем что он кончился и вычисляем продажи между старым и новым отчётами, считая значение в новом отчёте за 0, например, 5 - 0 = 5.
# Это основной отчёт: количество проданных товаров. На входе "остатки-..." из папки "ОСТАТКИ СЮДА", поступившие товары из "ОТЧЁТЫ/ПРИБЫЛО ТОВАРОВ" и пары из "ОТЧЁТЫ/found-pairs-{date}.txt". 
script60_path = os.path.join(project_root, "scripts", "60.py")

# 70 - нормализуем потребление к ежедневному
# Этот скрипт нормализует продажи товаров, вычисленные на предыдущем этапе, к ежедневному потреблению (например, товар А на складе Б рода 1 раз за 4 дня, значит потребление 0,25 в день. На входе — "ОТЧЁТЫ/ПРОДАНО ТОВАРОВ" и "ОТЧЁТЫ/found-pairs-{date}.txt", на выходе -- отчёты в папку СТАТИСТИКА
script70_path = os.path.join(project_root, "scripts", "70.py")

# 80 - вычисляем скользящее среднее за 10 дней.
# Этот скрипт вычисляет скользящее среднее (MA) потребление за 10 дней исходя из нормализованных цифр, полученных на предыдущем этапе
script80_path = os.path.join(project_root, "scripts", "80.py")

# 90 - строим гипотезы об отсутствующих товарах 
# скрипт копирует усреднённое потребление, полученное на предыдущем этапе, и создаёт "гипотезы" для отсутствующих товаров, например, если товар с артикулом 1111 есть на складе 2222, но его нет на складе 3333, то делает строку 3333 - 1111 с УСРЕДНЁННЫМ значением продаж этого товара для всех складов из "усреднённого" отчёта.
script90_path = os.path.join(project_root, "scripts", "90.py")

# 100 - оборачиваемость склада
# скрипт рассчитывает оборачиваемость склада на основании усреднённых данных о продажах всех товаров для этого склада из данных статистики
script100_path = os.path.join(project_root, "scripts", "100.py")

# 110 - рейтинг склада
# скрипт рассчитывает рейтинг склада: оборачиваемость товаров / срок поставки * 100 
script110_path = os.path.join(project_root, "scripts", "110.py")

# 120 - рейтинг товаров
# скрипт рассчитывает рейтинг товаров: оборачиваемость товаров * прибыльность
script120_path = os.path.join(project_root, "scripts", "120.py")

# 130 - сводный рейтинг
# скрипт составляет сводный рейтинг "рейтинг склада" * "рейтинг товара", что позволяет сгладить аберрации
script130_path = os.path.join(project_root, "scripts", "130.py")

# 140 - интервал между поставками
# Этот скрипт вычисляет интервал между поставками, основываясь на доле каждого склада в выручке и сроке доставки до него
script140_path = os.path.join(project_root, "scripts", "140.py")

# 150 - ОЖЗ
# Этот скрипт формирует желаемое состояние всех складов
script150_path = os.path.join(project_root, "scripts", "150.py")

# 160 - список теоретически допустимого к поставке товара
# Это ОЖЗ минус текущие остатки и товары в пути
script160_path = os.path.join(project_root, "scripts", "160.py")

# 170 - оценка дефицитности складов
# количество товара, который можно поставить, на рейтинг этих товаров
script170_path = os.path.join(project_root, "scripts", "170.py")

# 180 - расставляем приоритеты по складам
# дефицитность суммарная * рейтинг склада = приоритет склада
script180_path = os.path.join(project_root, "scripts", "180.py")

# 190 - ЧЕРНОВИК ПОСТАВКИ
# Этот скрипт формирует финальный черновик поставки для каждого склада, распределяя товары по их приоритетам и статусам
script190_path = os.path.join(project_root, "scripts", "190.py")


# Temporarily set the working directory to the PROJECT root
os.chdir(project_root)

# Run the scripts one by one
print("Шаг 00: проверяем интернет-соединение...")
subprocess.run(["python3", script00_path])
time.sleep(3)

print("Шаг 10: скачиваем файл остатков.")
subprocess.run(["python3", script10_path])
time.sleep(3)

print("Шаг 20: все файлы приводятся сортируются по дате и переименовываются в соответствии.")
subprocess.run(["python3", script20_path])
time.sleep(3)

print("\nШаг 30: составляем пары файлов для анализа.")
subprocess.run(["python3", script30_path])
time.sleep(3)

print("\nШаг 40: вычисляем разницу в днях между файлами.")
subprocess.run(["python3", script40_path])
time.sleep(3)

print("\nШаг 50: считаем, сколько товара прибыло за эти дни.")
subprocess.run(["python3", script50_path])
time.sleep(3)

print("\nШаг 60: считаем проданный товар с учётом поставленного")
subprocess.run(["python3", script60_path])
time.sleep(3)

print("\nШаг 70: считаем ежедневное потребление товаров")
subprocess.run(["python3", script70_path])
time.sleep(3)

print("\nШаг 80: считаем скользящее среднее за 10 дней")
subprocess.run(["python3", script80_path])
time.sleep(3)

print("\nШаг 90: строим гипотезы об отсутствующих товарах")
subprocess.run(["python3", script90_path])
time.sleep(3)

print("\nШаг 100: рассчитываем среднюю оборачиваемость склада")
subprocess.run(["python3", script100_path])
time.sleep(3)

print("\nШаг 110: вычисляем рейтинг склада по формуле: средняя оборачиваемость / срок поставки * 100, кстати, вот он:")
subprocess.run(["python3", script110_path])
time.sleep(3)

print("\nШаг 120: вычисляем рейтинг товаров по формуле: оборачиваемость товаров * прибыльность")
subprocess.run(["python3", script120_path])
time.sleep(3)

print("\nШаг 130: вычисляем сводный рейтинг: рейтинг товара * рейтинг склада")
subprocess.run(["python3", script130_path])
time.sleep(3)

print("\nШаг 140: вычисляем интервал между поставками, основываясь на доле каждого склада в выручке и сроке доставки до него")
subprocess.run(["python3", script140_path])
time.sleep(3)

print("\nШаг 150: формируем желаемое состояние склада")
subprocess.run(["python3", script150_path])
time.sleep(3)

print("\nШаг 160: ОЖЗ минус текущие остатки = черновик поставки на максималках")
subprocess.run(["python3", script160_path])
time.sleep(3)

print("\nШаг 170: оценка дефицитности складов")
subprocess.run(["python3", script170_path])
time.sleep(3)

print("\nШаг 180: расстановка приоритетов")
subprocess.run(["python3", script180_path])
time.sleep(3)

print("\nШаг 190: ЧЕРНОВИК ПОСТАВКИ")
subprocess.run(["python3", script190_path])
time.sleep(3)

print("\nВсё готово для вашей успешной работы! Хорошего дня 😉")
