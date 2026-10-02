---
name: rapid-mechanics-hypothesis
description: Turn a mechanics or simulation hypothesis into a small falsifiable test with rival explanations, frozen inputs, an independent benchmark, and explicit limits. Use for rapid feasibility checks in buckling, contact, metamaterials, or robot simulation.
---

First translate the question into a measurable contrast and the result that would refute it. Separate a candidate mechanism from observations already available. Identify a competing explanation such as boundary changes, mesh artifacts, calibration leakage, contact state, or actuator saturation.

Choose the smallest test that distinguishes the explanations. Freeze geometry, units, material law, constraints, loading/control mode, observables, and numerical tolerances before evaluating target results. Reuse the user's solver and code when possible. When a lightweight model helps, say which physical mechanisms it omits. A useful escalation is hand estimate → reduced model → mesh/time-step study → independent solver or held-out geometry; stop at the level that answers the requested question.

Use analytical benchmarks for verification and distinct held-out cases for predictive validation. Do not refit to the target and call the result a prediction. Compare quantities on the same equilibrium branch and in the same coordinates; a correct Hessian on the wrong branch does not validate the measured trajectory.

For instability, separate contact release, loss of local constrained stability, a fold, a finite jump, and lateral reversal. A zero eigenvalue needs higher-order or branch analysis. A force drop in a transient needs the energy and loading history. Use the tangent permitted by the current constraints and unilateral contact; the unconstrained Hessian is insufficient. Classical static snap-back concerns backward turning of an equilibrium path in a specified force/displacement diagram.

Return the hypothesis and rival, frozen inputs, commands and versions, observable results with uncertainty/sensitivity, failed cases, and the next smallest discriminating test. Mark the outcome supported, contradicted, or unresolved within the tested scope. Do not infer experimental validity from solver agreement.

Read [benchmark guidance](references/benchmark-guidance.md) when selecting buckling or robot smoke tests.
