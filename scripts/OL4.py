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
    "cookie": "__Secure-ab-group=26; rfuid=NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwtNjkwNDUzMjYwLC0xLDE2NzY3NzA5OTcsVzNzaWJtRnRaU0k2SWxCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxbElGQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMXBkVzBnVUVSR0lGWnBaWGRsY2lJc0ltUmxjMk55YVhCMGFXOXVJam9pVUc5eWRHRmliR1VnUkc5amRXMWxiblFnUm05eWJXRjBJaXdpYldsdFpWUjVjR1Z6SWpwYmV5SjBlWEJsSWpvaVlYQndiR2xqWVhScGIyNHZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlN4N0luUjVjR1VpT2lKMFpYaDBMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4xZGZTeDdJbTVoYldVaU9pSk5hV055YjNOdlpuUWdSV1JuWlNCUVJFWWdWbWxsZDJWeUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lKUWIzSjBZV0pzWlNCRWIyTjFiV1Z1ZENCR2IzSnRZWFFpTENKdGFXMWxWSGx3WlhNaU9sdDdJblI1Y0dVaU9pSmhjSEJzYVdOaGRHbHZiaTl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOUxIc2lkSGx3WlNJNkluUmxlSFF2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZWMTlMSHNpYm1GdFpTSTZJbGRsWWt0cGRDQmlkV2xzZEMxcGJpQlFSRVlpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgxZCxXeUp5ZFMxU1ZTSmQsMCwxLDAsMjQsMjM3NDE1OTMwLDgsMjI3MTI2NTIwLDAsMSwwLC00OTEyNzU1MjMsUjI5dloyeGxJRWx1WXk0Z1RtVjBjMk5oY0dVZ1IyVmphMjhnVEdsdWRYZ2dlRGcyWHpZMElEVXVNQ0FvV0RFeE95Qk1hVzUxZUNCNE9EWmZOalFwSUVGd2NHeGxWMlZpUzJsMEx6VXpOeTR6TmlBb1MwaFVUVXdzSUd4cGEyVWdSMlZqYTI4cElFTm9jbTl0WlM4eE16SXVNQzR3TGpBZ1UyRm1ZWEpwTHpVek55NHpOaUF5TURBek1ERXdOeUJOYjNwcGJHeGgsZXlKamFISnZiV1VpT25zaVlYQndJanA3SW1selNXNXpkR0ZzYkdWa0lqcG1ZV3h6WlN3aVNXNXpkR0ZzYkZOMFlYUmxJanA3SWtSSlUwRkNURVZFSWpvaVpHbHpZV0pzWldRaUxDSkpUbE5VUVV4TVJVUWlPaUpwYm5OMFlXeHNaV1FpTENKT1QxUmZTVTVUVkVGTVRFVkVJam9pYm05MFgybHVjM1JoYkd4bFpDSjlMQ0pTZFc1dWFXNW5VM1JoZEdVaU9uc2lRMEZPVGs5VVgxSlZUaUk2SW1OaGJtNXZkRjl5ZFc0aUxDSlNSVUZFV1Y5VVQxOVNWVTRpT2lKeVpXRmtlVjkwYjE5eWRXNGlMQ0pTVlU1T1NVNUhJam9pY25WdWJtbHVaeUo5ZlgxOSw2NSwtMTI4NTU1MTMsMSwxLC0xLDE2OTk5NTQ4ODcsMTY5OTk1NDg4NywzMzYwMzkxNzUsNA==; x-o3-language=ru; TS0121feed=0187c00a184ce46fe9d64b8ab054ac27abd3411e20a42db5c809a9286f01753202e51813eaa7a71baaa8806238b4093c47469ba0ed; __Secure-user-id=167665561; is_adult_confirmed=; is_alco_adult_confirmed=; abt_data=7.btmQXtBFVmybvM1MbiTpht9GvwhXvlrljZzCJiWKiArGcDcAJzvREYUKZCBd5ynDULvL1nfU8OK1_gxqeV2s252ycfTygK7h4Rsm5e2598Shoysfk_VM5rakNV1tavqnVMpAeDtPZsnVpYG7pz03k5HlWtUYZ7knpfY5IpiWmELOtXBMOCZabPedWyv9ddgxznNK0CHL4CuCD4B9SXBqyrwRcTy8huIb_hwpczuhitf2nktA1ljhsf8PVg9H9WukhyQ_Lum2jFsRJKqxTcnGsQ3CIDpShPcE-R8G_KPPiN-wfcr5FNOMqaoD9S50Ky_63Uc9UT48xQnPhtPTtHHyZEcNRJ3a02ez_uz7tytvP1D--OUffdqZRsiQGtCHiReCvf6T8ibs81zoWnTNSdNdi6xBYDGKkta8CZBFzIz2YPgrxGvXYrFY8xZZxLH9-dLY6UEfUly3LvyORd0NftCr; TS018529d3=0187c00a1821c41c835846c248588088ee4be272c46407087abf10f8833aeb12c1c1bd0c30ed209ba6f1ca6e1bf59f486f0bc9c6b6; bacntid=4421294; sc_company_id=283441; __Secure-ETC=65613690001d26000871e3dedce9cdc6; xcid=bbc02cca8af5249c0826733c5ca78aed; __Secure-ext_xcid=bbc02cca8af5249c0826733c5ca78aed; __Secure-access-token=7.167665561.-Z48TVeeQ_CZEaOl3E809w.26.AfLEJYvsQITBR3dqEOcBKGwUGLSP6oPwhsYyxOCd2kDuuV8YRh4SrkkLZ5ODPhZAwyRttTzVKBavC1YDLQr7q64.20240617094506.20250122104114.qIip8OyQJy3D7aehW_B7B5_xK0prYubXLp5mm9qM0S8.1579aa625ddd8f747; __Secure-refresh-token=7.167665561.-Z48TVeeQ_CZEaOl3E809w.26.AfLEJYvsQITBR3dqEOcBKGwUGLSP6oPwhsYyxOCd2kDuuV8YRh4SrkkLZ5ODPhZAwyRttTzVKBavC1YDLQr7q64.20240617094506.20250122104114.CMcuIsxxjRJrN1QIQ9fPpkMg9-TnOGz7xUGh3ECYEZc.1b5de83db278d00f3; TS0149423d=0187c00a18b913e2823baeaf45dd2e6cb3c252b17b25969ffaeee4a9989e8dacad807d15819bf80c6ee96d33270c4d3f1109ac7fe4",
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

