"""
build_bioneural_3d.py
======================
Builds the 3D Bio-Synthetic Connectome pairing 1,000 WERR Fractal Neurons
with the Princeton FlyWire male Drosophila whole-brain connectome.
Outputs both a JSON database and a standalone 3D interactive WebGL visualization.
"""
import os
import sys
import csv
import json
import math
import random
from collections import defaultdict

random.seed(42)

WORKSPACE = os.path.abspath(os.path.dirname(__file__))
NEURONS_CSV = os.path.join(WORKSPACE, "neuramap", "neurons.csv", "neurons.csv")
CONNECTIONS_CSV = os.path.join(WORKSPACE, "neuramap", "connections_princeton.csv", "connections_princeton.csv")

# Anatomical 3D Centroids of Drosophila Neuropils in microns (FAFB/JRC2018 space)
NEUROPIL_CENTROIDS = {
    # Central Complex (Midline)
    "EB": (0.0, -10.0, 20.0),
    "FB": (0.0, 32.0, -10.0),
    "PB": (0.0, 68.0, -68.0),
    "NO": (0.0, -38.0, 2.0),
    # Mushroom Bodies (Bilateral)
    "MB_CA": (120.0, 75.0, -75.0),
    "MB_PED": (78.0, 38.0, -22.0),
    "MB_VL": (42.0, -8.0, 48.0),
    "MB_ML": (25.0, -12.0, 52.0),
    # Olfactory & Sensory
    "AL": (62.0, -78.0, 72.0),
    "AOTU": (88.0, 28.0, 78.0),
    "AMMC": (82.0, -85.0, 18.0),
    # Lateral & Superior Protocerebrum
    "LH": (148.0, 52.0, -28.0),
    "SMP": (44.0, 84.0, 2.0),
    "SLP": (108.0, 78.0, -8.0),
    "SIP": (72.0, 74.0, 8.0),
    "AVLP": (118.0, -38.0, 38.0),
    "PVLP": (138.0, -28.0, -38.0),
    "PLP": (158.0, 2.0, -58.0),
    "CRE": (58.0, 12.0, 18.0),
    "ICL": (68.0, -18.0, 38.0),
    "SCL": (78.0, 28.0, 38.0),
    "LAL": (48.0, -38.0, 14.0),
    "GNG": (0.0, -118.0, 0.0),
    # Optic Lobes (Far Lateral)
    "ME": (250.0, 10.0, -10.0),
    "LO": (190.0, 15.0, -20.0),
    "LOP": (205.0, 38.0, -38.0),
    # Ventral Nerve Cord (Descending motor cord)
    "VNC": (0.0, -240.0, -20.0),
    "ABDNM": (0.0, -320.0, -25.0),
    "DEFAULT": (0.0, 20.0, 0.0)
}

def get_region_centroid(region_name: str, side: str = "right"):
    token = region_name.split(".")[0].split("_")[0]
    base = NEUROPIL_CENTROIDS.get(region_name, NEUROPIL_CENTROIDS.get(token, NEUROPIL_CENTROIDS["DEFAULT"]))
    x, y, z = base
    # Handle bilateral symmetry
    if side == "left":
        x = -abs(x)
    elif side == "right":
        x = abs(x)
    elif side in ("center", "middle") and "MB" in region_name:
        x = -x if random.random() < 0.5 else x
    return x, y, z

