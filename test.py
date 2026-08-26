from src.api.riot_client import watcher
from src.parsers.match_parser import parse_match
from config import REGION, MY_PUUID

# Получаем один матч
match_ids = watcher.match.matchlist_by_puuid(REGION, MY_PUUID, count=1)
match = watcher.match.by_id(REGION, match_ids[0])

# Расшифровываем
result = parse_match(match, MY_PUUID)

if result:
    print(f"✅ Чемпион: {result['champion']}")
    print(f"KDA: {result['kills']}/{result['deaths']}/{result['assists']}")
    print(f"Победа: {result['win']}")
    print("\nПредметы:")
    for item in result['items']:
        print(f"  - {item['name']} (ID: {item['id']})")
    print("\nРуны:")
    for rune in result['runes']:
        print(f"  - {rune['name']} (ID: {rune['id']})")
else:
    print("❌ Не найден игрок в матче")