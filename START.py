#!/usr/bin/env python3

import os
import time
import subprocess

# Define the PROJECT root folder
project_root = os.path.abspath(os.path.dirname(__file__))

# Define the paths to the scripts
# 1 - сортировка и переименование
script1_path = os.path.join(project_root, "scripts", "1.py")
# 2 - идентифицируем и сохраняем пары
script2_path = os.path.join(project_root, "scripts", "2.py")
# 3 - считаем дни между парами
script3_path = os.path.join(project_root, "scripts", "3.py")
# 4 - считаем сколько товара прибыло
script4_path = os.path.join(project_root, "scripts", "4.py")
# 5 - считаем сколько товара продано с учётом поставленного И ПУСТЫХ СТРОК
script5_path = os.path.join(project_root, "scripts", "5.py")
# 6 - нормализуем потребление к ежедневному 
script6_path = os.path.join(project_root, "scripts", "6.py")
# 7 - вычисляем среднее за 14 дней 
script7_path = os.path.join(project_root, "scripts", "7.py")
# 8 - вычисляем точку поставки 
script8_path = os.path.join(project_root, "scripts", "8.py")
# 9 - черновик поставки 
script9_path = os.path.join(project_root, "scripts", "9.py")
# 10 - обновление черновика поставки с учётом товаров в пути
#script10_path = os.path.join(project_root, "scripts", "10.py")

# Temporarily set the working directory to the PROJECT root
os.chdir(project_root)

# Run the scripts one by one
print("Шаг 1: все файлы приводятся сортируются по дате и переименовываются в соответствии.")
subprocess.run(["python3", script1_path])
time.sleep(3)

print("\nШаг 2: составляем пары файлов для анализа.")
subprocess.run(["python3", script2_path])
time.sleep(3)

print("\nШаг 3: вычисляем разницу в днях между файлами.")
subprocess.run(["python3", script3_path])
time.sleep(3)

print("\nШаг 4: считаем, сколько товара прибыло за эти дни.")
subprocess.run(["python3", script4_path])
time.sleep(3)

print("\nШаг 5: считаем проданный товар с учётом поставленного")
subprocess.run(["python3", script5_path])
time.sleep(3)

print("\nШаг 6: считаем ежедневное потребление товаров")
subprocess.run(["python3", script6_path])
time.sleep(3)

print("\nШаг 7: считаем среднее за 14 или 30 дней")
subprocess.run(["python3", script7_path])
time.sleep(3)

print("\nШаг 8: вычисляем точку поставки")
subprocess.run(["python3", script8_path])
time.sleep(3)

print("\nШаг 9: формируем черновик поставки")
subprocess.run(["python3", script9_path])
time.sleep(3)

#print("\nШаг 10: обновляем черновик поставки с учётом товаров в пути")
#subprocess.run(["python3", script10_path])
#time.sleep(3)


#print("Запускаем статистический анализ продаж")
#subprocess.run(["python3", script3_path])

#print("\nВНИМАНИЕ! Если необходимо, сейчас можно изменить справочные сроки поставки в файле warehouses.xlsx, и программа сформирует поставку с учётом новых сроков.")
#input("Нажмите [Enter] для продолжения")
#print("Формируем черновик поставки.")
#subprocess.run(["python3", script4_path])
#time.sleep(2)
#subprocess.run(["python3", script5_path])
#time.sleep(3)
#subprocess.run(["python3", script6_path])
#time.sleep(3)
#subprocess.run(["python3", script7_path])

print("\nВсё готово для вашей успешной работы! Хорошего дня 😉")
