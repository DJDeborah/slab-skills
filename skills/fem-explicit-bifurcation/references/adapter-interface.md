# Project-specific solver adapter

Reusable input: a units contract; geometry/mesh identity; material law; section/director conventions; named regions; BCs by region and DOF; contact pairs and initial gap; imperfection field and amplitude; load control/time/amplitude; solver settings; requested observables; convergence plan.

Reusable output: `registration.json`, input-file hash, completion records, equilibrium or dynamic histories, node/element/region maps, solver version, energy definitions and branch/event labels.

Boundary selectors in the demo support a named bounding box with a required expected count. A real adapter can resolve CAD faces, mesh labels, nearest reference locations or periodic maps. Always return selected IDs and inspect them. Fail empty/incorrect counts and conflicting assigned DOFs. Expected count alone cannot prove the selected region is physically correct.

For Abaqus/Standard: eigenvalue buckling estimates perturbation modes about a registered base state. Riks traces an equilibrium path under suitable proportional load control; it does not provide physical time evolution or automatically switch every bifurcating branch. A real extension needs imperfection studies, branch switching and constrained/contact-aware mode extraction.

For Explicit: preserve physical time, inertia, contact and dissipation. Use near-equilibrium stable windows when comparing to a static branch. Do not relabel the entire dynamic trajectory as equilibria. Couple analytical/ROM and FEM only after matching geometry, units, generalized coordinates, boundary conditions, load protocol and work-conjugate observables.

ODB JSON schema from the supplied adapter: `completed`, `solver_banner`, `step`, `history` rows with `time,U2,RF2,ALLIE,ALLKE,ALLAE`, `source_hashes`. Field requests provide additional nodal evidence. Missing requested outputs are failures, never substitute synthetic data. Stable-step/time increment and mass-scaling metadata should be added in a full application; the provided smoke deck uses automatic stable increment and no mass scaling.
