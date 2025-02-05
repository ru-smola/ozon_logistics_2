#!/usr/bin/env python3

import subprocess
import time

def check_connection(host="ya.ru"):
    """Пингует хост и ждет успешного пинга. Периодическая проверка каждую минуту."""
    while True:
        response = subprocess.run(
            ["ping", "-c", "1", "-W", "2", host],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        if response.returncode == 0:
            print("Соединение стабильно. Пинг успешен.")
            return True
        else:
            print("Нет соединения, пытаемся снова через 5 минут...")
            time.sleep(300)  # Пауза в 5 минут

if __name__ == "__main__":
    check_connection()

