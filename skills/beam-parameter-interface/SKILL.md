---
name: beam-parameter-interface
description: "Create and use a shareable beam parameter interface with live analytical previews and exportable Abaqus/sweep configurations. Use for communicating beam dimensions, section sensitivity, named boundaries and solver-ready parameters; previews are small-deflection theory, not FEM results."
license: MIT
---


# Beam parameter interface

Make beam parameters visible, editable and transferable into a registered numerical study.

1. Read [the interface contract](references/interface.md). Use the included `assets/index.html` as a self-contained starting interface: open it directly or serve the repository with `python -m http.server 8765 --bind 127.0.0.1`.
2. Adjust length, section, modulus, density, tip displacement, duration and element count. Inspect the labeled undeformed/deformed beam, ROOT/TIP boundary sketch, analytical reaction and parameter sensitivity. The display uses Euler–Bernoulli small-deflection theory with an explicit deformation magnification; it is not an Abaqus result.
3. Export `beam-explicit.json` or `sweep.json` from the UI. For sweeping, use the user's chosen parameter range and review the generated case count. Import a compatible beam JSON to restore a setting. The UI rejects unsupported units/adapter and boundary protocols instead of silently changing their meaning.
4. Pass exported sweep JSON through the abaqus-parametric-workflow planner when that skill is available. Otherwise use a project-specific backend matching [the configuration interface](references/interface.md). Each skill is independently installable; the UI itself needs no other skill.
5. Test parameter changes, import/export and invalid settings in the browser. Capture actual rendered screenshots, label them as the generic sharing example, and include the configuration that generated them. Preserve analytical and solver-result labels when extending the interface.

For a real beam model adapt geometry, constitutive law, BCs and observables together. Large rotations, contact, shear-dominated members and instability are beyond the displayed analytical approximation. Do not treat a beautiful deformation preview as verified branch prediction.
