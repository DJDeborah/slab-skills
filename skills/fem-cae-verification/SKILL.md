---
name: fem-cae-verification
description: Register analytical and FEM CAE models, verify solver completion and compare matched observables with convergence and negative controls. Use for Abaqus or other finite element model verification, not certification of real material behavior.
---

# FEM CAE verification

Read `references/verification-contract.md` when registering two models. Reuse the user's chosen solver and authorized scope.

1. Freeze and compare geometry, section convention, material, reference state, DOF order, root and tip constraints, loads, shear factor, mesh and outputs. Record an explicit physical rationale for any difference before comparing numbers.
2. Execute only a supported model. In Abaqus, check the completion record and open the ODB to read all expected steps. A process return code alone does not establish a completed analysis. Interactive jobs may have console output but no `.log` file.
3. Compare work-conjugate observables and root balance. Account for the endpoint moment arm when checking root moments. Use relative error only for nonzero reference entries; report absolute tolerances around zero.
4. Refine the mesh on the quantities of interest. Separate same-polyline solver agreement from convergence to a smooth centerline. Prefer a small informative set of meshes; do not extrapolate an order from an oscillatory sequence.
5. Run at least one physical mismatch control appropriate to the question, such as wrong chirality or rotation BC. Mark it as an intentionally rejected comparison.
6. Use `scripts/verify_results.py --results <results.json>` to verify the example evidence and source hashes. This helper audits computed evidence; it does not reproduce the solver or prove the underlying theory.

Return a registration summary, logs and ODB evidence, convergence table, source hashes and bounded conclusions. Verification of an elastic model does not establish experimental validation, a buckling capacity or post-buckling stability.
