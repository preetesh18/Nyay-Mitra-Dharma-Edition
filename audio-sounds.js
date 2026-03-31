/* ── AUDIO SOUNDS SYSTEM ── */
class SoundSystem {
  constructor() {
    this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    this.currentScrollTime = 0;
    this.scrollTimeout = null;
    this.isScrolling = false;
    
    // Background music properties
    this.bgMusicGain = this.audioCtx.createGain();
    this.bgMusicGain.connect(this.audioCtx.destination);
    this.bgMusicVolume = 0.15; // Default volume
    this.bgMusicGain.gain.value = this.bgMusicVolume;
    this.isMuted = false;
    this.lastVolume = this.bgMusicVolume;
    this.bgOscillators = [];
    this.bgMusicRunning = false;
    
    // Audio file properties
    this.audioBuffer = null;
    this.audioSource = null;
    this.isPlaying = false;
    
    // Load saved volume preference
    const savedVolume = localStorage.getItem('bgMusicVolume');
    const savedMuted = localStorage.getItem('bgMusicMuted');
    if (savedVolume !== null) this.bgMusicVolume = parseFloat(savedVolume);
    if (savedMuted !== null) this.isMuted = savedMuted === 'true';
    
    this.initScrollAmbience();
    this.createUI();
    this.loadAudioFile();
  }

