from flask import Flask, render_template
from src.api.data_dragon import get_rune_icon, get_item_icon, VERSION

app = Flask(__name__)



@app.context_processor
def utility_processor():
    return {
        'ddragon_version': VERSION,  

    }

@app.route('/builds')
def builds():
    return render_template('builds.html')

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')


@app.route('/runes')
def runes():
    return render_template('runes.html')

@app.route('/matchups')
def matchups():
    return render_template('matchups.html')
@app.route('/')
def index():
    print("🚀 Функция index() запущена!") 
    # Данные о рунах (ID, название, иконка)
    runes = [
        {'id': 8005, 'name': 'Решительное наступление', 'tree': 'primary'},
        {'id': 9111, 'name': 'Триумф', 'tree': 'primary'},
        {'id': 9104, 'name': 'Легенда: рвение', 'tree': 'primary'},
        {'id': 8014, 'name': 'Удар милосердия', 'tree': 'primary'},
        {'id': 8143, 'name': 'Внезапный удар', 'tree': 'secondary'},
        {'id': 8106, 'name': 'Абсолютный охотник', 'tree': 'secondary'},
    ]
    
    # Данные о предметах (ID, название)
    items = [
        {'id': 3143, 'name': 'Знамение Рандуина'},
        {'id': 3078, 'name': 'Тройственный Союз'},
        {'id': 3047, 'name': 'Бронированные сапоги'},
        {'id': 2523, 'name': 'Хекс-прицел С44'},
        {'id': 1018, 'name': 'Плащ ловкости'},
        {'id': 3340, 'name': 'Скрытый тотем'},
    ]

    for rune in runes:
        rune['icon'] = f"/static/images/runes/{rune['id']}.png"
        print(f"✅ {rune['name']}: {rune['icon']}")


    

    return render_template(
        'guide.html',
        runes=runes,
        items=items,
        version=VERSION
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)