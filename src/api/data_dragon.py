import requests  # Библиотека для отправки HTTP-запросов (скачивания файлов из интернета)
import json      # Библиотека для работы с JSON (превращает текст в словари Python)
import os        # Библиотека для работы с файловой системой (папки, файлы)

# 1. СОЗДАЁМ ПАПКУ ДЛЯ КЕША (сохранённых копий)
# exist_ok=True значит: "если папка уже есть, не ругайся"
os.makedirs("data/static", exist_ok=True)

# 2. ФУНКЦИЯ ПОЛУЧЕНИЯ АКТУАЛЬНОЙ ВЕРСИИ
def get_latest_version():
    """
    Спрашивает у Data Dragon: "Какая сейчас актуальная версия игры?"
    Возвращает: строку с номером версии, например "14.10.1"
    """
    try:
        # Ссылка на список всех версий
        url = "https://ddragon.leagueoflegends.com/api/versions.json"
        # Получаем ответ от сервера
        response = requests.get(url)
        # Если ответ успешный (код 200)
        if response.status_code == 200:
            # Превращаем JSON в список Python и берём первую (самую новую) версию
            versions = response.json()
            return versions[0]
        else:
            # Если ошибка - возвращаем запасной вариант, чтобы код не сломался
            print(f"⚠️ Ошибка получения версии: {response.status_code}")
            return "16.14.1"
    except Exception as e:
        # Если интернет отключён или сайт недоступен
        print(f"⚠️ Ошибка соединения: {e}")
        return "16.14.1"

# 3. ПОЛУЧАЕМ АКТУАЛЬНУЮ ВЕРСИЮ ПРЯМО СЕЙЧАС
# Эта строка выполняется при запуске файла
VERSION = get_latest_version()
print(f"🔍 Актуальная версия игры: {VERSION}")

# 4. ФУНКЦИЯ ЗАГРУЗКИ ПРЕДМЕТОВ
def get_items_data():
    """
    Загружает данные о предметах.
    Если они уже есть на диске - берёт оттуда.
    Если нет - скачивает с Data Dragon и сохраняет на диск.
    Возвращает: словарь с предметами (ID предмета → данные о нём)
    """
    # Путь к файлу кеша
    cache_file = "data/static/items.json"
    
    # 1. ПРОВЕРЯЕМ: есть ли файл с предметами на диске?
    if os.path.exists(cache_file):
        # Есть! Открываем файл, читаем и возвращаем данные
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # 2. ФАЙЛА НЕТ: скачиваем из интернета
    # Формируем ссылку с актуальной версией
    url = f"http://ddragon.leagueoflegends.com/cdn/{VERSION}/data/ru_RU/item.json"
    
    # Отправляем запрос на сервер
    response = requests.get(url)
    
    # Проверяем, что всё хорошо (код 200 = ОК)
    if response.status_code == 200:
        # Берём из ответа JSON и забираем только часть с данными (ключ 'data')
        data = response.json()['data']
        
        # Сохраняем этот словарь в файл, чтобы в следующий раз не качать
        with open(cache_file, 'w', encoding='utf-8') as f:
            # ensure_ascii=False - чтобы русские буквы не превращались в \uXXXX
            # indent=2 - чтобы файл был красиво отформатирован
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Возвращаем скачанные данные
        return data
    else:
        # Если что-то пошло не так
        print("❌ Ошибка загрузки предметов")
        return {}  # Возвращаем пустой словарь, чтобы код не упал

# 5. ФУНКЦИЯ ЗАГРУЗКИ РУН (аналогично предметам)
def get_runes_data():
    """
    Загружает данные о рунах.
    Если есть на диске - берёт оттуда.
    Если нет - скачивает с Data Dragon и сохраняет.
    Возвращает: список с деревьями рун.
    """
    cache_file = "data/static/runes.json"
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    url = f"http://ddragon.leagueoflegends.com/cdn/{VERSION}/data/ru_RU/runesReforged.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return data
    else:
        print("❌ Ошибка загрузки рун")
        return []

# 6. ЗАГРУЖАЕМ ДАННЫЕ (ЭТО ВЫПОЛНЯЕТСЯ СРАЗУ ПРИ ЗАПУСКЕ)
# Переменные items_data и runes_data будут доступны во всём файле
items_data = get_items_data()
runes_data = get_runes_data()

# 7. ФУНКЦИЯ ПОИСКА НАЗВАНИЯ ПРЕДМЕТА ПО ID
def get_item_name(item_id):
    """
    Принимает: ID предмета (например, 2055)
    Возвращает: название предмета (например, "Тотем контроля")
    """
    # Превращаем число в строку, так как в словаре ключи - строки
    item_id_str = str(item_id)
    
    # Если предмет есть в нашем словаре - возвращаем его название
    if item_id_str in items_data:
        return items_data[item_id_str]['name']
    
    # Если предмет не найден
    return "Неизвестный предмет"

# 8. ФУНКЦИЯ ПОИСКА НАЗВАНИЯ РУНЫ ПО ID
def get_rune_name(rune_id):
    """
    Принимает: ID руны (например, 8005)
    Возвращает: название руны (например, "Смертельный темп")
    """
    # Структура рун: дерево → слот → руна
    # Проходим по всем деревьям
    for tree in runes_data:
        # Проходим по всем слотам в дереве
        for slot in tree.get('slots', []):
            # Проходим по всем рунам в слоте
            for rune in slot.get('runes', []):
                if rune['id'] == rune_id:
                    return rune['name']
        # Проверяем: может быть, сам ID руны принадлежит дереву?
        if tree.get('id') == rune_id:
            return tree.get('name', 'Неизвестная руна')
    
    # Если руна не найдена
    return f"Руна #{rune_id}"

def get_rune_icon(rune_id):
    for tree in runes_data:
        for slot in tree.get('slots', []):
            for rune in slot.get('runes', []):
                if rune.get('id', 0) == rune_id:
                    icon_path = rune.get('icon', "")
                    if icon_path: 
                        return  f"https://ddragon.leagueoflegends.com/cdn/{VERSION}/img/{icon_path}"
    return ""

def get_item_icon(item_id):
    item_id_str= str(item_id)
    if item_id_str in items_data:
        return f"https://ddragon.leagueoflegends.com/cdn/{VERSION}/img/item/{item_id}.png"
    return ""

