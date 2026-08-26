import requests
import json
from riotwatcher import LolWatcher

# ========== 1. НАСТРОЙКА ==========
API_KEY = 'RGAPI-66e5071f-83da-44b2-bbbb-03cb81d0426d'
REGION = 'ru'
MY_PUUID = 'NjWjO5S0uMAkyL-FAtkkee1l8yi5jCw2xZt-KphWexEjxnhqlyiNOjcoapgnpaUWYx7nBPc-OvO-Wg'

watcher = LolWatcher(API_KEY)

# ========== 2. ФУНКЦИИ ДЛЯ ЗАГРУЗКИ ДАННЫХ ==========
def get_items_data():
    version = "14.10.1"
    url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/ru_RU/item.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print("❌ Не удалось загрузить данные предметов")
        return {}

def get_runes_data():
    version = "14.10.1"
    url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/ru_RU/runesReforged.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Не удалось загрузить данные рун")
        return []

items_data = get_items_data()
runes_data = get_runes_data()

# ========== 3. ФУНКЦИИ РАСШИФРОВКИ ==========
def get_item_name(item_id):
    item_id_str = str(item_id)
    if item_id_str in items_data:
        return items_data[item_id_str]['name']
    return "Неизвестный предмет"

def get_rune_name(rune_id):
    for tree in runes_data:
        for slot in tree.get('slots', []):
            for rune in slot.get('runes', []):
                if rune['id'] == rune_id:
                    return rune['name']
        if tree.get('id') == rune_id:
            return tree.get('name', 'Неизвестная руна')
    return f"Руна #{rune_id}"

# ========== 4. ПОЛУЧАЕМ МАТЧИ ==========
print("📊 Загружаем матчи...")
match_ids = watcher.match.matchlist_by_puuid(REGION, MY_PUUID, count=10)
print(f"Найдено матчей: {len(match_ids)}\n")

# ========== 5. АНАЛИЗИРУЕМ КАЖДЫЙ МАТЧ ==========
for match_id in match_ids:
    print(f"🔍 Матч {match_id}")
    match = watcher.match.by_id(REGION, match_id)
    
    # Ищем себя в матче
    for participant in match['info']['participants']:
        if participant['puuid'] == MY_PUUID:
            champion = participant['championName']
            kills = participant['kills']
            deaths = participant['deaths']
            assists = participant['assists']
            win = "Победа ✅" if participant['win'] else "Поражение ❌"
            
            print(f"  Чемпион: {champion} ({win})")
            print(f"  KDA: {kills}/{deaths}/{assists}")
            
            # Расшифровываем предметы
            print("  Предметы:")
            for i in range(0, 6):
                item_id = participant.get(f'item{i}')
                if item_id and item_id > 0:
                    item_name = get_item_name(item_id)
                    print(f"    - {item_name} (ID: {item_id})")
            
            # Расшифровываем руны
            print("  Руны:")
            perks = participant.get('perks', {}).get('styles', [])
            for style in perks:
                for selection in style.get('selections', []):
                    rune_id = selection.get('perk')
                    if rune_id:
                        rune_name = get_rune_name(rune_id)
                        print(f"    - {rune_name}")
            
            print()  # Пустая строка между матчами
            break  # Переходим к следующему матчу