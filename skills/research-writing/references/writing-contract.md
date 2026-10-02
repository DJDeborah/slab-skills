# Writing contract

A strong paragraph has one scientific job. Start with the relevant question or finding, use evidence to develop it, explain the physical implication and bound the interpretation. Remove generic novelty adjectives unless the adjacent comparison justifies them.

Before equations define reference configuration, coordinates, normalization, admissible perturbations, contact/compatibility constraints and units. A directional derivative operator D and a full perturbation direction d cannot be left implicit when the derivation depends on them. Define Cauchy and micropolar quantities in their own kinematic contexts rather than treating differently sized matrices as interchangeable.

Figure writing: identify the controlled difference, read the actual observable, explain the physical mechanism and state what the panel cannot establish. A matching displacement overlay does not prove branch identity, opening order or tangent stability. A finite equilibrium branch does not automatically give a realized dynamic landing.

Main/SI preservation: inventory core figures, controls, failed cases, derivation assumptions, frozen parameter fits, source code and data. `required_assets` are IDs that must remain in the manuscript narrative. Main and SI can share an argument without duplicating all curves. Keep essential interpretation with the main figure and full registration/convergence in SI.

Manifest: `claims` with `id,text,status,evidence_ids`; `evidence` with `id,path,sha256,role`; `figures` with `id,caption,evidence_ids`; `required_assets` with claim/figure IDs. Roles: `proposal`, `calibration`, `holdout`, `experiment`, `numerical-verification`, `theory`. Status: `proposed`, `supported`, `disputed`, `untested`. A supported claim needs non-proposal evidence; source review still determines sufficiency. Empty hashes are allowed while drafting but surfaced as warnings; freeze SHA-256 hashes for a final handoff.

The bundled audit intentionally checks only linkage, required content and evidence integrity. It is not a prose-quality metric, automated peer review or numerical reanalysis. An optional terminology warning highlights phrases for inspection without banning legitimate statements.
