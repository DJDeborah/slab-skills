---
name: research-writing
description: Draft or revise scientific manuscripts with claim-to-evidence traceability, clear physical definitions and preservation of essential Main/SI content. Use for mechanics research writing, figure narratives and bounded validation claims.
license: MIT
---


# Research writing

Make the scientific argument readable without losing the material that supports it.

1. Establish the requested language, audience, manuscript version and deliverable. Use the user's chosen format. Inspect the latest full evidence-bearing Main/SI, not just the shortest or newest text.
2. Read [the writing contract](references/writing-contract.md). Make a claim/evidence inventory and a preservation list before major restructuring. Use `assets/manuscript-map.json` as a schema example, with project-relative evidence paths.
3. Structure each result as question → observation → mechanism interpretation → evidence boundary. Give variables and DOF conventions before equations. Connect figure panels to the conclusion they support. Put physical meaning in Main and reproducible details in SI without deleting the bridge between them.
4. Mark traced draft statements with `[claim:C1]` and figure references with `[figure:F1]`. Run `python <skill-dir>/scripts/audit_manuscript.py <project>/manuscript-map.json <project>/draft.md --out <project>/writing-audit.json`. The inventory can represent a DOCX/TeX draft via an extracted Markdown audit copy; use the relevant artifact workflow for rendering the final file.
5. Inspect every flagged semantic issue yourself. Existing files or a phrase match cannot verify a scientific claim. Report supported, disputed and untested claims. Preserve originals and write the revised version to a new file unless the user asked to edit in place.
6. Deliver the revised text, a meaningful change summary and any missing evidence. Audit tags are for review; remove them from the clean final after retaining an annotated copy and the map.

Avoid translating `minimum eigenvalue = 0` into proven snap, calibration into prediction, repeated supercells into a new material family, or simulated performance into hardware demonstration. State the specific result and its range instead of making an absolute negative claim.
