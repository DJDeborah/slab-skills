---
name: mechanics-research-handoff
description: Package mechanics research evidence into a reproducible project and clear shareable guidance. Use when delivering FEM, rod or analytical model results to another researcher with inputs, solver artifacts and limitations.
---

# Mechanics research handoff

Package the runnable project separately from the skills that instruct future work. Keep private chat histories, local license server names and personal absolute paths out of shared content.

1. Organize the project into inputs, source code, computed results and solver evidence. Retain input decks and extraction scripts; include ODBs only when the intended receiver can use them.
2. Record versions, command lines and hashes. Link each quantitative claim to a result field and its generating source.
3. Label analytic derivation, FE verification, CAE replication, parameter identification and experimental validation separately. State what remains untested without turning a successful benchmark into certification.
4. Create two visual views: project physics/data flow and skill trigger/instructions/resources/outputs. The visual order should match actual runnable steps.
5. Provide copyable Codex prompts and reproducible commands, expected checks, troubleshooting and minimal environment requirements. For a Feishu document preserve headings, tables and embedded figures; import a verified DOCX and check imported formulas and figures.
6. Share standalone skill folders with SKILL.md, or repository `.agents/skills`. If plugin distribution is requested, check the current official plugin schema and create a real manifest. A ZIP archive alone is not an installed plugin.

Use `references/handoff-checklist.md` to check the final deliverable. Mark results copied from an earlier evaluation as earlier evidence, not a fresh execution. Do not publish or message an external recipient unless the user authorizes it.
