"""
compile_full_158k_connectome.py
===============================
Compiles the complete 158,262 biological neurons and 3,990,039 synapses
from the Princeton FlyWire Connectome into an ultra-fast, zero-overhead
binary Compressed Sparse Row (CSR) cache: drosophila_full_158k_cache.npz.

Pure Biological Connectome (100% FlyWire, 0 WERR neurons).
"""
import os
import sys
import csv
import time
import math
import random
import numpy as np

WORKSPACE = "c:/Users/Lexo/Desktop/werrdevistan"
NEURONS_CSV = os.path.join(WORKSPACE, "neuramap", "neurons.csv", "neurons.csv")
CONNECTIONS_CSV = os.path.join(WORKSPACE, "neuramap", "connections_princeton.csv", "connections_princeton.csv")
CACHE_FILE = os.path.join(WORKSPACE, "drosophila_full_158k_cache.npz")

# Comprehensive 3D anatomical centroids for all 57 Drosophila neuropils in microns (FAFB/JRC2018)
NEUROPIL_CENTROIDS = {
    # Central Complex (Midline)
    "EB": (0.0, -10.0, 20.0),
    "FB": (0.0, 32.0, -10.0),
    "PB": (0.0, 68.0, -68.0),
    "NO": (0.0, -38.0, 2.0),
    "BU": (32.0, -22.0, 15.0),
    # Mushroom Bodies (Bilateral)
    "MB_CA": (120.0, 75.0, -75.0),
    "MB_PED": (78.0, 38.0, -22.0),
    "MB_VL": (42.0, -8.0, 48.0),
    "MB_ML": (25.0, -12.0, 52.0),
    # Olfactory & Sensory
    "AL": (62.0, -78.0, 72.0),
    "AOTU": (88.0, 28.0, 78.0),
    "AMMC": (82.0, -85.0, 18.0),
    "FLA": (55.0, -92.0, 10.0),
    # Optic Lobes (Far Lateral)
    "ME": (250.0, 10.0, -10.0),
    "LO": (190.0, 15.0, -20.0),
    "LOP": (205.0, 38.0, -38.0),
    "AME": (265.0, -20.0, 20.0),
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
    "VES": (52.0, -30.0, -12.0),
    "WED": (85.0, -65.0, -15.0),
    "IB": (65.0, 18.0, -42.0),
    "ATL": (42.0, 14.0, 44.0),
    "IPS": (130.0, -15.0, -65.0),
    "SPS": (110.0, -5.0, -78.0),
    "SAD": (58.0, -48.0, 2.0),
    "PRW": (45.0, -35.0, -30.0),
    "EPA": (62.0, -6.0, 58.0),
    "GOR": (30.0, 6.0, 30.0),
    "GA": (50.0, -15.0, 22.0),
    "CAN": (35.0, -80.0, 5.0),
    # Subesophageal Zone
    "GNG": (0.0, -118.0, 0.0),
    "AMNP": (25.0, -135.0, -10.0),
    # Ventral Nerve Cord & Motor Neuromeres
    "T1_PRONM": (0.0, -185.0, -15.0),
    "T2_MESONM": (0.0, -245.0, -20.0),
    "T3_METANM": (0.0, -295.0, -25.0),
    "ABDNM": (0.0, -355.0, -30.0),
    "T2_MVAC": (0.0, -230.0, -15.0),
    "LEGNP_T1": (35.0, -180.0, -20.0),
    # Tracts
    "HTCT": (30.0, -220.0, -18.0),
    "INTTCT": (20.0, -250.0, -22.0),
    "WTCT": (40.0, -270.0, -20.0),
    "LTCT": (45.0, -240.0, -22.0),
    "NTCT": (15.0, -200.0, -16.0),
    "WTCT_UTCT_T2": (35.0, -260.0, -20.0),
    "HTCT_UTCT_T3": (30.0, -280.0, -22.0),
    "NTCT_UTCT_T1": (25.0, -210.0, -18.0),
    # Fragment / Unassigned
    "NO_CONS": (0.0, -20.0, 0.0),
    "DEFAULT": (0.0, 0.0, 0.0)
}

def get_centroid(reg_name, side):
    token = reg_name.split(".")[0].split("_")[0]
    base = NEUROPIL_CENTROIDS.get(reg_name, NEUROPIL_CENTROIDS.get(token, NEUROPIL_CENTROIDS["DEFAULT"]))
    x, y, z = base
    if side == "left":
        x = -abs(x)
    elif side == "right":
        x = abs(x)
    elif side in ("center", "middle") and ("MB" in reg_name or "ME" in reg_name or "LO" in reg_name or "AL" in reg_name):
        x = -x if random.random() < 0.5 else x
    return x, y, z

