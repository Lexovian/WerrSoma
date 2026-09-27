# Contributing to WerrSoma

Thank you for your interest in contributing to **WerrSoma**, an open-science bio-synthetic neuromorphic connectome interfacing initiative.

---

## 🏛️ Intellectual Property & Licensing Scope

1. **Non-Commercial Academic & Research Use:**
   * This project is licensed under the **[Business Source License 1.1 (BSL 1.1)](LICENSE)**.
   * Academic researchers, educators, and peer-reviewers are warmly encouraged to replicate, benchmark, and extend the algorithms for non-commercial scientific research.
2. **Commercial Deployment Restrictions:**
   * Any commercial exploitation, including integration into proprietary clinical BCIs, commercial robotics/drones, medical devices, or closed-source neural co-processors, requires an explicit written commercial license from the Licensors.
3. **Patent Priority:**
   * Core neuromorphic coprocessor architectures, whole-brain connectome steering methods, and biophysical anti-burnout gating mechanisms are officially protected under national priority patent application **TÜRKPATENT TR 2026/016633** (Filed Sept 27, 2026, 06:16:04 UTC+3) and international PCT applications.

---

## 🔬 How to Contribute

### 1. Reproducing Scientific Benchmarks
Before submitting pull requests or experimental modifications, run the full 6-protocol automated benchmark suite:
```bash
pip install -r requirements.txt
python run_scientific_experiments.py
python test_bioneural_phases.py
```
Ensure all tests exit with status `0` and do not violate the biophysical homeostasis bounds (membrane potential clamp $\le -50\text{ mV}$, peak refractory clamp $\ge 20.0\text{ ms}$).

### 2. Submitting Pull Requests
1. Fork the repository and create a new feature branch (`git checkout -b feature/biophysical-improvement`).
2. Adhere to PEP 8 standards and keep type annotations consistent.
3. If introducing new neural circuits or neuropil compartments from FlyWire, provide the corresponding neuron IDs and synapse matrices.
4. Submit the PR with a comprehensive description of the hypothesis and empirical delta.

---

## 👥 Scientific Inquiries & Liaison

For research collaborations, data sharing, or commercial licensing inquiries:
* **Corresponding Author:** Volkan Dağlı (`ask@answerr.me`)
* **Project Portal:** [https://lexovian.pcworm.net/](https://lexovian.pcworm.net/)
* **Zenodo Repository:** [https://doi.org/10.5281/zenodo.22996626](https://doi.org/10.5281/zenodo.22996626)
