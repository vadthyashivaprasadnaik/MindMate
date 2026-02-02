document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-btn');
    const landingPage = document.getElementById('landing-page');
    const mainDashboard = document.getElementById('main-dashboard');
    const thunderFlash = document.getElementById('thunder-flash');

    // --- 1. LANDING TO DASHBOARD TRANSITION (ROBUST) ---
    startBtn.addEventListener('click', () => {
        console.log("Start Chat Clicked");

        // Safety Fallback: Ensure GSAP exists, otherwise do manual transition
        if (typeof gsap === 'undefined') {
            landingPage.style.display = 'none';
            mainDashboard.classList.add('active');
            mainDashboard.style.opacity = '1';
            mainDashboard.style.transform = 'rotateY(0deg)';
            return;
        }

        try {
            // A. Flash effect
            gsap.to(thunderFlash, {
                opacity: 1,
                duration: 0.1,
                yoyo: true,
                repeat: 3,
                onComplete: () => {
                    gsap.to(thunderFlash, { opacity: 0, duration: 0.5 });
                }
            });

            // B. Rotate and Reveal
            gsap.to(landingPage, {
                scale: 1.5,
                opacity: 0,
                rotation: 10,
                duration: 1,
                ease: "power2.in",
                onComplete: () => {
                    landingPage.style.display = 'none'; // CRITICAL: Must hide
                    // Double check in case GSAP fails weirdly
                    setTimeout(() => { if (landingPage.style.display !== 'none') landingPage.style.display = 'none'; }, 50);
                }
            });

            // C. Show Dashboard
            // Start showing slightly earlier than 600ms to ensure overlap feels continuous
            setTimeout(() => {
                mainDashboard.classList.add('active'); // CSS handles rotateY(0)
                // Force styles just in case CSS class fails or override issues
                mainDashboard.style.opacity = '1';
                mainDashboard.style.pointerEvents = 'auto';

                // Trigger a lightning strike on canvas
                if (window.triggerLightning) window.triggerLightning();

            }, 600);

        } catch (e) {
            console.error("GSAP Animation Failed:", e);
            // Fallback if error
            landingPage.style.display = 'none';
            mainDashboard.classList.add('active');
        }
    });

    // --- 2. PARTICLE & LIGHTNING SYSTEM ---
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let width, height;
    let particles = [];

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
    }

    window.addEventListener('resize', resize);
    resize();

    // Lightning Function
    window.triggerLightning = function () {
        ctx.strokeStyle = "rgba(255, 255, 255, 0.8)";
        ctx.lineWidth = 2;
        ctx.shadowBlur = 20;
        ctx.shadowColor = "#00f3ff";

        let x = Math.random() * width;
        let y = 0;

        ctx.beginPath();
        ctx.moveTo(x, y);

        while (y < height) {
            let nextX = x + (Math.random() - 0.5) * 100; // zigzag
            let nextY = y + Math.random() * 50 + 20;
            ctx.lineTo(nextX, nextY);
            x = nextX;
            y = nextY;
        }
        ctx.stroke();

        // Clear quickly
        setTimeout(() => {
            // We set a flag so animate loop can handle visual clearing or effects
            window.flashActive = true;
            setTimeout(() => window.flashActive = false, 100);
        }, 50);
    };

    // Auto lightning
    setInterval(() => {
        if (Math.random() > 0.9) window.triggerLightning();
    }, 5000);

    // Particle Logic
    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * 1.5;
            this.vy = (Math.random() - 0.5) * 1.5;
            this.size = Math.random() * 2 + 1;
            this.color = `rgba(${Math.random() > 0.5 ? '0, 243, 255' : '188, 19, 254'}, ${Math.random() * 0.8 + 0.2})`; // Neon
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            if (this.x < 0 || this.x > width) this.vx *= -1;
            if (this.y < 0 || this.y > height) this.vy *= -1;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
        }
    }

    function initParticles() {
        particles = [];
        for (let i = 0; i < 50; i++) {
            particles.push(new Particle());
        }
    }

    function animate() {
        if (!window.flashActive) {
            ctx.clearRect(0, 0, width, height);

            particles.forEach(p => {
                p.update();
                p.draw();
            });

            // Electric connections
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 120) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(0, 243, 255, ${0.4 - dist / 400})`;
                        ctx.lineWidth = 1;
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
        }
        requestAnimationFrame(animate);
    }

    initParticles();
    animate();

    // Magic Click Burst
    window.addEventListener('click', (e) => {
        if (typeof gsap !== 'undefined') {
            const colors = ['#ffffff', '#00f3ff', '#bc13fe'];
            for (let i = 0; i < 15; i++) {
                const p = document.createElement('div');
                p.classList.add('magic-particle');
                p.style.background = colors[Math.floor(Math.random() * colors.length)];
                document.body.appendChild(p);

                const size = Math.random() * 5 + 2;
                gsap.set(p, { x: e.clientX, y: e.clientY, width: size, height: size });
                gsap.to(p, {
                    x: e.clientX + (Math.random() - 0.5) * 150,
                    y: e.clientY + (Math.random() - 0.5) * 150,
                    opacity: 0,
                    duration: 0.6,
                    onComplete: () => p.remove()
                });
            }
        }
    });
});
