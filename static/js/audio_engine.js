// MindMate Audio Engine (Web Audio API)
// Generates Real-time Binaural Beats & Ambient Drones

const AudioEngine = {
    ctx: null,
    oscillators: [],
    gainNodes: [],
    isPlaying: false,

    init() {
        if (!this.ctx) {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        }
    },

    playTone(type) {
        this.stop(); // Stop any current sound
        this.init();
        this.isPlaying = true;

        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }

        const masterGain = this.ctx.createGain();
        masterGain.gain.setValueAtTime(0.01, this.ctx.currentTime); // Low volume start
        masterGain.connect(this.ctx.destination);
        // Fade in
        masterGain.gain.exponentialRampToValueAtTime(0.3, this.ctx.currentTime + 2);
        this.gainNodes.push(masterGain);

        if (type === 'calm_binaural') {
            // 432Hz + 436Hz (4Hz Theta)
            console.log("Playing: Calm Binaural");
            this.createOscillator(432, 'sine', masterGain);
            // Binaural Beat
            const pannerR = this.ctx.createStereoPanner();
            pannerR.pan.value = 1;
            pannerR.connect(masterGain);
            this.createOscillator(436, 'sine', pannerR);

            const pannerL = this.ctx.createStereoPanner();
            pannerL.pan.value = -1;
            pannerL.connect(masterGain);
            this.createOscillator(432, 'sine', pannerL);
        }
        else if (type === 'gentle_piano') {
            // Simulating piano using chords (Harmonic series)
            // C Major 7: C4, E4, G4, B4
            // Using triangle waves with decay
            console.log("Playing: Gentle Piano Drone");
            [261.63, 329.63, 392.00, 493.88].forEach(freq => {
                this.createOscillator(freq, 'triangle', masterGain);
            });
        }
        else if (type === 'rain_sounds') {
            console.log("Playing: Rain Sounds (Pink Noise)");
            this.createNoise('pink', masterGain);
        }
        else if (type === 'focus_noise') {
            console.log("Playing: Focus (Brown Noise)");
            this.createNoise('brown', masterGain);
        }
        else if (type === 'lofi_beats') {
            console.log("Playing: Lofi Drone (Low Fidelity)");
            // Brown noise + Low Sine
            this.createNoise('brown', masterGain);
            this.createOscillator(60, 'sine', masterGain); // Sub bass
        }
    },

    createOscillator(freq, type, destination) {
        const osc = this.ctx.createOscillator();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
        osc.connect(destination);
        osc.start();
        this.oscillators.push(osc);
    },

    createNoise(type, destination) {
        const bufferSize = 2 * this.ctx.sampleRate;
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const output = buffer.getChannelData(0);

        for (let i = 0; i < bufferSize; i++) {
            const white = Math.random() * 2 - 1;
            if (type === 'pink') {
                output[i] = (lastOut + (0.02 * white)) / 1.02;
                lastOut = output[i];
                output[i] *= 3.5; // Compensate for gain loss
            }
            else if (type === 'brown') {
                output[i] = (lastOut + (0.02 * white)) / 1.02;
                lastOut = output[i];
                output[i] *= 3.5;
            }
            else {
                output[i] = white; // white
            }
        }
        // Hacky pink noise approximation above is actually simple low pass.
        // Let's use standard white noise source node and filter it for better result.

        const noiseSource = this.ctx.createBufferSource();
        // Fill buffer with random
        for (let i = 0; i < bufferSize; i++) {
            output[i] = Math.random() * 2 - 1;
        }
        noiseSource.buffer = buffer;
        noiseSource.loop = true;

        // Filter
        const filter = this.ctx.createBiquadFilter();
        if (type === 'pink' || type === 'rain') {
            filter.type = 'lowpass';
            filter.frequency.value = 800; // Muffles it to look like rain
        } else if (type === 'brown') {
            filter.type = 'lowpass';
            filter.frequency.value = 200; // Deep rumble
        }

        noiseSource.connect(filter);
        filter.connect(destination);
        noiseSource.start();
        this.oscillators.push(noiseSource); // Keep track to stop later
    },

    stop() {
        this.oscillators.forEach(osc => {
            try { osc.stop(); } catch (e) { }
        });
        this.oscillators = [];
        this.gainNodes.forEach(g => {
            try { g.disconnect(); } catch (e) { }
        });
        this.gainNodes = [];
        this.isPlaying = false;
        console.log("Audio Stopped");
    }
};

let lastOut = 0; // For noise generation state

// Expose globally
window.AudioEngine = AudioEngine;
