// Enhanced Flashcards with 3D Flip and improved content
document.addEventListener('DOMContentLoaded', () => {
    const cardContainer = document.getElementById('flashcard-container');

    // Expanded local dataset in case backend fetch fails or to supplement it
    const localCards = [
        { type: "Calm", front: "🌿 Breathe", back: "Inhale for 4 seconds, hold for 7, exhale for 8. Repeat 3 times." },
        { type: "Focus", front: "🎯 5-Minute Rule", back: "Commit to doing the task for just 5 minutes. Usually, you'll keep going." },
        { type: "Anxiety", front: "🌊 Ride the Wave", back: "Anxiety is a wave. It peaks and then falls. You just need to float until it passes." },
        { type: "Self-Love", front: "❤️ You are enough", back: "Your productivity does not define your worth. You are valuable just by being." },
        { type: "Grounding", front: "🦶 Feet on Floor", back: "Feel the weight of your feet. Wiggle your toes. You are here, in this moment." },
        { type: "Sleep", front: "🌙 Screen Off", back: "Turn off screens 30 mins before bed to let your melatonin rise naturally." },
        { type: "Stress", front: "🧊 Cold Water", back: "Splash cold water on your face to trigger the 'Dive Reflex' and instantly lower heart rate." }
    ];

    // Try to fetch, else use local
    fetch('/get_flashcards')
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(data => {
            // Combine or use data. Let's start with local for guaranteed design quality then append
            const combined = [...localCards];
            // If data has distinct items, we could add them. For now, let's just use local for the "Premium" look guaranteed.
            renderCards(combined);
        })
        .catch(err => {
            console.log("Using local cards due to fetch error", err);
            renderCards(localCards);
        });

    function renderCards(cards) {
        cardContainer.innerHTML = '';
        cards.forEach((card, index) => {
            const cardEl = document.createElement('div');
            cardEl.className = 'flashcard';

            // Add slight stagger animation
            cardEl.style.animation = `fadeInUp 0.5s ease forwards ${index * 0.1}s`;
            // cardEl.style.opacity = '0'; // REMOVED: Caused visibility issues if anim failed

            cardEl.innerHTML = `
                <div class="flashcard-inner">
                    <div class="flashcard-front">
                        <h4 class="m-0" style="font-family: 'Orbitron'; color: var(--neon-blue);">${card.front}</h4>
                        <div class="mt-2"><span class="badge rounded-pill bg-dark border border-secondary">${card.type}</span></div>
                        <div class="small text-muted mt-3">Click to Flip ↻</div>
                    </div>
                    <div class="flashcard-back">
                        <p class="lead">${card.back}</p>
                    </div>
                </div>
            `;

            // Toggle flip on click
            cardEl.addEventListener('click', () => {
                cardEl.classList.toggle('flipped');
            });

            cardContainer.appendChild(cardEl);
        });
    }
});
