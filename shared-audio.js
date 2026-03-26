/* ── SHARED AUDIO SYSTEM (Cross-Page) ── */

class SharedAudioManager{
  constructor(){
    this.audioElement=null;
    this.isPlaying=false;
    this.currentTime=0;
    this.volume=0.15;
    this.isMuted=false;
    this.lastVolume=0.15;
    
    this.loadAudioState();
  }

  // Load audio state from sessionStorage
  loadAudioState(){
    const state=JSON.parse(sessionStorage.getItem('audio-state')||'{}');
    this.volume=state.volume||0.15;
    this.isMuted=state.isMuted||false;
    this.currentTime=state.currentTime||0;
    this.isPlaying=state.isPlaying||false;
  }

  // Save audio state to sessionStorage
  saveAudioState(){
    sessionStorage.setItem('audio-state',JSON.stringify({
      volume:this.volume,
      isMuted:this.isMuted,
      currentTime:this.audioElement?this.audioElement.currentTime:this.currentTime,
      isPlaying:this.isPlaying
    }));
  }

  // Initialize audio element
  initAudio(){
    if(this.audioElement)return;
    
    this.audioElement=document.getElementById('shared-audio-element');
    if(!this.audioElement){
      this.audioElement=document.createElement('audio');
      this.audioElement.id='shared-audio-element';
      this.audioElement.loop=true;
      this.audioElement.preload='auto';
      this.audioElement.src='Interstellar Theme Song _ Interstellar Background Music _ Interstellar BGM _ Interstellar Ringtone.mp3';
      document.body.appendChild(this.audioElement);
    }
    
    // Set volume
    this.audioElement.volume=this.isMuted?0:this.volume;
    
    // Restore playback position
    if(this.currentTime>0&&this.isPlaying){
      this.audioElement.currentTime=this.currentTime;
    }
    
    // Event listeners
    this.audioElement.addEventListener('timeupdate',()=>this.saveAudioState());
    this.audioElement.addEventListener('ended',()=>{
      // Loop is set, but just in case
      this.audioElement.currentTime=0;
      this.audioElement.play();
    });
  }

  // Start audio
  start(){
    if(!sessionStorage.getItem('user-entered')){
      sessionStorage.setItem('user-entered','true');
    }
    
    this.initAudio();
    this.audioElement.volume=this.isMuted?0:this.volume;
    this.audioElement.play().catch(e=>console.log('Audio play failed:',e));
    this.isPlaying=true;
    this.saveAudioState();
    this.updateIndicator();
  }

  // Stop audio
  stop(){
    if(this.audioElement){
      this.audioElement.pause();
      this.isPlaying=false;
      this.saveAudioState();
      this.updateIndicator();
    }
  }

  // Set volume
  setVolume(val){
    this.volume=Math.max(0,Math.min(1,val));
    this.initAudio();
    if(!this.isMuted){
      this.audioElement.volume=this.volume;
    }
    this.saveAudioState();
  }

  // Toggle mute
  toggleMute(){
    this.isMuted=!this.isMuted;
    this.initAudio();
    this.audioElement.volume=this.isMuted?0:this.volume;
    this.saveAudioState();
    this.updateIndicator();
  }

  // Update indicator
  updateIndicator(){
    const indicator=document.getElementById('audio-indicator');
    if(indicator){
      if(this.isPlaying&&!this.isMuted){
        indicator.classList.add('playing');
      }else{
        indicator.classList.remove('playing');
      }
    }
  }

