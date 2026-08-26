import requests

API_KEY = 'RGAPI-66e5071f-83da-44b2-bbbb-03cb81d0426d'  # Вставьте свой ключ

# Правильный эндпоинт для поиска по Riot ID
url = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/Выйди%20из%20ульты/метка"
headers = {"X-Riot-Token": API_KEY}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    puuid = data['puuid']
    print(f"✅ Ваш PUUID: {puuid}")
    print(f"Имя: {data['gameName']}")
    print(f"Тег: {data['tagLine']}")
else:
    print(f"❌ Ошибка: {response.status_code}")
    print(response.text)