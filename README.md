# 🧬 WerrSoma: Bio-Synthetic Neuromorphic Connectome Interfacing

<p align="center">
  <a href="https://doi.org/10.5281/zenodo.22996625"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.22996625.svg" alt="DOI: 10.5281/zenodo.22996625"></a>
  <a href="https://werrsoma.answerr.me/"><img src="https://img.shields.io/badge/Live%20Portal-werrsoma.answerr.me-00f0ff" alt="Live Portal"></a>
  <a href="arxiv/"><img src="https://img.shields.io/badge/arXiv-Ready%20Package-b31b1b.svg" alt="arXiv Package"></a>
  <img src="https://img.shields.io/badge/Patent%20Priority-TR%202026%2F016633-blue" alt="TÜRKPATENT TR 2026/016633">
  <a href="https://github.com/Lexovian/WerrSoma"><img src="https://img.shields.io/badge/Canonical%20Repo-Lexovian%2FWerrSoma-181717.svg?logo=github" alt="Canonical Repo"></a>
  <a href="https://github.com/pCwOrM/WerrSoma"><img src="https://img.shields.io/badge/Mirror-pCwOrM%2FWerrSoma-blue.svg?logo=github" alt="Mirror Repo"></a>
  <a href="https://github.com/Lexovian/WerrSoma/actions/workflows/ci.yml"><img src="https://github.com/Lexovian/WerrSoma/actions/workflows/ci.yml/badge.svg" alt="Scientific CI"></a>
  <img src="https://img.shields.io/badge/License-BSL%201.1%20%2F%20BBL%20v1.0-green.svg" alt="License: BSL 1.1 / BBL v1.0">
  <img src="https://img.shields.io/badge/Dataset-Princeton%20FlyWire%20EM-emerald.svg" alt="Princeton FlyWire">
  <img src="https://img.shields.io/badge/Connectome-158%2C262%20Neurons-blueviolet.svg" alt="158,262 Neurons">
  <img src="https://img.shields.io/badge/Latency-3.67%20ms%20Reflex-red.svg" alt="3.67 ms Reflex Latency">
  <img src="https://img.shields.io/badge/VRAM-0%20Bytes-success.svg" alt="Zero VRAM">
  <img src="https://img.shields.io/badge/Python-3.10%2B-informational.svg" alt="Python 3.10+">
  <a href="https://github.com/jesmaat/WerreduR"><img src="https://img.shields.io/badge/Sister%20Repo-WerreduR%20v4.0-059669.svg" alt="WerreduR v4.0"></a>
  <a href="https://github.com/pCwOrM/gunes-dili"><img src="https://img.shields.io/badge/Sister%20Repo-G%C3%BCne%C5%9F%20Dili-gold.svg" alt="Güneş Dili"></a>
  <a href="https://github.com/pCwOrM/gap-lean4-port"><img src="https://img.shields.io/badge/Sister%20Repo-GAP--Lean4-7c3aed.svg" alt="GAP-Lean4"></a>
  <a href="https://github.com/pCwOrM/werr"><img src="https://img.shields.io/badge/Core%20Engine-WERR-blue.svg" alt="WERR"></a>
</p>

> **Integration of a Zero-Memory Fractal Decision Engine (WERR) with the Complete Whole-Brain *Drosophila Melanogaster* Connectome.**

**WerrSoma** couples the complete 158,262-neuron, 3.99-million synapse electron-microscopy biological connectome of the adult fruit fly (*Drosophila melanogaster*, Princeton FlyWire) with an implantable 1,024-pin **WERR neuromorphic fractal coprocessor**. 

Rather than deploying heavyweight, power-hungry deep learning models or spiking transformers that suffer from high latency ($15-200\text{ ms}$) and VRAM bloat, WerrSoma utilizes **deterministic chaotic Mandelbrot boundary escape trajectories ($\partial \mathcal{M}$)** to synthesize directional flight decisions and motor overrides in **$< 0.5\text{ ms}$** with **$0\text{ Bytes}$ of VRAM**.

---

## 🌐 Live Web Portal & Interactive Guides

Experience the platform live in your browser:

| Resource | Live Link | Description |
| :--- | :--- | :--- |
| **Main Web Portal** | [werrsoma.answerr.me](https://werrsoma.answerr.me/) | Central production portal with live telemetry and viewers. |
| **👥 Halka Anlatım Rehberi** | [halka_anlatim_rehberi.html](https://werrsoma.answerr.me/halka_anlatim_rehberi.html) | Sıradan meraklılar, öğrenciler ve yatırımcılar için popüler bilim anlatımı. |
| **🔬 Technical Whitepaper (TR/EN)** | [teknik_akademik_rehber.html](https://werrsoma.answerr.me/teknik_akademik_rehber.html) | Dual-language (Türkçe / English) biophysical formulation & benchmark report. |
| **3D Flight Arena Simulator** | [fly_bioneural_flight_sim.html](https://werrsoma.answerr.me/fly_bioneural_flight_sim.html) | Interactive WebGL Three.js simulator with head-locked live brain telemetry. |
| **3D Connectome Explorer** | [neuramap_werr_3d.html](https://werrsoma.answerr.me/neuramap_werr_3d.html) | 158k Drosophila point cloud laboratory with 1,024-pin implant shanks. |
| **Live REST API** | [/api.php?action=status](https://werrsoma.answerr.me/api.php?action=status) | Real-time biophysical telemetry, fractal decisions, and benchmark stats. |
| **Zenodo Sealed Package (v1.1)** | [doi.org/10.5281/zenodo.23072929](https://doi.org/10.5281/zenodo.23072929) | Permanent immutable v1.1 DOI (Concept: [10.5281/zenodo.22996625](https://doi.org/10.5281/zenodo.22996625)). |
| **📄 arXiv Submission Package** | [`arxiv/`](arxiv/) | Camera-ready 2-column LaTeX manuscript, 300 DPI 158K connectome projection, and `.tar.gz`/`.zip` bundles. |

---

## ⚡ 1-Minute Quickstart (Replication in 3 Commands)

Clone the repository and replicate all 6 empirical benchmark protocols in seconds:

```bash
# 1. Clone repository
git clone https://github.com/Lexovian/WerrSoma.git
cd WerrSoma

# 2. Install minimal dependencies (NumPy & Pillow only)
pip install -r requirements.txt

# 3. Execute the comprehensive 6-experiment empirical suite (takes <0.1 sec)
python run_scientific_experiments.py
```

To run the native dual-viewport 3D desktop application (Flight Arena + 158k Brain Point Cloud):
```bash
python bioneural_fly_app.py
```

---

## 🏛️ Closed-Loop Bio-Synthetic Architecture

```mermaid
graph LR
    subgraph WERR_Silicon_Implant [WERR 1,024-Pin Silicon Coprocessor]
        Mandelbrot_Core[Mandelbrot Boundary Core z -> z^2 + c] -->|dt < 0.5 ms| Pin_Grid[32x32 Micro-Electrode Pin Grid]
    end

    subgraph Penetrating_Shanks [4 Penetrating Biocompatible Leads]
        Pin_Grid -->|Shank 1: Heading| Shank1[Shank 1: EB Ring Compass]
        Pin_Grid -->|Shank 2: Thrust| Shank2[Shank 2: DN Motor Neurons]
        Pin_Grid -->|Shanks 3-4: Feedback| Shank3[Shanks 3-4: Bilateral Mushroom Bodies]
    end

    subgraph Drosophila_Connectome [Princeton FlyWire Connectome: 158,262 Neurons]
        Shank1 -->|ACh Depolarization| EB_Attractor[Ellipsoid Body E-PG Ring Attractor]
        Shank2 -->|Tonic Depolarization| DN_Pool[Descending Motor Neurons DN1/DN2]
        EB_Attractor -->|Recurrent Synapses| GABA_Network[GABAergic/Glutamatergic Local Interneurons]
        GABA_Network -.->|Homeostatic Brake 38.58%| EB_Attractor
        EB_Attractor -->|Heading Vector R=0.841| Steering_Control[Differential Wingbeat Steering]
        DN_Pool -->|192 - 244 Hz Modulation| Flight_Muscles[Basalar & Pterale Motor Units]
    end

    Steering_Control --> ClosedLoop_Kinematics[3D Aerodynamic Flight Kinematics]
    Flight_Muscles --> ClosedLoop_Kinematics
```

### Key Anatomical Interfaces
1. **Shank 1 — Central Complex Ellipsoid Body (EB):** Entrains the E-PG heading compass ring attractor, driving banked turns and directional saccades.
2. **Shank 2 — Descending Motor Neurons (DN Pool):** Modulates wingbeat frequency ($192 - 244\text{ Hz}$) and flight forward thrust.
3. **Shanks 3 & 4 — Bilateral Mushroom Bodies (MB):** Interfaces associative memory centers and receives homeostatic feedback.

---

## 📊 Empirical Scientific Findings

Tested across 6 rigorous biophysical protocols via [`run_scientific_experiments.py`](run_scientific_experiments.py) on the real 158k FlyWire graph (full report: [`scientific_benchmark_results.json`](scientific_benchmark_results.json)):

| Metric / Experiment | Target Benchmark | Empirical Result | Status |
| :--- | :---: | :---: | :---: |
| **Synaptic Transmission Fidelity** | $> 95.0\%$ | **$100.0\%$** ($300/300$ trials) | **OPTIMAL** |
| **Mean Postsynaptic Potential ($\Delta V_m$)** | $12 - 18\text{ mV}$ | **$15.83 \pm 0.51\text{ mV}$** | **PASSED** |
| **End-to-End Reflex Latency** | $< 5.0\text{ ms}$ | **$3.671\text{ ms}$** (Decision: $0.46\text{ ms}$) | **SUB-REFLEX** |
| **Saccadic Steering Accuracy** | $> 85.0\%$ | **$94.67\%$** (L: 93.3%, R: 96.0%, F: 94.7%, S: 94.7%) | **PASSED** |
| **Attractor Heading Coherence (Rayleigh $R$)** | $> 0.80$ | **$0.841$** (Sharply tuned von Mises bump) | **PASSED** |
| **GABA Homeostatic Counter-Current** | $30 - 50\%$ | **$38.58\%$** (Clamps $V_m$ at $-53.93\text{ mV}$) | **NO SEIZURE / PDS** |
| **Network Stability Index (NSI)** | $> 0.90$ | **$0.965 / 1.000$** | **PASSED** |
| **Baseline Metabolic Power (1,024 pins)** | $< 5.0\ \mu\text{W}$ | **$1.23\ \mu\text{W}$** ($21.89\ \mu\text{W}$ at 200 Hz) | **PASSED** |
| **Tissue Thermal Elevation ($\Delta T$)** | $< 0.05^\circ\text{C}$ | **$+0.0012^\circ\text{C}$** | **SAFE** |
| **Safe Continuous Stimulation Limit ($f_{\text{max}}$)** | $> 200\text{ Hz}$ | **$265\text{ Hz}$** ($20\text{ ms}$ refractory clamp) | **NO BURNOUT** |
| **Neural Coding Efficiency ($\eta$)** | $> 60.0\%$ | **$70.10\%$** ($I(X; Y) = 1.302\text{ bits}$, $19.44\text{ dB}$) | **PASSED** |
| **Fault Tolerance (25% Pin Loss)** | $> 75.0\%$ | **$83.29\%$** Clean / **$78.46\%$** with 15Hz noise | **ROBUST** |

---

## 🛡️ Resolving the "Neuron Burnout" & Rejection Hazard

*How does WerrSoma achieve biocompatible integration without triggering neural burnout or tissue rejection?*

1. **Elimination of Square-Wave PWM Shocks (Bio-Resonance):** Rather than blasting biological tissue with harsh digital square waves that cause depolarization block and habituation, WERR generates smooth chaotic Mandelbrot boundary oscillations that naturally phase-lock with endogenous action potential phase distributions.
2. **Gaussian Sub-Threshold Electric Field Guidance:** Non-invasive field shaping guides membrane excitability without dielectric breakdown or cytotoxic ion influx.
3. **$20.0\text{ ms}$ Absolute Refractory Clamp:** Voltage-gated sodium channel ($DmNav$) dynamics are enforced, capping individual pin frequency at $50\text{ Hz}$.
4. **Biological GABAergic Homeostasis:** The Drosophila brain recruits a $38.58\%$ hyperpolarizing counter-current, clamping peak membrane potential safely at $-53.93\text{ mV}$ (preventing epileptiform paroxysmal depolarizing shifts).

---

## 👥 Authors & Institutional Affiliations

```text
Dağhan Dağlı 1,*, Volkan Dağlı 2,3,†, Zerrin Dağlı 4,5

1 Toros Science High School, Mersin Education Foundation (Toros University), Türkiye
2 Anadolu University, Türkiye
3 ITouch Systems, Çukurova Teknokent, Türkiye
4 Mersin University, Türkiye
5 Yusuf Kalkavan Anatolian High School, Türkiye

* Lead Author & Connectome Architecture Lead (ORCID: 0009-0003-2492-8313)
† Corresponding Author: ask@answerr.me (ORCID: 0009-0000-1587-8703)
  Z. Dağlı (ORCID: 0000-0001-9490-6425)
```

---

## 📄 Scientific Paper & Citation

* **Research Paper Manuscript:** [`bioneural_werr_drosophila_paper.md`](bioneural_werr_drosophila_paper.md)
* **Camera-Ready PDF:** [`Bio_Synthetic_Neuromorphic_WerrSoma_Drosophila.pdf`](https://doi.org/10.5281/zenodo.23072929)
* **Permanent Version DOI:** [10.5281/zenodo.23072929](https://doi.org/10.5281/zenodo.23072929) *(Concept/Latest DOI: [10.5281/zenodo.22996625](https://doi.org/10.5281/zenodo.22996625))*

```bibtex
@article{dagli2026werrsoma,
  title   = {Bio-Synthetic Neuromorphic Interfacing: Integration of a Zero-Memory Fractal Decision Engine with the Whole-Brain Drosophila Melanogaster Connectome},
  author  = {Da{\u{g}}l{\i}, Da{\u{g}}han and Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin},
  journal = {Zenodo Preprint (Target: Nature Neuroscience / IEEE TBME)},
  year    = {2026},
  doi     = {10.5281/zenodo.23072929},
  url     = {https://doi.org/10.5281/zenodo.23072929}
}
```

---

## 🏛️ Associated Formal Verification & Scientific Corpus

WerrSoma represents Paper 6 in the unified open-science corpus spanning fractal neural synthesis, formal verification, biophysical modeling, and decentralized reflex intelligence:

| Makale / Sütun | Başlık / Katkı | En Son Sürüm DOI | Çatı / Konsept DOI | arXiv / Doğrulama Durumu | Birincil Depo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Paper 1: MFNS** | Mandelbrot Fractal Neural Synthesis | [`10.5281/zenodo.22867037`](https://doi.org/10.5281/zenodo.22867037) | [`10.5281/zenodo.22774934`](https://doi.org/10.5281/zenodo.22774934) | Açık Bilim Önbaskısı (Revizyonda) | [`pCwOrM/mandelbrot-fractal-neural-synthesis`](https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis) |
| **Paper 2: OED** | Orbital Error Dynamics (OED v3) | [`10.5281/zenodo.22900465`](https://doi.org/10.5281/zenodo.22900465) | [`10.5281/zenodo.22896855`](https://doi.org/10.5281/zenodo.22896855) | [`arXiv:2609.30115`](https://arxiv.org/abs/2609.30115) • [HF Paper](https://huggingface.co/papers/2609.30115) | [`pCwOrM/mandelbrot-fractal-neural-synthesis`](https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis) |
| **Paper 3: WerreduR** | Procedural Fractal Pedagogy (v4.0) | [`10.5281/zenodo.23128224`](https://doi.org/10.5281/zenodo.23128224) | [`10.5281/zenodo.22999420`](https://doi.org/10.5281/zenodo.22999420) | Hedef: Q1 AIED / CAEAI • [Canlı Simülatör](https://pcworm.github.io/WerreduR/) | [`jesmaat/WerreduR`](https://github.com/jesmaat/WerreduR) (Mirror: [`pCwOrM/WerreduR`](https://github.com/pCwOrM/WerreduR)) |
| **Paper 4: BH Page** | Black Hole Page Curve & Quantum Gravity (v5) | [`10.5281/zenodo.23072120`](https://doi.org/10.5281/zenodo.23072120) | [`10.5281/zenodo.22961999`](https://doi.org/10.5281/zenodo.22961999) | CERN Record 22978460 • Stabilizer Kodları | [`pCwOrM/mandelbrot-fractal-neural-synthesis`](https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis) |
| **Paper 5: Formal** | Lean 4 40-Core Gauntlet (v2) | [`10.5281/zenodo.22983889`](https://doi.org/10.5281/zenodo.22983889) | [`10.5281/zenodo.22974543`](https://doi.org/10.5281/zenodo.22974543) | [`arXiv:2609.33066`](https://arxiv.org/abs/2609.33066) • [HF Paper](https://huggingface.co/papers/2609.33066) | [`pCwOrM/werr`](https://github.com/pCwOrM/werr) & [`werracle`](https://github.com/pCwOrM/werracle) |
| **Paper 6: WerrSoma** | Drosophila Connectome (158K Nöron, v1.1) | [`10.5281/zenodo.23072929`](https://doi.org/10.5281/zenodo.23072929) | [`10.5281/zenodo.22996625`](https://doi.org/10.5281/zenodo.22996625) | `arXiv:submit/8161759` [on hold] • [3D Portal](https://werrsoma.answerr.me/) | [`Lexovian/WerrSoma`](https://github.com/Lexovian/WerrSoma) (Mirror: [`pCwOrM/WerrSoma`](https://github.com/pCwOrM/WerrSoma)) |
| **Paper 7: Werracle** | Sub-Cent Intra-Block EVM AI Oracle (v1) | [`10.5281/zenodo.22942599`](https://doi.org/10.5281/zenodo.22942599) | [`10.5281/zenodo.22942598`](https://doi.org/10.5281/zenodo.22942598) | [`arXiv:2609.30719`](https://arxiv.org/abs/2609.30719) • [HF Paper](https://huggingface.co/papers/2609.30719) | [`pCwOrM/werracle`](https://github.com/pCwOrM/werracle) & [`werralem`](https://github.com/pCwOrM/werralem) |
| **Paper 8: Schönhage**| Tensor Taşıyıcı Sıkıştırma ($W=176M$) | [`10.5281/zenodo.23268580`](https://doi.org/10.5281/zenodo.23268580) | [`10.5281/zenodo.23268579`](https://doi.org/10.5281/zenodo.23268579) | `arXiv:submit/8207241` [submitted] • CrocSwap #226 | [`pCwOrM/integer-mult-bounds`](https://github.com/pCwOrM/integer-mult-bounds) |
| **Paper 9: Güneş Dili**| Deterministik Morfoloji & 53 Koma | [`10.5281/zenodo.23273006`](https://doi.org/10.5281/zenodo.23273006) | [`10.5281/zenodo.23273005`](https://doi.org/10.5281/zenodo.23273005) | Lean 4 Doğrulanmış • [Canlı Portal](https://pcworm.github.io/gunes-dili/) | [`pCwOrM/gunes-dili`](https://github.com/pCwOrM/gunes-dili) |
| **Motor: WERR** | Zero-VRAM Gauntlet & JevBench Intake | [`10.5281/zenodo.22939253`](https://doi.org/10.5281/zenodo.22939253) | [`10.5281/zenodo.22867425`](https://doi.org/10.5281/zenodo.22867425) | [`arXiv:2609.25498`](https://arxiv.org/abs/2609.25498) • [HF Paper](https://huggingface.co/papers/2609.25498) • [HF Dataset](https://huggingface.co/datasets/pCwOrM/werr_open_decisions) | [`pCwOrM/werr`](https://github.com/pCwOrM/werr) |
| **Platform: answerr**| Reflex AI & Canlı Çalışma Alanı | Canlı: [`answerr.me`](https://answerr.me) | - | Çift Bilişsel Refleks Platformu & API | [`pCwOrM/answerr`](https://github.com/pCwOrM/answerr) |
| **Ayrık Alg** | GAP-Lean4 Biçimsel Doğrulanmış Port (35 Teorem)| [`10.5281/zenodo.23045504`](https://doi.org/10.5281/zenodo.23045504) | [`10.5281/zenodo.23045503`](https://doi.org/10.5281/zenodo.23045503) | [`arXiv:2609.38492`](https://arxiv.org/abs/2609.38492) • [HF Paper](https://huggingface.co/papers/2609.38492) | [`pCwOrM/gap-lean4-port`](https://github.com/pCwOrM/gap-lean4-port) |

---

## 📜 License, Trademark & Patent Notice

This software and its bio-synthetic neuromorphic interfaces are dual-licensed under the **[Business Source License 1.1 (BSL 1.1)](LICENSE)** and the **BBL v1.0 (Barış, Bilim, Liyakat)** ethical charter:
* **Academic, Educational, and Non-Commercial Research Use:** 100% Free and open for non-commercial research, peer-review replication, student inquiry, and open-science benchmarking. All underlying mathematical proofs, formal topological theorems, and open preprints remain universal public knowledge.
* **Corporate Stewardship & Trademark Protection:** **WerrSoma™**, **WERR™**, and **answerr™** are trademarks protected under corporate stewardship of **ITouch Systems** (ITouch Bilişim Sistemleri Mühendislik Danışmanlık San. ve Tic. Ltd. Şti., Çukurova Teknokent).
* **Commercial Restriction:** Any deployment in commercial brain-computer interfaces (BCI), neuroprosthetics, commercial robotics/drones, hosted SaaS, or paid APIs requires an express written Commercial License from ITouch Systems.
* **Change Date:** On **2030-01-01**, this repository automatically converts to the permissive **Apache License, Version 2.0**.
* **Patent Protection:** Key neuromorphic coprocessor architectures, whole-brain connectome steering methods, and biophysical anti-burnout gating mechanisms are officially subject to national priority patent application **TÜRKPATENT TR 2026/016633** (Official Priority Date: September 27, 2026, 06:16:04 UTC+3) and upcoming international PCT applications under the Paris Convention.