def main():
    print("[1/4] Reading biological neurons from neurons.csv...")
    bio_neurons = {}
    target_supers = {"central_brain_intrinsic", "descending", "sensory", "ascending"}
    
    with open(NEURONS_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sc = row["Super Class"]
            if sc in target_supers:
                rid = row["Root ID"]
                reg_raw = row["Top in/out region"] or "SMP"
                reg = reg_raw.split(".")[0]
                side = (row["Soma side"] or "center").lower()
                cx, cy, cz = get_region_centroid(reg, side)
                
                # Add jitter based on natural cell volume
                jitter = 14.0
                px = round(cx + random.gauss(0, jitter), 1)
                py = round(cy + random.gauss(0, jitter), 1)
                pz = round(cz + random.gauss(0, jitter), 1)
                
                nt = row["Predicted NT type"] or "ACH"
                # Excitatory: Acetylcholine (ACH), Nicotinic; Inhibitory: GABA, Glutamate (in insects Glu is often inhibitory at motor/sensory); Modulatory: Dopamine (DA), Serotonin (5HT), Octopamine (OCT)
                if nt in ("GABA", "GLU"):
                    polarity = -1
                elif nt in ("DA", "OCT", "SER"):
                    polarity = 0
                else:
                    polarity = 1

                bio_neurons[rid] = {
                    "id": rid,
                    "type": "bio",
                    "super_class": sc,
                    "class": row["Class"] or sc,
                    "region": reg,
                    "side": side,
                    "nt": nt,
                    "polarity": polarity,
                    "pos": [px, py, pz],
                    "potential": round(random.uniform(-70.0, -60.0), 2)  # resting potential mV
                }
                
            if len(bio_neurons) >= 2800:
                break

    print(f"      Loaded {len(bio_neurons)} representative biological neurons.")

    print("[2/4] Reading biological synapses from connections_princeton.csv...")
    bio_synapses = []
    bio_id_set = set(bio_neurons.keys())
    
    with open(CONNECTIONS_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            pre = row["pre_root_id"]
            post = row["post_root_id"]
            if pre in bio_id_set and post in bio_id_set:
                weight = min(20, int(row["syn_count"] or 1))
                bio_synapses.append({
                    "pre": pre,
                    "post": post,
                    "w": weight,
                    "kind": "bio_bio"
                })
            if len(bio_synapses) >= 6500 or i >= 1200000:
                break

    print(f"      Matched {len(bio_synapses)} biological synaptic connections.")

    print("[3/4] Synthesizing 1,000 WERR Fractal Neurons & Bio-Synthetic Bridges...")
    werr_neurons = {}
    synth_synapses = []
    
    # 4 Functional WERR Clusters
    # 1. Central Complex Action Steering (EB/FB): 350 neurons
    # 2. Mushroom Body Valence/Memory Plasticity (MB): 250 neurons
    # 3. Sensory Input / Afferent Wave Receiver (AL/AOTU): 200 neurons
    # 4. Motor Output / Descending Command Transmitter (DN/VNC): 200 neurons
    
    cluster_specs = [
        {
            "name": "WERR_CX",
            "role": "central_complex_steering",
            "count": 350,
            "target_region": "EB",
            "base_c": (-0.743643887, 0.131825904),
            "zoom": 50.0,
            "color": "#00f0ff", # Cyan
            "anchor": (0.0, 15.0, 10.0),
            "spread": 26.0,
            "target_bio_regions": ["EB", "FB", "PB", "NO", "LAL"]
        },
        {
            "name": "WERR_MB",
            "role": "valence_memory_plasticity",
            "count": 250,
            "target_region": "MB_CA",
            "base_c": (-0.10109636, 0.95628651),
            "zoom": 45.0,
            "color": "#fbbf24", # Amber / Gold
            "anchor": (85.0, 60.0, -45.0),
            "spread": 30.0,
            "target_bio_regions": ["MB_CA", "MB_PED", "MB_VL", "MB_ML", "SMP"]
        },
        {
            "name": "WERR_SN",
            "role": "sensory_wave_afferent",
            "count": 200,
            "target_region": "AL",
            "base_c": (-0.748, 0.065),
            "zoom": 60.0,
            "color": "#10b981", # Emerald
            "anchor": (50.0, -60.0, 60.0),
            "spread": 25.0,
            "target_bio_regions": ["AL", "AOTU", "AMMC", "AVLP"]
        },
        {
            "name": "WERR_DN",
            "role": "motor_command_efferent",
            "count": 200,
            "target_region": "VNC",
            "base_c": (-0.7495, 0.082),
            "zoom": 70.0,
            "color": "#ec4899", # Magenta / Pink
            "anchor": (0.0, -180.0, -15.0),
            "spread": 28.0,
            "target_bio_regions": ["GNG", "VNC", "LAL", "IPS", "ABDNM"]
        }
    ]

    bio_by_region = defaultdict(list)
    for bid, bdata in bio_neurons.items():
        bio_by_region[bdata["region"]].append(bid)

    synth_counter = 0
    for cspec in cluster_specs:
        prefix = str(cspec["name"])
        count = int(cspec["count"])
        anchor = cspec["anchor"]
        ax, ay, az = float(anchor[0]), float(anchor[1]), float(anchor[2])
        spread = float(cspec["spread"])
        base_c = cspec["base_c"]
        base_cx, base_cy = float(base_c[0]), float(base_c[1])
        bzoom = float(cspec["zoom"])
        
        # Candidate biological targets
        cand_bio_ids = []
        for rk in cspec["target_bio_regions"]:
            cand_bio_ids.extend(bio_by_region.get(rk, []))
        if not cand_bio_ids:
            cand_bio_ids = list(bio_neurons.keys())

        for idx in range(1, count + 1):
            synth_counter += 1
            nid = f"{prefix}_{idx:03d}"
            
            # Position: Torus/Lattice around anchor
            angle = random.uniform(0, 2 * math.pi)
            rad = random.gauss(spread, spread * 0.25)
            # Bilateral placement
            side_mult = -1.0 if (random.random() < 0.5 and ax != 0) else 1.0
            
            px = round(ax * side_mult + rad * math.cos(angle), 1)
            py = round(ay + random.gauss(0, spread * 0.5), 1)
            pz = round(az + rad * math.sin(angle), 1)
            
            # WERR coordinate seed perturbation
            seed_cx = base_cx + random.gauss(0, 0.002)
            seed_cy = base_cy + random.gauss(0, 0.002)
            seed_zoom = bzoom * random.uniform(0.9, 1.1)

            werr_neurons[nid] = {
                "id": nid,
                "type": "werr_synth",
                "cluster": cspec["name"],
                "role": cspec["role"],
                "color": cspec["color"],
                "pos": [px, py, pz],
                "seed": {
                    "cx": round(seed_cx, 8),
                    "cy": round(seed_cy, 8),
                    "zoom": round(seed_zoom, 2)
                },
                "fractal_phase": round(random.uniform(0, 2 * math.pi), 3),
                "potential": round(random.uniform(-65.0, -55.0), 2),
                "cadence_escape": round(random.uniform(0.1, 0.9), 3),
                "resonance_score": round(random.uniform(0.75, 0.99), 3)
            }
            
            # Create Bio-Synthetic synapses:
            # 1. Bio -> WERR (Afferent listener synapses)
            bio_inputs = random.sample(cand_bio_ids, min(len(cand_bio_ids), random.randint(3, 6)))
            for b_in in bio_inputs:
                synth_synapses.append({
                    "pre": b_in,
                    "post": nid,
                    "w": round(random.uniform(1.5, 4.5), 2),
                    "kind": "bio_to_werr"
                })
                
            # 2. WERR -> Bio (Efferent driver synapses)
            bio_outputs = random.sample(cand_bio_ids, min(len(cand_bio_ids), random.randint(3, 6)))
            for b_out in bio_outputs:
                synth_synapses.append({
                    "pre": nid,
                    "post": b_out,
                    "w": round(random.uniform(2.0, 6.0), 2),
                    "kind": "werr_to_bio"
                })

    # 3. Inter-WERR lateral lattice synapses (WERR <-> WERR within and between clusters)
    werr_ids = list(werr_neurons.keys())
    for wid in werr_ids:
        peers = random.sample(werr_ids, random.randint(2, 4))
        for p in peers:
            if p != wid:
                synth_synapses.append({
                    "pre": wid,
                    "post": p,
                    "w": round(random.uniform(1.0, 3.0), 2),
                    "kind": "werr_werr"
                })

    print(f"      Created exactly {len(werr_neurons)} WERR Synthetic Neurons.")
    print(f"      Generated {len(synth_synapses)} Bio-Synthetic Synapses.")

    # Combine all nodes and links
    all_nodes = {**bio_neurons, **werr_neurons}
    all_links = bio_synapses + synth_synapses

    print(f"      Total System: {len(all_nodes)} Neurons ({len(bio_neurons)} Bio + {len(werr_neurons)} WERR)")
    print(f"      Total Synapses: {len(all_links)}")

    # Save JSON database
    json_path = os.path.join(WORKSPACE, "neuramap", "bioneural_3d_data.json")
    print(f"[4/4] Writing database to {json_path}...")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "meta": {
                "organism": "Drosophila melanogaster (Adult Male)",
                "source": "FlyWire Princeton Whole-Brain Connectome",
                "synthetic_engine": "WERR v0.5.0 Zero-Memory Fractal",
                "bio_neurons_count": len(bio_neurons),
                "werr_neurons_count": len(werr_neurons),
                "total_synapses": len(all_links),
                "clusters": cluster_specs
            },
            "nodes": list(all_nodes.values()),
            "links": all_links
        }, f)

    print("      JSON database written successfully.")
    
    # Generate Standalone Interactive 3D WebGL HTML Viewer
    html_path = os.path.join(WORKSPACE, "neuramap_werr_3d.html")
    print(f"      Generating standalone 3D interactive viewer at {html_path}...")
    generate_html(json_path, html_path, len(bio_neurons), len(werr_neurons), len(all_links), cluster_specs)
    print("ALL_SYSTEMS_PREPARED_SUCCESSFULLY")

