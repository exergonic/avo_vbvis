# avogadro-vbvis

[![Project Status: WIP](https://img.shields.io/badge/status-work%20in%20progress-orange.svg)](https://github.com/exergonic/avo_vbvis)
[![Environment: Pixi](https://img.shields.io/badge/environment-pixi-blue.svg)](https://pixi.sh)
[![Python: >=3.11](https://img.shields.io/badge/python-≥3.11-green.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

Bridging molecular geometry with qualitative chemical intuition. **avogadro-vbvis** is a modern Python-driven plugin for Avogadro 2 designed to algorithmically determine and visualize valence bond orbitals (hybridization, localized lone pairs, and orbital overlap lobes) typically taught in undergraduate general and organic chemistry courses.

> ⚠️ **Project Status: Work in Progress** > This project is under active foundational development. The core framework, Avogadro UI menu hooks, isolated Pixi environment management, and CJSON data-logging pipelines are completely functional. Local coordinate vector math and orbital mesh rendering algorithms are currently being prototyped.

---

## 🧪 The Vision

While standard computational chemistry software excels at calculating highly delocalized Molecular Orbitals (MOs) via quantum mechanics, students and researchers often reason using the localized framework of **Valence Bond (VB) Theory** and **VSEPR**. 

This plugin aims to:
* Automatically analyze local coordination environments of central atoms.
* Determine hybridization states ($sp$, $sp^2$, $sp^3$, $sp^3d$, etc.) based on geometric configurations.
* Direct and render 3D geometric meshes representing localized bonding pairs and lone pair lobes directly in the Avogadro 2 viewport.

---

## 🛠️ Architecture & Tech Stack

The plugin leverages a modern, ultra-fast Python stack isolated entirely from global system variables:

* **[Avogadro 2 Plugin API](https://two.avogadro.cc/)**: Utilizes the external script plugin framework to communicate via standard I/O streams using Chemical JSON (CJSON) payloads.
* **[Pixi](https://pixi.sh)**: A rapid, Rust-powered package management tool used to handle binary dependencies and lock environments deterministically.
* **[uv_build](https://github.com/astral-sh/uv)**: A blazing-fast backend to manage python package metadata and project scripts.
* **NumPy & SciPy**: Vectorized math structures optimized for rapid spatial neighbor lookups, coordinate translation, and angular evaluations.

---

## 🚀 Quick Start for Developers

### Prerequisites
Ensure you have [Pixi installed](https://pixi.sh/latest/#installation) on your machine.

### Installation

1. Clone the repository into your local Avogadro 2 plugins directory:
   ```bash
   git clone [https://github.com/exergonic/avo_vbvis.git](https://github.com/exergonic/avo_vbvis.git)
   cd avo_vbvis
   ```

2. Initialize and lock the isolated environment:
   ```bash
   pixi run python -m pip install -e .
   ```
   *Note: This performs an editable install, creating the executable shortcuts required by Avogadro 2 while linking directly to your active development files.*

### Debugging & Prototyping
To view real-time plugin diagnostics and execution logs without launching the full Avogadro GUI, pipe a mock CJSON structure directly into the CLI tool:
```bash
pixi run avogadro-vbvis display-valence-orbitals < tests/mock_molecule.json
```

---

## 🗺️ Roadmap
- [x] Establish Avogadro 2 GUI Extension menu handshake.
- [x] Configure robust `pyproject.toml` and Pixi task tracking environment.
- [x] Implement structured file logging via `sys.stderr`.
- [ ] Build standalone CJSON parsing utility for atomic coordinates and indices.
- [ ] Implement VSEPR coordination number and vector math evaluation.
- [ ] Generate 3D grid/cube mappings for orbital lobe orientations.
- [ ] Render meshes back into the Avogadro viewport.