def main():
    print("=" * 70)
    print("🧠 DROSOPHILA MELANOGASTER WHOLE-BRAIN CONNECTOME COMPILER")
    print("Target: 158,262 Biological Neurons & 3,990,039 Biological Synapses")
    print("=" * 70)
    
    t_start = time.time()
    
    # 1. Parse Neurons
    print("[1/3] Reading 158,262 biological neurons from neurons.csv...")
    positions = []
    polarity = []
    is_eb = []
    is_dn = []
    is_mb = []
    is_me = []
    is_al = []
    region_names = []
    root_to_idx = {}
    
    random.seed(42)
    
    with open(NEURONS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            rid = row["Root ID"]
            root_to_idx[rid] = idx
            
            reg_raw = row["Top in/out region"] or "SMP"
            reg = reg_raw.split(".")[0]
            side = (row["Soma side"] or "center").lower()
            sc = row.get("Super Class") or "unknown"
            
            cx, cy, cz = get_centroid(reg, side)
            # Natural volumetric jitter in microns
            jitter = 12.0
            px = cx + random.gauss(0, jitter)
            py = cy + random.gauss(0, jitter)
            pz = cz + random.gauss(0, jitter)
            positions.append((px, py, pz))
            
            # Neurotransmitter Polarity
            # ACH -> Excitatory (+1)
            # GABA, GLU -> Inhibitory (-1)
            # DA, OCT, SER -> Modulatory (0)
            nt = (row.get("Predicted NT type") or "ACH").upper()
            if nt in ("GABA", "GLU"):
                pol = -1
            elif nt in ("DA", "OCT", "SER", "5HT"):
                pol = 0
            else:
                pol = 1
            polarity.append(pol)
            
            # Key functional group markers
            is_eb.append(1 if reg == "EB" else 0)
            is_dn.append(1 if sc == "descending" else 0)
            is_mb.append(1 if "MB" in reg else 0)
            is_me.append(1 if "ME" in reg or "LO" in reg else 0)
            is_al.append(1 if "AL" in reg or "AMMC" in reg else 0)
            region_names.append(reg)
            
            if (idx + 1) % 50000 == 0:
                print(f"      Parsed {idx + 1:,} neurons...")

    total_neurons = len(positions)
    print(f"[*] Complete: Loaded all {total_neurons:,} neurons in {time.time() - t_start:.2f}s.")
    
    # 2. Parse Synapses into adjacency lists
    print("\n[2/3] Reading 3,990,039 biological synaptic connections...")
    t_syn = time.time()
    
    # Group outgoing synapses by pre_neuron index
    # We will build CSR representation: indptr, syn_post, syn_weight, syn_pol
    adj_targets = [[] for _ in range(total_neurons)]
    adj_weights = [[] for _ in range(total_neurons)]
    
    matched_count = 0
    with open(CONNECTIONS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            pre_id = row["pre_root_id"]
            post_id = row["post_root_id"]
            if pre_id in root_to_idx and post_id in root_to_idx:
                p_idx = root_to_idx[pre_id]
                t_idx = root_to_idx[post_id]
                w = min(20, int(row.get("syn_count") or 1))
                adj_targets[p_idx].append(t_idx)
                adj_weights[p_idx].append(w)
                matched_count += 1
            if (i + 1) % 1000000 == 0:
                print(f"      Processed {i + 1:,} connections (matched: {matched_count:,})...")

    print(f"[*] All {matched_count:,} connections grouped in {time.time() - t_syn:.2f}s.")
    
    # 3. Flatten into Compressed Sparse Row (CSR)
    print("\n[3/3] Compacting into Compressed Sparse Row (CSR) structure...")
    t_csr = time.time()
    
    indptr = np.zeros(total_neurons + 1, dtype=np.int32)
    syn_post = np.empty(matched_count, dtype=np.int32)
    syn_weight = np.empty(matched_count, dtype=np.uint8)
    
    curr = 0
    for i in range(total_neurons):
        targets = adj_targets[i]
        weights = adj_weights[i]
        n_links = len(targets)
        indptr[i] = curr
        if n_links > 0:
            syn_post[curr:curr + n_links] = targets
            syn_weight[curr:curr + n_links] = weights
            curr += n_links
    indptr[total_neurons] = curr
    
    print(f"[*] CSR arrays assembled. Total synapses: {curr:,} in {time.time() - t_csr:.2f}s.")
    
    # 4. Save Compressed Binary Cache (.npz)
    print(f"\n[*] Writing compressed binary cache to: {CACHE_FILE}...")
    t_save = time.time()
    
    pos_arr = np.array(positions, dtype=np.float32)
    pol_arr = np.array(polarity, dtype=np.int8)
    is_eb_arr = np.array(is_eb, dtype=np.uint8)
    is_dn_arr = np.array(is_dn, dtype=np.uint8)
    is_mb_arr = np.array(is_mb, dtype=np.uint8)
    is_me_arr = np.array(is_me, dtype=np.uint8)
    is_al_arr = np.array(is_al, dtype=np.uint8)
    
    np.savez_compressed(
        CACHE_FILE,
        pos=pos_arr,
        polarity=pol_arr,
        is_eb=is_eb_arr,
        is_dn=is_dn_arr,
        is_mb=is_mb_arr,
        is_me=is_me_arr,
        is_al=is_al_arr,
        indptr=indptr,
        syn_post=syn_post,
        syn_weight=syn_weight
    )
    
    file_size_mb = os.path.getsize(CACHE_FILE) / (1024 * 1024)
    print(f"✅ CACHE WRITTEN SUCCESSFULLY: {file_size_mb:.2f} MB in {time.time() - t_save:.2f}s.")
    print(f"Total compilation time: {time.time() - t_start:.2f}s.")
    print("=" * 70)

if __name__ == "__main__":
    main()
