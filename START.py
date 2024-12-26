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
# 5 - считаем сколько товара продано с учётом поставленного
script5_path = os.path.join(project_root, "scripts", "5.py")
#script5_path = os.path.join(project_root, "scripts", "enroute.py")
#script6_path = os.path.join(project_root, "scripts", "advicer.py")
#script7_path = os.path.join(project_root, "scripts", "commit.py")

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
