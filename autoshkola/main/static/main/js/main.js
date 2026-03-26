document.addEventListener('DOMContentLoaded', function () {

    // ——— Неоновая линия сверху ———
    const neonLine = document.createElement('div');
    neonLine.className = 'neon-line-top';
    document.body.prepend(neonLine);

    // ——— Мобильное меню ———
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav');

    if (menuToggle) {
        menuToggle.addEventListener('click', function () {
            nav.classList.toggle('open');
            const icon = this.querySelector('span');
            if (nav.classList.contains('open')) {
                icon.textContent = '✕';
                this.style.boxShadow = '0 0 12px rgba(255,255,255,0.1)';
                this.style.borderColor = 'rgba(255,255,255,0.2)';
            } else {
                icon.textContent = '☰';
                this.style.boxShadow = '';
                this.style.borderColor = '';
            }
        });
    }

    // Закрытие меню при клике на ссылку
    document.querySelectorAll('.nav-list a').forEach(link => {
        link.addEventListener('click', function () {
            if (window.innerWidth <= 768 && nav) {
                nav.classList.remove('open');
                if (menuToggle) {
                    menuToggle.querySelector('span').textContent = '☰';
                    menuToggle.style.boxShadow = '';
                    menuToggle.style.borderColor = '';
                }
            }
        });
    });

    // ——— Анимация появления при скролле ———
    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.07,
        rootMargin: '0px 0px -50px 0px'
    });

    document.querySelectorAll(
        '.glass-card, .info-item, .gallery-item, .schedule-item, ' +
        '.exam-item, .doc-item, .consent-option, .group-card'
    ).forEach((el, i) => {
        el.style.opacity = '0';
        el.style.animationDelay = Math.min(i * 0.05, 0.5) + 's';
        observer.observe(el);
    });

    // ——— Модальное окно для галереи ———
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const modalClose = document.querySelector('.modal-close');

    function openModal(src) {
        if (!modal) return;
        modal.classList.add('active');
        modalImg.src = src;
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        if (!modal) return;
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (modal) {
        document.querySelectorAll('.gallery-item img').forEach(img => {
            img.addEventListener('click', function () {
                openModal(this.src);
            });
        });

        modal.addEventListener('click', function (e) {
            if (e.target === modal) closeModal();
        });

        if (modalClose) modalClose.addEventListener('click', closeModal);

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') closeModal();
        });
    }

    // ——— Хедер при скролле ———
    const header = document.querySelector('.header');
    let ticking = false;

    window.addEventListener('scroll', function () {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(function () {
            if (window.pageYOffset > 60) {
                header.style.background = 'rgba(0, 0, 0, 0.95)';
                header.style.boxShadow = '0 5px 30px rgba(0,0,0,0.6), 0 0 1px rgba(255,255,255,0.03)';
            } else {
                header.style.background = 'rgba(0, 0, 0, 0.85)';
                header.style.boxShadow = '';
            }
            ticking = false;
        });
    });

    // ——— Мышиный след белого свечения на карточках ———
    document.querySelectorAll('.glass-card').forEach(card => {
        card.addEventListener('mousemove', function (e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            card.style.background =
                'radial-gradient(500px circle at ' + x + 'px ' + y + 'px, ' +
                'rgba(255,255,255,0.02) 0%, rgba(10,10,10,0.9) 100%)';
        });

        card.addEventListener('mouseleave', function () {
            card.style.background = 'rgba(10, 10, 10, 0.9)';
        });
    });

    // ——— Мерцание неоновой линии ———
    let flickerInterval = setInterval(function () {
        if (!neonLine) return;
        const base = 0.5;
        const rand = Math.random() * 0.5;
        neonLine.style.opacity = (base + rand).toString();
    }, 2500 + Math.random() * 2000);
});