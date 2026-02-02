document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const messagesArea = document.getElementById('messages-area');
    const sessionId = document.getElementById('session-id').value;
    const stressBar = document.getElementById('stress-bar');

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // Add User Message
        addMessage(text, 'user');
        userInput.value = '';

        // Show typing indicator (optional placeholder)

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, session_id: sessionId })
            });

            const data = await response.json();

            // Add Bot Message
            addMessage(data.response, 'bot');

            // TTS: Speak the response
            speakText(data.response);

            // ADVANCED MUSIC THERAPY OFFER
            if (data.music_data) {
                const musicType = data.music_data.type;
                const autoPlay = data.music_data.autoplay;

                // Friendly Name Map
                const names = {
                    'calm_binaural': 'Calming Binaural Beats',
                    'gentle_piano': 'Uplifting Piano',
                    'rain_sounds': 'Soothing Rain',
                    'focus_noise': 'Deep Focus Noise',
                    'lofi_beats': 'Lofi Beats'
                };
                const name = names[musicType] || 'Healing Frequencies';

                if (autoPlay) {
                    addMessage(`System: Automatically initializing ${name} therapy due to high stress levels...`, 'bot');
                    AudioEngine.playTone(musicType);
                    if (window.showStopControl) window.showStopControl();
                } else {
                    const musicDiv = document.createElement('div');
                    musicDiv.className = 'message bot-message bg-dark border border-info';
                    musicDiv.innerHTML = `
                        <p class="mb-2 text-info">I recommend <strong>${name}</strong> to help shift your state.</p>
                        <div class="d-flex gap-2">
                            <button class="btn btn-sm btn-outline-info" onclick="AudioEngine.playTone('${musicType}'); if(window.showStopControl) window.showStopControl(); addMessage('Playing ${name}...', 'bot');">🎵 Play ${name}</button>
                            <button class="btn btn-sm btn-outline-secondary" onclick="addMessage('Maybe later.', 'user');">No thanks</button>
                        </div>
                    `;
                    messagesArea.appendChild(musicDiv);
                }
            }
            // Fallback for simple rule-based output if older logic hits
            else if (data.offer_music) {
                const musicDiv = document.createElement('div');
                musicDiv.className = 'message bot-message bg-dark border border-info';
                musicDiv.innerHTML = `
                    <p class="mb-2 text-info">Would you like to listen to some healing frequencies?</p>
                    <div class="d-flex gap-2">
                        <button class="btn btn-sm btn-outline-info" onclick="showMusicOptions()">🎵 Show Options</button>
                        <button class="btn btn-sm btn-outline-warning" onclick="if(window.startBreathing) window.startBreathing()">🧘 Breathing Exercise</button>
                    </div>
                `;
                messagesArea.appendChild(musicDiv);
            }
            messagesArea.scrollTop = messagesArea.scrollHeight;

            // New UI Hooks
            if (window.uiUpdate) window.uiUpdate(data);
            if (window.updateStressParticles) window.updateStressParticles(data.stress_score);

        } catch (error) {
            console.error('Error:', error);
            addMessage("I'm having a little trouble connecting right now. Can we try again?", 'bot');
        }
    }

    // TEXT TO SPEECH ENGINE
    function speakText(text) {
        if ('speechSynthesis' in window) {
            // Cancel current speech to avoid overlap
            window.speechSynthesis.cancel();

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            utterance.rate = 1.0;
            utterance.pitch = 1.0;

            // Try to find a nice voice (Google US English or generic female if possible)
            const voices = window.speechSynthesis.getVoices();
            const preferredVoice = voices.find(voice => voice.name.includes("Google US English") || voice.name.includes("Female"));
            if (preferredVoice) utterance.voice = preferredVoice;

            window.speechSynthesis.speak(utterance);
        }
    }

    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.classList.add('message');
        div.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
        div.textContent = text;
        messagesArea.appendChild(div);
        messagesArea.scrollTop = messagesArea.scrollHeight;

        // Simple entry animation handling via CSS class
    }

    // Expose functions to global scope for inline onclicks
    window.addMessage = addMessage;

    // GLOBAL HELPER FOR MUSIC
    window.showMusicOptions = function () {
        const div = document.createElement('div');
        div.className = 'message bot-message';
        div.innerHTML = `
            <p>Select a frequency level:</p>
            <button class="btn btn-sm btn-info m-1" onclick="AudioEngine.playTone('level1'); addMessage('Playing Level 1: 432Hz Calm...', 'bot');">Level 1 (Calm)</button>
            <button class="btn btn-sm btn-warning m-1" onclick="AudioEngine.playTone('level2'); addMessage('Playing Level 2: 528Hz Healing...', 'bot');">Level 2 (Comfort)</button>
            <button class="btn btn-sm btn-primary m-1" onclick="AudioEngine.playTone('level3'); addMessage('Playing Level 3: Deep Theta...', 'bot');">Level 3 (Sleep)</button>
            <button class="btn btn-sm btn-danger m-1" onclick="AudioEngine.stop(); addMessage('Music stopped.', 'bot');">⏹ Stop</button>
        `;
        document.getElementById('messages-area').appendChild(div);
        document.getElementById('messages-area').scrollTop = document.getElementById('messages-area').scrollHeight;
    };

    // Voice Input (Web Speech API) - ROBUST FIX
    const micBtn = document.getElementById('mic-btn');
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();

        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.interimResults = false;

        micBtn.addEventListener('click', () => {
            try {
                recognition.start();
                micBtn.classList.add('btn-danger'); // Red to indicate recording
                micBtn.classList.remove('btn-outline-light');
                micBtn.innerText = "🛑";
                userInput.placeholder = "Listening...";
                userInput.focus();
            } catch (e) {
                console.log("Mic already active or error", e);
            }
        });

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            resetMicBtn();
            sendMessage(); // Auto send
        };

        recognition.onspeechend = () => {
            recognition.stop();
            resetMicBtn();
        };

        recognition.onerror = (event) => {
            console.error("Speech error", event.error);
            resetMicBtn();
            userInput.placeholder = "Mic error. Try typing.";
        };

        function resetMicBtn() {
            micBtn.classList.remove('btn-danger');
            micBtn.classList.add('btn-outline-light');
            micBtn.innerText = "🎤";
            userInput.placeholder = "Speak your mind...";
        }
    } else {
        micBtn.style.display = 'none';
        console.warn("Web Speech API not supported");
    }

    // FILE UPLOAD HANDLER (Health Reports)
    const reportUpload = document.getElementById('report-upload');
    if (reportUpload) {
        reportUpload.addEventListener('change', async function () {
            if (this.files.length === 0) return;

            const file = this.files[0];
            const formData = new FormData();
            formData.append('file', file);
            formData.append('session_id', sessionId);

            // Show uploading message
            addMessage("📄 Uploading health report...", 'user');
            addMessage("Analyzing report data... please wait.", 'bot');

            try {
                const response = await fetch('/upload_report', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.status === 'success') {
                    // Success logic
                    let findingsText = "Report analyzed successfully. ";
                    if (data.findings && data.findings.length > 0) {
                        findingsText += "Key findings: " + data.findings.join(", ");
                    } else {
                        findingsText += "No critical anomalies detected.";
                    }
                    addMessage("Analysis Complete. " + findingsText, 'bot');
                    addMessage("I will now tailor my advice based on this health context.", 'bot');
                } else {
                    addMessage("Error analyzing report: " + data.message, 'bot');
                }
            } catch (e) {
                console.error(e);
                addMessage("Upload failed. Please try again.", 'bot');
            }

            // Reset input
            this.value = '';
        });
    }


    // Connect global reset function
    window.resetChat = async function () {
        if (!confirm("Start a new conversation? This will clear current history.")) return;

        try {
            await fetch('/reset_chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId })
            });
            // Clear UI
            messagesArea.innerHTML = '';
            // Add intro again
            const introDiv = document.createElement('div');
            introDiv.className = 'message bot-message';
            introDiv.textContent = "I am ready to listen again. A fresh start. How are you feeling now?";
            messagesArea.appendChild(introDiv);

            // Reset visual meters
            if (window.uiUpdate) window.uiUpdate({ stress_score: 20 });

        } catch (e) {
            console.error("Reset failed", e);
        }
    };
    // MUSIC & BREATHING HELPERS
    window.showStopControl = function () {
        // Remove existing stop if present
        const oldBtn = document.getElementById('music-stop-btn');
        if (oldBtn) oldBtn.remove();

        const stopBtn = document.createElement('button');
        stopBtn.id = 'music-stop-btn';
        stopBtn.className = 'btn btn-danger btn-sm rounded-pill position-fixed bottom-0 end-0 m-4 shadow-lg';
        stopBtn.style.zIndex = '9999';
        stopBtn.innerHTML = '⏹ Stop Music';
        stopBtn.onclick = function () {
            AudioEngine.stop();
            this.remove();
            addMessage('Music stopped.', 'bot');
        };
        document.body.appendChild(stopBtn);
    };

    window.startBreathing = function () {
        const overlay = document.createElement('div');
        overlay.id = 'breath-overlay';
        overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:10000;display:flex;flex-direction:column;justify-content:center;align-items:center;color:white;text-align:center;font-family:sans-serif;';

        overlay.innerHTML = `
            <div id="breath-circle" style="width:100px;height:100px;background:#00d2ff;border-radius:50%;box-shadow:0 0 50px #00d2ff;transition:all 4s ease-in-out;"></div>
            <h2 id="breath-text" style="margin-top:2rem;font-weight:300;">Inhale...</h2>
            <button class="btn btn-outline-light mt-4" onclick="document.getElementById('breath-overlay').remove()">Close</button>
        `;
        document.body.appendChild(overlay);

        const circle = document.getElementById('breath-circle');
        const text = document.getElementById('breath-text');

        let breathing = true;

        function breathCycle() {
            if (!document.getElementById('breath-overlay')) return;
            // Inhale
            circle.style.transform = 'scale(3)';
            text.innerText = 'Inhale...';

            setTimeout(() => {
                if (!document.getElementById('breath-overlay')) return;
                // Hold
                text.innerText = 'Hold...';

                setTimeout(() => {
                    if (!document.getElementById('breath-overlay')) return;
                    // Exhale
                    circle.style.transform = 'scale(1)';
                    text.innerText = 'Exhale...';

                    setTimeout(breathCycle, 4000); // 4s Exhale
                }, 2000); // 2s Hold
            }, 4000); // 4s Inhale
        }

        // Start after slight delay
        setTimeout(breathCycle, 100);
    };

});
