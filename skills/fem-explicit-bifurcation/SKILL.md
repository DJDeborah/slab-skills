---
name: fem-explicit-bifurcation
description: Prepare and verify configurable FEM Explicit studies and separate dynamic events from equilibrium instability. Includes named-set boundary registration, an Abaqus beam adapter, ODB extraction, energy checks and analytical branch benchmarks; use for buckling and snap-through verification.
license: MIT
---


# FEM Explicit and bifurcation

Use the backend that answers the actual question. This package supplies a runnable Abaqus Explicit beam adapter and separate analytical normal-form benchmarks; it is not a general FE continuation solver.

1. Read [the analysis contract](references/analysis-contract.md). Register geometry, section axes, material/units, DOFs, constraints, contact, imperfection, load control, rate and observables. For a supplied mesh, adapt selectors to named regions; never assume that a coordinate from the demo identifies the user's boundary.
2. For the beam demonstration, copy `assets/beam-explicit.json` into the project. Run `python <skill-dir>/scripts/prepare_explicit.py <config> --out <run-directory>`. Review `registration.json`: selected node IDs/counts, conflicting DOFs and resolved geometry. It writes an INP deck but does not launch a job.
3. When solver execution is requested or already authorized, run `abaqus job=beam_explicit input=beam_explicit.inp double=both interactive` in that run directory. For other geometries/backends, use a project-specific adapter following [the adapter interface](references/adapter-interface.md). Reuse the chosen solver, not the demo physics.
4. Extract using `abaqus python <skill-dir>/scripts/extract_odb.py beam_explicit.odb history.json`. Require the actual completion record, readable expected ODB step and requested outputs. A zero launcher exit code is insufficient.
5. Run `python <skill-dir>/scripts/audit_history.py history.json --config <config> --out quality.json`. Interpret kinetic/internal and artificial/internal energy only over the configured meaningful window, with a nonzero-energy mask. Snap transients can have high kinetic energy. Report the window and loading-rate sensitivity; do not hide a transient by presenting only the final ratio.
6. For dynamic event candidates, use `scripts/detect_events.py` with `assets/events.json` as the configurable force sign/drop window example. Add an opening field, threshold and persistence count when that observable exists. These are observable labels, not stability certificates.
7. For equilibrium bifurcation claims, compute registered equilibrium residuals and constrained tangent modes along the actual branch with a project-specific continuation solver. Read [stability and contact](references/stability.md). Run `python <skill-dir>/scripts/branch_benchmarks.py --out branches.json` only as a fold/pitchfork analytic sanity test; it does not validate the user's FEM.
8. Deliver completion evidence, registration, mesh/rate sensitivity for the selected observable, event candidates and explicitly bounded stability claims. Propagate those distinctions to the manuscript.

Reusable boundary selectors, energy extraction and evidence categories are the shared part. Material failure, contact topology, rigid bodies, follower loads, periodic-cell constraints and full eigenmode extraction require explicit project adaptation.