  // Creates audio control UI
  createControls(){
    if(document.getElementById('audio-controls'))return;
    
    const controls=document.createElement('div');
    controls.id='audio-controls';
    controls.innerHTML=`
      <div class="audio-panel">
        <button id="vol-btn" class="vol-btn" title="Mute/Unmute">🔊</button>
        <div class="vol-slider-container" id="vol-slider-container">
          <button id="vol-down" class="vol-arrow" title="Volume Down">−</button>
          <input type="range" id="vol-slider" class="vol-slider" min="0" max="100" value="${Math.round(this.volume*100)}" title="Volume">
          <button id="vol-up" class="vol-arrow" title="Volume Up">+</button>
        </div>
      </div>
    `;
    
    // Injected styles for controls (if not already present)
    if(!document.getElementById('audio-controls-style')){
      const style=document.createElement('style');
      style.id='audio-controls-style';
      style.textContent=`
        #audio-controls{position:fixed;bottom:2.5rem;right:2.5rem;z-index:95;pointer-events:auto}
        .audio-panel{display:flex;align-items:center;gap:0.8rem;background:rgba(8,6,4,.85);border:1px solid rgba(201,168,76,.25);padding:0.6rem;backdrop-filter:blur(10px);clip-path:polygon(8px 0%,100% 0%,calc(100% - 8px) 100%,0% 100%);box-shadow:0 10px 40px rgba(0,0,0,.5)}
        .vol-btn{background:rgba(201,168,76,.1);border:1px solid rgba(201,168,76,.3);color:var(--gold);padding:0.5rem 0.8rem;border-radius:4px;cursor:pointer;font-size:1.1rem;transition:all .2s;font-family:'Cinzel',serif}
        .vol-btn:hover{background:rgba(201,168,76,.2);border-color:rgba(201,168,76,.5)}
        .vol-slider-container{display:flex;align-items:center;gap:0.5rem;maxHeight:30px}
        .vol-arrow{background:rgba(201,168,76,.1);border:1px solid rgba(201,168,76,.3);color:var(--gold);width:28px;height:28px;border-radius:3px;cursor:pointer;font-size:0.85rem;transition:all .2s;font-family:'Cinzel',serif;display:flex;align-items:center;justify-content:center}
        .vol-arrow:hover{background:rgba(201,168,76,.2)}
        .vol-slider{width:100px;height:4px;appearance:none;background:linear-gradient(90deg,rgba(201,168,76,.3),rgba(201,168,76,.8));border-radius:2px;outline:none;padding:0;cursor:pointer}
        .vol-slider::-webkit-slider-thumb{appearance:none;width:14px;height:14px;background:var(--gold);border-radius:50%;cursor:pointer;box-shadow:0 0 8px rgba(201,168,76,.6)}
        .vol-slider::-moz-range-thumb{width:14px;height:14px;background:var(--gold);border:none;border-radius:50%;cursor:pointer;box-shadow:0 0 8px rgba(201,168,76,.6)}
        @media(max-width:768px){#audio-controls{bottom:1.5rem;right:1.5rem}.vol-slider-container{display:none}}
      `;
      document.head.appendChild(style);
    }
    
    document.body.appendChild(controls);
    this.attachControlsEvents();
  }

  // Attach events to controls
  attachControlsEvents(){
    const volBtn=document.getElementById('vol-btn');
    const volSlider=document.getElementById('vol-slider');
    const volDown=document.getElementById('vol-down');
    const volUp=document.getElementById('vol-up');
    
    if(volBtn){
      volBtn.addEventListener('click',()=>this.toggleMute());
    }
    
    if(volSlider){
      volSlider.addEventListener('input',(e)=>{
        this.setVolume(e.target.value/100);
        volSlider.value=Math.round(this.volume*100);
      });
    }
    
    if(volDown){
      volDown.addEventListener('click',()=>{
        this.setVolume(this.volume-0.1);
        if(volSlider)volSlider.value=Math.round(this.volume*100);
      });
    }
    
    if(volUp){
      volUp.addEventListener('click',()=>{
        this.setVolume(this.volume+0.1);
        if(volSlider)volSlider.value=Math.round(this.volume*100);
      });
    }
  }
}

// Global instance
let sharedAudio=null;

// Initialize shared audio
function initializeSharedAudio(){
  if(!sharedAudio){
    sharedAudio=new SharedAudioManager();
  }
  sharedAudio.createControls();
  
  // Auto-start if user already logged in and was playing
  if(sessionStorage.getItem('user-entered')){
    const state=JSON.parse(sessionStorage.getItem('audio-state')||'{}');
    if(state.isPlaying){
      sharedAudio.start();
    }
  }
}

// Start shared audio
function startSharedAudio(){
  if(!sharedAudio){
    sharedAudio=new SharedAudioManager();
  }
  sharedAudio.start();
}

// Stop shared audio
function stopSharedAudio(){
  if(sharedAudio){
    sharedAudio.stop();
  }
}

// Get shared audio manager
function getSharedAudio(){
  if(!sharedAudio){
    sharedAudio=new SharedAudioManager();
  }
  return sharedAudio;
}

// Initialize on page visibilitychange to restore audio if needed
document.addEventListener('visibilitychange',()=>{
  if(!document.hidden){
    if(!sharedAudio){
      sharedAudio=new SharedAudioManager();
    }
    const state=JSON.parse(sessionStorage.getItem('audio-state')||'{}');
    if(state.isPlaying){
      setTimeout(()=>sharedAudio.start(),100);
    }
  }
});
