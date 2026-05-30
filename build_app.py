import json

truths = json.load(open('truths.json', encoding='utf-8'))
truths_json = json.dumps(truths, ensure_ascii=False, separators=(',', ':'))

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Quid est veritas? &mdash; A Treasury of Truths</title>
<style>
  :root{
    --serif: "Iowan Old Style", "Palatino Linotype", Palatino, "Cormorant Garamond", Georgia, "Times New Roman", serif;
    --sans: "Avenir Next", "Segoe UI", system-ui, -apple-system, Helvetica, Arial, sans-serif;
  }
  *{ box-sizing:border-box; margin:0; padding:0; }
  html,body{ height:100%; overflow:hidden; }
  body{
    font-family:var(--sans);
    color:#f3ecdf;
    background:#070a16;
    -webkit-font-smoothing:antialiased;
    user-select:none;
    cursor:default;
  }

  /* ---------- Background ---------- */
  .bg{
    position:fixed; inset:-10%;
    background:
      radial-gradient(120% 120% at 22% 18%, #20335e 0%, transparent 58%),
      radial-gradient(120% 120% at 80% 26%, #3c2a64 0%, transparent 58%),
      radial-gradient(150% 150% at 50% 108%, #0e4045 0%, transparent 60%),
      linear-gradient(160deg, #0a1024 0%, #150f2c 50%, #081a1e 100%);
    animation: drift 60s ease-in-out infinite alternate;
    will-change: transform, filter;
  }
  @keyframes drift{
    0%   { transform: scale(1) translate(0,0);        filter: hue-rotate(0deg)   saturate(1); }
    100% { transform: scale(1.1) translate(-2.5%,-2%); filter: hue-rotate(28deg) saturate(1.15); }
  }

  /* page-wide colour sweep that builds toward the reveal */
  .sweep{
    position:fixed; inset:0; opacity:0; pointer-events:none;
    background:linear-gradient(125deg,#6a3bd0 0%,#2bbfd0 45%,#f1c673 100%);
    background-size:240% 240%;
    mix-blend-mode:screen;
    transition:opacity 1.2s ease;
  }
  .state-revealing .sweep{ opacity:.6; animation: sweepmove 2.8s ease-in-out forwards; }
  .state-revealed  .sweep{ opacity:.12; transition:opacity 2s ease; }
  @keyframes sweepmove{
    0%{ background-position:0% 50%;  filter:hue-rotate(0deg)   brightness(.9); }
   100%{ background-position:100% 50%; filter:hue-rotate(55deg) brightness(1.25); }
  }

  /* rotating light rays */
  .rays{
    position:fixed; left:50%; top:50%; width:200vmax; height:200vmax;
    transform:translate(-50%,-50%);
    background:repeating-conic-gradient(from 0deg,
      rgba(255,250,235,.06) 0deg 1.4deg, transparent 1.4deg 9deg);
    opacity:0; pointer-events:none;
    animation: spin 150s linear infinite;
    transition:opacity 2s ease;
    -webkit-mask-image:radial-gradient(circle, #000 0%, transparent 62%);
            mask-image:radial-gradient(circle, #000 0%, transparent 62%);
  }
  .state-revealing .rays,.state-revealed .rays{ opacity:.55; }
  @keyframes spin{ to{ transform:translate(-50%,-50%) rotate(360deg); } }

  /* central radiant glow (the "opening" bloom) */
  .glow{
    position:fixed; left:50%; top:50%;
    width:46vmax; height:46vmax; border-radius:50%;
    transform:translate(-50%,-50%) scale(0);
    background:radial-gradient(circle,
      rgba(255,248,232,.95) 0%,
      rgba(255,216,150,.55) 30%,
      rgba(180,150,255,.18) 55%,
      transparent 72%);
    opacity:0; pointer-events:none;
    filter:blur(2px);
  }
  .state-revealing .glow{
    opacity:1; transform:translate(-50%,-50%) scale(1.45);
    transition: opacity .7s ease, transform 2.8s cubic-bezier(.18,.72,.2,1);
  }
  .state-revealed .glow{
    opacity:.22; transform:translate(-50%,-50%) scale(1.12);
    transition: opacity 1.8s ease, transform 1.8s ease;
  }

  /* floating motes */
  .motes{ position:fixed; inset:0; opacity:0; pointer-events:none; transition:opacity 1.8s ease; }
  .state-revealing .motes,.state-revealed .motes{ opacity:1; }
  .mote{
    position:absolute; bottom:-24px; width:7px; height:7px; border-radius:50%;
    background:radial-gradient(circle, rgba(255,250,235,.95), transparent 70%);
    animation:rise linear infinite;
  }
  @keyframes rise{
    0%  { transform:translateY(0) translateX(0);    opacity:0; }
    12% { opacity:.9; }
    100%{ transform:translateY(-112vh) translateX(var(--drift,0)); opacity:0; }
  }

  /* ---------- Stage / content ---------- */
  .stage{
    position:fixed; inset:0;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    text-align:center; padding:7vh 8vw;
  }

  .intro{ transition:opacity 1s ease; max-width:760px; }
  .state-revealing .intro,.state-revealed .intro{ opacity:0; pointer-events:none; }

  .title{
    font-family:var(--serif); font-weight:500; font-style:italic;
    font-size:clamp(2.4rem,7vw,4.6rem); letter-spacing:.02em;
    color:#f7efe0; text-shadow:0 2px 40px rgba(180,160,255,.35);
  }
  .subtitle{
    margin-top:.4rem; font-size:clamp(.85rem,2.4vw,1.1rem);
    letter-spacing:.42em; text-transform:uppercase; color:#b9b2cf; font-weight:300;
  }
  .scripture-ask{
    margin-top:1.4rem; font-family:var(--serif); font-style:italic;
    color:#8f9bbf; font-size:clamp(.85rem,2.4vw,1rem); opacity:.85;
  }

  .orb{
    margin-top:3.2rem;
    font-family:var(--serif); font-size:1.15rem; letter-spacing:.06em;
    color:#1c1530;
    padding:1.05rem 2.6rem; border:none; border-radius:999px;
    background:radial-gradient(circle at 35% 30%, #fff6e2, #f3cf87 60%, #e0ad5b);
    box-shadow:0 0 0 1px rgba(255,255,255,.4) inset,
               0 8px 40px rgba(243,207,135,.45),
               0 0 70px rgba(243,207,135,.25);
    cursor:pointer;
    transition:transform .4s ease, box-shadow .5s ease;
    animation: breathe 5.5s ease-in-out infinite;
  }
  .orb:hover{ transform:scale(1.05);
    box-shadow:0 0 0 1px rgba(255,255,255,.55) inset,
               0 10px 60px rgba(243,207,135,.6),
               0 0 110px rgba(243,207,135,.4); }
  .orb:active{ transform:scale(.97); }
  @keyframes breathe{
    0%,100%{ box-shadow:0 0 0 1px rgba(255,255,255,.4) inset,0 8px 40px rgba(243,207,135,.4),0 0 60px rgba(243,207,135,.2);}
    50%    { box-shadow:0 0 0 1px rgba(255,255,255,.5) inset,0 10px 56px rgba(243,207,135,.6),0 0 100px rgba(243,207,135,.38);}
  }
  .hint{ margin-top:1.6rem; font-size:.8rem; letter-spacing:.28em;
    text-transform:uppercase; color:#7b87a8; font-weight:300; }

  /* ---------- Revealed truth ---------- */
  .truth{
    position:absolute; max-width:880px; width:100%;
    pointer-events:none;
  }
  .truth-num,.truth-text,.truth-ref{
    opacity:0; transform:translateY(16px);
    transition:opacity 1.1s ease, transform 1.1s ease;
  }
  .truth-num{
    font-size:.95rem; letter-spacing:.38em; text-transform:uppercase;
    color:#e7c987; font-weight:400; margin-bottom:1.6rem;
    text-shadow:0 0 22px rgba(231,201,135,.4);
  }
  .truth-text{
    font-family:var(--serif); font-weight:400;
    font-size:clamp(1.7rem,4.6vw,3.1rem); line-height:1.4;
    color:#f8f2e6; text-shadow:0 2px 44px rgba(120,140,255,.25);
  }
  .truth-ref{
    margin-top:1.9rem; font-family:var(--serif); font-style:italic;
    font-size:clamp(1rem,2.6vw,1.4rem); color:#bcc6e6;
    padding-left:18%;
  }
  .state-revealed .truth-num { opacity:.95; transform:none; transition-delay:.15s; }
  .state-revealed .truth-text{ opacity:1;   transform:none; transition-delay:.55s; }
  .state-revealed .truth-ref { opacity:.9;  transform:none; transition-delay:1.25s; }

  .again{
    pointer-events:auto;
    margin-top:3.4rem;
    opacity:0; transform:translateY(16px);
    font-family:var(--serif); font-size:1rem; letter-spacing:.05em;
    color:#ece4d4; background:transparent;
    padding:.85rem 2.1rem; border:1px solid rgba(236,228,212,.4); border-radius:999px;
    cursor:pointer;
    transition:opacity 1.1s ease, transform 1.1s ease, background .4s ease, border-color .4s ease;
  }
  .state-revealed .again{ opacity:.95; transform:none; transition-delay:2s; }
  .again:hover{ background:rgba(236,228,212,.1); border-color:rgba(236,228,212,.8); }

  /* footer / treasury count */
  .treasury{
    position:fixed; bottom:max(1.4rem, env(safe-area-inset-bottom)); left:0; right:0;
    text-align:center; font-size:.72rem; letter-spacing:.26em; text-transform:uppercase;
    color:#6b7593; font-weight:300; pointer-events:none;
    transition:opacity 1s ease;
  }

  /* sound toggle */
  .mute{
    position:fixed; top:max(1.2rem, env(safe-area-inset-top)); right:1.4rem;
    width:46px; height:46px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.16);
    color:#e9e1d2; font-size:1.05rem; cursor:pointer; z-index:5;
    backdrop-filter:blur(6px);
    transition:background .3s ease, opacity .3s ease, transform .3s ease;
  }
  .mute:hover{ background:rgba(255,255,255,.14); transform:scale(1.06); }
  .mute.off{ opacity:.5; }

  @media (max-width:560px){
    .truth-ref{ padding-left:0; }
    .subtitle{ letter-spacing:.3em; }
  }
  @media (prefers-reduced-motion: reduce){
    .bg{ animation:none; } .rays{ animation:none; } .orb{ animation:none; }
  }
</style>
</head>
<body>
  <div id="app" class="state-idle">
    <div class="bg"></div>
    <div class="sweep"></div>
    <div class="rays"></div>
    <div class="motes" id="motes"></div>
    <div class="glow"></div>

    <button id="mute" class="mute" title="Toggle sound" aria-label="Toggle sound">&#9834;</button>

    <main class="stage">
      <div class="intro">
        <h1 class="title">Quid est veritas?</h1>
        <p class="subtitle">What is truth?</p>
        <p class="scripture-ask">&ldquo;Pilate said to him, &lsquo;What is truth?&rsquo;&rdquo; &mdash; John 18:38</p>
        <button id="reveal" class="orb">Reveal a Truth</button>
        <p class="hint">A treasury of 300 truths awaits</p>
      </div>

      <div class="truth" id="truth">
        <div class="truth-num">Truth&nbsp;#<span id="num"></span></div>
        <p class="truth-text" id="text"></p>
        <p class="truth-ref" id="ref"></p>
        <button id="again" class="again">Reveal Another</button>
      </div>
    </main>

    <p class="treasury" id="treasury">A treasury of 300 truths</p>
  </div>

<script>
const TRUTHS = __TRUTHS_JSON__;

/* ---------- DOM ---------- */
const app   = document.getElementById('app');
const numEl = document.getElementById('num');
const textEl= document.getElementById('text');
const refEl = document.getElementById('ref');
const revealBtn = document.getElementById('reveal');
const againBtn  = document.getElementById('again');
const muteBtn   = document.getElementById('mute');
const treasury  = document.getElementById('treasury');

/* ---------- floating motes ---------- */
(function makeMotes(){
  const wrap = document.getElementById('motes');
  for(let i=0;i<34;i++){
    const m = document.createElement('span');
    m.className = 'mote';
    const s = 3 + Math.random()*7;
    m.style.left = (Math.random()*100) + 'vw';
    m.style.width = s + 'px';
    m.style.height = s + 'px';
    m.style.opacity = (0.3 + Math.random()*0.6).toFixed(2);
    m.style.animationDuration = (10 + Math.random()*16) + 's';
    m.style.animationDelay = (-Math.random()*20) + 's';
    m.style.setProperty('--drift', (Math.random()*120-60)+'px');
    wrap.appendChild(m);
  }
})();

/* ---------- truth selection (shuffled bag, no repeats until exhausted) ---------- */
let bag = [];
let seen = new Set();
function refill(){
  bag = TRUTHS.map((_,i)=>i);
  for(let i=bag.length-1;i>0;i--){ const j=(Math.random()*(i+1))|0; [bag[i],bag[j]]=[bag[j],bag[i]]; }
}
function pickTruth(){
  if(bag.length===0) refill();
  const t = TRUTHS[bag.pop()];
  seen.add(t.n);
  return t;
}

/* ================= AUDIO ENGINE (procedural, fully embedded) ================= */
let actx=null, master=null, reverb=null, ambientGain=null, started=false, muted=false;

function fade(param,to,sec){
  const t=actx.currentTime;
  param.cancelScheduledValues(t);
  param.setValueAtTime(param.value,t);
  param.linearRampToValueAtTime(to,t+sec);
}
function noiseBuffer(dur){
  const len=Math.floor(actx.sampleRate*dur);
  const b=actx.createBuffer(1,len,actx.sampleRate);
  const d=b.getChannelData(0);
  for(let i=0;i<len;i++) d[i]=Math.random()*2-1;
  return b;
}
function makeIR(dur,decay){
  const len=Math.floor(actx.sampleRate*dur);
  const b=actx.createBuffer(2,len,actx.sampleRate);
  for(let c=0;c<2;c++){
    const d=b.getChannelData(c);
    for(let i=0;i<len;i++) d[i]=(Math.random()*2-1)*Math.pow(1-i/len,decay);
  }
  return b;
}

function initAudio(){
  if(started) return;
  started=true;
  const AC = window.AudioContext || window.webkitAudioContext;
  actx = new AC();

  master = actx.createGain();
  master.gain.value = 0.0001;
  master.connect(actx.destination);

  reverb = actx.createConvolver();
  reverb.buffer = makeIR(3.6, 2.2);
  const revGain = actx.createGain();
  revGain.gain.value = 0.85;
  reverb.connect(revGain);
  revGain.connect(master);

  startAmbient();
  if(!muted) fade(master.gain, 0.9, 4);
}

function startAmbient(){
  // A gentle, sustained A-major-ish chord, softly breathing.
  const freqs=[110.00,164.81,220.00,277.18,329.63];
  const fil=actx.createBiquadFilter();
  fil.type='lowpass'; fil.frequency.value=950; fil.Q.value=0.6;

  ambientGain=actx.createGain(); ambientGain.gain.value=0.0;
  fil.connect(ambientGain);
  ambientGain.connect(master);   // dry
  ambientGain.connect(reverb);   // wet

  freqs.forEach((f,i)=>{
    const o=actx.createOscillator();
    o.type = (i%2)? 'sine':'triangle';
    o.frequency.value=f;
    o.detune.value=(Math.random()*8-4);
    const g=actx.createGain(); g.gain.value=0.05;
    o.connect(g); g.connect(fil); o.start();
    // slow amplitude shimmer
    const lfo=actx.createOscillator(); lfo.frequency.value=0.04+Math.random()*0.06;
    const la=actx.createGain(); la.gain.value=0.028;
    lfo.connect(la); la.connect(g.gain); lfo.start();
  });

  // slow filter sweep so the pad gently opens and closes
  const flfo=actx.createOscillator(); flfo.frequency.value=0.025;
  const fa=actx.createGain(); fa.gain.value=320;
  flfo.connect(fa); fa.connect(fil.frequency); flfo.start();

  fade(ambientGain.gain, 0.5, 5);
}

// a soft bell tone (additive partials with long decay)
function bell(freq,t0,dur,vol){
  const partials=[[1,1],[2.0,0.45],[2.76,0.3],[3.95,0.18],[5.4,0.1]];
  partials.forEach(([m,a])=>{
    const o=actx.createOscillator(); o.type='sine'; o.frequency.value=freq*m;
    const g=actx.createGain();
    g.gain.setValueAtTime(0.0001,t0);
    g.gain.linearRampToValueAtTime(vol*a,t0+0.012);
    g.gain.exponentialRampToValueAtTime(0.0001,t0+dur);
    o.connect(g); g.connect(master); g.connect(reverb);
    o.start(t0); o.stop(t0+dur+0.1);
  });
}

// rising swell during the build-up
function buildupSound(){
  if(!actx) return;
  const t0=actx.currentTime, dur=2.55;

  const src=actx.createBufferSource(); src.buffer=noiseBuffer(dur+0.4);
  const bp=actx.createBiquadFilter(); bp.type='bandpass'; bp.Q.value=3.5;
  bp.frequency.setValueAtTime(280,t0);
  bp.frequency.exponentialRampToValueAtTime(3200,t0+dur);
  const ng=actx.createGain();
  ng.gain.setValueAtTime(0.0001,t0);
  ng.gain.exponentialRampToValueAtTime(0.16,t0+dur);
  ng.gain.exponentialRampToValueAtTime(0.0001,t0+dur+0.35);
  src.connect(bp); bp.connect(ng); ng.connect(master); ng.connect(reverb);
  src.start(t0); src.stop(t0+dur+0.5);

  // rising shimmer pad
  const o=actx.createOscillator(); o.type='triangle';
  o.frequency.setValueAtTime(220,t0);
  o.frequency.exponentialRampToValueAtTime(660,t0+dur);
  const og=actx.createGain();
  og.gain.setValueAtTime(0.0001,t0);
  og.gain.exponentialRampToValueAtTime(0.07,t0+dur);
  og.gain.exponentialRampToValueAtTime(0.0001,t0+dur+0.45);
  o.connect(og); og.connect(master); og.connect(reverb);
  o.start(t0); o.stop(t0+dur+0.6);
}

// gentle ascending arpeggio at the moment of reveal
function revealChime(){
  if(!actx) return;
  const t=actx.currentTime;
  const notes=[440.00,554.37,659.25,880.00]; // A C# E A
  notes.forEach((f,i)=> bell(f, t + i*0.17, 3.4, 0.15));
}

/* ---------- mute ---------- */
function applyMute(){
  muteBtn.classList.toggle('off', muted);
  muteBtn.innerHTML = muted ? '&#128263;' : '&#9834;';
  if(actx && master) fade(master.gain, muted?0.0001:0.9, 1.2);
}
muteBtn.addEventListener('click', ()=>{ muted=!muted; applyMute(); });

/* ================= REVEAL FLOW ================= */
let busy=false, tA=null, tB=null;

function reveal(){
  if(busy) return;
  busy=true;
  initAudio();
  if(actx && actx.state==='suspended') actx.resume();

  const t=pickTruth();
  numEl.textContent = t.n;
  textEl.textContent = t.text;
  refEl.textContent = '— ' + t.ref;

  app.classList.remove('state-idle','state-revealed');
  // force reflow so re-revealing restarts the sweep animation
  void app.offsetWidth;
  app.classList.add('state-revealing');
  treasury.style.opacity = '0';

  buildupSound();

  clearTimeout(tA); clearTimeout(tB);
  tA=setTimeout(revealChime, 2350);
  tB=setTimeout(()=>{
    app.classList.remove('state-revealing');
    app.classList.add('state-revealed');
    treasury.textContent = seen.size + ' of 300 truths beheld';
    treasury.style.opacity = '0.9';
    busy=false;
  }, 2750);
}

revealBtn.addEventListener('click', reveal);
againBtn.addEventListener('click', reveal);

// allow space / enter to reveal
window.addEventListener('keydown', e=>{
  if((e.code==='Space'||e.code==='Enter') && !busy){ e.preventDefault(); reveal(); }
});
</script>
</body>
</html>
'''

html = TEMPLATE.replace('__TRUTHS_JSON__', truths_json)
open('index.html', 'w', encoding='utf-8').write(html)
print('index.html written,', len(truths), 'truths,', len(html), 'bytes')
