---
name: cauchy-micropolar-modeling
description: Derive and verify Cauchy and micropolar analytical models with independent microrotation, curvature energy and explicit boundary conditions. Use for Cosserat continuum comparison, not for treating a single rod matrix as homogenized material.
---

# Cauchy and micropolar modeling

Identify the scale: a Cosserat rod section, a rod endpoint port, and a bulk micropolar material are different objects. Define work-conjugate strains and stresses before assigning a name to a matrix.

Read `references/shear-layer.md` for a reproducible analytic benchmark. This material is phenomenological; its parameters are not inferred from the example helix.

1. State displacement, independent microrotation, macrospin, curvature and the sign convention. Specify plane stress or plane strain and whether shear is tensorial or engineering shear.
2. Write the strain energy. Report every parameter's units; use a declared length l0 when normalizing curvature entries of Q. Never take an unscaled eigenvalue comparison across dimensionally different blocks.
3. Derive equilibrium and the force/couple traction boundary terms variationally. A constrained rotation and a free couple traction are different boundary conditions.
4. Derive Cauchy restriction and any relaxed-rotation limit separately. Eliminating a local microrotation with zero curvature does not justify discarding finite-size boundary layers.
5. Run `scripts/layer_reference.py` for the clamped-rotation shear benchmark. Compare it with an independent displacement/rotation FE discretization and mesh refinement. Also run a free-rotation control and deliberately change a rotation constraint to check that the comparison detects the difference.
6. If homogenization is requested, define an RVE, generalized affine probes, periodic fluctuations, rigid-mode constraints and energy density normalization. Fit on calibration probes and reserve independent curvature and finite-size holdouts. Do not insert a rod port matrix into Q or claim a chiral bulk constitutive law from a helix response alone.

Deliver equations, assumptions, C and Q conventions, solved fields, reaction/energy comparison and unverified scale-transfer steps. The supplied isotropic Q has no chiral off-diagonal block; that is a benchmark choice, not a universal micropolar restriction.
