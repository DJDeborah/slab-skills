---
name: register-analytical-fem
description: Register analytical and FEM cases to the same reference geometry, units, ports, boundary and loading conventions before comparing branches or fitting parameters. Use when initial nodes, section orientation, DOF mapping, or case identity may explain a mismatch.
---

Read the source geometry and solver deck rather than inferring dimensions from rendered figures. Record undeformed coordinates, section dimensions and directors, units, material law, physical supports, load history/control, imperfection, contact convention, observable definitions, and case/version identity. Make any correspondence between reduced-model ports and FEM nodes explicit. Keep mesh topology and reduced-model assumptions separate from physical case registration.

Use `python scripts/compare_registration.py analytical.json fem.json` for the supported simple SI/mm–N registration schema in [the fixture](assets/registration-example.json). The checker compares reference ports, elastic modulus/Poisson ratio, rectangular section, constraint records, loading amplitude and observable conventions after unit normalization. It does not parse Abaqus decks or infer node maps; provide aligned named ports and explicit records. Unsupported constitutive/section/constraint formats require a problem-specific comparison. Never convert missing input into agreement.

Only after registration, compare branch-wise observables, contact states, reaction and energy balance, event order, and held-out response. Freeze the calibration role and parameters. A modified reference geometry is a new registered model, not silent correction of the test set. Report mismatches and their concrete implications.
