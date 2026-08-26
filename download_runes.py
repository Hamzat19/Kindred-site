import requests
import os
from src.api.data_dragon import get_rune_icon

runes = [
    {'id': 8005, 'name': 'Решительное наступление'},
    {'id': 9111, 'name': 'Триумф'},
    {'id': 9104, 'name': 'Легенда: рвение'},
    {'id': 8014, 'name': 'Удар милосердия'},
    {'id': 8143, 'name': 'Внезапный удар'},
    {'id': 8106, 'name': 'Абсолютный охотник'},
]

os.makedirs("static/images/runes", exist_ok=True)

for rune in runes:
    url = get_rune_icon(rune['id'])
    if not url:
        print(f"❌ Нет ссылки для {rune['name']}")
        continue
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_path = f"static/images/runes/{rune['id']}.png"
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ {rune['name']} сохранён")
        else:
            print(f"❌ Ошибка {rune['name']}: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка {rune['name']}: {e}")