
        const abilities = {
    p: {
        name: 'P - Знак Киндред',
        description: 'По нажатию на иконку чемпиона на специальной панели, овечка помечает чемпиона меткой в течение 8 секунд, при участии в убийстве помеченного врага, Киндред забирают метку. Волк ставит метки на лесных монстров не своего леса. Метки усиливают базовые умения и увеличивают дальность автоатак. На 4 метке дальность увеличивается на 75 единиц, каждые последующие 3 - на 25.',
        video: '/static/videos/Passive Kindred.mp4'
    },
    q: {
        name: 'Q — Танец стрел',
        description: 'Овечка совершает рывок по направлению курсора, выпуская по одной стреле на каждого ближайшого врага (не более 3 стрел в сумме). Рывок позволяет перегрыгивать через стены. Помимо этого Киндред получают прибавку к скорости атаки.',
        video: '/static/videos/Kindred Q.mp4'
    },
    w: {
        name: 'W — Волчье бешенство',
        description: 'Волк отдаляется от Овечки и создает вокруг себя зону, в которой самостоятельно атакует врагов, нанося магический, процентный урон от текущего запаса здоровья. Во время действие умения перезарядка Q танца стрел уменьшается. Волк дает обзор. ',
        video: '/static/videos/Kindred W.mp4'
    },
    e: {
        name: 'E — Всепоглощающий ужас',
        description: 'Овечка замедляет врага и накладывает метку, при 3-й атаке Волк наносит физический урон в проценте от недостающего здоровья.',
        video: '/static/videos/Kindred E.mp4'
    },
    r: {
        name: 'R — Милость Овечки',
        description: 'Создает зону, где ни у кого не может упасть здоровье ниже 10%, а после окончания действия все получают исцеление. Умение работает и на союзников, и на врагов, и на миньнов, и даже на лесных монстров',
        video: '/static/videos/Kindred R.mp4'
    }
};

document.querySelectorAll('.ability-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        // Убираем активный класс у всех кнопок
        document.querySelectorAll('.ability-btn').forEach(b => b.classList.remove('active'));
        // Добавляем текущей кнопке
        this.classList.add('active');
        
        const key = this.dataset.ability;
        const data = abilities[key];
        
        // Меняем название и описание
        document.getElementById('ability-name').textContent = data.name;
        document.getElementById('ability-description').textContent = data.description;
        
        // Меняем видео
        const videoSource = document.getElementById('video-source');
        videoSource.src = data.video;
        const video = videoSource.parentElement;
        video.load(); // Перезагружаем видео
        video.play(); // Автоматически запускаем
    });
});


document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, есть ли модальное окно на странице
    const modal = document.getElementById('imageModal');
    if (!modal) return; // Если нет — выходим, ошибок не будет

    const closeBtn = document.getElementById('modalClose');

    // Открыть модалку
    window.openModal = function(imgSrc, captionText) {
        const modalImg = document.getElementById('modalImg');
        const caption = document.getElementById('modalCaption');
        modal.style.display = "flex";
        modalImg.src = imgSrc;
        caption.textContent = captionText;
        document.body.style.overflow = "hidden";
    };

    // Закрыть модалку
    window.closeModal = function() {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    };

    // Закрытие по крестику
    if (closeBtn) {
        closeBtn.addEventListener('click', window.closeModal);
    }

    // Закрытие по клику вне картинки
    modal.addEventListener('click', function(event) {
        if (event.target === this) {
            window.closeModal();
        }
    });

    // Закрытие по ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === "Escape") {
            window.closeModal();
        }
    });
});