
# Avogadro VB Orbital Visualization Plugin

== WORK IN PROGRESS ==
This project is in its beginning stages. Nothing works and you shouldn't even be looking at it. :)

This repository contains the initial scaffold for an Avogadro 2 Pixi plugin that will visualize valence bond orbitals.

## Project layout

- `pyproject.toml` - Pixi plugin manifest and package metadata
- `src/avo_vbvis/` - Python package source
- `PROJECT.md` - high-level goals and planning notes

## Usage

The plugin exposes the entry point `avogadro-vbvis` and is intended to be invoked by Avogadro using the Pixi package API.

Example invocation:

```bash
pixi run avogadro-vbvis display-valence-orbitals
```

## Next steps

- implement the VSEPR-based orbital pipeline in `src/avo_vbvis/orbitals.py`
- add rounded scalar-grid generation for Avogadro cube output
- test the `display-valence-orbitals` menu command in Avogadro
