---
name: research-significance
description: "Develop evidence-bounded research significance for mechanics, metamaterials and robotics: connect a changed scientific or design decision to mechanisms, rival explanations and discriminating tests. Use for contribution framing and hypothesis prioritization."
license: MIT
---


# Research significance

Turn an interesting result into a defensible explanation of why it changes a scientific or engineering decision.

1. Identify the target decision, baseline capability, proposed change, physical mechanism, observable, and intended scope. Ask for missing information only when it changes the decision; otherwise record an assumption.
2. Read [the significance contract](references/contract.md). Start from the user's evidence, not an adjective such as novel, programmable or unprecedented. Distinguish a new geometry from a new mechanism, prediction or accessible design space.
3. Give at least one plausible rival mechanism and one discriminating test with a measurable failure condition. If claiming predictive transfer, identify calibration and holdout groups before fitting.
4. Fill `assets/significance.json` in the working project. Keep proposed significance separate from established findings. Run `python <skill-dir>/scripts/audit_significance.py <project>/significance.json --out <project>/significance-audit.json`.
5. Write a short significance paragraph plus a table mapping contribution → evidence → limitation → next test. A passing audit checks the contract, not scientific truth or importance. Do not inflate the paragraph to make it pass.

For numerical mechanisms, request the actual physical registration and stability evidence appropriate to the claim. A force drop, zero eigenvalue, lower-energy candidate and realized landing answer different questions. For robots, a simulated controller does not establish hardware feasibility.
