// Interactions for Tools, Timeline, and Overlays

// --- NEURAL NETWORK BACKGROUND (Mental Health Theme) ---
function initNeuralBackground() {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let width, height;
    let particles = [];

    // Neuro-Colors: Vivid Neon for High Contrast on Dark BG
    const colors = ['#00FFFF', '#FF00FF', '#FFFFFF', '#00FF00'];

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * 1.5; // Faster drift
            this.vy = (Math.random() - 0.5) * 1.5;
            this.size = Math.random() * 4 + 2; // Bigger (2-6px)
            this.color = colors[Math.floor(Math.random() * colors.length)];
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            // Bounce
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

    function init() {
        resize();
        particles = [];
        const count = Math.min(100, (width * height) / 15000); // Responsive density
        for (let i = 0; i < count; i++) particles.push(new Particle());
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        // Update & Draw Particles
        particles.forEach(p => {
            p.update();
            p.draw();
        });

        // Draw Connections (Synapses)
        ctx.lineWidth = 0.5;
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 150) { // Connection threshold
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(0, 242, 234, ${1 - dist / 150})`; // Fade out
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(animate);
    }

    window.addEventListener('resize', () => {
        resize();
        init();
    });

    init();
    animate();
}

// Start Background Immediately
document.addEventListener('DOMContentLoaded', initNeuralBackground);


// --- Overlays ---
function openTool(toolName) {
    closeOverlays();
    const overlay = document.getElementById(`overlay-${toolName}`);
    if (overlay) {
        overlay.classList.add('active');
        if (toolName === 'breathe') startBreathingAnimation();
    }
}

function closeOverlays() {
    document.querySelectorAll('.tool-overlay').forEach(el => el.classList.remove('active'));
    stopBreathingAnimation();
}

// --- Breathing Logic ---
let breathInterval;
function startBreathingAnimation() {
    const circle = document.getElementById('breath-circle');
    const text = document.getElementById('breath-text');

    function cycle() {
        text.innerText = "Inhale...";
        gsap.to(circle, { scale: 1.5, duration: 4, ease: "power1.inOut" });

        setTimeout(() => {
            text.innerText = "Hold...";

            setTimeout(() => {
                text.innerText = "Exhale...";
                gsap.to(circle, { scale: 1.0, duration: 8, ease: "power1.inOut" });
            }, 7000);

        }, 4000);
    }

    cycle();
    breathInterval = setInterval(cycle, 19000); // 4+7+8 = 19s
}

function stopBreathingAnimation() {
    clearInterval(breathInterval);
    gsap.killTweensOf("#breath-circle");
}

// --- Timeline Graph ---
const timelineEl = document.getElementById('timeline-graph');
function updateTimeline(score) {
    if (!timelineEl) return;

    // Create new bar
    const bar = document.createElement('div');
    bar.style.width = '10px';
    bar.style.height = `${score}%`;
    bar.style.backgroundColor = getScoreColor(score);
    bar.style.marginRight = '4px';
    bar.style.borderRadius = '2px';
    bar.style.transition = 'height 0.5s';

    // Append
    timelineEl.appendChild(bar);

    // Keep max 20 bars
    if (timelineEl.children.length > 30) {
        timelineEl.removeChild(timelineEl.firstChild);
    }
}

function getScoreColor(score) {
    if (score < 30) return '#00f2ea'; // Cyan
    if (score < 70) return '#ffd700'; // Yellow
    return '#ff4d4d'; // Red
}

// --- Global Hook ---
window.uiUpdate = function (data) {
    if (data.stress_score !== undefined) {
        updateTimeline(data.stress_score);

        if (document.getElementById('stress-val')) document.getElementById('stress-val').innerText = Math.round(data.stress_score) + '%';

        const moodBadge = document.getElementById('session-mood');
        if (moodBadge && data.stress_score) {
            if (data.stress_score < 30) {
                moodBadge.innerText = "Session Mood: Calm";
                moodBadge.className = "ms-auto badge rounded-pill bg-success border border-success text-light p-2";
            } else if (data.stress_score < 70) {
                moodBadge.innerText = "Session Mood: Reflective";
                moodBadge.className = "ms-auto badge rounded-pill bg-warning border border-warning text-dark p-2";
            } else {
                moodBadge.innerText = "Session Mood: Heavy";
                moodBadge.className = "ms-auto badge rounded-pill bg-danger border border-danger text-light p-2";
            }
        }
    }
};

// --- Report Download ---
function downloadReport() {
    const sessionId = document.getElementById('session-id').value;
    window.location.href = `/download_report?session_id=${sessionId}`;
}

// --- Music Player ---
let isPlaying = false;
function toggleMusic(e) {
    if (e) e.stopPropagation();
    const audio = document.getElementById('bg-music');
    const btn = document.getElementById('play-pause-btn');

    if (isPlaying) {
        audio.pause();
        btn.innerText = "♫";
        btn.classList.remove('text-success');
        btn.classList.add('text-info');
    } else {
        audio.volume = 0.3;
        audio.play().catch(e => console.log("Audio play failed (user interaction needed)", e));
        btn.innerText = "II";
        btn.classList.remove('text-info');
        btn.classList.add('text-success');
    }
    isPlaying = !isPlaying;
}

// --- End Session Flow ---
window.endSession = async function () {
    if (!confirm("Are you ready to end? This will download your report and clear your mind (and this chat).")) return;

    downloadReport();

    setTimeout(() => {
        if (window.resetChat) resetChat();
        if (window.toggleChat) {
            const chat = document.getElementById('chat-interface');
            if (chat) chat.style.display = 'none';
        }
    }, 2000);
};

// --- Focus Timer Logic ---
let focusInterval;
let focusTimeRemaining = 0;
let totalFocusTime = 0;

function startFocusTimer(minutes) {
    clearInterval(focusInterval);
    focusTimeRemaining = minutes * 60;
    totalFocusTime = focusTimeRemaining;

    updateTimerDisplay();
    document.getElementById('timer-status').innerText = "Focus Mode Active...";
    document.getElementById('timer-controls').innerHTML = '<button class="btn btn-sm btn-outline-warning w-100" onclick="stopFocusTimer()">Stop</button>';

    focusInterval = setInterval(() => {
        focusTimeRemaining--;
        updateTimerDisplay();

        if (focusTimeRemaining <= 0) {
            clearInterval(focusInterval);
            focusComplete();
        }
    }, 1000);
}

function stopFocusTimer() {
    clearInterval(focusInterval);
    document.getElementById('timer-status').innerText = "Paused.";
    resetTimerUI();
}

function updateTimerDisplay() {
    const m = Math.floor(focusTimeRemaining / 60);
    const s = focusTimeRemaining % 60;
    document.getElementById('timer-display').innerText = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;

    const progress = ((totalFocusTime - focusTimeRemaining) / totalFocusTime) * 100;
    document.getElementById('timer-progress').style.width = `${progress}%`;
}

function focusComplete() {
    document.getElementById('timer-display').innerText = "00:00";
    document.getElementById('timer-status').innerText = "Focus Complete!";
    alert("Great work! Take a breath. Drink some water.");

    const controls = document.getElementById('timer-controls');
    controls.innerHTML = `
        <button class="btn btn-sm btn-outline-info" onclick="startFocusTimer(5)">5m</button>
        <button class="btn btn-sm btn-outline-info" onclick="startFocusTimer(10)">10m</button>
        <button class="btn btn-sm btn-outline-info" onclick="startFocusTimer(25)">25m</button>
    `;
    document.getElementById('timer-status').innerText = "Select next focus block:";
}

function resetTimerUI() {
    document.getElementById('timer-controls').innerHTML = '<button class="btn btn-sm btn-outline-danger flex-grow-1" onclick="startFocusTimer(5)">Start 5m</button>';
}

// --- ZEN MODE LOGIC ---
function toggleZenMode() {
    document.body.classList.toggle('zen-active');
    const isActive = document.body.classList.contains('zen-active');

    if (isActive) {
        // Auto-start calming audio if not playing
        if (window.AudioEngine && !window.AudioEngine.isPlaying) {
            window.AudioEngine.playTone('calm_binaural');
        }
    }
}
