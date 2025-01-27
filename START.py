#!/usr/bin/env python3

import os
import time
import subprocess

# Define the PROJECT root folder
project_root = os.path.abspath(os.path.dirname(__file__))

# Задаём пути к скриптам

# подготовка перед работой: проверяем стабильность интеренет-соединения. Если соединения нет, скрипт ждёт пока появится и не запускает следующие.
scriptPRE_path = os.path.join(project_root, "scripts", "connection-checker.py")

# 0 - скачивание файла
# этот скрипт скачивает файл остатков с озона. Эмулирует запрос от пользователя через бразуер с помощью куки. Если (когда) кука просрочится, перестанет работать: надо иногда менять
script0_path = os.path.join(project_root, "scripts", "OL4.py")

# 1 - сортировка и переименование. 
# Этот скрипт сортирует и переименовывает файлы xlsx в папке ОСТАТКИ СЮДА, при этом не трогает уже промаркированные файлы (начинаются с "остатки"), любые другие обрабатывает и ищет в ячейке B2 у них дату для переименования. Сохраняет там же, без перемещений.
script1_path = os.path.join(project_root, "scripts", "1.py")

# 2 - идентифицируем и сохраняем пары.
# Этот скрипт сопоставляет пары файлов, используя даты в названиях файлов, и составляет список таких пар для дальнейшего анализа. На входе: файлы "остатки-..." из папки "ОСТАТКИ СЮДА", на выходе файл found-pairs-дата.txt в папке ОТЧЁТЫ
script2_path = os.path.join(project_root, "scripts", "2.py")

# 3 - считаем дни между парами
# Этот скрипт вычисляет разницу в днях между парами файлов, сопоставленными на предыдущем этапе, и дописывает в found-pairs-дата.txt в папке ОТЧЁТЫ.
script3_path = os.path.join(project_root, "scripts", "3.py")

# 4 - считаем сколько товара прибыло
# Этот скрипт вычисляет количество поступивших товаров, чтобы избежать арифметической ошибки при расчёте проданных товаров (на входе -- файлы "остатки-..." из папки "ОСТАТКИ СЮДА"), и сохраняет в ОТЧЁТЫ/ПРИБЫЛО ТОВАРОВ в виде xlsx.
script4_path = os.path.join(project_root, "scripts", "4.py")

# 5 - считаем сколько товара продано с учётом поставленного И ПУСТЫХ СТРОК (то есть если в более новом отчёте товар не значится, то мы считаем что он кончился и вычисляем продажи между старым и новым отчётами, считая значение в новом отчёте за 0, например, 5 - 0 = 5.
# Это основной отчёт: количество проданных товаров. На входе "остатки-..." из папки "ОСТАТКИ СЮДА", поступившие товары из "ОТЧЁТЫ/ПРИБЫЛО ТОВАРОВ" и пары из "ОТЧЁТЫ/found-pairs-{date}.txt". 
script5_path = os.path.join(project_root, "scripts", "5.py")

# 6 - нормализуем потребление к ежедневному
# Этот скрипт нормализует продажи товаров, вычисленные на предыдущем этапе, к ежедневному потреблению (например, товар А на складе Б рода 1 раз за 4 дня, значит потребление 0,25 в день. На входе — "ОТЧЁТЫ/ПРОДАНО ТОВАРОВ" и "ОТЧЁТЫ/found-pairs-{date}.txt", на выходе -- отчёты в папку СТАТИСТИКА
script6_path = os.path.join(project_root, "scripts", "6.py")

# 7 - вычисляем среднее за 14 дней.
# Этот скрипт вычисляет среднее за 14 дней потребление исходя из нормализованных цифр, полученных на предыдущем этапе
script7_path = os.path.join(project_root, "scripts", "7.py")

# 8 - строим гипотезы об отсутствующих товарах 
# скрипт копирует усреднённое потребление, полученное на предыдущем этапе, и создаёт "гипотезы" для отсутствующих товаров, например, если товар с артикулом 1111 есть на складе 2222, но его нет на складе 3333, то делает строку 3333 - 1111 с УСРЕДНЁННЫМ значением продаж этого товара для всех складов из "усреднённого" отчёта.
script8_path = os.path.join(project_root, "scripts", "8.py")

# 9 - оборачиваемость склада
# скрипт рассчитывает оборачиваемость склада на основании усреднённых данных о продажах всех товаров для этого склада из данных статистики
script9_path = os.path.join(project_root, "scripts", "9.py")

# 10 - рейтинг склада
# скрипт рассчитывает рейтинг склада: оборачиваемость товаров / срок поставки * 100 
script10_path = os.path.join(project_root, "scripts", "10.py")

# 11 - рейтинг товаров
# скрипт рассчитывает рейтинг товаров: оборачиваемость товаров * прибыльность
script11_path = os.path.join(project_root, "scripts", "11.py")

# 12 - сводный рейтинг
# скрипт составляет сводный рейтинг "рейтинг склада" * "рейтинг товара", что позволяет сгладить аберрации
script12_path = os.path.join(project_root, "scripts", "12.py")

# 13 - точка поставки
# Этот скрипт вычисляет точку поставки, то есть ПРИ КАКОМ ОСТАТКЕ пора поставлять товар
script13_path = os.path.join(project_root, "scripts", "13.py")

# Temporarily set the working directory to the PROJECT root
os.chdir(project_root)

# Run the scripts one by one
print("Подготовка: проверяем интернет-соединение...")
subprocess.run(["python3", scriptPRE_path])
time.sleep(3)

print("Шаг 0: скачиваем файл остатков. Время от времени файл авторизации будет устаревать, тогда этот шаг будет неуспешным. Рекомендуем проверять вручную актуальность остатков.")
subprocess.run(["python3", script0_path])
time.sleep(3)

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

print("\nШаг 7: считаем среднее за 14 дней")
subprocess.run(["python3", script7_path])
time.sleep(3)

print("\nШаг 8: строим гипотезы об отсутствующих товарах")
subprocess.run(["python3", script8_path])
time.sleep(3)

print("\nШаг 9: рассчитываем среднюю оборачиваемость склада")
subprocess.run(["python3", script9_path])
time.sleep(3)

print("\nШаг 10: вычисляем рейтинг склада по формуле: средняя оборачиваемость / срок поставки * 100, кстати, вот он:")
subprocess.run(["python3", script10_path])
time.sleep(3)

print("\nШаг 11: вычисляем рейтинг товаров по формуле: оборачиваемость товаров * прибыльность")
subprocess.run(["python3", script11_path])
time.sleep(3)

print("\nШаг 12: вычисляем сводный рейтинг товар * склад")
subprocess.run(["python3", script12_path])
time.sleep(3)

print("\nШаг 13: вычисляем точку поставки,то есть КОГДА пора поставлять товар на склад")
subprocess.run(["python3", script13_path])
time.sleep(3)



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
