from src.api.data_dragon import get_item_name, get_rune_name


def parse_match(match_data, puuid):
    for participant in match_data['info']['participants']:
        if puuid == participant['puuid']: # проверяем соответствие нужного puuid

# берем слоты
            items = []
            for i in range(0,7):
                item_id = participant.get(f'item{i}')
                if item_id and item_id > 0:
                    items.append({'id': item_id, 'name':get_item_name(item_id)})

# берем руны
            runes = []
            for style in participant.get('perks', {}).get('styles', []):
                 for selection in style.get('selections', []):
                    rune_id = selection.get('perk')
                    if rune_id:
                        runes.append({'id': rune_id, 'name': get_rune_name(rune_id)})

            return {
                'champion': participant['championName'],
                'win': participant['win'],
                'kills': participant['kills'],
                'deaths': participant['deaths'],
                'assists': participant['assists'],
                'runes': runes,
                'items': items
            }

    return None



