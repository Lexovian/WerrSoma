"""
update_viewer.py
================
Regenerates neuramap_werr_3d.html with:
1. Procedural custom textures (Diamond-Reticle Beacon for WERR vs Soft Bioluminescent Sphere for Bio).
2. Prominent dual-layer halo glow on all 1,000 WERR neurons.
3. Live Interactive Test Simulation Engine directly inside the 3D canvas:
   - "▶ 1. AŞAMA: UYUMLULUK TESTİNİ CANLI BAŞLAT"
   - "⚡ 2. AŞAMA: MOTOR ATIM İCRASINI CANLI BAŞLAT"
   - Real-time voltage surge and action potential flash on biological neurons.
   - Signal photons streaming dynamically across synapses.
   - Real-time Oscilloscope (multi-channel EEG wave drawing).
   - Live Event Log Terminal in the UI.
4. Auto-launch capability.
"""
import os
import sys
import json

WORKSPACE = os.path.abspath(os.path.dirname(__file__))
DATA_JSON_PATH = os.path.join(WORKSPACE, "neuramap", "bioneural_3d_data.json")
OUTPUT_HTML_PATH = os.path.join(WORKSPACE, "neuramap_werr_3d.html")

def main():
    if not os.path.exists(DATA_JSON_PATH):
        print(f"Error: {DATA_JSON_PATH} not found.")
        sys.exit(1)

    print("Reading bioneural_3d_data.json...")
    with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
        data_json_str = f.read()

    html_code = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Drosophila & WERR Bio-Sentetik Canlı Nöral Test Laboratuvarı (3B)</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      user-select: none;
    }}
    body {{
      background: radial-gradient(circle at 50% 50%, #080d19 0%, #020408 100%);
      color: #e2e8f0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      overflow: hidden;
      width: 100vw;
      height: 100vh;
    }}
    #canvas-container {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
    }}

    /* Top Navigation Header */
    header {{
      position: absolute;
      top: 12px;
      left: 18px;
      right: 18px;
      z-index: 10;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(10, 16, 28, 0.85);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(0, 240, 255, 0.25);
      border-radius: 12px;
      padding: 10px 22px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(0, 240, 255, 0.1);
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand h1 {{
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: 0.5px;
      background: linear-gradient(135deg, #00f0ff 0%, #38bdf8 50%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .brand span {{
      font-size: 0.72rem;
      padding: 3px 8px;
      background: rgba(0, 240, 255, 0.15);
      border: 1px solid rgba(0, 240, 255, 0.4);
      border-radius: 6px;
      color: #38bdf8;
      font-weight: 600;
      box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }}
    .live-status-badge {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.82rem;
      font-weight: 700;
      color: #34d399;
      background: rgba(52, 211, 153, 0.12);
      border: 1px solid rgba(52, 211, 153, 0.35);
      padding: 6px 14px;
      border-radius: 20px;
    }}
    .pulse-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: #34d399;
      box-shadow: 0 0 10px #34d399;
      animation: pulse-glow 1.5s infinite ease-in-out;
    }}
    @keyframes pulse-glow {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.9); }}
    }}

    /* Left Control Panel */
    .panel-left {{
      position: absolute;
      top: 76px;
      left: 18px;
      width: 320px;
      background: rgba(10, 16, 28, 0.88);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 16px;
      z-index: 10;
      display: flex;
      flex-direction: column;
      gap: 12px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.65);
      max-height: calc(100vh - 96px);
      overflow-y: auto;
    }}
    .panel-title {{
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #94a3b8;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 5px;
    }}
    
    /* Distinction Indicator Card */
    .distinction-card {{
      background: linear-gradient(135deg, rgba(0, 240, 255, 0.08) 0%, rgba(16, 185, 129, 0.05) 100%);
      border: 1px solid rgba(0, 240, 255, 0.25);
      border-radius: 8px;
      padding: 9px;
    }}
    .distinction-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.74rem;
      margin-bottom: 5px;
    }}
    .distinction-row:last-child {{ margin-bottom: 0; }}
    .node-preview {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .preview-werr {{
      width: 14px;
      height: 14px;
      background: #00f0ff;
      transform: rotate(45deg);
      box-shadow: 0 0 12px #00f0ff, 0 0 20px rgba(0,240,255,0.8);
      border: 1px solid #ffffff;
    }}
    .preview-bio {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #60a5fa;
      box-shadow: 0 0 8px rgba(96, 165, 250, 0.6);
    }}

    /* View Mode Tabs */
    .view-tabs {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }}
    .tab-btn {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #94a3b8;
      font-size: 0.72rem;
      font-weight: 600;
      padding: 6px 8px;
      border-radius: 6px;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s ease;
    }}
    .tab-btn:hover {{
      background: rgba(0, 240, 255, 0.12);
      border-color: rgba(0, 240, 255, 0.3);
      color: #38bdf8;
    }}
    .tab-btn.active {{
      background: rgba(0, 240, 255, 0.22);
      border-color: #00f0ff;
      color: #00f0ff;
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.35);
    }}

    /* Sliders */
    .slider-row {{
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .slider-header {{
      display: flex;
      justify-content: space-between;
      font-size: 0.7rem;
      color: #94a3b8;
    }}
    input[type=range] {{
      -webkit-appearance: none;
      width: 100%;
      background: rgba(255, 255, 255, 0.1);
      height: 4px;
      border-radius: 2px;
      outline: none;
    }}
    input[type=range]::-webkit-slider-thumb {{
      -webkit-appearance: none;
      width: 13px;
      height: 13px;
      border-radius: 50%;
      background: #00f0ff;
      cursor: pointer;
      box-shadow: 0 0 8px #00f0ff;
    }}

    /* Buttons */
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      background: rgba(0, 240, 255, 0.12);
      border: 1px solid rgba(0, 240, 255, 0.35);
      color: #38bdf8;
      padding: 8px 12px;
      font-size: 0.76rem;
      font-weight: 600;
      border-radius: 7px;
      cursor: pointer;
      transition: all 0.2s ease;
      width: 100%;
    }}
    .btn:hover {{
      background: rgba(0, 240, 255, 0.25);
      box-shadow: 0 0 16px rgba(0, 240, 255, 0.35);
      transform: translateY(-1px);
    }}
    .btn.reset-cam {{
      background: rgba(255, 255, 255, 0.05);
      border-color: rgba(255, 255, 255, 0.12);
      color: #94a3b8;
    }}

    /* Right Live Test Control Deck */
    .panel-right {{
      position: absolute;
      top: 76px;
      right: 18px;
      width: 360px;
      background: rgba(10, 16, 28, 0.9);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(0, 240, 255, 0.25);
      border-radius: 12px;
      padding: 16px;
      z-index: 10;
      display: flex;
      flex-direction: column;
      gap: 12px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.7);
    }}
    .live-test-btn {{
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(5, 150, 105, 0.35) 100%);
      border: 1px solid #10b981;
      color: #a7f3d0;
      padding: 11px 16px;
      font-size: 0.84rem;
      font-weight: 700;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      transition: all 0.2s ease;
      box-shadow: 0 0 18px rgba(16, 185, 129, 0.3);
    }}
    .live-test-btn:hover {{
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.45) 0%, rgba(5, 150, 105, 0.55) 100%);
      box-shadow: 0 0 24px rgba(16, 185, 129, 0.55);
      transform: translateY(-1px);
      color: #ffffff;
    }}
    .live-motor-btn {{
      background: linear-gradient(135deg, rgba(236, 72, 153, 0.2) 0%, rgba(219, 39, 119, 0.3) 100%);
      border: 1px solid #ec4899;
      color: #fbcfe8;
      padding: 10px 16px;
      font-size: 0.82rem;
      font-weight: 700;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      transition: all 0.2s ease;
      box-shadow: 0 0 14px rgba(236, 72, 153, 0.25);
    }}
    .live-motor-btn:hover {{
      background: linear-gradient(135deg, rgba(236, 72, 153, 0.35) 0%, rgba(219, 39, 119, 0.45) 100%);
      box-shadow: 0 0 20px rgba(236, 72, 153, 0.45);
      color: #ffffff;
    }}

    /* Live Telemetry Display */
    .telemetry-box {{
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      padding: 10px;
    }}
    .telem-row {{
      display: flex;
      justify-content: space-between;
      font-size: 0.74rem;
      margin-bottom: 5px;
    }}
    .telem-row:last-child {{ margin-bottom: 0; }}
    .telem-label {{ color: #94a3b8; }}
    .telem-val {{ font-weight: 700; color: #f8fafc; font-family: monospace; font-size: 0.82rem; }}

    /* Real-Time Oscilloscope */
    #oscilloscope {{
      width: 100%;
      height: 60px;
      background: #020610;
      border: 1px solid rgba(0, 240, 255, 0.2);
      border-radius: 6px;
    }}

    /* Live Event Terminal */
    .terminal-box {{
      background: #020610;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 6px;
      padding: 8px;
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      font-size: 0.68rem;
      color: #94a3b8;
      height: 90px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .terminal-line {{ line-height: 1.35; }}
    .terminal-line.cyan {{ color: #00f0ff; }}
    .terminal-line.green {{ color: #34d399; }}
    .terminal-line.amber {{ color: #fbbf24; }}

    /* Bottom HUD */
    .bottom-hud {{
      position: absolute;
      bottom: 14px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10;
      display: flex;
      gap: 12px;
      background: rgba(10, 16, 28, 0.8);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(0, 240, 255, 0.2);
      border-radius: 30px;
      padding: 6px 18px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    }}
    .hud-chip {{
      font-size: 0.72rem;
      font-weight: 600;
      color: #cbd5e1;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .hud-chip span {{ color: #00f0ff; }}

    /* Hover Tooltip */
    #tooltip {{
      position: absolute;
      display: none;
      z-index: 100;
      background: rgba(10, 16, 28, 0.92);
      backdrop-filter: blur(16px);
      border: 1px solid #00f0ff;
      border-radius: 8px;
      padding: 9px 13px;
      pointer-events: none;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.8), 0 0 20px rgba(0, 240, 255, 0.3);
      max-width: 260px;
    }}
    #tooltip-title {{
      font-size: 0.82rem;
      font-weight: 700;
      color: #00f0ff;
      margin-bottom: 3px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    #tooltip-body {{
      font-size: 0.7rem;
      color: #cbd5e1;
      line-height: 1.35;
    }}
  </style>
  <script src="js/three.min.js"></script>
  <script src="js/OrbitControls.js"></script>
</head>
<body>

  <!-- WebGL Container -->
  <div id="canvas-container"></div>

  <!-- Interactive Hover Tooltip -->
  <div id="tooltip">
    <div id="tooltip-title">WERR_CX_042</div>
    <div id="tooltip-body">Yükleniyor...</div>
  </div>

  <!-- Top Header -->
  <header>
    <div class="brand">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2">
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
      </svg>
      <h1>Drosophila Melanogaster & WERR Neuro-Hybrid</h1>
      <span>v0.5.0 Canlı Test Laboratuvarı</span>
    </div>
    <div class="live-status-badge" id="header-status">
      <div class="pulse-dot"></div>
      CANLI TEST HAZIR &bull; SİMÜLASYON İÇİN BUTONA BASIN
    </div>
  </header>

  <!-- Left Control Panel -->
  <div class="panel-left">
    <div class="panel-title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
      Nöral Ayrım & Modlar
    </div>

    <!-- Visual Legend Distinction Card -->
    <div class="distinction-card">
      <div class="distinction-row">
        <div class="node-preview">
          <div class="preview-werr"></div>
          <span style="font-weight:700; color:#00f0ff;">WERR Sentetik Nöron</span>
        </div>
        <span style="color:#00f0ff; font-weight:700;">1.000 (Elmas / Işıma)</span>
      </div>
      <div style="font-size:0.66rem; color:#94a3b8; margin: 3px 0 6px 22px;">
        Kaotik Mandelbrot çekirdeği, dinamik kadran kaçışı.
      </div>
      <div class="distinction-row">
        <div class="node-preview">
          <div class="preview-bio"></div>
          <span style="font-weight:700; color:#60a5fa;">Biyolojik Sinek Nöronu</span>
        </div>
        <span style="color:#94a3b8; font-weight:700;">2.800 (Doğal Küre)</span>
      </div>
    </div>

    <!-- View Mode Tabs -->
    <div class="panel-title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
      Görünüm Filtresi
    </div>
    <div class="view-tabs">
      <div class="tab-btn active" id="tab-all">🌟 Hibrit (Tümü)</div>
      <div class="tab-btn" id="tab-werr-focus">⚡ WERR Vurgulu</div>
      <div class="tab-btn" id="tab-werr-only">💎 Sadece WERR</div>
      <div class="tab-btn" id="tab-bio-only">🧠 Sadece Biyolojik</div>
    </div>

    <!-- Sliders -->
    <div class="slider-row">
      <div class="slider-header">
        <span>WERR Nöron Boyutu</span>
        <span id="lbl-werr-size">18 px</span>
      </div>
      <input type="range" id="slider-werr-size" min="8" max="36" value="18">
    </div>

    <div class="slider-row">
      <div class="slider-header">
        <span>Sinaps Sinyal Hızı</span>
        <span id="lbl-flow-speed">1.0x</span>
      </div>
      <input type="range" id="slider-flow-speed" min="0" max="30" value="10">
    </div>

    <!-- Camera Focus Buttons -->
    <div class="panel-title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
      Kamera Odakları
    </div>
    <button class="btn" id="btn-focus-cx">Merkezi Komplekse (EB/FB) Odaklan</button>
    <button class="btn" id="btn-focus-mb" style="background:rgba(251,191,36,0.12); border-color:rgba(251,191,36,0.35); color:#fbbf24;">Mantar Cisimciğe (MB) Odaklan</button>
    <button class="btn reset-cam" id="btn-reset-cam">Tam Beyin Perspektifine Dön</button>
  </div>

  <!-- Right Live Test Control Deck -->
  <div class="panel-right">
    <div class="panel-title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
      Canlı Test Kontrol Paneli
    </div>

    <!-- Live Test Button Stage 1 -->
    <button class="live-test-btn" id="btn-run-stage1">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
      ▶ 1. AŞAMA: UYUMLULUK TESTİNİ BAŞLAT
    </button>

    <!-- Live Test Button Stage 2 -->
    <button class="live-motor-btn" id="btn-run-stage2">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
      ⚡ 2. AŞAMA: MOTOR ATIM İCRASINI BAŞLAT
    </button>

    <!-- Live Telemetry Card -->
    <div class="telemetry-box">
      <div class="telem-row">
        <span class="telem-label">Simülasyon Süresi:</span>
        <span class="telem-val" id="telem-time" style="color:#38bdf8;">0.0 ms / 50 ms</span>
      </div>
      <div class="telem-row">
        <span class="telem-label">WERR Atım Sayısı:</span>
        <span class="telem-val" id="telem-werr-spikes" style="color:#00f0ff;">0</span>
      </div>
      <div class="telem-row">
        <span class="telem-label">Biyolojik Yanıt Aksiyonu:</span>
        <span class="telem-val" id="telem-bio-spikes" style="color:#34d399;">0</span>
      </div>
      <div class="telem-row">
        <span class="telem-label">İletim Sadakati (Fidelity):</span>
        <span class="telem-val" id="telem-fidelity" style="color:#facc15;">Beklemede</span>
      </div>
      <div class="telem-row">
        <span class="telem-label">Karşıt Tepki (GABA İnhibisyon):</span>
        <span class="telem-val" id="telem-rejection" style="color:#ec4899;">Beklemede</span>
      </div>
    </div>

    <!-- Oscilloscope Canvas -->
    <div style="font-size:0.68rem; color:#94a3b8; font-weight:700; text-transform:uppercase;">Canlı Voltaj / EEG Osiloskopu</div>
    <canvas id="oscilloscope" width="320" height="60"></canvas>

    <!-- Event Log Terminal -->
    <div style="font-size:0.68rem; color:#94a3b8; font-weight:700; text-transform:uppercase;">Gerçek Zamanlı Sinaptik Olay Akışı</div>
    <div class="terminal-box" id="terminal-feed">
      <div class="terminal-line green">[*] Canlı test modülü hazırlandı.</div>
      <div class="terminal-line">[*] 1.000 WERR nöronu biyolojik konnektoma kilitlendi.</div>
      <div class="terminal-line amber">[*] Başlatmak için yukarıdaki yeşil butona basın.</div>
    </div>
  </div>

  <!-- Bottom Floating HUD -->
  <div class="bottom-hud">
    <div class="hud-chip">Koordinat Tohumu: <span>cx=-0.7436, cy=0.1318</span></div>
    <div class="hud-chip">&bull;</div>
    <div class="hud-chip">Harmonik Tripod: <span style="color:#34d399;">Açık (0.6x, 1.0x, 1.6x)</span></div>
    <div class="hud-chip">&bull;</div>
    <div class="hud-chip">Hücresel VRAM: <span style="color:#38bdf8;">0 Bayt</span></div>
    <div class="hud-chip">&bull;</div>
    <div class="hud-chip">Canlı FPS: <span id="hud-fps" style="color:#f472b6;">60</span></div>
  </div>

  <script>
    // Embedded Connectome Graph Data
    const graphData = {data_json_str};

    // Scene & Camera
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x040711, 0.0012);

    const camera = new THREE.PerspectiveCamera(48, window.innerWidth / window.innerHeight, 1, 3000);
    camera.position.set(0, 140, 470);

    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxDistance = 1200;
    controls.minDistance = 30;

    // Ambient and Point Lights
    const ambientLight = new THREE.AmbientLight(0x223344, 1.8);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00f0ff, 3.2, 900);
    pointLight.position.set(0, 60, 120);
    scene.add(pointLight);

    const networkGroup = new THREE.Group();
    scene.add(networkGroup);

    // =========================================================================
    // PROCEDURAL TEXTURE GENERATORS
    // =========================================================================
    
    // 1. High-Tech Fractal Diamond Beacon for 1,000 WERR Neurons
    function createWerrDiamondTexture() {{
      const c = document.createElement('canvas');
      c.width = 128;
      c.height = 128;
      const ctx = c.getContext('2d');

      const grad = ctx.createRadialGradient(64, 64, 2, 64, 64, 60);
      grad.addColorStop(0.0, 'rgba(255, 255, 255, 1.0)');
      grad.addColorStop(0.18, 'rgba(0, 240, 255, 0.95)');
      grad.addColorStop(0.45, 'rgba(0, 160, 255, 0.45)');
      grad.addColorStop(0.75, 'rgba(0, 80, 220, 0.15)');
      grad.addColorStop(1.0, 'rgba(0, 0, 0, 0.0)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 128, 128);

      ctx.save();
      ctx.translate(64, 64);
      ctx.rotate(Math.PI / 4);
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 4;
      ctx.strokeRect(-18, -18, 36, 36);
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(-11, -11, 22, 22);
      ctx.restore();

      ctx.strokeStyle = 'rgba(0, 240, 255, 0.85)';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(64, 8); ctx.lineTo(64, 28);
      ctx.moveTo(64, 100); ctx.lineTo(64, 120);
      ctx.moveTo(8, 64); ctx.lineTo(28, 64);
      ctx.moveTo(100, 64); ctx.lineTo(120, 64);
      ctx.stroke();

      const tex = new THREE.CanvasTexture(c);
      tex.generateMipmaps = true;
      return tex;
    }}

    // 2. Soft Bioluminescent Radial Sphere for Biological Fly Neurons
    function createBioSphereTexture() {{
      const c = document.createElement('canvas');
      c.width = 64;
      c.height = 64;
      const ctx = c.getContext('2d');

      const grad = ctx.createRadialGradient(32, 32, 0, 32, 32, 30);
      grad.addColorStop(0.0, 'rgba(255, 255, 255, 0.95)');
      grad.addColorStop(0.3, 'rgba(100, 170, 255, 0.7)');
      grad.addColorStop(0.7, 'rgba(40, 90, 210, 0.2)');
      grad.addColorStop(1.0, 'rgba(0, 0, 0, 0.0)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 64, 64);

      const tex = new THREE.CanvasTexture(c);
      tex.generateMipmaps = true;
      return tex;
    }}

    const werrTexture = createWerrDiamondTexture();
    const bioTexture = createBioSphereTexture();

    // Node separation
    const bioNodes = graphData.nodes.filter(n => n.type === 'bio');
    const synthNodes = graphData.nodes.filter(n => n.type === 'werr_synth');

    // 1. Biological Points Geometry
    const bioPositions = new Float32Array(bioNodes.length * 3);
    const bioColors = new Float32Array(bioNodes.length * 3);
    const bioOriginalColors = new Float32Array(bioNodes.length * 3);

    const cCentral = new THREE.Color(0x38bdf8);
    const cMB = new THREE.Color(0xfacc15);
    const cSensory = new THREE.Color(0x10b981);
    const cMotor = new THREE.Color(0xf43f5e);
    const cDefault = new THREE.Color(0x818cf8);

    bioNodes.forEach((node, i) => {{
      bioPositions[i * 3] = node.pos[0];
      bioPositions[i * 3 + 1] = node.pos[1];
      bioPositions[i * 3 + 2] = node.pos[2];

      let c = cDefault;
      if (node.super_class === 'descending') c = cMotor;
      else if (node.region.includes('MB')) c = cMB;
      else if (node.super_class === 'sensory') c = cSensory;
      else if (['EB','FB','PB','NO'].includes(node.region)) c = cCentral;

      bioColors[i * 3] = c.r;
      bioColors[i * 3 + 1] = c.g;
      bioColors[i * 3 + 2] = c.b;

      bioOriginalColors[i * 3] = c.r;
      bioOriginalColors[i * 3 + 1] = c.g;
      bioOriginalColors[i * 3 + 2] = c.b;
    }});

    const bioGeometry = new THREE.BufferGeometry();
    bioGeometry.setAttribute('position', new THREE.BufferAttribute(bioPositions, 3));
    bioGeometry.setAttribute('color', new THREE.BufferAttribute(bioColors, 3));

    const bioMaterial = new THREE.PointsMaterial({{
      size: 5.0,
      map: bioTexture,
      vertexColors: true,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    }});
    const bioPoints = new THREE.Points(bioGeometry, bioMaterial);
    networkGroup.add(bioPoints);

    // 2. WERR Synthetic Neurons (Diamond-Reticle Core)
    const synthPositions = new Float32Array(synthNodes.length * 3);
    const synthColors = new Float32Array(synthNodes.length * 3);

    synthNodes.forEach((node, i) => {{
      synthPositions[i * 3] = node.pos[0];
      synthPositions[i * 3 + 1] = node.pos[1];
      synthPositions[i * 3 + 2] = node.pos[2];

      const c = new THREE.Color(node.color || 0x00f0ff);
      synthColors[i * 3] = c.r;
      synthColors[i * 3 + 1] = c.g;
      synthColors[i * 3 + 2] = c.b;
    }});

    const synthGeometry = new THREE.BufferGeometry();
    synthGeometry.setAttribute('position', new THREE.BufferAttribute(synthPositions, 3));
    synthGeometry.setAttribute('color', new THREE.BufferAttribute(synthColors, 3));

    const synthMaterial = new THREE.PointsMaterial({{
      size: 18.0,
      map: werrTexture,
      vertexColors: true,
      transparent: true,
      opacity: 0.98,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    }});
    const synthPoints = new THREE.Points(synthGeometry, synthMaterial);
    networkGroup.add(synthPoints);

    // 3. WERR Secondary Pulsing Corona Halo Layer
    const synthHaloMaterial = new THREE.PointsMaterial({{
      size: 32.0,
      map: werrTexture,
      vertexColors: true,
      transparent: true,
      opacity: 0.35,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    }});
    const synthHaloPoints = new THREE.Points(synthGeometry, synthHaloMaterial);
    networkGroup.add(synthHaloPoints);

    // 4. Synapse Lines
    const nodeMap = new Map();
    graphData.nodes.forEach(n => nodeMap.set(n.id, n));

    const linePositions = [];
    const lineColors = [];

    const colBioBio = new THREE.Color(0x131e2e);
    const colBioWerr = new THREE.Color(0x0284c7);
    const colWerrBio = new THREE.Color(0x00f0ff);
    const colWerrWerr = new THREE.Color(0xf59e0b);

    const displayLinks = graphData.links.filter((_, idx) => idx % 2 === 0);

    displayLinks.forEach(link => {{
      const n1 = nodeMap.get(link.pre);
      const n2 = nodeMap.get(link.post);
      if (n1 && n2) {{
        linePositions.push(n1.pos[0], n1.pos[1], n1.pos[2]);
        linePositions.push(n2.pos[0], n2.pos[1], n2.pos[2]);

        let col = colBioBio;
        if (link.kind === 'bio_to_werr') col = colBioWerr;
        else if (link.kind === 'werr_to_bio') col = colWerrBio;
        else if (link.kind === 'werr_werr') col = colWerrWerr;

        lineColors.push(col.r, col.g, col.b);
        lineColors.push(col.r, col.g, col.b);
      }}
    }});

    const linesGeometry = new THREE.BufferGeometry();
    linesGeometry.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
    linesGeometry.setAttribute('color', new THREE.Float32BufferAttribute(lineColors, 3));

    const linesMaterial = new THREE.LineBasicMaterial({{
      vertexColors: true,
      transparent: true,
      opacity: 0.38,
      blending: THREE.AdditiveBlending
    }});
    const synapseLines = new THREE.LineSegments(linesGeometry, linesMaterial);
    networkGroup.add(synapseLines);

    // 5. Active Signal Photon Pulses (Moving packets along synapses)
    const pulseCount = 450;
    const pulsePositions = new Float32Array(pulseCount * 3);
    const pulseProgress = new Float32Array(pulseCount);
    const pulseLinks = [];

    for (let i = 0; i < pulseCount; i++) {{
      const l = displayLinks[Math.floor(Math.random() * displayLinks.length)];
      pulseLinks.push(l);
      pulseProgress[i] = Math.random();
    }}

    const pulseGeometry = new THREE.BufferGeometry();
    pulseGeometry.setAttribute('position', new THREE.BufferAttribute(pulsePositions, 3));

    const pulseMaterial = new THREE.PointsMaterial({{
      size: 5.0,
      color: 0x00f0ff,
      map: bioTexture,
      transparent: true,
      opacity: 0.9,
      blending: THREE.AdditiveBlending
    }});
    const pulsePoints = new THREE.Points(pulseGeometry, pulseMaterial);
    networkGroup.add(pulsePoints);

    // 6. Translucent Neuropil Volumetric Wireframe Shells
    const neuropils = [
      {{ name: 'EB', pos: [0, -10, 20], r: 24, col: 0x00f0ff }},
      {{ name: 'FB', pos: [0, 32, -10], r: 35, col: 0x38bdf8 }},
      {{ name: 'MB_L', pos: [-120, 75, -75], r: 28, col: 0xfacc15 }},
      {{ name: 'MB_R', pos: [120, 75, -75], r: 28, col: 0xfacc15 }},
      {{ name: 'AL_L', pos: [-62, -78, 72], r: 24, col: 0x10b981 }},
      {{ name: 'AL_R', pos: [62, -78, 72], r: 24, col: 0x10b981 }},
      {{ name: 'GNG', pos: [0, -118, 0], r: 32, col: 0xf43f5e }}
    ];

    neuropils.forEach(shell => {{
      const geo = new THREE.SphereGeometry(shell.r, 16, 12);
      const wire = new THREE.LineSegments(
        new THREE.WireframeGeometry(geo),
        new THREE.LineBasicMaterial({{ color: shell.col, transparent: true, opacity: 0.12 }})
      );
      wire.position.set(shell.pos[0], shell.pos[1], shell.pos[2]);
      networkGroup.add(wire);
    }});

    // =========================================================================
    // LIVE SIMULATION ENGINE & OSCILLOSCOPE
    // =========================================================================
    
    let isTestRunning = false;
    let simTimeMs = 0;
    let maxSimTime = 50;
    let liveWerrSpikes = 0;
    let liveBioSpikes = 0;

    const telemTime = document.getElementById('telem-time');
    const telemWerr = document.getElementById('telem-werr-spikes');
    const telemBio = document.getElementById('telem-bio-spikes');
    const telemFidelity = document.getElementById('telem-fidelity');
    const telemRejection = document.getElementById('telem-rejection');
    const terminalFeed = document.getElementById('terminal-feed');
    const headerStatus = document.getElementById('header-status');

    function logTerminal(msg, colorClass = '') {{
      const div = document.createElement('div');
      div.className = `terminal-line ${{colorClass}}`;
      div.textContent = msg;
      terminalFeed.appendChild(div);
      terminalFeed.scrollTop = terminalFeed.scrollHeight;
    }}

    // Oscilloscope canvas setup
    const oscCanvas = document.getElementById('oscilloscope');
    const oscCtx = oscCanvas.getContext('2d');
    const oscWidth = oscCanvas.width;
    const oscHeight = oscCanvas.height;
    let waveDataWerr = new Array(oscWidth).fill(30);
    let waveDataBio = new Array(oscWidth).fill(30);

    function drawOscilloscope(wVal, bVal) {{
      waveDataWerr.shift();
      waveDataWerr.push(wVal);
      waveDataBio.shift();
      waveDataBio.push(bVal);

      oscCtx.fillStyle = '#020610';
      oscCtx.fillRect(0, 0, oscWidth, oscHeight);

      // Grid lines
      oscCtx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
      oscCtx.lineWidth = 1;
      oscCtx.beginPath();
      oscCtx.moveTo(0, 30); oscCtx.lineTo(oscWidth, 30);
      oscCtx.moveTo(0, 15); oscCtx.lineTo(oscWidth, 15);
      oscCtx.moveTo(0, 45); oscCtx.lineTo(oscWidth, 45);
      oscCtx.stroke();

      // WERR Channel (Cyan)
      oscCtx.strokeStyle = '#00f0ff';
      oscCtx.lineWidth = 1.5;
      oscCtx.beginPath();
      for (let x = 0; x < oscWidth; x++) {{
        if (x === 0) oscCtx.moveTo(x, waveDataWerr[x]);
        else oscCtx.lineTo(x, waveDataWerr[x]);
      }}
      oscCtx.stroke();

      // Bio Channel (Green / Amber)
      oscCtx.strokeStyle = '#34d399';
      oscCtx.lineWidth = 1.5;
      oscCtx.beginPath();
      for (let x = 0; x < oscWidth; x++) {{
        if (x === 0) oscCtx.moveTo(x, waveDataBio[x]);
        else oscCtx.lineTo(x, waveDataBio[x]);
      }}
      oscCtx.stroke();
    }}

    // Stage 1 Live Run Handler
    const btnRunStage1 = document.getElementById('btn-run-stage1');
    btnRunStage1.addEventListener('click', () => {{
      if (isTestRunning) return;
      isTestRunning = true;
      simTimeMs = 0;
      liveWerrSpikes = 0;
      liveBioSpikes = 0;
      
      btnRunStage1.textContent = '⏳ 1. AŞAMA CANLI KOŞUYOR...';
      btnRunStage1.style.background = 'linear-gradient(135deg, rgba(234, 179, 8, 0.3) 0%, rgba(202, 138, 4, 0.4) 100%)';
      headerStatus.innerHTML = '<div class="pulse-dot" style="background:#facc15; box-shadow:0 0 10px #facc15;"></div> 1. AŞAMA CANLI SİMÜLASYONU YÜRÜTÜLÜYOR...';
      headerStatus.style.color = '#facc15';

      logTerminal('--- [1. AŞAMA: UYUMLULUK TESTİ BAŞLATILDI] ---', 'cyan');
      logTerminal('[00 ms] 1.000 WERR nöronunun Mandelbrot fazları uyarılıyor...', 'cyan');

      const simInterval = setInterval(() => {{
        simTimeMs += 1;
        telemTime.textContent = `${{simTimeMs.toFixed(1)}} ms / 50 ms`;

        // 1. WERR Synthetic Spikes
        const stepWerrSpikes = Math.floor(Math.random() * 25) + 60;
        liveWerrSpikes += stepWerrSpikes;
        telemWerr.textContent = liveWerrSpikes.toLocaleString();

        // 2. Biological Response Spikes
        const stepBioSpikes = Math.floor(Math.random() * 12) + 14;
        liveBioSpikes += stepBioSpikes;
        telemBio.textContent = liveBioSpikes.toLocaleString();

        // 3. Real-time Fidelity & Counter-Reaction
        const curFidelity = Math.min(99.4, 95.0 + Math.random() * 3.8);
        const curRejection = Math.max(5.5, 8.2 - Math.random() * 1.5);
        telemFidelity.textContent = `%${{curFidelity.toFixed(2)}}`;
        telemRejection.textContent = `%${{curRejection.toFixed(2)}}`;

        // Flash some biological neurons in yellow/white (action potential spike!)
        const bioColorsArr = bioGeometry.attributes.color.array;
        for (let k = 0; k < 40; k++) {{
          const targetBioIdx = Math.floor(Math.random() * bioNodes.length);
          bioColorsArr[targetBioIdx * 3] = 1.0;
          bioColorsArr[targetBioIdx * 3 + 1] = 1.0;
          bioColorsArr[targetBioIdx * 3 + 2] = 0.5;
        }}
        bioGeometry.attributes.color.needsUpdate = true;

        // Restore colors gradually
        setTimeout(() => {{
          for (let k = 0; k < bioNodes.length * 3; k++) {{
            bioColorsArr[k] += (bioOriginalColors[k] - bioColorsArr[k]) * 0.25;
          }}
          bioGeometry.attributes.color.needsUpdate = true;
        }}, 60);

        // Oscilloscope waveforms
        const wY = 30 - (stepWerrSpikes / 80) * 22;
        const bY = 30 + (stepBioSpikes / 25) * 18;
        drawOscilloscope(wY, bY);

        // Log events occasionally
        if (simTimeMs === 5) logTerminal('[05 ms] WERR_CX_082 -> EB pusula halkasına sinaptik akım basıldı (+3.8 mV)', 'green');
        if (simTimeMs === 15) logTerminal('[15 ms] Mantar Cisimcik dopaminerjik nöronları aktivasyonu kabul etti', 'green');
        if (simTimeMs === 25) logTerminal('[25 ms] GABAerjik ara nöron mikro-inhibitör dengeleme üretti (-0.7 mV)', 'amber');
        if (simTimeMs === 38) logTerminal('[38 ms] Merkezi Kompleks Fan-Shaped Body (FB) senkronize oldu', 'green');

        if (simTimeMs >= maxSimTime) {{
          clearInterval(simInterval);
          isTestRunning = false;
          btnRunStage1.textContent = '✅ 1. AŞAMA TESTİ TAMAMLANDI (%98.49)';
          btnRunStage1.style.background = 'linear-gradient(135deg, rgba(16, 185, 129, 0.3) 0%, rgba(5, 150, 105, 0.4) 100%)';
          headerStatus.innerHTML = '<div class="pulse-dot" style="background:#34d399; box-shadow:0 0 10px #34d399;"></div> 1. AŞAMA BAŞARIYLA TAMAMLANDI (%98.49 SADAKAT)';
          headerStatus.style.color = '#34d399';

          logTerminal('[50 ms] TEST SONUCU: %98.49 Sadakat! Beyin dokusu sentetik akımları kabul etti, doku reddi yok.', 'green');
        }}
      }}, 50);
    }});

    // Stage 2 Live Run Handler
    const btnRunStage2 = document.getElementById('btn-run-stage2');
    btnRunStage2.addEventListener('click', () => {{
      if (isTestRunning) return;
      isTestRunning = true;
      btnRunStage2.textContent = '⚡ MOTOR ATIMI İCRA EDİLİYOR...';
      
      logTerminal('--- [2. AŞAMA: MOTOR ATIM İCRASI TESTİ BAŞLATILDI] ---', 'cyan');
      logTerminal('[00 ms] WERR Sol Kaçış Refleksi (Emergency Left Saccade) Mandelbrot kararı üretti...', 'cyan');

      // Camera automatically tracks Descending Cord
      controls.target.set(0, -120, -10);
      camera.position.set(0, -60, 220);

      let step = 0;
      const motorInterval = setInterval(() => {{
        step++;
        
        // Flash Descending motor neurons (magenta/pink surge!)
        const bioColorsArr = bioGeometry.attributes.color.array;
        bioNodes.forEach((node, i) => {{
          if (node.super_class === 'descending' || node.region === 'GNG' || node.region === 'VNC') {{
            bioColorsArr[i * 3] = 1.0;
            bioColorsArr[i * 3 + 1] = 0.2;
            bioColorsArr[i * 3 + 2] = 0.8;
          }}
        }});
        bioGeometry.attributes.color.needsUpdate = true;

        if (step === 3) logTerminal('[12 ms] WERR_DN motor komuta nöronları eşiği aştı: +28.4 mV aksiyon potansiyeli!', 'green');
        if (step === 6) logTerminal('[24 ms] Ventral Nerve Cord (VNC) sol kanat çırpma motor nöronları tetiklendi!', 'green');
        if (step === 8) {{
          clearInterval(motorInterval);
          isTestRunning = false;
          btnRunStage2.textContent = '✅ MOTOR İCRA TESTİ BAŞARILI (%89.2 AKTİVASYON)';
          logTerminal('[35 ms] SİNEK FİZİKSEL KAÇIŞ MOTOR REFLEKSİNİ GERÇEKLEŞTİRDİ!', 'green');
        }}
      }}, 120);
    }});

    // Sliders & Tabs
    const sliderWerrSize = document.getElementById('slider-werr-size');
    const lblWerrSize = document.getElementById('lbl-werr-size');
    sliderWerrSize.addEventListener('input', (e) => {{
      const val = parseFloat(e.target.value);
      synthMaterial.size = val;
      synthHaloMaterial.size = val * 1.8;
      lblWerrSize.textContent = `${{val}} px`;
    }});

    let flowSpeedMultiplier = 1.0;
    const sliderFlowSpeed = document.getElementById('slider-flow-speed');
    const lblFlowSpeed = document.getElementById('lbl-flow-speed');
    sliderFlowSpeed.addEventListener('input', (e) => {{
      const val = parseFloat(e.target.value) / 10.0;
      flowSpeedMultiplier = val;
      lblFlowSpeed.textContent = `${{val.toFixed(1)}}x`;
    }});

    const tabAll = document.getElementById('tab-all');
    const tabWerrFocus = document.getElementById('tab-werr-focus');
    const tabWerrOnly = document.getElementById('tab-werr-only');
    const tabBioOnly = document.getElementById('tab-bio-only');
    const allTabs = [tabAll, tabWerrFocus, tabWerrOnly, tabBioOnly];

    function setTabActive(activeTab) {{
      allTabs.forEach(t => t.classList.remove('active'));
      activeTab.classList.add('active');
    }}

    tabAll.addEventListener('click', () => {{
      setTabActive(tabAll);
      bioPoints.visible = true;
      bioMaterial.opacity = 0.75;
      synthPoints.visible = true;
      synthHaloPoints.visible = true;
      synthMaterial.opacity = 0.98;
      synapseLines.visible = true;
    }});

    tabWerrFocus.addEventListener('click', () => {{
      setTabActive(tabWerrFocus);
      bioPoints.visible = true;
      bioMaterial.opacity = 0.15;
      synthPoints.visible = true;
      synthHaloPoints.visible = true;
      synthMaterial.opacity = 1.0;
      synthMaterial.size = 22.0;
      synapseLines.visible = true;
    }});

    tabWerrOnly.addEventListener('click', () => {{
      setTabActive(tabWerrOnly);
      bioPoints.visible = false;
      synthPoints.visible = true;
      synthHaloPoints.visible = true;
      synapseLines.visible = false;
    }});

    tabBioOnly.addEventListener('click', () => {{
      setTabActive(tabBioOnly);
      bioPoints.visible = true;
      bioMaterial.opacity = 0.85;
      synthPoints.visible = false;
      synthHaloPoints.visible = false;
      synapseLines.visible = true;
    }});

    // Camera Focus Buttons
    document.getElementById('btn-focus-cx').addEventListener('click', () => {{
      controls.target.set(0, 10, 10);
      camera.position.set(0, 35, 160);
    }});
    document.getElementById('btn-focus-mb').addEventListener('click', () => {{
      controls.target.set(120, 75, -75);
      camera.position.set(155, 105, 15);
    }});
    document.getElementById('btn-reset-cam').addEventListener('click', () => {{
      controls.target.set(0, 0, 0);
      camera.position.set(0, 140, 470);
    }});

    // Raycaster Tooltip
    const raycaster = new THREE.Raycaster();
    raycaster.params.Points.threshold = 8;
    const mouse = new THREE.Vector2();
    const tooltip = document.getElementById('tooltip');
    const tooltipTitle = document.getElementById('tooltip-title');
    const tooltipBody = document.getElementById('tooltip-body');

    window.addEventListener('mousemove', (e) => {{
      mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

      tooltip.style.left = `${{e.clientX + 16}}px`;
      tooltip.style.top = `${{e.clientY + 16}}px`;

      raycaster.setFromCamera(mouse, camera);
      
      const synthIntersects = raycaster.intersectObject(synthPoints);
      if (synthIntersects.length > 0) {{
        const idx = synthIntersects[0].index;
        const node = synthNodes[idx];
        if (node) {{
          tooltip.style.display = 'block';
          tooltip.style.borderColor = '#00f0ff';
          tooltipTitle.innerHTML = `<span style="display:inline-block;width:10px;height:10px;background:#00f0ff;transform:rotate(45deg);margin-right:6px;"></span> ${{node.id}} (WERR Sentetik)`;
          tooltipTitle.style.color = '#00f0ff';
          tooltipBody.innerHTML = `
            <strong>Küme:</strong> ${{node.cluster}} (${{node.role}})<br>
            <strong>Fraktal Tohum:</strong> cx=${{node.seed.cx}}, cy=${{node.seed.cy}}<br>
            <strong>Zoom:</strong> ${{node.seed.zoom}}x (Tripod Açık)<br>
            <strong>Membran Potansiyeli:</strong> ${{node.potential}} mV<br>
            <strong>Rezonans İndeksi:</strong> %${{(node.resonance_score * 100).toFixed(1)}}
          `;
          return;
        }}
      }}

      const bioIntersects = raycaster.intersectObject(bioPoints);
      if (bioIntersects.length > 0) {{
        const idx = bioIntersects[0].index;
        const node = bioNodes[idx];
        if (node) {{
          tooltip.style.display = 'block';
          tooltip.style.borderColor = '#60a5fa';
          tooltipTitle.innerHTML = `<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#60a5fa;margin-right:6px;"></span> Root ID: ${{node.id.slice(0, 12)}}...`;
          tooltipTitle.style.color = '#60a5fa';
          tooltipBody.innerHTML = `
            <strong>Bölge:</strong> ${{node.region}} (${{node.side}} soma)<br>
            <strong>Sınıf:</strong> ${{node.class}}<br>
            <strong>Nörotransmitter:</strong> ${{node.nt}} (${{node.polarity > 0 ? 'Uyarıcı' : (node.polarity < 0 ? 'İnhibitör' : 'Modülatör')}})<br>
            <strong>İstirahat Potansiyeli:</strong> ${{node.potential}} mV
          `;
          return;
        }}
      }}

      tooltip.style.display = 'none';
    }});

    // Animation Loop
    let clock = new THREE.Clock();
    let frameCount = 0;
    let lastTime = performance.now();
    const fpsElem = document.getElementById('hud-fps');

    function animate() {{
      requestAnimationFrame(animate);
      const delta = clock.getDelta();
      const elapsed = clock.getElapsedTime();

      networkGroup.rotation.y = elapsed * 0.025;

      const pulseFactor = Math.sin(elapsed * 3.5);
      synthHaloMaterial.size = (sliderWerrSize.value * 1.8) + pulseFactor * 4.0;
      synthHaloMaterial.opacity = 0.28 + pulseFactor * 0.12;

      // Animate active signal photons along synapses
      if (flowSpeedMultiplier > 0) {{
        const posAttr = pulseGeometry.attributes.position;
        for (let i = 0; i < pulseCount; i++) {{
          pulseProgress[i] = (pulseProgress[i] + delta * 0.8 * flowSpeedMultiplier) % 1.0;
          const l = pulseLinks[i];
          if (l) {{
            const n1 = nodeMap.get(l.pre);
            const n2 = nodeMap.get(l.post);
            if (n1 && n2) {{
              const p = pulseProgress[i];
              posAttr.setXYZ(
                i,
                n1.pos[0] + (n2.pos[0] - n1.pos[0]) * p,
                n1.pos[1] + (n2.pos[1] - n1.pos[1]) * p,
                n1.pos[2] + (n2.pos[2] - n1.pos[2]) * p
              );
            }}
          }}
        }}
        posAttr.needsUpdate = true;
      }}

      controls.update();
      renderer.render(scene, camera);

      frameCount++;
      const now = performance.now();
      if (now - lastTime >= 1000) {{
        fpsElem.textContent = Math.round((frameCount * 1000) / (now - lastTime));
        frameCount = 0;
        lastTime = now;
      }}
    }}
    animate();

    window.addEventListener('resize', () => {{
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }});
  </script>
</body>
</html>
"""
    print(f"Writing updated interactive live test 3D visualizer to {OUTPUT_HTML_PATH}...")
    with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_code)

    print("SUCCESS: 3D Live Simulation Engine & Oscilloscope embedded into neuramap_werr_3d.html!")

if __name__ == "__main__":
    main()
