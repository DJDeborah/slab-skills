---
name: helix-rod-design
description: Generate and analyze helical rod geometry, section frames and linear axial twist coupling. Use for helix pitch, handedness and rod design; distinguish rod port stiffness from bulk constitutive tensors.
---

# Helix rod design

Freeze the physical contract before computing: length and force units, E and nu, circular radius or full section tensor, centerline, stress-free reference configuration, material director convention, endpoint constraints and load application point. Record the handedness by a formula rather than an ambiguous RH label.

1. Read `references/rod-model.md` for the baseline formulas and circular-section assumptions.
2. For geometry-only requests run `scripts/helix_geometry.py --config <json> --out <csv>`. Start from `assets/helix.json` if the user supplies no baseline. Record turn-clearance and curvature-to-section ratios. The CSV is a centerline, not a solid CAD model.
3. For mechanics use a declared curved-rod energy or a beam FE solver. Track six work-conjugate endpoint coordinates `[ux,uy,uz,theta_x,theta_y,theta_z]` and wrenches `[Fx,Fy,Fz,Mx,My,Mz]`. Hold the root fixed and release the other tip coordinates for compliance probes. Constrained lateral ports produce a different response.
4. Compare a smooth-centerline energy integral with increasing polyline resolution. Do not call numerical quadrature a closed-form solution. Normalize rotation coordinates by a declared reference length before comparing whole matrices.
5. Verify reciprocal compliance and positive energy, then reflect handedness while retaining the same global load axes. Report both diagonal responses and the coupling sign. Use small physical loads for the displayed deformation.
6. For design sweeps show pitch, height and wire length together. Fix material volume or density if making an equal-material comparison; otherwise state the changed material amount. A scalar axial force response is insufficient to identify all section properties.

Return geometry, the frozen contract, compliance or stiffness with DOF ordering, mesh evidence and an explicit prediction scope. Buckling, contact, plasticity and finite rotations require their own model and validation.
