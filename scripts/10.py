#!/usr/bin/env python3

import requests
import datetime

# получим и отформатим дату
current_date = datetime.datetime.now()
formatted_date = current_date.strftime("%d-%m-%Y")

# URL для запроса
url = "https://seller.ozon.ru/api/som-stocks-bff/Report/GetStockApiReport"

# Заголовки, скопированные из Network Monitor
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ru",
    "content-length": "23",
    "content-type": "application/json",
    "cookie": "__Secure-ab-group=26; TS0149423d=0187c00a18240b65aee1a199055c00def507383016633d54ded82afb4d038041017163d06055861f07bb21b781183fd944ca19cfd8; TS0121feed=0187c00a18240b65aee1a199055c00def507383016633d54ded82afb4d038041017163d06055861f07bb21b781183fd944ca19cfd8; TS018529d3=0187c00a18240b65aee1a199055c00def507383016633d54ded82afb4d038041017163d06055861f07bb21b781183fd944ca19cfd8; x-o3-language=ru; rfuid=NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwxMzQ3MDc1MTIzLC0xLDM2NjM4MTI3NyxXM3NpYm1GdFpTSTZJbEJFUmlCV2FXVjNaWElpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgwc2V5SnVZVzFsSWpvaVEyaHliMjFsSUZCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxcGRXMGdVRVJHSUZacFpYZGxjaUlzSW1SbGMyTnlhWEIwYVc5dUlqb2lVRzl5ZEdGaWJHVWdSRzlqZFcxbGJuUWdSbTl5YldGMElpd2liV2x0WlZSNWNHVnpJanBiZXlKMGVYQmxJam9pWVhCd2JHbGpZWFJwYjI0dmNHUm1JaXdpYzNWbVptbDRaWE1pT2lKd1pHWWlmU3g3SW5SNWNHVWlPaUowWlhoMEwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjFkZlN4N0ltNWhiV1VpT2lKTmFXTnliM052Wm5RZ1JXUm5aU0JRUkVZZ1ZtbGxkMlZ5SWl3aVpHVnpZM0pwY0hScGIyNGlPaUpRYjNKMFlXSnNaU0JFYjJOMWJXVnVkQ0JHYjNKdFlYUWlMQ0p0YVcxbFZIbHdaWE1pT2x0N0luUjVjR1VpT2lKaGNIQnNhV05oZEdsdmJpOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5TEhzaWRIbHdaU0k2SW5SbGVIUXZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlYxOUxIc2libUZ0WlNJNklsZGxZa3RwZENCaWRXbHNkQzFwYmlCUVJFWWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDFkLFd5SnlkUzFTVlNKZCwwLDEsMCwyNCwyMzc0MTU5MzAsOCwyMjcxMjY1MjAsMCwxLDAsLTQ5MTI3NTUyMyxSMjl2WjJ4bElFbHVZeTRnVG1WMGMyTmhjR1VnUjJWamEyOGdUR2x1ZFhnZ2VEZzJYelkwSURVdU1DQW9XREV4T3lCTWFXNTFlQ0I0T0RaZk5qUXBJRUZ3Y0d4bFYyVmlTMmwwTHpVek55NHpOaUFvUzBoVVRVd3NJR3hwYTJVZ1IyVmphMjhwSUVOb2NtOXRaUzh4TXpJdU1DNHdMakFnVTJGbVlYSnBMelV6Tnk0ek5pQXlNREF6TURFd055Qk5iM3BwYkd4aCxleUpqYUhKdmJXVWlPbnNpWVhCd0lqcDdJbWx6U1c1emRHRnNiR1ZrSWpwbVlXeHpaU3dpU1c1emRHRnNiRk4wWVhSbElqcDdJa1JKVTBGQ1RFVkVJam9pWkdsellXSnNaV1FpTENKSlRsTlVRVXhNUlVRaU9pSnBibk4wWVd4c1pXUWlMQ0pPVDFSZlNVNVRWRUZNVEVWRUlqb2libTkwWDJsdWMzUmhiR3hsWkNKOUxDSlNkVzV1YVc1blUzUmhkR1VpT25zaVEwRk9UazlVWDFKVlRpSTZJbU5oYm01dmRGOXlkVzRpTENKU1JVRkVXVjlVVDE5U1ZVNGlPaUp5WldGa2VWOTBiMTl5ZFc0aUxDSlNWVTVPU1U1SElqb2ljblZ1Ym1sdVp5SjlmWDE5LDY1LC0xMjg1NTUxMywxLDEsLTEsMTY5OTk1NDg4NywxNjk5OTU0ODg3LDI5MjQzNTM4Myw0; __Secure-access-token=7.167665561.2CSm_lJqTZKW73Fs3DnvqA.26.Ae8bmPJAhwlzMR6_xnCrNR9_f7y7vYrYNPtk1ewVeJ34HxnYVM3Qz_jQBZsMvwiOQ8qOEBsHIlaMdWrMjE-jtPk.20240617094506.20250128043702.1z4QAvn-S2sPPfAiMTaU8UN3HJ-kw1GSqtTAKhlptJY.1216d871290d48240; __Secure-refresh-token=7.167665561.2CSm_lJqTZKW73Fs3DnvqA.26.Ae8bmPJAhwlzMR6_xnCrNR9_f7y7vYrYNPtk1ewVeJ34HxnYVM3Qz_jQBZsMvwiOQ8qOEBsHIlaMdWrMjE-jtPk.20240617094506.20250128043702.h_yk2sGd7JORQguewZ_YJAefZPrKknUEjdHkfsRNi8g.15f017623711f5901; __Secure-user-id=167665561; is_adult_confirmed=; is_alco_adult_confirmed=; abt_data=7.K_zXQhWMkpeaQVtwvAnGrnR2EbXcV-KO4uK2vqY3J5D-9BcY_tJwKrCOtNhd7MDWMiCa-ReFOcD2a7W7iliV3UT8uZFmjnNnvtNCco5yXsKPjUCD0__388MCyMSUW5xrKxHGTUDfXEKS1S7avBMA2JFIuRK3i3hbJFE68v7FMY781deoplkdGRvGPSfdxaPQJsI_upUB8gm5ikh_lDTztjKXH_BtyAykTmiDCLJ8ZeDGBqzwaj8npdsYOckcvk1fsGZ0QPcfbGL1Dyz3LSc7YENe24Lcb7edomJZRvIM1W3XjyENFMmv5olAfEeP9m1G2oxmt-KBS7Zs4ZBJ8ub8spVb4FpewLE18qhkNecdBs4Z-xyU5wMex3bhg9hPp6vhnm7sXsYcX-GqjhmWlyiYvX_9-dVWbsY6aBsFYDousfaoryXtl1iE0JP4oIqSpFBdhlR5vdof__QrCZqhjj1uvEzY; bacntid=4421294; sc_company_id=283441",
    "origin": "https://seller.ozon.ru",
    "priority": "u=1, i",
    "referer": "https://seller.ozon.ru/app/fbo-stocks/stocks-management/reports",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "x-o3-app-name": "seller-ui",
    "x-o3-company-id": "283441",
    "x-o3-language": "ru",
    "x-o3-page-type": "fbo-stocks"
}

# Тело запроса
payload = {
    "warehouseType": "All"
}

# Отправляем запрос
response = requests.post(url, headers=headers, json=payload)

# Проверяем ответ
if response.status_code == 200:
    # Сохраняем файл
    with open(f"/home/andrey/Песочница/ozon_logistics_2/ОСТАТКИ СЮДА/report-{formatted_date}.xlsx", "wb") as file:
        file.write(response.content)
    print(f"Файл успешно скачан и сохранён в '/Песочница/ozon_logistics_2/ОСТАТКИ СЮДА/report-{formatted_date}.xlsx'")
else:
    print(f"Ошибка при выполнении запроса: {response.status_code}")
    print(f"Ответ сервера: {response.text}")

