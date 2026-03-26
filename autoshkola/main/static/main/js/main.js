document.addEventListener('DOMContentLoaded', function () {

    // =================================================================
    // СЕТЕВЫЕ ЧАСТИЦЫ (NETWORK PARTICLES)
    // =================================================================
    const canvas = document.createElement('canvas');
    canvas.id = 'networkCanvas';
    document.body.prepend(canvas);
    const ctx = canvas.getContext('2d');

    let W, H;
    let particles = [];
    let mouse = { x: null, y: null, radius: 150 };
    const PARTICLE_COUNT_BASE = 80;
    const CONNECTION_DISTANCE = 180;
    const MOUSE_CONNECTION_DISTANCE = 200;
    const PARTICLE_SPEED = 0.3;

    function resize() {
        W = canvas.width = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    // Отслеживание мыши
    window.addEventListener('mousemove', function (e) {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });
    window.addEventListener('mouseleave', function () {
        mouse.x = null;
        mouse.y = null;
    });

    class Particle {
        constructor() {
            this.x = Math.random() * W;
            this.y = Math.random() * H;
            this.vx = (Math.random() - 0.5) * PARTICLE_SPEED * 2;
            this.vy = (Math.random() - 0.5) * PARTICLE_SPEED * 2;
            this.radius = Math.random() * 1.5 + 0.5;
            this.baseAlpha = Math.random() * 0.3 + 0.1;
            this.alpha = this.baseAlpha;
            this.pulseSpeed = Math.random() * 0.02 + 0.005;
            this.pulsePhase = Math.random() * Math.PI * 2;
        }

        update(time) {
            this.x += this.vx;
            this.y += this.vy;

            // Отскок от краёв
            if (this.x < 0 || this.x > W) this.vx *= -1;
            if (this.y < 0 || this.y > H) this.vy *= -1;

            // Удержание в границах
            this.x = Math.max(0, Math.min(W, this.x));
            this.y = Math.max(0, Math.min(H, this.y));

            // Пульсация
            this.alpha = this.baseAlpha + Math.sin(time * this.pulseSpeed + this.pulsePhase) * 0.1;

            // Притяжение к мыши
            if (mouse.x !== null && mouse.y !== null) {
                const dx = mouse.x - this.x;
                const dy = mouse.y - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < MOUSE_CONNECTION_DISTANCE) {
                    const force = (MOUSE_CONNECTION_DISTANCE - dist) / MOUSE_CONNECTION_DISTANCE * 0.008;
                    this.vx += dx * force;
                    this.vy += dy * force;
                    this.alpha = Math.min(this.alpha + 0.15, 0.6);
                }
            }

            // Ограничение скорости
            const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
            if (speed > PARTICLE_SPEED * 3) {
                this.vx = (this.vx / speed) * PARTICLE_SPEED * 3;
                this.vy = (this.vy / speed) * PARTICLE_SPEED * 3;
            }
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(255, 255, 255, ' + this.alpha + ')';
            ctx.fill();

            // Маленький ореол
            if (this.alpha > 0.2) {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius + 2, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(255, 255, 255, ' + (this.alpha * 0.15) + ')';
                ctx.fill();
            }
        }
    }

    function initParticles() {
        particles = [];
        // Адаптивное количество частиц
        const count = Math.min(
            PARTICLE_COUNT_BASE,
            Math.floor((W * H) / 15000)
        );
        for (let i = 0; i < count; i++) {
            particles.push(new Particle());
        }
    }
    initParticles();
    window.addEventListener('resize', initParticles);

    function drawConnections() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < CONNECTION_DISTANCE) {
                    const opacity = (1 - dist / CONNECTION_DISTANCE) * 0.15;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = 'rgba(255, 255, 255, ' + opacity + ')';
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }

            // Линии к мыши
            if (mouse.x !== null && mouse.y !== null) {
                const dx = particles[i].x - mouse.x;
                const dy = particles[i].y - mouse.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < MOUSE_CONNECTION_DISTANCE) {
                    const opacity = (1 - dist / MOUSE_CONNECTION_DISTANCE) * 0.25;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(mouse.x, mouse.y);
                    ctx.strokeStyle = 'rgba(255, 255, 255, ' + opacity + ')';
                    ctx.lineWidth = 0.8;
                    ctx.stroke();
                }
            }
        }
    }

    let animTime = 0;
    function animateNetwork() {
        ctx.clearRect(0, 0, W, H);
        animTime++;

        for (const p of particles) {
            p.update(animTime);
            p.draw();
        }

        drawConnections();

        // Рисуем курсор-точку
        if (mouse.x !== null && mouse.y !== null) {
            ctx.beginPath();
            ctx.arc(mouse.x, mouse.y, 3, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
            ctx.fill();

            ctx.beginPath();
            ctx.arc(mouse.x, mouse.y, 8, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(255, 255, 255, 0.03)';
            ctx.fill();
        }

        requestAnimationFrame(animateNetwork);
    }
    animateNetwork();


    // =================================================================
    // НЕОНОВАЯ ЛИНИЯ СВЕРХУ
    // =================================================================
    const neonLine = document.createElement('div');
    neonLine.className = 'neon-line-top';
    document.body.prepend(neonLine);


    // =================================================================
    // МОБИЛЬНОЕ МЕНЮ
    // =================================================================
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

    document.querySelectorAll('.nav-list a').forEach(function (link) {
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


    // =================================================================
    // АНИМАЦИИ ПОЯВЛЕНИЯ ПРИ СКРОЛЛЕ
    // =================================================================
    const animations = ['animate-in', 'animate-slide-right', 'animate-slide-left', 'animate-scale'];

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                // Случайная анимация
                const anim = animations[Math.floor(Math.random() * animations.length)];
                entry.target.classList.add(anim);
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
    ).forEach(function (el, i) {
        el.style.opacity = '0';
        el.style.animationDelay = Math.min(i * 0.06, 0.6) + 's';
        observer.observe(el);
    });


    // =================================================================
    // МОДАЛЬНОЕ ОКНО ГАЛЕРЕИ
    // =================================================================
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
        document.querySelectorAll('.gallery-item img').forEach(function (img) {
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


    // =================================================================
    // ЭФФЕКТ ХЕДЕРА
    // =================================================================
    const header = document.querySelector('.header');
    let ticking = false;

    window.addEventListener('scroll', function () {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(function () {
            if (window.pageYOffset > 60) {
                header.style.background = 'rgba(0,0,0,0.95)';
                header.style.boxShadow = '0 5px 30px rgba(0,0,0,0.6), 0 0 1px rgba(255,255,255,0.03)';
            } else {
                header.style.background = 'rgba(0,0,0,0.85)';
                header.style.boxShadow = '';
            }
            ticking = false;
        });
    });


    // =================================================================
    // МЫШИНЫЙ СВЕТ НА КАРТОЧКАХ
    // =================================================================
    document.querySelectorAll('.glass-card').forEach(function (card) {
        card.addEventListener('mousemove', function (e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            card.style.background =
                'radial-gradient(600px circle at ' + x + 'px ' + y + 'px, ' +
                'rgba(255,255,255,0.025) 0%, rgba(10,10,10,0.9) 100%)';
        });

        card.addEventListener('mouseleave', function () {
            card.style.background = 'rgba(10,10,10,0.9)';
        });
    });


    // =================================================================
    // МЕРЦАНИЕ НЕОНОВОЙ ЛИНИИ
    // =================================================================
    setInterval(function () {
        if (!neonLine) return;
        neonLine.style.opacity = (0.4 + Math.random() * 0.6).toString();
    }, 2000 + Math.random() * 3000);

});