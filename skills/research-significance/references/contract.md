# What makes significance defensible

The useful chain is: limitation of the baseline → consequence for a scientific/design decision → proposed mechanism → observation that distinguishes it from alternatives → feasible scope.

Use evidence tiers `proposal`, `calibrated`, `holdout`, `experiment`. These are labels, not a universal ranking: an experiment with a confound can be weaker than a controlled calculation. If a proposed result is numerical, name the discretization and model assumptions. If a claim generalizes, name both tested and untested conditions.

A boundary-condition study can matter because it changes the accessible threshold spectrum or path topology. Merely changing which local feature moves first may be descriptive. A repeated supercell is not automatically a new infinite-periodic family. Coupling claims require an appropriate zero-coupling, symmetry, density or geometry control; choose the control from the mechanism, not a fixed checklist.

JSON contract: `question`, `decision`, `baseline`, `mechanism`, `observable`, `scope`, `claim`, `evidence_tier`, `evidence` (list of IDs, roles and source descriptions), `rivals` (explanation and discriminating_test), `falsifier` (metric, comparator, threshold), `controls`, `calibration_cases`, `holdout_cases`. Thresholds are preregistered or transparently exploratory, never inferred solely to rescue a claim.

The helper checks complete fields, references, evidence labels, distinct holdout groups and falsifier syntax. It cannot determine whether the test actually separates the mechanisms or whether a source supports the claim. Codex must assess those meanings from the underlying materials.