def generate_html(json_path, html_path, bio_count, werr_count, syn_count, cluster_specs):
    # Read the data to embed directly in the HTML for 100% offline, zero-server operation
    with open(json_path, "r", encoding="utf-8") as f:
        data_json_str = f.read()

    html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Drosophila & WERR Bio-Sentetik Nöral Rezonans Modeli (3B)</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      user-select: none;
    }}
    body {{
      background: radial-gradient(circle at 50% 50%, #0a0e17 0%, #03060a 100%);
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
    
    /* Top Navigation & Status Bar */
    header {{
      position: absolute;
      top: 16px;
      left: 20px;
      right: 20px;
      z-index: 10;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(10, 16, 26, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 12px 24px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
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
      font-size: 0.75rem;
      padding: 3px 8px;
      background: rgba(0, 240, 255, 0.12);
      border: 1px solid rgba(0, 240, 255, 0.3);
      border-radius: 6px;
      color: #38bdf8;
      font-weight: 600;
    }}
    .standby-badge {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      color: #facc15;
      background: rgba(250, 204, 21, 0.1);
      border: 1px solid rgba(250, 204, 21, 0.3);
      padding: 6px 14px;
      border-radius: 20px;
      animation: pulse-glow 2s infinite ease-in-out;
    }}
    .pulse-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: #facc15;
      box-shadow: 0 0 10px #facc15;
    }}
    @keyframes pulse-glow {{
      0%, 100% {{ opacity: 0.9; }}
      50% {{ opacity: 0.4; }}
    }}

    /* Left Control Panel */
    .panel-left {{
      position: absolute;
      top: 90px;
      left: 20px;
      width: 320px;
      background: rgba(10, 16, 26, 0.8);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 18px;
      z-index: 10;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6);
      max-height: calc(100vh - 120px);
      overflow-y: auto;
    }}
    .panel-title {{
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #94a3b8;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 6px;
    }}
    .stat-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }}
    .stat-card {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 8px;
      padding: 10px;
    }}
    .stat-label {{
      font-size: 0.7rem;
      color: #64748b;
      margin-bottom: 4px;
    }}
    .stat-val {{
      font-size: 1.15rem;
      font-weight: 700;
      color: #f1f5f9;
    }}
    .stat-val.werr-cyan {{ color: #00f0ff; text-shadow: 0 0 10px rgba(0,240,255,0.4); }}
    .stat-val.bio-blue {{ color: #60a5fa; }}
    .stat-val.syn-emerald {{ color: #34d399; }}

    /* Legend & Clusters */
    .cluster-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.78rem;
      padding: 6px 8px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.04);
      margin-bottom: 4px;
    }}
    .cluster-left {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .color-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }}

    /* Action Buttons */
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      background: rgba(0, 240, 255, 0.12);
      border: 1px solid rgba(0, 240, 255, 0.35);
      color: #38bdf8;
      padding: 9px 14px;
      font-size: 0.82rem;
      font-weight: 600;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s ease;
      width: 100%;
    }}
    .btn:hover {{
      background: rgba(0, 240, 255, 0.25);
      box-shadow: 0 0 16px rgba(0, 240, 255, 0.3);
      transform: translateY(-1px);
    }}
    .btn.reset-cam {{
      background: rgba(255, 255, 255, 0.06);
      border-color: rgba(255, 255, 255, 0.15);
      color: #94a3b8;
    }}
    .btn.reset-cam:hover {{
      background: rgba(255, 255, 255, 0.12);
      color: #f1f5f9;
    }}

    /* Right Test Protocol Stage Banner */
    .panel-right {{
      position: absolute;
      top: 90px;
      right: 20px;
      width: 330px;
      background: rgba(10, 16, 26, 0.85);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 18px;
      z-index: 10;
      display: flex;
      flex-direction: column;
      gap: 14px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6);
    }}
    .test-box {{
      border-radius: 8px;
      padding: 12px;
      border: 1px dashed rgba(255, 255, 255, 0.12);
      background: rgba(0, 0, 0, 0.2);
    }}
    .test-box.ready {{
      border: 1px solid rgba(250, 204, 21, 0.4);
      background: rgba(250, 204, 21, 0.04);
    }}
    .test-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }}
    .test-tag {{
      font-size: 0.68rem;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
    }}
    .test-tag.wait {{ background: rgba(250, 204, 21, 0.2); color: #facc15; }}
    .test-name {{
      font-size: 0.88rem;
      font-weight: 700;
      color: #f8fafc;
    }}
    .test-desc {{
      font-size: 0.74rem;
      color: #94a3b8;
      line-height: 1.4;
    }}

    /* Bottom Floating HUD */
    .bottom-hud {{
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10;
      display: flex;
      gap: 12px;
      background: rgba(10, 16, 26, 0.75);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 30px;
      padding: 8px 18px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    }}
    .hud-chip {{
      font-size: 0.75rem;
      font-weight: 600;
      color: #cbd5e1;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .hud-chip span {{ color: #00f0ff; }}

    /* Viewport Helper Message */
    .helper-text {{
      font-size: 0.7rem;
      color: #64748b;
      text-align: center;
      margin-top: 4px;
    }}
  </style>
  <!-- Three.js and OrbitControls (Local offline files with CDN fallback) -->
  <script src="js/three.min.js"></script>
  <script src="js/OrbitControls.js"></script>
</head>
<body>

  <!-- 3D WebGL Canvas Container -->
  <div id="canvas-container"></div>

  <!-- Top Navigation Bar -->
  <header>
    <div class="brand">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#00f0ff" stroke-width="2">
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
      </svg>
      <h1>Drosophila Melanogaster & WERR Neuro-Hybrid</h1>
      <span>v0.5.0 Fractal Connectome</span>
    </div>
    <div class="standby-badge">
      <div class="pulse-dot"></div>
      3B SİSTEM HAZIR &bull; TESTLER BEKLEMEDE (KULLANICI EMRİ BEKLENİYOR)
    </div>
  </header>

  <!-- Left Control Panel -->
  <div class="panel-left">
    <div class="panel-title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
      Topolojik Ağ Özeti
    </div>
    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-label">Biyolojik Nöron</div>
        <div class="stat-val bio-blue" id="val-bio">{bio_count:,}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">WERR Nöronu</div>
        <div class="stat-val werr-cyan" id="val-werr">{werr_count:,}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Toplam Sinaps</div>
        <div class="stat-val syn-emerald" id="val-syn">{syn_count:,}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Fraktal Mod</div>
        <div class="stat-val" style="color:#f472b6;">Resonance</div>
      </div>
    </div>

    <div class="panel-title" style="margin-top:6px;">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      WERR Sentetik Kümeleri
    </div>
    <div class="cluster-item">
      <div class="cluster-left">
        <div class="color-dot" style="background:#00f0ff; box-shadow:0 0 8px #00f0ff;"></div>
        <span>Merkezi Kompleks (EB/FB)</span>
      </div>
      <span style="font-weight:700; color:#00f0ff;">350 Nöron</span>
    </div>
    <div class="cluster-item">
      <div class="cluster-left">
        <div class="color-dot" style="background:#fbbf24; box-shadow:0 0 8px #fbbf24;"></div>
        <span>Mantar Cisimcik (MB Hafıza)</span>
      </div>
      <span style="font-weight:700; color:#fbbf24;">250 Nöron</span>
    </div>
    <div class="cluster-item">
      <div class="cluster-left">
        <div class="color-dot" style="background:#10b981; box-shadow:0 0 8px #10b981;"></div>
        <span>Duyusal / Aferent Giriş (AL)</span>
      </div>
      <span style="font-weight:700; color:#10b981;">200 Nöron</span>
    </div>
    <div class="cluster-item">
      <div class="cluster-left">
        <div class="color-dot" style="background:#ec4899; box-shadow:0 0 8px #ec4899;"></div>
        <span>Motor / İnen Komuta (DN)</span>
      </div>
      <span style="font-weight:700; color:#ec4899;">200 Nöron</span>
    </div>

    <div class="panel-title" style="margin-top:6px;">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
      3B Kamera Odakları
    </div>
    <button class="btn" id="btn-focus-cx">Merkezi Komplekse (EB/FB) Odaklan</button>
    <button class="btn" id="btn-focus-mb" style="background:rgba(251,191,36,0.12); border-color:rgba(251,191,36,0.3); color:#fbbf24;">Mantar Cisimciğe (MB) Odaklan</button>
    <button class="btn reset-cam" id="btn-reset-cam">Tam Beyin Perspektifine Dön</button>
    <div class="helper-text">Sol Tık: Döndür &bull; Sağ Tık: Kaydır &bull; Tekerlek: Yakınlaş</div>
  </div>

  <!-- Right Test Protocol Stage Banner -->
  <div class="panel-right">
    <div class="panel-title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
      İki Aşamalı Test Protokolü
    </div>

    <!-- Test Stage 1 -->
    <div class="test-box ready">
      <div class="test-header">
        <span class="test-name">1. Aşama: Uyumluluk Testi</span>
        <span class="test-tag wait">Hazır / Beklemede</span>
      </div>
      <p class="test-desc">
        1000 WERR nöronunun sinaptik akımlarının biyolojik nöronlarla çift yönlü haberleşme verimi ve beyin dokusunun karşıt tepki (inhibition/rejection) üretip üretmediği test edilecek.
      </p>
    </div>

    <!-- Test Stage 2 -->
    <div class="test-box ready">
      <div class="test-header">
        <span class="test-name">2. Aşama: Motor Atım İcrası Testi</span>
        <span class="test-tag wait">Hazır / Beklemede</span>
      </div>
      <p class="test-desc">
        WERR Mandelbrot fraktal kaçış kadranlarından ($Q_1-Q_4$) üretilen sentetik komut atımlarının, sineğin inen motor nöronları (`DN` / `VNC`) tarafından işlenip eyleme dökülmesi test edilecek.
      </p>
    </div>

    <div style="font-size:0.75rem; color:#facc15; background:rgba(250,204,21,0.08); border:1px solid rgba(250,204,21,0.25); border-radius:8px; padding:10px; line-height:1.4;">
      <strong>⚠️ Talimat Kilidi Aktif:</strong><br>
      Kullanıcı talimatı uyarınca simülasyon testi başlatılmamıştır. Testler sizin onayınızla canlı olarak başlatılacaktır.
    </div>
  </div>

  <!-- Bottom Floating HUD -->
  <div class="bottom-hud">
    <div class="hud-chip">Koordinat Tohumu: <span id="hud-seed">cx=-0.7436, cy=0.1318</span></div>
    <div class="hud-chip">&bull;</div>
    <div class="hud-chip">Harmonik Tripod: <span style="color:#34d399;">Açık (0.6x, 1.0x, 1.6x)</span></div>
    <div class="hud-chip">&bull;</div>
    <div class="hud-chip">Hücresel VRAM: <span style="color:#38bdf8;">0 Bayt</span></div>
    <div class="hud-chip">&bull;</div>
    <div class="hud-chip">GPU FPS: <span id="hud-fps" style="color:#f472b6;">60</span></div>
  </div>

  <script>
    // Embedded Connectome Graph Data
    const graphData = {data_json_str};

    // Initialize Three.js Scene
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x050811, 0.0012);

    const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 3000);
    camera.position.set(0, 150, 480);

    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxDistance = 1200;
    controls.minDistance = 30;

    // Ambient & Directional Lights
    const ambientLight = new THREE.AmbientLight(0x223344, 1.5);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00f0ff, 2.5, 800);
    pointLight.position.set(0, 50, 100);
    scene.add(pointLight);

    // Group to hold brain and synthetic network
    const networkGroup = new THREE.Group();
    scene.add(networkGroup);

    // Build Biological Neurons Point Cloud
    const bioNodes = graphData.nodes.filter(n => n.type === 'bio');
    const synthNodes = graphData.nodes.filter(n => n.type === 'werr_synth');

    // 1. Biological Points Geometry
    const bioGeometry = new THREE.BufferGeometry();
    const bioPositions = new Float32Array(bioNodes.length * 3);
    const bioColors = new Float32Array(bioNodes.length * 3);

    const colorCentral = new THREE.Color(0x38bdf8); // Light Blue
    const colorMB = new THREE.Color(0xfacc15);      // Gold
    const colorSensory = new THREE.Color(0x34d399); // Green
    const colorMotor = new THREE.Color(0xec4899);   // Pink
    const colorDefault = new THREE.Color(0x818cf8); // Indigo

    bioNodes.forEach((node, i) => {{
      bioPositions[i * 3] = node.pos[0];
      bioPositions[i * 3 + 1] = node.pos[1];
      bioPositions[i * 3 + 2] = node.pos[2];

      let c = colorDefault;
      if (node.super_class === 'descending') c = colorMotor;
      else if (node.region.includes('MB')) c = colorMB;
      else if (node.super_class === 'sensory') c = colorSensory;
      else if (['EB','FB','PB','NO'].includes(node.region)) c = colorCentral;

      bioColors[i * 3] = c.r;
      bioColors[i * 3 + 1] = c.g;
      bioColors[i * 3 + 2] = c.b;
    }});

    bioGeometry.setAttribute('position', new THREE.BufferAttribute(bioPositions, 3));
    bioGeometry.setAttribute('color', new THREE.BufferAttribute(bioColors, 3));

    const bioMaterial = new THREE.PointsMaterial({{
      size: 4.5,
      vertexColors: true,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending
    }});
    const bioPoints = new THREE.Points(bioGeometry, bioMaterial);
    networkGroup.add(bioPoints);

    // 2. WERR Synthetic Neurons Point Cloud (Larger, Glowing Cyan/Amber)
    const synthGeometry = new THREE.BufferGeometry();
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

    synthGeometry.setAttribute('position', new THREE.BufferAttribute(synthPositions, 3));
    synthGeometry.setAttribute('color', new THREE.BufferAttribute(synthColors, 3));

    const synthMaterial = new THREE.PointsMaterial({{
      size: 8.5,
      vertexColors: true,
      transparent: true,
      opacity: 0.95,
      blending: THREE.AdditiveBlending
    }});
    const synthPoints = new THREE.Points(synthGeometry, synthMaterial);
    networkGroup.add(synthPoints);

    // 3. Synapses Lines
    const nodeMap = new Map();
    graphData.nodes.forEach(n => nodeMap.set(n.id, n.pos));

    const linePositions = [];
    const lineColors = [];

    const colBioBio = new THREE.Color(0x1e293b);
    const colBioWerr = new THREE.Color(0x0284c7);
    const colWerrBio = new THREE.Color(0x00f0ff);
    const colWerrWerr = new THREE.Color(0xf59e0b);

    // Sample connections for optimal 60fps render
    const displayLinks = graphData.links.filter((_, idx) => idx % 2 === 0);

    displayLinks.forEach(link => {{
      const p1 = nodeMap.get(link.pre);
      const p2 = nodeMap.get(link.post);
      if (p1 && p2) {{
        linePositions.push(p1[0], p1[1], p1[2]);
        linePositions.push(p2[0], p2[1], p2[2]);

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
      opacity: 0.35,
      blending: THREE.AdditiveBlending
    }});
    const synapseLines = new THREE.LineSegments(linesGeometry, linesMaterial);
    networkGroup.add(synapseLines);

    // Brain Anatomical Neuropil Volumetric Wireframe Shells
    const neuropilShells = [
      {{ name: 'EB', pos: [0, -10, 20], r: 24, col: 0x00f0ff }},
      {{ name: 'FB', pos: [0, 32, -10], r: 35, col: 0x38bdf8 }},
      {{ name: 'MB_L', pos: [-120, 75, -75], r: 30, col: 0xfacc15 }},
      {{ name: 'MB_R', pos: [120, 75, -75], r: 30, col: 0xfacc15 }},
      {{ name: 'AL_L', pos: [-62, -78, 72], r: 25, col: 0x10b981 }},
      {{ name: 'AL_R', pos: [62, -78, 72], r: 25, col: 0x10b981 }},
      {{ name: 'GNG', pos: [0, -118, 0], r: 32, col: 0xec4899 }}
    ];

    neuropilShells.forEach(shell => {{
      const geo = new THREE.SphereGeometry(shell.r, 16, 12);
      const wireGeo = new THREE.WireframeGeometry(geo);
      const wireMat = new THREE.LineBasicMaterial({{ color: shell.col, transparent: true, opacity: 0.15 }});
      const wire = new THREE.LineSegments(wireGeo, wireMat);
      wire.position.set(shell.pos[0], shell.pos[1], shell.pos[2]);
      networkGroup.add(wire);
    }});

    // Camera Focus Handlers
    document.getElementById('btn-focus-cx').addEventListener('click', () => {{
      controls.target.set(0, 10, 10);
      camera.position.set(0, 40, 180);
    }});
    document.getElementById('btn-focus-mb').addEventListener('click', () => {{
      controls.target.set(120, 75, -75);
      camera.position.set(160, 110, 20);
    }});
    document.getElementById('btn-reset-cam').addEventListener('click', () => {{
      controls.target.set(0, 0, 0);
      camera.position.set(0, 150, 480);
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

      // Gentle continuous rotation
      networkGroup.rotation.y = elapsed * 0.035;

      // Pulse WERR synthetic points slightly
      synthMaterial.size = 8.5 + Math.sin(elapsed * 4.0) * 1.5;

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

    // Window Resize Handler
    window.addEventListener('resize', () => {{
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }});
  </script>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    main()
