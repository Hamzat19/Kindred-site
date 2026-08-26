import requests
from src.api.data_dragon import VERSION


url = f"https://ddragon.leagueoflegends.com/cdn/{VERSION}/data/ru_RU/runesReforged.json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()  # ← Вот твой файл!
    print("✅ Файл загружен")
else:
    print(f"❌ Ошибка: {response.status_code}")