  /* ── CREATE VOLUME CONTROL UI ── */
  createUI() {
    // Create control panel
    const controls = document.createElement('div');
    controls.id = 'audio-controls';
    controls.innerHTML = `
      <div class="audio-panel">
        <button id="vol-btn" class="vol-btn" title="Mute/Unmute">🔊</button>
        <div class="vol-slider-container" id="vol-slider-container">
          <button id="vol-down" class="vol-arrow" title="Volume Down">−</button>
          <input type="range" id="vol-slider" class="vol-slider" min="0" max="100" value="15" title="Volume">
          <button id="vol-up" class="vol-arrow" title="Volume Up">+</button>
        </div>
      </div>
      <audio id="bg-music" style="display:none" loop preload="auto">
        <source src="Interstellar Theme Song _ Interstellar Background Music _ Interstellar BGM _ Interstellar Ringtone.mp3" type="audio/mpeg">
      </audio>
    `;
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
      #audio-controls {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        z-index: 999;
        font-family: 'Cinzel', serif;
      }
      .audio-panel {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        background: rgba(8, 6, 4, 0.92);
        border: 1px solid rgba(201, 168, 76, 0.25);
        padding: 0.9rem 1.2rem;
        border-radius: 50px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
      }
      .vol-btn {
        background: linear-gradient(135deg, rgba(201, 168, 76, 0.2), rgba(232, 131, 26, 0.1));
        border: 1px solid rgba(201, 168, 76, 0.3);
        color: var(--gold-lt, #F0D483);
        width: 36px;
        height: 36px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
        font-weight: 700;
        flex-shrink: 0;
      }
      .vol-btn:hover {
        background: linear-gradient(135deg, rgba(201, 168, 76, 0.35), rgba(232, 131, 26, 0.2));
        box-shadow: 0 0 16px rgba(201, 168, 76, 0.4);
        transform: scale(1.08);
      }
      .vol-btn.muted {
        color: rgba(201, 168, 76, 0.5);
        opacity: 0.6;
      }
      .vol-slider-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        max-width: 180px;
        opacity: 1;
        transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
        overflow: hidden;
      }
      .vol-slider-container.collapsed {
        max-width: 0;
        opacity: 0;
        gap: 0;
      }
      .vol-arrow {
        background: transparent;
        border: 1px solid rgba(201, 168, 76, 0.25);
        color: rgba(201, 168, 76, 0.7);
        width: 28px;
        height: 28px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: 700;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0;
        flex-shrink: 0;
      }
      .vol-arrow:hover {
        background: rgba(201, 168, 76, 0.1);
        color: rgba(201, 168, 76, 0.9);
        border-color: rgba(201, 168, 76, 0.4);
      }
      .vol-slider {
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, rgba(232, 131, 26, 0.2), rgba(201, 168, 76, 0.3));
        border-radius: 2px;
        outline: none;
        -webkit-appearance: none;
        appearance: none;
        flex-shrink: 0;
      }
      .vol-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 14px;
        height: 14px;
        background: linear-gradient(135deg, #F0D483, #C9A84C);
        border-radius: 50%;
        cursor: pointer;
        box-shadow: 0 0 8px rgba(201, 168, 76, 0.5);
        transition: all 0.2s;
      }
      .vol-slider::-webkit-slider-thumb:hover {
        box-shadow: 0 0 16px rgba(201, 168, 76, 0.8);
        transform: scale(1.2);
      }
      .vol-slider::-moz-range-thumb {
        width: 14px;
        height: 14px;
        background: linear-gradient(135deg, #F0D483, #C9A84C);
        border: none;
        border-radius: 50%;
        cursor: pointer;
        box-shadow: 0 0 8px rgba(201, 168, 76, 0.5);
        transition: all 0.2s;
      }
      .vol-slider::-moz-range-thumb:hover {
        box-shadow: 0 0 16px rgba(201, 168, 76, 0.8);
        transform: scale(1.2);
      }
      /* Hover state expansion */
      .audio-panel:hover .vol-slider-container.collapsed {
        max-width: 180px;
        opacity: 1;
        gap: 0.5rem;
      }
      @media (max-width: 768px) {
        #audio-controls {
          bottom: 1rem;
          right: 1rem;
        }
        .audio-panel {
          padding: 0.7rem 1rem;
          gap: 0.6rem;
        }
        .vol-slider {
          width: 70px;
        }
      }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(controls);
    
    // Attach event listeners
    document.getElementById('vol-btn').addEventListener('click', () => this.toggleMute());
    document.getElementById('vol-up').addEventListener('click', () => this.volumeUp());
    document.getElementById('vol-down').addEventListener('click', () => this.volumeDown());
    document.getElementById('vol-slider').addEventListener('input', (e) => this.setVolume(e.target.value / 100));
    
    // Toggle collapse/expand on button click
    document.getElementById('vol-btn').addEventListener('click', () => {
      const container = document.getElementById('vol-slider-container');
      if (container.classList.contains('collapsed')) {
        container.classList.remove('collapsed');
      } else {
        container.classList.add('collapsed');
      }
    });
    
    // Collapse by default
    document.getElementById('vol-slider-container').classList.add('collapsed');
    this.updateUI();
  }

  /* ── UPDATE UI STATE ── */
  updateUI() {
    const btn = document.getElementById('vol-btn');
    const slider = document.getElementById('vol-slider');
    
    if (this.isMuted) {
      btn.textContent = '🔇';
      btn.classList.add('muted');
      slider.value = 0;
    } else {
      btn.textContent = this.bgMusicVolume > 0.5 ? '🔊' : this.bgMusicVolume > 0 ? '🔉' : '🔇';
      btn.classList.remove('muted');
      slider.value = this.bgMusicVolume * 100;
    }
  }

  /* ── VOLUME CONTROLS ── */
  toggleMute() {
    const audio = document.getElementById('bg-music');
    if (!audio) return;
    
    if (this.isMuted) {
      this.isMuted = false;
      audio.volume = this.lastVolume;
      this.bgMusicGain.gain.value = this.lastVolume;
    } else {
      this.isMuted = true;
      this.lastVolume = audio.volume;
      audio.volume = 0;
      this.bgMusicGain.gain.value = 0;
    }
    localStorage.setItem('bgMusicMuted', this.isMuted);
    this.updateUI();
    this.playClickSound('soft');
  }

  volumeUp() {
    const audio = document.getElementById('bg-music');
    if (!audio) return;
    const newVol = Math.min(audio.volume + 0.1, 1);
    this.setVolume(newVol);
    this.playClickSound('soft');
  }

  volumeDown() {
    const audio = document.getElementById('bg-music');
    if (!audio) return;
    const newVol = Math.max(audio.volume - 0.1, 0);
    this.setVolume(newVol);
    this.playClickSound('soft');
  }

  setVolume(vol) {
    const audio = document.getElementById('bg-music');
    if (!audio) return;
    
    this.bgMusicVolume = Math.max(0, Math.min(vol, 1));
    if (!this.isMuted) {
      audio.volume = this.bgMusicVolume;
      this.bgMusicGain.gain.value = this.bgMusicVolume;
    }
    this.lastVolume = this.bgMusicVolume;
    localStorage.setItem('bgMusicVolume', this.bgMusicVolume);
    this.updateUI();
  }

  /* ── BACKGROUND MUSIC GENERATOR ── */
  startBackgroundMusic() {
    const audio = document.getElementById('bg-music');
    if (!audio) {
      console.error('Audio element not found');
      return;
    }
    
    // Set volume on both audio systems
    audio.volume = this.isMuted ? 0 : this.bgMusicVolume;
    this.bgMusicGain.gain.value = this.isMuted ? 0 : this.bgMusicVolume;
    
    // Play audio
    const playPromise = audio.play();
    if (playPromise !== undefined) {
      playPromise
        .then(() => {
          console.log('Background music started playing');
          this.isPlaying = true;
        })
        .catch(error => {
          console.error('Error playing audio:', error);
        });
    }
  }

  /* ── LOAD AUDIO FILE ── */
  loadAudioFile() {
    const audio = document.getElementById('bg-music');
    if (!audio) {
      console.error('Audio element not found');
      return;
    }
    
    // Log when audio is ready
    audio.addEventListener('canplay', () => {
      console.log('Audio file is ready to play');
    });
    
    audio.addEventListener('play', () => {
      console.log('Audio is playing');
      this.isPlaying = true;
    });
    
    audio.addEventListener('pause', () => {
      console.log('Audio is paused');
      this.isPlaying = false;
    });
    
    audio.addEventListener('error', (e) => {
      console.error('Error loading audio:', e);
    });
  }

  generateInterstellarMusic(startTime) {
    // Interstellar ambience: layered pads with smooth, evolving frequencies
    const chords = [
      [110, 165, 220],      // A2, E3, A3
      [123.47, 185.00, 246.94], // B2, B3, B4
      [130.81, 196.00, 261.63], // C#3, G3, C#4
      [146.83, 220, 293.66]  // D3, A3, D4
    ];
    
    const chordIndex = Math.floor((startTime * 0.5) % chords.length);
    const chord = chords[chordIndex];
    
    // Create smooth pad voices
    chord.forEach((freq, idx) => {
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      const filter = this.audioCtx.createBiquadFilter();
      const vibrato = this.audioCtx.createOscillator();
      const vibratoGain = this.audioCtx.createGain();
      
      // Pad oscillator
      osc.type = 'sine';
      osc.frequency.value = freq;
      
      // Vibrato LFO
      vibrato.type = 'sine';
      vibrato.frequency.value = 0.3 + idx * 0.1;
      vibratoGain.gain.value = 2 + idx;
      
      // Smooth filter
      filter.type = 'lowpass';
      filter.frequency.value = 800 + Math.sin(startTime * 0.1 + idx) * 400;
      filter.Q.value = 2;
      
      // Envelope
      const duration = 8 + idx * 0.5; // Each layer has slightly different length
      const fadeIn = 2;
      const fadeOut = 3;
      
      gain.gain.setValueAtTime(0.01, startTime);
      gain.gain.linearRampToValueAtTime(0.08, startTime + fadeIn);
      gain.gain.setValueAtTime(0.08, startTime + duration - fadeOut);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
      
      // Connect
      vibrato.connect(vibratoGain);
      vibratoGain.connect(osc.frequency);
      osc.connect(filter);
      filter.connect(gain);
      gain.connect(this.bgMusicGain);
      
      // Start and schedule stop
      osc.start(startTime);
      vibrato.start(startTime);
      osc.stop(startTime + duration);
      vibrato.stop(startTime + duration);
      
      // Schedule next chord
      setTimeout(() => {
        this.generateInterstellarMusic(startTime + duration);
      }, (duration * 1000) - 100);
    });
  }

  /* ── SCROLL AMBIENCE ── */
  initScrollAmbience() {
    window.addEventListener('scroll', () => {
      if (!this.isScrolling) {
        this.playScrollAmbience();
        this.isScrolling = true;
      }
      clearTimeout(this.scrollTimeout);
      this.scrollTimeout = setTimeout(() => {
        this.isScrolling = false;
      }, 800);
    });
  }

  playScrollAmbience() {
    const now = this.audioCtx.currentTime;
    const duration = 1.2;
    
    // Create OSC for lofi ambience
    const osc1 = this.audioCtx.createOscillator();
    const osc2 = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();
    const filter = this.audioCtx.createBiquadFilter();
    
    // Low frequency base
    osc1.frequency.value = 80 + Math.random() * 20;
    osc1.type = 'sine';
    
    // Mid tone for lofi character
    osc2.frequency.value = 150 + Math.random() * 30;
    osc2.type = 'triangle';
    
    filter.type = 'lowpass';
    filter.frequency.value = 340;
    filter.Q.value = 4;
    
    gain.gain.setValueAtTime(0.02, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + duration);
    
    osc1.connect(filter);
    osc2.connect(filter);
    filter.connect(gain);
    gain.connect(this.audioCtx.destination);
    
    osc1.start(now);
    osc2.start(now);
    osc1.stop(now + duration);
    osc2.stop(now + duration);
  }

  /* ── CLICK SOUND ── */
  playClickSound(type = 'standard') {
    const now = this.audioCtx.currentTime;
    const osc = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();
    const filter = this.audioCtx.createBiquadFilter();
    
    if (type === 'standard') {
      osc.frequency.setValueAtTime(520, now);
      osc.frequency.exponentialRampToValueAtTime(180, now + 0.15);
      osc.type = 'sine';
      filter.frequency.value = 3200;
    } else if (type === 'soft') {
      osc.frequency.setValueAtTime(380, now);
      osc.frequency.exponentialRampToValueAtTime(140, now + 0.12);
      osc.type = 'triangle';
      filter.frequency.value = 2400;
    }
    
    filter.type = 'highpass';
    gain.gain.setValueAtTime(0.15, now);
    gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
    
    osc.connect(filter);
    filter.connect(gain);
    gain.connect(this.audioCtx.destination);
    
    osc.start(now);
    osc.stop(now + 0.15);
  }

  /* ── PAGE TRANSITION SOUND ── */
  playTransitionSound() {
    const now = this.audioCtx.currentTime;
    const duration = 0.6;
    
    // Ascending arpeggio for smooth transition
    const notes = [
      { freq: 220, time: 0, dur: 0.15 },    // A3
      { freq: 276.63, time: 0.12, dur: 0.15 }, // D#4
      { freq: 329.63, time: 0.24, dur: 0.2 }   // E4
    ];
    
    notes.forEach(note => {
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      const filter = this.audioCtx.createBiquadFilter();
      
      osc.type = 'sine';
      osc.frequency.value = note.freq;
      
      filter.type = 'lowpass';
      filter.frequency.value = 2000;
      
      gain.gain.setValueAtTime(0.12, now + note.time);
      gain.gain.exponentialRampToValueAtTime(0.01, now + note.time + note.dur);
      
      osc.connect(filter);
      filter.connect(gain);
      gain.connect(this.audioCtx.destination);
      
      osc.start(now + note.time);
      osc.stop(now + note.time + note.dur);
    });
  }

  /* ── ATTACH TO ELEMENTS ── */
  attachClickSounds() {
    // Click sound on buttons and links
    document.querySelectorAll('a, button, .btn').forEach(el => {
      el.addEventListener('click', (e) => {
        // Check if it's a page navigation
        const href = el.getAttribute('href');
        if (href && (href.endsWith('.html') || href.startsWith('/'))) {
          this.playTransitionSound();
        } else if (!href || href.startsWith('#')) {
          this.playClickSound('standard');
        }
      }, false);
    });

    // Soft click on other interactive elements
    document.querySelectorAll('[onclick], input[type="checkbox"], input[type="radio"]').forEach(el => {
      el.addEventListener('click', () => this.playClickSound('soft'), false);
    });
  }

  /* ── PAGE TRANSITION LISTENER ── */
  initPageTransitions() {
    document.querySelectorAll('a[href$=".html"]').forEach(link => {
      link.addEventListener('click', (e) => {
        // Sound is already played on click, but we can add fade out effect
        e.preventDefault();
        this.playTransitionSound();
        setTimeout(() => {
          window.location.href = link.getAttribute('href');
        }, 300);
      });
    });
  }

  /* ── USER GESTURE UNLOCK ── */
  unlockAudio() {
    // Unlock audio context on user gesture
    if (this.audioCtx.state === 'suspended') {
      this.audioCtx.resume().then(() => {
        console.log('Audio context unlocked');
      });
    }
  }
}

// Initialize on page load
let soundSystem;
document.addEventListener('DOMContentLoaded', () => {
  soundSystem = new SoundSystem();
  soundSystem.attachClickSounds();
  soundSystem.initPageTransitions();
  // Start background music after a short delay to allow audio to load
  setTimeout(() => {
    soundSystem.startBackgroundMusic();
  }, 500);
});

// Unlock audio on any user interaction
document.addEventListener('click', () => {
  if (soundSystem) soundSystem.unlockAudio();
});
document.addEventListener('keydown', () => {
  if (soundSystem) soundSystem.unlockAudio();
});
