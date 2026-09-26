"""
bioneural_fly_app.py
====================
Standalone Native Python Desktop Application for:
Drosophila Melanogaster WHOLE-BRAIN CONNECTOME (158,262 Real Biological Neurons)
with WERR BIONEURAL COPROCESSOR CHIP (Implantable Neuromorphic Micro-Grid).

Key Architecture:
- 100% Real Biological Fly Connectome: 158,262 Neurons & 3,990,039 Synapses
  from the Princeton FlyWire Electron Microscopy Connectome.
- WERR Neural Coprocessor Implant: A 1,024-pin high-density neuromorphic silicon
  chip mounted on the dorsal cranial surface, with penetrating micro-electrode shanks
  interfacing directly with the Ellipsoid Body (EB) and Descending Motor Neurons (DN).
- Plug-and-Play (Tak-Çıkar Modüler Çip):
  * [C] Tuşu veya Buton: Çipi Tak (Engage) / Çıkar (Bypass).
  * Çip Takılıyken: Mandelbrot fraktal kararları ve WASD telepatik override elektrot
    iğnelerinden biyolojik beynin motor devrelerine akar; anlık kaçış refleksleri üretir.
  * Çip Çıkarıldığında: Sinek %100 saf biyolojik otonomiye döner; çip sönümlenir.
- Dual 3D Viewport:
  1. 3D Uçuş Arenası: Fizik tabanlı sinek modeli, çırpınan kanatlar (200-244 Hz),
     vorteks izleri ve sineğin toraksı üstündeki parlayan biyonik mikro-çip.
  2. Canlı 3D Beyin: 158.262 biyolojik nöron nokta bulutu + dorsalde yüzen WERR
     silikon çipi ve beyin derinliklerine inen parlayan elektrot iğneleri (shanks).
- Çok Kanallı Osiloskop: Biyolojik motor voltajı (Sarı) + WERR Çip Sinyali (Camgöbeği).
- 100% Çevrimdışı, Bağımsız, Tkinter, NumPy ve Pillow tabanlı.
"""
import os
import sys
import time
import math
import random
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

WORKSPACE = os.path.abspath(os.path.dirname(__file__))
CACHE_FILE = os.path.join(WORKSPACE, "drosophila_full_158k_cache.npz")
WERRENGINE_DIR = os.path.join(WORKSPACE, "werrengine")
if WERRENGINE_DIR not in sys.path:
    sys.path.insert(0, WERRENGINE_DIR)

import werr

def load_dataset():
    """Loads 158,262 biological nodes and 3.99M synapses from binary CSR cache."""
    if not os.path.exists(CACHE_FILE):
        print(f"[*] Cache file not found at {CACHE_FILE}. Compiling now...")
        import compile_full_158k_connectome
        compile_full_158k_connectome.main()

    print(f"[*] Fast-loading 158,262 biological neurons & 3.99M synapses from {CACHE_FILE}...")
    t0 = time.time()
    data = np.load(CACHE_FILE)
    loaded = {
        "pos": data["pos"],
        "polarity": data["polarity"],
        "is_eb": data["is_eb"],
        "is_dn": data["is_dn"],
        "is_mb": data["is_mb"],
        "is_me": data["is_me"],
        "is_al": data["is_al"],
        "indptr": data["indptr"],
        "syn_post": data["syn_post"],
        "syn_weight": data["syn_weight"]
    }
    print(f"[*] Dataset ready in {time.time() - t0:.3f}s. Total neurons: {len(loaded['pos']):,}, synapses: {len(loaded['syn_post']):,}.")
    return loaded

class BioNeuralFlyChipApp:
    def __init__(self, root, net_data):
        self.root = root
        self.root.title("Drosophila Melanogaster & WERR Biyo-Nöral İmplant Çipi Simülatörü [158.262 Biyolojik + 1.024 Çip Pini]")
        self.root.geometry("1420x920")
        self.root.configure(bg="#040711")

        self.net = net_data
        self.TOTAL_NODES = len(self.net["pos"])
        self.TOTAL_SYNAPSES = len(self.net["syn_post"])
        print(f"[*] Initializing Biological LIF Engine for {self.TOTAL_NODES:,} neurons...")

        # Biophysical State Arrays (Biological Connectome)
        self.V_m = np.full(self.TOTAL_NODES, -65.0, dtype=np.float32)
        self.V_rest = -65.0
        self.V_thresh = -50.0
        self.refractory = np.zeros(self.TOTAL_NODES, dtype=np.float32)
        
        self.pos = self.net["pos"]
        self.polarity = self.net["polarity"]
        self.is_eb = self.net["is_eb"]
        self.is_dn = self.net["is_dn"]
        self.is_mb = self.net["is_mb"]
        self.is_me = self.net["is_me"]
        self.is_al = self.net["is_al"]
        self.indptr = self.net["indptr"]
        self.syn_post = self.net["syn_post"]
        self.syn_weight = self.net["syn_weight"]

        # Pre-filter functional indices
        self.eb_indices = np.where(self.is_eb == 1)[0]
        self.dn_indices = np.where(self.is_dn == 1)[0]
        self.mb_indices = np.where(self.is_mb == 1)[0]
        self.me_indices = np.where(self.is_me == 1)[0]
        self.al_indices = np.where(self.is_al == 1)[0]

        # Precalculate anatomical polar angles of each Central Complex EB ring neuron
        eb_x = self.pos[self.eb_indices, 0]
        eb_z = self.pos[self.eb_indices, 2] - 20.0
        self.eb_angles = np.arctan2(eb_x, eb_z).astype(np.float32)

        # Pre-assign base point colors (RGB uint8)
        self.base_colors = np.zeros((self.TOTAL_NODES, 3), dtype=np.uint8)
        self.base_colors[:] = [55, 90, 140]           # Protocerebrum: deep slate blue
        self.base_colors[self.me_indices] = [0, 175, 255] # Optic Lobes: Azure / Cyan
        self.base_colors[self.eb_indices] = [185, 80, 255] # Central Complex: Electric Violet
        self.base_colors[self.mb_indices] = [0, 230, 120] # Mushroom Body: Emerald Bio-Green
        self.base_colors[self.al_indices] = [255, 70, 130] # Antennal / Sensory: Coral Pink
        self.base_colors[self.dn_indices] = [255, 180, 20] # Descending Motor: Amber Gold

        # Uncorrelated Pseudo-hash Noise Phases (Prevents artificial traveling waves in the EB compass)
        self.noise_phase = np.array([(i * 12345.67) % (2.0 * math.pi) for i in range(self.TOTAL_NODES)], dtype=np.float32)

        # -------------------------------------------------------------
        # WERR BIONEURAL COPROCESSOR CHIP (IMPLANTABLE MODULE)
        # -------------------------------------------------------------
        self.chip_engaged = True # Start with chip engaged
        self.CHIP_GRID_X = 32
        self.CHIP_GRID_Z = 32
        self.CHIP_TOTAL_PINS = self.CHIP_GRID_X * self.CHIP_GRID_Z # 1,024 micro-electrode pins

        # Chip physical coordinates (Dorsal cranial surface: x in [-40, 40], y=105, z in [15, 55] um)
        chip_x = np.linspace(-38.0, 38.0, self.CHIP_GRID_X, dtype=np.float32)
        chip_z = np.linspace(15.0, 55.0, self.CHIP_GRID_Z, dtype=np.float32)
        grid_xx, grid_zz = np.meshgrid(chip_x, chip_z)
        grid_yy = np.full_like(grid_xx, 105.0) # Elevated dorsal plane

        self.chip_pos = np.column_stack([grid_xx.ravel(), grid_yy.ravel(), grid_zz.ravel()]).astype(np.float32)
        self.chip_output_current = 0.0
        self.chip_pulse_phase = 0.0

        # 1,024 WERR Neuromorphic Silicon Neurons (32x32 micro-grid coprocessor)
        self.werr_vm = np.full(self.CHIP_TOTAL_PINS, -65.0, dtype=np.float32)
        self.werr_refractory = np.zeros(self.CHIP_TOTAL_PINS, dtype=np.float32)
        self.werr_thresh = -45.0
        self.werr_rest = -65.0

        # Map 1,024 pins into specialized functional WERR processing sectors:
        # - Left Columns (0..10): Saccade Left / Counter-clockwise Turn Engine
        # - Right Columns (21..31): Saccade Right / Clockwise Turn Engine
        # - Anterior Center (Cols 11..20, Rows 0..15): Thrust & Wingbeat Acceleration Engine
        # - Posterior Center (Cols 11..20, Rows 16..31): Brake & GABA Inhibitory Engine
        cols = np.tile(np.arange(self.CHIP_GRID_X), self.CHIP_GRID_Z)
        rows = np.repeat(np.arange(self.CHIP_GRID_Z), self.CHIP_GRID_X)
        self.werr_idx_left = np.where(cols < 11)[0]
        self.werr_idx_right = np.where(cols > 20)[0]
        self.werr_idx_thrust = np.where((cols >= 11) & (cols <= 20) & (rows < 16))[0]
        self.werr_idx_brake = np.where((cols >= 11) & (cols <= 20) & (rows >= 16))[0]

        # WERR Engine Instance
        self.werr_engine = werr.WerrEngine(tripod=True, mode="resonance")

        # 4 Penetrating Electrode Shanki (Silicon leads plunging into key circuits)
        self.probe_targets = [
            ("SHANK-1: EB PUSULA", np.array([0.0, -10.0, 20.0], dtype=np.float32), (185, 80, 255)),
            ("SHANK-2: DN MOTOR", np.array([0.0, -180.0, -15.0], dtype=np.float32), (255, 180, 20)),
            ("SHANK-3: SOL MB", np.array([-100.0, 70.0, -60.0], dtype=np.float32), (0, 230, 120)),
            ("SHANK-4: SAĞ MB", np.array([100.0, 70.0, -60.0], dtype=np.float32), (0, 230, 120))
        ]

        # Dynamic Flight Kinematics
        self.fly_pos = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.fly_heading = 0.0
        self.fly_target_heading = 0.0
        self.fly_pitch = 0.0
        self.fly_roll = 0.0
        self.fly_speed = 1.4  # m/s
        self.fly_wbf = 218    # Hz
        self.epg_ring_angle = 0.0
        self.motor_vm = -65.0
        self.boundary_stim_timer = 0.0
        self.commanded_heading = 0.0
        self.neural_coherence = 1.0

        # Keys
        self.keys = {"w": False, "a": False, "s": False, "d": False}

        # Spontaneous wander cadence & visual landmarks
        self.auto_meander_time = 0.0
        self.vortex_trail = []
        
        # 3D Neon Rings along circular flight patrol route (R=48m)
        self.neon_rings = []
        for i in range(8):
            ang = i * (2.0 * math.pi / 8.0)
            rx = math.cos(ang) * 48.0
            rz = math.sin(ang) * 48.0
            ry = math.sin(i * 1.5) * 1.8
            tangent = ang + math.pi / 2.0
            self.neon_rings.append((rx, ry, rz, 7.5, tangent))

        # 3D Flight Camera State
        self.cam_flight_pos = np.array([0.0, 4.2, -13.0], dtype=np.float32)

        # 3D Brain Camera
        self.cam_yaw = 0.0
        self.cam_pitch = 0.25
        self.cam_dist = 520.0
        self.is_head_locked = False # Default to stable Free Orbit mode
        self.drag_start = None

        # Telemetry & Rates
        self.last_frame_time = time.perf_counter()
        self.last_sec_time = time.perf_counter()
        self.spike_accumulator = 0
        self.spikes_per_sec = 0
        self.recent_spiking_indices = np.array([], dtype=np.int32)
        
        self.traffic_optic = 0
        self.traffic_eb = 0
        self.traffic_mb = 0
        self.traffic_dn = 0
        self.stimulus_decay = 0.0

        # Build GUI
        self.setup_ui()

        # Keyboard Bindings
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.focus_set()

        # Start Real-Time Loop (~60 FPS)
        self.update_loop()

    def setup_ui(self):
        # 1. Top Ribbon
        top_bar = tk.Frame(self.root, bg="#080f22", height=66)
        top_bar.pack(side=tk.TOP, fill=tk.X)

        title_box = tk.Frame(top_bar, bg="#080f22")
        title_box.pack(side=tk.LEFT, padx=18, pady=8)

        lbl_app = tk.Label(
            title_box,
            text="🧬 DROSOPHILA MELANOGASTER & WERR BİYO-NÖRAL İMPLANT ÇİPİ",
            font=("Segoe UI", 12, "bold"),
            fg="#f8fafc", bg="#080f22"
        )
        lbl_app.pack(anchor="w")

        lbl_sub = tk.Label(
            title_box,
            text="158.262 Biyolojik Nöron (FlyWire FAFB) + 1.024 Kanallı WERR Nöromorfik Protez Çipi (Tak-Çıkar Modül)",
            font=("Segoe UI", 8),
            fg="#94a3b8", bg="#080f22"
        )
        lbl_sub.pack(anchor="w")

        # Chip Action Buttons on Right
        btn_box = tk.Frame(top_bar, bg="#080f22")
        btn_box.pack(side=tk.RIGHT, padx=16, pady=10)

        self.btn_chip = tk.Button(
            btn_box,
            text="🔌 ÇİPİ ÇIKAR (C)",
            font=("Consolas", 10, "bold"),
            bg="#005577", fg="#00f2fe",
            relief="ridge", bd=2, cursor="hand2",
            command=self.toggle_chip, padx=14, pady=4
        )
        self.btn_chip.pack(side=tk.RIGHT, padx=6)

        self.badge_mode = tk.Label(
            btn_box,
            text="⚡ WERR NÖRAL İMPLANT AKTİF (1.024 Pin)",
            font=("Consolas", 10, "bold"),
            fg="#00f2fe", bg="#0c2538",
            padx=12, pady=6, relief="ridge", bd=1
        )
        self.badge_mode.pack(side=tk.RIGHT, padx=6)

        # 2. Main Content Split: Left = 3D Flight Arena, Right = 158k 3D Brain
        content = tk.Frame(self.root, bg="#040711")
        content.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=6)

        # Left Column: Flight Arena
        left_box = tk.Frame(content, bg="#070c1a", relief="ridge", bd=1)
        left_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        flight_hdr = tk.Frame(left_box, bg="#0c152e", height=32)
        flight_hdr.pack(side=tk.TOP, fill=tk.X)
        tk.Label(
            flight_hdr,
            text="✈️ 3B UÇUŞ ARENASI & BİYONİK İMPLANT SİNEK KİNEMATİĞİ",
            font=("Segoe UI", 9, "bold"),
            fg="#38bdf8", bg="#0c152e"
        ).pack(side=tk.LEFT, padx=10, pady=5)

        self.canvas_flight = tk.Canvas(left_box, bg="#02050c", highlightthickness=0)
        self.canvas_flight.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Right Column: 158k Brain & WERR Chip
        right_box = tk.Frame(content, bg="#070c1a", relief="ridge", bd=1)
        right_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=4)

        brain_hdr = tk.Frame(right_box, bg="#0c152e", height=32)
        brain_hdr.pack(side=tk.TOP, fill=tk.X)
        tk.Label(
            brain_hdr,
            text="🧠 CANLI KONNEKTOM (158.262 NÖRON) + 🔲 WERR ÇİP MATRİSİ",
            font=("Segoe UI", 9, "bold"),
            fg="#c084fc", bg="#0c152e"
        ).pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_lock = tk.Button(
            brain_hdr,
            text="🔄 Serbest Orbit Mod",
            font=("Segoe UI", 8, "bold"),
            bg="#2a1b3d", fg="#c084fc",
            relief="flat", cursor="hand2",
            command=self.toggle_head_lock, padx=10
        )
        self.btn_lock.pack(side=tk.RIGHT, padx=8, pady=3)

        self.canvas_brain = tk.Canvas(right_box, bg="#020409", highlightthickness=0)
        self.canvas_brain.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas_brain.bind("<ButtonPress-1>", self.on_brain_drag_start)
        self.canvas_brain.bind("<B1-Motion>", self.on_brain_drag_motion)
        self.canvas_brain.bind("<MouseWheel>", self.on_brain_zoom)

        # 3. Sensory Stimulus & Chip Quick Commands Ribbon
        stim_bar = tk.Frame(self.root, bg="#091124", height=42)
        stim_bar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=2)

        tk.Label(
            stim_bar,
            text="🕹️ ÇİP & BİYO-KOMUTLAR:",
            font=("Segoe UI", 9, "bold"),
            fg="#94a3b8", bg="#091124"
        ).pack(side=tk.LEFT, padx=10, pady=6)

        btn_saccade_l = tk.Button(
            stim_bar, text="[A] ← Sola Kaçış (EB)",
            font=("Segoe UI", 8, "bold"), bg="#0f2e42", fg="#00f2fe",
            command=self.trigger_left_saccade, relief="flat", padx=8
        )
        btn_saccade_l.pack(side=tk.LEFT, padx=4, pady=4)

        btn_saccade_r = tk.Button(
            stim_bar, text="[D] Sağa Kaçış (EB) →",
            font=("Segoe UI", 8, "bold"), bg="#0f2e42", fg="#00f2fe",
            command=self.trigger_right_saccade, relief="flat", padx=8
        )
        btn_saccade_r.pack(side=tk.LEFT, padx=4, pady=4)

        btn_thrust = tk.Button(
            stim_bar, text="[W] ↑ Turbo Kanat İtişi (244 Hz)",
            font=("Segoe UI", 8, "bold"), bg="#382810", fg="#fbbf24",
            command=self.trigger_thrust, relief="flat", padx=8
        )
        btn_thrust.pack(side=tk.LEFT, padx=4, pady=4)

        btn_brake = tk.Button(
            stim_bar, text="[S] ↓ GABA Freni",
            font=("Segoe UI", 8, "bold"), bg="#3d1418", fg="#f87171",
            command=self.trigger_brake, relief="flat", padx=8
        )
        btn_brake.pack(side=tk.LEFT, padx=4, pady=4)

        btn_optic = tk.Button(
            stim_bar, text="[1] 👁️ Optik Flaş",
            font=("Segoe UI", 8), bg="#0f293d", fg="#38bdf8",
            command=self.inject_optic, relief="flat", padx=8
        )
        btn_optic.pack(side=tk.LEFT, padx=4, pady=4)

        btn_odor = tk.Button(
            stim_bar, text="[2] 🌸 Koku / MB",
            font=("Segoe UI", 8), bg="#103628", fg="#34d399",
            command=self.inject_odor, relief="flat", padx=8
        )
        btn_odor.pack(side=tk.LEFT, padx=4, pady=4)

        # 4. Telemetry & Oscilloscope Bottom Panel
        bot_panel = tk.Frame(self.root, bg="#070c1a", height=130, relief="ridge", bd=1)
        bot_panel.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=6)

        # Intercom Bar
        self.lbl_intercom = tk.Label(
            bot_panel,
            text="⚡ [WERR ÇİPİ AKTİF] 1.024 kanallı mikro-elektrot arayüzü EB pusulası ve DN motor nöronlarına kilitlendi!",
            font=("Consolas", 9),
            fg="#00f2fe", bg="#0a152d",
            anchor="w", padx=12, pady=4
        )
        self.lbl_intercom.pack(side=tk.TOP, fill=tk.X)

        bot_content = tk.Frame(bot_panel, bg="#070c1a")
        bot_content.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=12, pady=6)

        # Live Metrics Grid
        metrics_box = tk.Frame(bot_content, bg="#070c1a")
        metrics_box.pack(side=tk.LEFT, fill=tk.Y, padx=8)

        self.lbl_speed = tk.Label(metrics_box, text="HIZ: 1.40 m/s", font=("Consolas", 10, "bold"), fg="#38bdf8", bg="#070c1a")
        self.lbl_speed.pack(anchor="w")

        self.lbl_wbf = tk.Label(metrics_box, text="KANAT: 218 Hz", font=("Consolas", 10, "bold"), fg="#fbbf24", bg="#070c1a")
        self.lbl_wbf.pack(anchor="w")

        self.lbl_heading = tk.Label(metrics_box, text="EB PUSULA: 000°", font=("Consolas", 10, "bold"), fg="#c084fc", bg="#070c1a")
        self.lbl_heading.pack(anchor="w")

        self.lbl_chip_status = tk.Label(metrics_box, text="ÇİP GÜCÜ: +35.0 mV", font=("Consolas", 10, "bold"), fg="#00f2fe", bg="#070c1a")
        self.lbl_chip_status.pack(anchor="w")

        self.lbl_spikes = tk.Label(metrics_box, text="SPİKE: 0 Hz", font=("Consolas", 10, "bold"), fg="#34d399", bg="#070c1a")
        self.lbl_spikes.pack(anchor="w")

        # Oscilloscope Canvas (Dual-Trace: Yellow = DN Motor, Cyan = WERR Chip)
        osc_frame = tk.Frame(bot_content, bg="#020409", relief="sunken", bd=1)
        osc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=14)

        self.canvas_osc = tk.Canvas(osc_frame, bg="#030611", height=54, highlightthickness=0)
        self.canvas_osc.pack(fill=tk.BOTH, expand=True)
        self.osc_dn_history = [27] * 280
        self.osc_chip_history = [45] * 280

        # Legend / Regional Activity
        info_box = tk.Frame(bot_content, bg="#070c1a")
        info_box.pack(side=tk.RIGHT, fill=tk.Y, padx=8)

        self.lbl_traffic = tk.Label(
            info_box,
            text="Biyo-Trafik: Optik: 0 Hz | Central: 0 Hz | Motor: 0 Hz",
            font=("Consolas", 8), fg="#94a3b8", bg="#070c1a"
        )
        self.lbl_traffic.pack(anchor="e")

        legend_text = "🔵 Optik (ME)  🟣 Central (EB)  🟡 Motor (DN)  🔲 WERR Nöral Çip Matrisi (1.024 Pin)"
        tk.Label(info_box, text=legend_text, font=("Segoe UI", 8), fg="#64748b", bg="#070c1a").pack(anchor="e", pady=3)

    def toggle_chip(self):
        """Plugs in or unplugs the WERR Neural Coprocessor Chip."""
        self.chip_engaged = not self.chip_engaged
        if self.chip_engaged:
            self.btn_chip.configure(text="🔌 ÇİPİ ÇIKAR (C)", bg="#005577", fg="#00f2fe")
            self.badge_mode.configure(text="⚡ WERR NÖRAL İMPLANT AKTİF (1.024 Pin)", fg="#00f2fe", bg="#0c2538")
            self.lbl_intercom.configure(
                text="⚡ [WERR ÇİPİ TAKILDI] 1.024 kanallı mikro-elektrot arayüzü EB pusulası ve DN motor nöronlarına kilitlendi!",
                fg="#00f2fe"
            )
        else:
            self.btn_chip.configure(text="🔌 ÇİPİ TAK (C)", bg="#2a1b3d", fg="#c084fc")
            self.badge_mode.configure(text="🟢 SAF BİYOLOJİK OTONOM UÇUŞ (Çip Bypass)", fg="#34d399", bg="#0a2618")
            self.chip_output_current = 0.0
            self.lbl_intercom.configure(
                text="🟢 [WERR ÇİPİ ÇIKARILDI] İmplant elektrotları ayrıldı. Sinek %100 saf biyolojik otonomiye döndü.",
                fg="#34d399"
            )

    def toggle_head_lock(self):
        self.is_head_locked = not self.is_head_locked
        if self.is_head_locked:
            self.btn_lock.configure(text="🎯 Kafaya Kilitli Mod", bg="#0f2b38", fg="#00f0ff")
        else:
            self.btn_lock.configure(text="🔄 Serbest Orbit Mod", bg="#2a1b3d", fg="#c084fc")

    def on_brain_drag_start(self, event):
        self.drag_start = (event.x, event.y)

    def on_brain_drag_motion(self, event):
        if self.drag_start:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]
            self.cam_yaw += dx * 0.008
            self.cam_pitch = np.clip(self.cam_pitch - dy * 0.008, -1.2, 1.2)
            self.drag_start = (event.x, event.y)

    def on_brain_zoom(self, event):
        if event.delta > 0:
            self.cam_dist = max(240.0, self.cam_dist - 35.0)
        else:
            self.cam_dist = min(980.0, self.cam_dist + 35.0)

    def on_key_press(self, event):
        k = event.keysym.lower()
        char = event.char.lower()
        if char == "c":
            self.toggle_chip()
        elif k in self.keys:
            self.keys[k] = True
        elif char == "1":
            self.inject_optic()
        elif char == "2":
            self.inject_odor()

    def on_key_release(self, event):
        k = event.keysym.lower()
        if k in self.keys:
            self.keys[k] = False

    def trigger_left_saccade(self):
        # Injects current into Left WERR Processing Sector
        self.werr_vm[self.werr_idx_left] += 32.0
        self.lbl_intercom.configure(text="⚡ [GİRDİ -> WERR ÇİPİ] Sol WERR nöronları uyarıldı (+32 mV) -> Shank-1 EB pusulasına aktarıyor", fg="#00f2fe")

    def trigger_right_saccade(self):
        # Injects current into Right WERR Processing Sector
        self.werr_vm[self.werr_idx_right] += 32.0
        self.lbl_intercom.configure(text="⚡ [GİRDİ -> WERR ÇİPİ] Sağ WERR nöronları uyarıldı (+32 mV) -> Shank-1 EB pusulasına aktarıyor", fg="#00f2fe")

    def trigger_thrust(self):
        # Injects current into Anterior Thrust WERR Processing Sector
        self.werr_vm[self.werr_idx_thrust] += 35.0
        self.lbl_intercom.configure(text="⚡ [GİRDİ -> WERR ÇİPİ] İleri Motor WERR nöronları uyarıldı (+35 mV) -> Shank-2 DN motor havuzuna aktarıyor", fg="#fbbf24")

    def trigger_brake(self):
        # Injects current into Posterior Inhibitory WERR Processing Sector
        self.werr_vm[self.werr_idx_brake] += 30.0
        self.lbl_intercom.configure(text="🛑 [GİRDİ -> WERR ÇİPİ] Fren WERR nöronları uyarıldı (+30 mV) -> Shank-2 GABA bastırma akımı üretiyor", fg="#f87171")

    def inject_optic(self):
        if len(self.me_indices) > 0:
            me_list = self.me_indices.tolist()
            sample = random.sample(me_list, min(1200, len(me_list)))
            self.V_m[sample] += 22.0
        self.lbl_intercom.configure(text="👁️ [OPTİK UYARAN] Görsel loblara parlama enjekte edildi -> Kaçış dönüşü!", fg="#38bdf8")

    def inject_odor(self):
        if len(self.al_indices) > 0:
            al_list = self.al_indices.tolist()
            sample = random.sample(al_list, min(600, len(al_list)))
            self.V_m[sample] += 22.0
        if len(self.mb_indices) > 0:
            mb_list = self.mb_indices.tolist()
            sample_mb = random.sample(mb_list, min(800, len(mb_list)))
            self.V_m[sample_mb] += 18.0
        self.lbl_intercom.configure(text="🌸 [KOKU UYARANI] Anten ve Mantar Cisimciğine koku gradyanı bağlandı!", fg="#34d399")

    def update_loop(self):
        now = time.perf_counter()
        dt = min(now - self.last_frame_time, 0.04)
        self.last_frame_time = now

        # -------------------------------------------------------------
        # 1. USER INPUT -> 1,024 WERR SILICON COPROCESSOR NEURONS
        # -------------------------------------------------------------
        # All keyboard inputs (W, A, S, D) enter ONLY into WERR silicon neurons!
        if self.keys["a"]:
            self.werr_vm[self.werr_idx_left] += dt * 420.0
        if self.keys["d"]:
            self.werr_vm[self.werr_idx_right] += dt * 420.0
        if self.keys["w"]:
            self.werr_vm[self.werr_idx_thrust] += dt * 450.0
        if self.keys["s"]:
            self.werr_vm[self.werr_idx_brake] += dt * 380.0

        # WERR Neuromorphic Dynamics (Leaky Integrate & Fire on 1,024 WERR nodes)
        self.werr_vm += (self.werr_rest - self.werr_vm) * (dt * 12.0)
        self.werr_refractory = np.maximum(0.0, self.werr_refractory - dt * 1000.0)

        # WERR Spiking and Reset
        werr_spikes = (self.werr_vm >= self.werr_thresh) & (self.werr_refractory <= 0.0)
        if np.any(werr_spikes):
            self.werr_vm[werr_spikes] = -70.0
            self.werr_refractory[werr_spikes] = 14.0

        # -------------------------------------------------------------
        # 2. WERR CHIP -> PENETRATING SHANKS -> BIOLOGICAL FLY CIRCUITS
        # -------------------------------------------------------------
        if self.chip_engaged:
            self.chip_pulse_phase += dt * 10.0
            
            # Read real physical electrical activity from WERR neuron pools (mV above resting)
            left_werr_act = float(np.mean(np.maximum(0.0, self.werr_vm[self.werr_idx_left] - (-62.0))))
            right_werr_act = float(np.mean(np.maximum(0.0, self.werr_vm[self.werr_idx_right] - (-62.0))))
            thrust_werr_act = float(np.mean(np.maximum(0.0, self.werr_vm[self.werr_idx_thrust] - (-62.0))))
            brake_werr_act = float(np.mean(np.maximum(0.0, self.werr_vm[self.werr_idx_brake] - (-62.0))))

            total_chip_act = left_werr_act + right_werr_act + thrust_werr_act + brake_werr_act
            self.chip_output_current = min(40.0, total_chip_act * 3.5)

            # SHANK-1 (Harmonic Gaussian Bio-Steering on Central Complex EB Compass)
            steering_act = (left_werr_act - right_werr_act)
            if abs(steering_act) > 0.15:
                # Physiological turning rate: max 1.2 rad/s (~70 deg/s) - bump tracks perfectly!
                turn_rate = float(np.clip(steering_act * 0.08, -1.2, 1.2))
                self.commanded_heading += turn_rate * dt
                self.commanded_heading = (self.commanded_heading + math.pi) % (2.0 * math.pi) - math.pi

                # Project smooth Gaussian attractor bump into EB compass ring
                diff_ang = np.abs((self.eb_angles - self.commanded_heading + math.pi) % (2.0 * math.pi) - math.pi)
                gaussian_field = np.exp(- (diff_ang ** 2) / (2.0 * (0.45 ** 2))) * (2.4 * 60.0 * dt)
                # Physiological ceiling at -48.0 mV (healthy depolarized bump, avoids seizure bursting!)
                self.V_m[self.eb_indices] = np.minimum(-48.0, self.V_m[self.eb_indices] + gaussian_field)

                self.lbl_intercom.configure(
                    text=f"⚡ [BİYO-NÖRAL UYUM: SHANK-1] EB Pusulası Gauss Kılavuzuna Kilitlendi (Uyum: %{int(self.neural_coherence*100)})",
                    fg="#00f2fe"
                )
            else:
                # Strong continuous holding carrier: sustains attractor bump against biological leak!
                diff_ang = np.abs((self.eb_angles - self.commanded_heading + math.pi) % (2.0 * math.pi) - math.pi)
                carrier = np.exp(- (diff_ang ** 2) / (2.0 * (0.45 ** 2))) * (2.1 * 60.0 * dt)
                self.V_m[self.eb_indices] = np.minimum(-52.0, self.V_m[self.eb_indices] + carrier)

            # Compute real-time Neural Coherence Index (how aligned the biological bump is with chip command)
            heading_err = abs((self.epg_ring_angle - self.commanded_heading + math.pi) % (2.0 * math.pi) - math.pi)
            self.neural_coherence = float(np.clip(1.0 - (heading_err / math.pi), 0.0, 1.0))

            # SHANK-2 (Tonic Biological Entrainment on Descending Motor Neurons DN Pool)
            if thrust_werr_act > 0.15 and len(self.dn_indices) > 0:
                # Target physiological flight drive (-56.0 mV), no runaway hyper-polarization
                target_dn = -56.0
                dn_err = target_dn - self.V_m[self.dn_indices]
                self.V_m[self.dn_indices] += np.clip(dn_err * (dt * 5.0), 0.0, 1.2)
                self.lbl_intercom.configure(text=f"⚡ [BİYO-NÖRAL UYUM: SHANK-2] DN motor havuzu ritmik modüle edildi (232 Hz Turbo)", fg="#fbbf24")

            if brake_werr_act > 0.15 and len(self.dn_indices) > 0:
                # Target resting hyperpolarization (-68.0 mV)
                target_dn = -68.0
                dn_err = target_dn - self.V_m[self.dn_indices]
                self.V_m[self.dn_indices] += np.clip(dn_err * (dt * 5.0), -1.2, 0.0)
                self.lbl_intercom.configure(text=f"🛑 [BİYO-NÖRAL UYUM: FREN] GABAerjik dinlenme fazı aktif", fg="#f87171")

            active_pins = len(np.where(self.werr_vm > -58.0)[0])
            self.lbl_chip_status.configure(text=f"WERR ÇİPİ: UYUM %{int(self.neural_coherence*100)} | {active_pins}/1024 Pin")
        else:
            # Chip is BYPASSED / UNPLUGGED: User inputs excite WERR chip but cannot cross severed leads!
            self.chip_output_current = 0.0
            if any(self.keys.values()):
                self.lbl_intercom.configure(text="⚠️ [ÇİP BYPASS] Girdi WERR çipinde işleniyor ancak biyo-bağlantı (Shank) kesik! Sinek otonom biyolojide.", fg="#f87171")
            self.lbl_chip_status.configure(text="ÇİP: BYPASS (0 mV) - İĞNELER KESİK")

        # Spontaneous biological wander in EB ring (ONLY active in pure autonomous mode)
        if not self.chip_engaged:
            self.auto_meander_time += dt
            if self.auto_meander_time > 2.8:
                self.auto_meander_time = 0.0
                if len(self.eb_indices) > 0:
                    eb_list = self.eb_indices.tolist()
                    sector = random.sample(eb_list, min(45, len(eb_list)))
                    self.V_m[sector] += 10.0
        else:
            self.auto_meander_time = 0.0

        # -------------------------------------------------------------
        # 2. BIOPHYSICAL LEAKY INTEGRATE-AND-FIRE ON 158,262 NODES
        # -------------------------------------------------------------
        self.V_m += (self.V_rest - self.V_m) * (dt * 9.0)
        self.refractory = np.maximum(0.0, self.refractory - dt * 1000.0)

        # Baseline spontaneous stochastic fluctuations (uncorrelated isotropic noise)
        self.V_m += (np.sin(now * 2.0 + self.noise_phase) * 0.35).astype(np.float32)

        # Detect Spiking Neurons (Vm >= Vthresh and not in refractory)
        spiking_mask = (self.V_m >= self.V_thresh) & (self.refractory <= 0.0)
        spiking_indices = np.where(spiking_mask)[0]
        spikes_count = len(spiking_indices)
        self.spike_accumulator += spikes_count
        self.recent_spiking_indices = spiking_indices

        # Synaptic Event Propagation
        if spikes_count > 0:
            self.V_m[spiking_indices] = -70.0
            self.refractory[spiking_indices] = 20.0

            if spikes_count <= 60:
                prop_nodes = spiking_indices
            else:
                prop_nodes = random.sample(spiking_indices.tolist(), 60)
            
            for p_idx in prop_nodes:
                p_start = self.indptr[p_idx]
                p_end = self.indptr[p_idx + 1]
                if p_end > p_start:
                    targets = self.syn_post[p_start:p_end]
                    weights = self.syn_weight[p_start:p_end]
                    pol = float(self.polarity[p_idx])
                    dV = np.clip(weights * (0.05 * pol), -1.8, 1.8)
                    self.V_m[targets] += dV

                    if self.is_me[p_idx]: self.traffic_optic += 1
                    elif self.is_eb[p_idx]: self.traffic_eb += 1
                    elif self.is_dn[p_idx]: self.traffic_dn += 1

        # -------------------------------------------------------------
        # 3. PURE BIOLOGICAL KINEMATIC INTEGRATION
        # -------------------------------------------------------------
        # Biological Motor Pool (DN): Drives wingbeat frequency & speed
        if len(self.dn_indices) > 0:
            dn_mean_vm = float(np.mean(self.V_m[self.dn_indices]))
            self.motor_vm = dn_mean_vm
            target_wbf = 214.0 + (dn_mean_vm - (-65.0)) * 2.2
            self.fly_wbf = int(np.clip(target_wbf, 192.0, 244.0))
            target_speed = 1.2 + max(0.0, (dn_mean_vm - (-65.0)) * 0.12)
            self.fly_speed += (target_speed - self.fly_speed) * dt * 2.0

        # Biological Central Complex (EB): Drives flight heading from attractor bump!
        eb_potentials = np.maximum(0.0, self.V_m[self.eb_indices] - (-58.0))
        if np.sum(eb_potentials) > 1.0:
            sin_val = float(np.sum(eb_potentials * np.sin(self.eb_angles)))
            cos_val = float(np.sum(eb_potentials * np.cos(self.eb_angles)))
            self.epg_ring_angle = math.atan2(sin_val, cos_val)

        # Smooth Arena Boundary Guidance (Circular flight arena R=85m)
        arena_radius = 85.0
        dist = float(math.sqrt(self.fly_pos[0]**2 + self.fly_pos[2]**2))
        if dist > arena_radius:
            inward_angle = math.atan2(-self.fly_pos[0], -self.fly_pos[2])
            if self.chip_engaged:
                # Harmoniously turn the chip's commanded heading inward (no rogue current fighting the chip!)
                inward_err = (inward_angle - self.commanded_heading + math.pi) % (2.0 * math.pi) - math.pi
                self.commanded_heading += inward_err * (dt * 1.5)
            else:
                heading_err = (inward_angle - self.fly_heading + math.pi) % (2.0 * math.pi) - math.pi
                self.fly_heading += heading_err * (dt * 2.5)
                self.boundary_stim_timer -= dt
                if self.boundary_stim_timer <= 0.0:
                    diff_ang = np.abs((self.eb_angles - inward_angle + math.pi) % (2.0 * math.pi) - math.pi)
                    inward_eb = self.eb_indices[diff_ang < 0.8]
                    if len(inward_eb) > 0:
                        self.V_m[inward_eb] += 12.0
                    self.boundary_stim_timer = 0.5
        else:
            self.boundary_stim_timer = max(0.0, self.boundary_stim_timer - dt)

        self.fly_target_heading = self.epg_ring_angle

        heading_diff = (self.fly_target_heading - self.fly_heading + math.pi) % (2 * math.pi) - math.pi
        self.fly_heading += heading_diff * dt * 3.2
        target_roll = float(np.clip(heading_diff * 0.40, -0.60, 0.60))
        self.fly_roll += (target_roll - self.fly_roll) * dt * 5.0
        self.fly_pitch = math.sin(now * 2.0) * 0.04

        forward_vec = np.array([
            math.sin(self.fly_heading),
            math.sin(now * 1.8) * 0.05,
            math.cos(self.fly_heading)
        ], dtype=np.float32)
        self.fly_pos += forward_vec * (self.fly_speed * dt * 4.5)

        if len(self.vortex_trail) == 0 or np.linalg.norm(self.fly_pos - self.vortex_trail[-1]) > 1.2:
            self.vortex_trail.append(self.fly_pos.copy())
            if len(self.vortex_trail) > 50:
                self.vortex_trail.pop(0)

        # -------------------------------------------------------------
        # 4. RENDER DUAL VIEWPORTS (Flight Canvas + 158k Brain & Chip Canvas)
        # -------------------------------------------------------------
        self.render_flight_canvas(now)
        self.render_brain_canvas(now)

        # -------------------------------------------------------------
        # 5. TELEMETRY & OSCILLOSCOPE
        # -------------------------------------------------------------
        dn_y = int(27 - (self.motor_vm - (-65.0)) * 1.2)
        chip_y = int(48 - (self.chip_output_current / 42.0) * 20.0)
        self.update_oscilloscope(dn_y, chip_y)

        self.lbl_speed.configure(text=f"HIZ: {self.fly_speed:.2f} m/s")
        self.lbl_wbf.configure(text=f"KANAT: {self.fly_wbf} Hz")
        heading_deg = int(((self.fly_heading % (math.pi * 2)) + math.pi * 2) % (math.pi * 2) * (180.0 / math.pi))
        self.lbl_heading.configure(text=f"EB PUSULA: {heading_deg:03d}°")

        if now - self.last_sec_time >= 1.0:
            self.spikes_per_sec = int(self.spike_accumulator / (now - self.last_sec_time))
            self.lbl_spikes.configure(text=f"SPİKE FREKANSI: {self.spikes_per_sec:,} Hz")
            self.spike_accumulator = 0
            self.lbl_traffic.configure(
                text=f"Biyo-Trafik: Optik: {self.traffic_optic} Hz | Central: {self.traffic_eb} Hz | Motor: {self.traffic_dn} Hz"
            )
            self.traffic_optic = 0
            self.traffic_eb = 0
            self.traffic_dn = 0
            self.last_sec_time = now

        # Schedule Next Frame (~60 FPS)
        self.root.after(16, self.update_loop)

    def render_flight_canvas(self, now):
        W = self.canvas_flight.winfo_width()
        H = self.canvas_flight.winfo_height()
        if W < 50 or H < 50: return

        cam_dist = 14.0
        cam_height = 4.2
        target_cam_pos = np.array([
            self.fly_pos[0] - math.sin(self.fly_heading) * cam_dist,
            self.fly_pos[1] + cam_height,
            self.fly_pos[2] - math.cos(self.fly_heading) * cam_dist
        ], dtype=np.float32)

        # Smooth pursuit camera behind fly
        self.cam_flight_pos += (target_cam_pos - self.cam_flight_pos) * 0.18
        cam_pos = self.cam_flight_pos

        look_target = np.array([
            self.fly_pos[0],
            self.fly_pos[1] + 0.6,
            self.fly_pos[2] + math.sin(self.fly_heading) * 1.5
        ], dtype=np.float32)

        f_vec = look_target - cam_pos
        f_norm = float(np.linalg.norm(f_vec))
        if f_norm < 1e-4: return
        f = f_vec / f_norm
        world_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        r_vec = np.cross(f, world_up)
        r_norm = float(np.linalg.norm(r_vec))
        r = (r_vec / r_norm) if r_norm > 1e-4 else np.array([1.0, 0.0, 0.0], dtype=np.float32)
        u = np.cross(r, f)

        fov = 380.0
        def project_pt(pt_3d):
            rel = pt_3d - cam_pos
            cz = float(np.dot(rel, f))
            if cz < 1.0: return None, cz
            cx_val = float(np.dot(rel, r))
            cy_val = float(np.dot(rel, u))
            sx = int(cx_val * fov / cz + W / 2)
            sy = int(-cy_val * fov / cz + H / 2)
            return (sx, sy), cz

        # Near-plane 3D Line Segment Clipper (Prevents disappearing/cutting lines)
        def project_segment(p1_w, p2_w):
            rel1 = p1_w - cam_pos
            rel2 = p2_w - cam_pos
            z1 = float(np.dot(rel1, f))
            z2 = float(np.dot(rel2, f))
            NEAR = 1.0
            if z1 < NEAR and z2 < NEAR:
                return None
            if z1 < NEAR:
                t = (NEAR - z1) / (z2 - z1)
                rel1 = rel1 + t * (rel2 - rel1)
                z1 = NEAR
            elif z2 < NEAR:
                t = (NEAR - z2) / (z1 - z2)
                rel2 = rel2 + t * (rel1 - rel2)
                z2 = NEAR
            
            x1, y1 = float(np.dot(rel1, r)), float(np.dot(rel1, u))
            x2, y2 = float(np.dot(rel2, r)), float(np.dot(rel2, u))
            s1 = (int(x1 * fov / z1 + W / 2), int(-y1 * fov / z1 + H / 2))
            s2 = (int(x2 * fov / z2 + W / 2), int(-y2 * fov / z2 + H / 2))
            return s1, s2, (z1 + z2) * 0.5

        img = Image.new("RGB", (W, H), (2, 5, 14))
        draw = ImageDraw.Draw(img)

        # 1. 3D Infinite Dynamic Ground Grid
        ground_y = -8.0
        grid_step = 8.0
        grid_radius = 56.0

        center_x = round(float(self.fly_pos[0]) / grid_step) * grid_step
        center_z = round(float(self.fly_pos[2]) / grid_step) * grid_step

        gx_min = center_x - grid_radius
        gx_max = center_x + grid_radius
        gz_min = center_z - grid_radius
        gz_max = center_z + grid_radius

        for gx in np.arange(gx_min, gx_max + grid_step, grid_step, dtype=np.float32):
            p1_w = np.array([gx, ground_y, gz_min], dtype=np.float32)
            p2_w = np.array([gx, ground_y, gz_max], dtype=np.float32)
            res = project_segment(p1_w, p2_w)
            if res:
                s1, s2, cz_avg = res
                fade = int(np.clip(140.0 - cz_avg * 2.2, 8.0, 50.0))
                draw.line([s1, s2], fill=(fade // 3, fade // 2, fade), width=1)

        for gz in np.arange(gz_min, gz_max + grid_step, grid_step, dtype=np.float32):
            p1_w = np.array([gx_min, ground_y, gz], dtype=np.float32)
            p2_w = np.array([gx_max, ground_y, gz], dtype=np.float32)
            res = project_segment(p1_w, p2_w)
            if res:
                s1, s2, cz_avg = res
                fade = int(np.clip(140.0 - cz_avg * 2.2, 8.0, 50.0))
                draw.line([s1, s2], fill=(fade // 3, fade // 2, fade), width=1)

        # 2. 3D Neon Gate Rings along circular flight course
        segments = 16
        for rx, ry, rz, radius, tangent_ang in self.neon_rings:
            ring_center = np.array([rx, ry, rz], dtype=np.float32)
            cos_t, sin_t = math.cos(tangent_ang), math.sin(tangent_ang)
            norm_x = -sin_t
            norm_z = cos_t
            
            for s in range(segments):
                ang1 = s * (2.0 * math.pi / segments)
                ang2 = (s + 1) * (2.0 * math.pi / segments)
                pt1_local = np.array([norm_x * math.cos(ang1) * radius, math.sin(ang1) * radius, norm_z * math.cos(ang1) * radius], dtype=np.float32)
                pt2_local = np.array([norm_x * math.cos(ang2) * radius, math.sin(ang2) * radius, norm_z * math.cos(ang2) * radius], dtype=np.float32)
                
                res = project_segment(ring_center + pt1_local, ring_center + pt2_local)
                if res:
                    s1, s2, cz_avg = res
                    dist_to_fly = float(np.linalg.norm(ring_center - self.fly_pos))
                    gate_col = (0, 255, 255) if dist_to_fly < 15.0 else (0, 175, 230)
                    draw.line([s1, s2], fill=gate_col, width=2)

        # 3. 3D Trailing Vortex Trail
        if len(self.vortex_trail) > 1:
            for i in range(len(self.vortex_trail) - 1):
                p1_w = self.vortex_trail[i] + np.array([0.0, 0.2, 0.0], dtype=np.float32)
                p2_w = self.vortex_trail[i + 1] + np.array([0.0, 0.2, 0.0], dtype=np.float32)
                res = project_segment(p1_w, p2_w)
                if res:
                    s1, s2, cz_avg = res
                    alpha = (i + 1) / float(len(self.vortex_trail))
                    col_b = int(255 * alpha)
                    col_g = int(190 * alpha)
                    col_r = int(50 * alpha)
                    draw.line([s1, s2], fill=(col_r, col_g, col_b), width=2)

        # 4. Render 3D Drosophila Fly Model (Painter's Algorithm)
        render_queue = []
        cy_h, sy_h = math.cos(self.fly_heading), math.sin(self.fly_heading)
        cr, sr = math.cos(self.fly_roll), math.sin(self.fly_roll)
        cp, sp_pitch = math.cos(self.fly_pitch), math.sin(self.fly_pitch)

        def to_fly_world(local_pt):
            x1 = local_pt[0] * cr - local_pt[1] * sr
            y1 = local_pt[0] * sr + local_pt[1] * cr
            z1 = local_pt[2]
            x2 = x1
            y2 = y1 * cp - z1 * sp_pitch
            z2 = y1 * sp_pitch + z1 * cp
            x3 = x2 * cy_h + z2 * sy_h
            y3 = y2
            z3 = -x2 * sy_h + z2 * cy_h
            return self.fly_pos + np.array([x3, y3, z3], dtype=np.float32)

        light_dir = np.array([0.4, 0.8, -0.4], dtype=np.float32)
        light_dir /= np.linalg.norm(light_dir)

        # Fly Segments: (name, local_center_3d, rx, ry, rz, (r, g, b))
        fly_parts = [
            ("head", np.array([0.0, 0.2, 2.2], dtype=np.float32), 0.8, 0.7, 0.8, (140, 40, 30)),
            ("eye_l", np.array([-0.65, 0.35, 2.3], dtype=np.float32), 0.45, 0.55, 0.5, (220, 30, 20)),
            ("eye_r", np.array([0.65, 0.35, 2.3], dtype=np.float32), 0.45, 0.55, 0.5, (220, 30, 20)),
            ("thorax", np.array([0.0, 0.3, 0.9], dtype=np.float32), 0.95, 0.85, 1.2, (75, 55, 40)),
            ("abdom_1", np.array([0.0, 0.1, -0.6], dtype=np.float32), 0.9, 0.75, 0.8, (160, 120, 50)),
            ("abdom_2", np.array([0.0, -0.1, -1.6], dtype=np.float32), 0.8, 0.7, 0.8, (40, 30, 25)),
            ("abdom_3", np.array([0.0, -0.3, -2.5], dtype=np.float32), 0.65, 0.6, 0.7, (150, 110, 45)),
            ("abdom_tip", np.array([0.0, -0.5, -3.3], dtype=np.float32), 0.45, 0.4, 0.5, (30, 25, 20)),
        ]

        for name, center, rx, ry, rz, base_col in fly_parts:
            w_center = to_fly_world(center)
            sp, cz = project_pt(w_center)
            if sp:
                norm_est = (w_center - self.fly_pos) / max(1.0, float(np.linalg.norm(w_center - self.fly_pos)))
                diff = max(0.2, float(np.dot(norm_est, light_dir)))
                col = (int(base_col[0] * diff), int(base_col[1] * diff), int(base_col[2] * diff))
                scale = fov / cz
                prx = max(2, int(rx * scale))
                pry = max(2, int(ry * scale))
                render_queue.append((cz, "ellipse", sp, prx, pry, col))

        # WERR Cyber-Backpack Implant Chip on Dorsal Thorax
        chip_backpack_pos = to_fly_world(np.array([0.0, 1.25, 0.9], dtype=np.float32))
        sp_chip, cz_chip = project_pt(chip_backpack_pos)
        if sp_chip:
            scale_ch = fov / cz_chip
            chip_col = (0, 240, 255) if self.chip_engaged else (90, 100, 115)
            render_queue.append((cz_chip, "chip_box", sp_chip, int(0.7 * scale_ch), int(0.5 * scale_ch), chip_col))

        # Animated Wings (Flapping at 200-244 Hz)
        wing_phase = now * (self.fly_wbf * 2.0 * math.pi)
        wing_flap = math.sin(wing_phase) * 0.55

        # Left Wing
        w_hinge_l = to_fly_world(np.array([-0.8, 0.8, 1.0], dtype=np.float32))
        w_tip_l = to_fly_world(np.array([-4.4, 0.8 + wing_flap * 2.2, -1.8], dtype=np.float32))
        w_edge_l = to_fly_world(np.array([-3.2, 0.8 + wing_flap * 1.5, 0.6], dtype=np.float32))
        p_hl, cz_hl = project_pt(w_hinge_l)
        p_tl, cz_tl = project_pt(w_tip_l)
        p_el, cz_el = project_pt(w_edge_l)
        if p_hl and p_tl and p_el:
            cz_avg = (cz_hl + cz_tl + cz_el) / 3.0
            render_queue.append((cz_avg, "polygon", [p_hl, p_el, p_tl], (180, 230, 255, 120)))

        # Right Wing (Synchronous flapping with left wing)
        w_hinge_r = to_fly_world(np.array([0.8, 0.8, 1.0], dtype=np.float32))
        w_tip_r = to_fly_world(np.array([4.4, 0.8 + wing_flap * 2.2, -1.8], dtype=np.float32))
        w_edge_r = to_fly_world(np.array([3.2, 0.8 + wing_flap * 1.5, 0.6], dtype=np.float32))
        p_hr, cz_hr = project_pt(w_hinge_r)
        p_tr, cz_tr = project_pt(w_tip_r)
        p_er, cz_er = project_pt(w_edge_r)
        if p_hr and p_tr and p_er:
            cz_avg = (cz_hr + cz_tr + cz_er) / 3.0
            render_queue.append((cz_avg, "polygon", [p_hr, p_er, p_tr], (180, 230, 255, 120)))

        # Painter's Algorithm Depth Sort (Farthest to Closest)
        render_queue.sort(key=lambda item: item[0], reverse=True)

        for item in render_queue:
            cz, kind = item[0], item[1]
            if kind == "ellipse":
                sp, prx, pry, col = item[2], item[3], item[4], item[5]
                draw.ellipse([sp[0] - prx, sp[1] - pry, sp[0] + prx, sp[1] + pry], fill=col, outline=(col[0]//2, col[1]//2, col[2]//2))
            elif kind == "chip_box":
                sp, prx, pry, col = item[2], item[3], item[4], item[5]
                # High-tech cyber implant rectangle on fly's back
                draw.rectangle([sp[0] - prx, sp[1] - pry, sp[0] + prx, sp[1] + pry], fill=col, outline=(255, 255, 255))
            elif kind == "polygon":
                pts, col = item[2], item[3]
                draw.polygon(pts, fill=col[:3], outline=(220, 245, 255))

        # HUD Overlay
        draw.text((14, 14), f"PUSULA: {int(((self.fly_heading%(math.pi*2))+math.pi*2)%(math.pi*2)*(180/math.pi)):03d}°", fill=(0, 240, 255))
        draw.text((14, 30), f"HIZ: {self.fly_speed:.2f} m/s", fill=(56, 189, 248))
        draw.text((14, 46), f"KANAT: {self.fly_wbf} Hz", fill=(251, 191, 36))
        chip_label = "ÇİP: BAĞLI [1.024 PIN]" if self.chip_engaged else "ÇİP: AYRILDI (BYPASS)"
        draw.text((14, 62), chip_label, fill=(0, 242, 254) if self.chip_engaged else (148, 163, 184))

        self.tk_img_flight = ImageTk.PhotoImage(img)
        self.canvas_flight.create_image(0, 0, image=self.tk_img_flight, anchor="nw")

    def render_brain_canvas(self, now):
        W = self.canvas_brain.winfo_width()
        H = self.canvas_brain.winfo_height()
        if W < 50 or H < 50: return

        # Dynamic Head-Locked vs Free Orbit
        brain_yaw = (self.fly_heading + math.pi + self.cam_yaw) if self.is_head_locked else self.cam_yaw
        brain_pitch = self.cam_pitch

        cy, sy = math.cos(brain_yaw), math.sin(brain_yaw)
        cp, sp = math.cos(brain_pitch), math.sin(brain_pitch)

        f = np.array([sy * cp, sp, cy * cp], dtype=np.float32)
        r = np.array([cy, 0.0, -sy], dtype=np.float32)
        u = np.cross(r, f)
        cam_pos = -f * self.cam_dist

        # -------------------------------------------------------------
        # 1. Project 158,262 Biological Neurons
        # -------------------------------------------------------------
        rel = self.pos - cam_pos
        cz = np.dot(rel, f)
        valid = cz > 20.0

        cx = np.dot(rel[valid], r)
        cy_val = np.dot(rel[valid], u)
        fov = 480.0

        sx = (cx * fov / cz[valid] + W / 2).astype(np.int32)
        sy_arr = (-cy_val * fov / cz[valid] + H / 2).astype(np.int32)

        in_bounds = (sx >= 0) & (sx < W) & (sy_arr >= 0) & (sy_arr < H)
        sx_in = sx[in_bounds]
        sy_in = sy_arr[in_bounds]

        # Initialize Image Buffer
        img_arr = np.zeros((H, W, 3), dtype=np.uint8)
        img_arr[:] = [3, 6, 15] # Deep obsidian background

        # Plot Biological Base Point Cloud
        active_colors = self.base_colors[valid][in_bounds]
        img_arr[sy_in, sx_in] = active_colors

        # Render Spiking Biological Neurons as White Beacons
        if len(self.recent_spiking_indices) > 0:
            spk_indices = self.recent_spiking_indices
            rel_spk = self.pos[spk_indices] - cam_pos
            cz_spk = np.dot(rel_spk, f)
            valid_spk = cz_spk > 20.0
            if np.any(valid_spk):
                cx_spk = np.dot(rel_spk[valid_spk], r)
                cy_spk = np.dot(rel_spk[valid_spk], u)
                sx_spk = (cx_spk * fov / cz_spk[valid_spk] + W / 2).astype(np.int32)
                sy_spk = (-cy_spk * fov / cz_spk[valid_spk] + H / 2).astype(np.int32)
                in_spk = (sx_spk >= 2) & (sx_spk < W - 2) & (sy_spk >= 2) & (sy_spk < H - 2)
                sx_s = sx_spk[in_spk]
                sy_s = sy_spk[in_spk]

                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        img_arr[sy_s + dy, sx_s + dx] = [255, 255, 255]

        # -------------------------------------------------------------
        # 2. Project WERR Neural Coprocessor Chip (1,024 Micro-Grid Pins)
        # -------------------------------------------------------------
        rel_chip = self.chip_pos - cam_pos
        cz_chip = np.dot(rel_chip, f)
        valid_ch = cz_chip > 20.0

        if np.any(valid_ch):
            cx_ch = np.dot(rel_chip[valid_ch], r)
            cy_ch = np.dot(rel_chip[valid_ch], u)
            sx_ch = (cx_ch * fov / cz_chip[valid_ch] + W / 2).astype(np.int32)
            sy_ch = (-cy_ch * fov / cz_chip[valid_ch] + H / 2).astype(np.int32)

            in_ch = (sx_ch >= 1) & (sx_ch < W - 1) & (sy_ch >= 1) & (sy_ch < H - 1)
            sx_c = sx_ch[in_ch]
            sy_c = sy_ch[in_ch]

            # Dynamic RGB coloring per WERR silicon neuron based on real-time membrane potential
            w_vm_visible = self.werr_vm[valid_ch][in_ch]
            if self.chip_engaged:
                norm_act = np.clip((w_vm_visible - (-65.0)) / 20.0, 0.0, 1.0)
                # Resting: Deep electric cyan/blue [15, 85, 210]
                # Active / Spiking: Brilliant Amber-Gold to Pure White [255, 235, 70] -> [255, 255, 255]
                r_ch = (15 + norm_act * 240).astype(np.uint8)
                g_ch = (85 + norm_act * 155).astype(np.uint8)
                b_ch = (210 - norm_act * 110 + (norm_act > 0.75) * 150).astype(np.uint8)
                pin_colors = np.column_stack([r_ch, g_ch, b_ch])
            else:
                pin_colors = np.full((len(sx_c), 3), [65, 75, 90], dtype=np.uint8)

            # Plot 2x2 pixels for each chip pin
            for dx in (0, 1):
                for dy in (0, 1):
                    img_arr[sy_c + dy, sx_c + dx] = pin_colors

        # Convert to PIL Image for Vector Overlays (Silicon Frame & Probes)
        img = Image.fromarray(img_arr)
        draw = ImageDraw.Draw(img)

        # -------------------------------------------------------------
        # 3. Draw Chip Silicon Substrate Frame & Penetrating Probes
        # -------------------------------------------------------------
        # Chip Carrier Corners in 3D:
        c_corners = [
            np.array([-40.0, 105.0, 15.0], dtype=np.float32),
            np.array([40.0, 105.0, 15.0], dtype=np.float32),
            np.array([40.0, 105.0, 55.0], dtype=np.float32),
            np.array([-40.0, 105.0, 55.0], dtype=np.float32),
        ]
        s_corners = []
        for pt in c_corners:
            rel_pt = pt - cam_pos
            cz_pt = float(np.dot(rel_pt, f))
            if cz_pt > 20.0:
                cx_pt = float(np.dot(rel_pt, r))
                cy_pt = float(np.dot(rel_pt, u))
                sx_p = int(cx_pt * fov / cz_pt + W / 2)
                sy_p = int(-cy_pt * fov / cz_pt + H / 2)
                s_corners.append((sx_p, sy_p))

        if len(s_corners) == 4:
            s_corners.append(s_corners[0]) # Close loop
            frame_col = (0, 242, 254) if self.chip_engaged else (80, 90, 105)
            draw.line(s_corners, fill=frame_col, width=2)
            draw.text((s_corners[0][0] - 10, s_corners[0][1] - 16), "WERR-CHIP v1.2", fill=frame_col)

        # Draw Penetrating Electrode Shanki Leads (Chip to Brain Circuit Targets)
        chip_center_3d = np.array([0.0, 105.0, 35.0], dtype=np.float32)
        rel_cc = chip_center_3d - cam_pos
        cz_cc = float(np.dot(rel_cc, f))
        
        if cz_cc > 20.0:
            sx_cc = int(float(np.dot(rel_cc, r)) * fov / cz_cc + W / 2)
            sy_cc = int(-float(np.dot(rel_cc, u)) * fov / cz_cc + H / 2)

            for probe_name, target_3d, probe_col in self.probe_targets:
                rel_t = target_3d - cam_pos
                cz_t = float(np.dot(rel_t, f))
                if cz_t > 20.0:
                    sx_t = int(float(np.dot(rel_t, r)) * fov / cz_t + W / 2)
                    sy_t = int(-float(np.dot(rel_t, u)) * fov / cz_t + H / 2)

                    if self.chip_engaged:
                        # Active probe line with pulse packet
                        draw.line([(sx_cc, sy_cc), (sx_t, sy_t)], fill=probe_col, width=2)
                        # Sliding pulse bead
                        bead_alpha = (math.sin(self.chip_pulse_phase + cz_t * 0.1) * 0.5 + 0.5)
                        bx = int(sx_cc + (sx_t - sx_cc) * bead_alpha)
                        by = int(sy_cc + (sy_t - sy_cc) * bead_alpha)
                        draw.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(255, 255, 255))
                    else:
                        # Inactive dim line
                        draw.line([(sx_cc, sy_cc), (sx_t, sy_t)], fill=(50, 60, 75), width=1)

        # 3D Gyroscopic Axis Gizmo
        axis_len = 28.0
        p_orig = np.array([W - 48, H - 48])
        ax_x = p_orig + np.array([int(r[0] * axis_len), int(-r[1] * axis_len)])
        ax_y = p_orig + np.array([int(u[0] * axis_len), int(-u[1] * axis_len)])
        ax_z = p_orig + np.array([int(f[0] * axis_len), int(-f[1] * axis_len)])
        draw.line([tuple(p_orig), tuple(ax_x)], fill=(255, 80, 80), width=2)
        draw.line([tuple(p_orig), tuple(ax_y)], fill=(80, 255, 80), width=2)
        draw.line([tuple(p_orig), tuple(ax_z)], fill=(80, 180, 255), width=2)
        draw.text((W - 55, H - 90), "FAFB-3D", fill=(148, 163, 184))

        # Status text
        draw.text((14, 14), f"BİYOLOJİK NÖRON: {self.TOTAL_NODES:,} (FlyWire)", fill=(241, 245, 249))
        draw.text((14, 30), f"WERR ÇİP ELEKTROTLARI: 1.024 Pin ({'AKTİF' if self.chip_engaged else 'BYPASS'})", fill=(0, 242, 254) if self.chip_engaged else (148, 163, 184))
        draw.text((14, 46), f"SİNAPTİK KÖPRÜLER: 3.99M Biyo + 4 Penetran Shank", fill=(192, 132, 252))

        self.tk_img_brain = ImageTk.PhotoImage(img)
        self.canvas_brain.create_image(0, 0, image=self.tk_img_brain, anchor="nw")

    def update_oscilloscope(self, dn_y, chip_y):
        self.osc_dn_history.pop(0)
        self.osc_dn_history.append(int(np.clip(dn_y, 4, 50)))

        self.osc_chip_history.pop(0)
        self.osc_chip_history.append(int(np.clip(chip_y, 4, 50)))

        self.canvas_osc.delete("all")
        W = self.canvas_osc.winfo_width()
        H = self.canvas_osc.winfo_height()
        if W < 20 or H < 20: return

        # Baseline
        base_y = 27
        self.canvas_osc.create_line(0, base_y, W, base_y, fill="#1e293b", dash=(3, 3))

        # 1. DN Motor Voltage Waveform (Amber)
        pts_dn = []
        n_pts = len(self.osc_dn_history)
        step = W / max(1, n_pts - 1)
        for i, val in enumerate(self.osc_dn_history):
            pts_dn.extend([int(i * step), val])

        if len(pts_dn) >= 4:
            self.canvas_osc.create_line(pts_dn, fill="#fbbf24", width=2)

        # 2. WERR Chip Output Voltage Waveform (Cyan)
        pts_chip = []
        for i, val in enumerate(self.osc_chip_history):
            pts_chip.extend([int(i * step), val])

        if len(pts_chip) >= 4 and self.chip_engaged:
            self.canvas_osc.create_line(pts_chip, fill="#00f2fe", width=2)

        self.canvas_osc.create_text(8, 10, text="Sarı: DN Biyo-Voltajı | Mavi: WERR Çip İmpuls", fill="#fbbf24", anchor="w", font=("Consolas", 8))
        self.canvas_osc.create_text(W - 8, 10, text=f"DN: {self.motor_vm:.1f} mV | Çip: +{self.chip_output_current:.1f} mV", fill="#f8fafc", anchor="e", font=("Consolas", 8, "bold"))

def main():
    print("=" * 70)
    print("🧠 DROSOPHILA & WERR BİYO-NÖRAL İMPLANT ÇİPİ SİMÜLATÖRÜ")
    print("158.262 Biyolojik Nöron + 1.024 Kanallı WERR Protez Çip Matrisi")
    print("======================================================================\n")
    net_data = load_dataset()
    root = tk.Tk()
    app = BioNeuralFlyChipApp(root, net_data)
    root.mainloop()

if __name__ == "__main__":
    main()
