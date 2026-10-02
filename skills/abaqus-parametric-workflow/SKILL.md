---
name: abaqus-parametric-workflow
description: "Prepare and run bounded Abaqus parameter sweeps with frozen configurations, stable case IDs, named boundary registration, per-case completion evidence and resumable results. Use for reproducible parameter studies; the supplied adapter is an elastic planar B21 cantilever."
license: MIT
---


# Abaqus parametric workflow

Turn a parameter study into traceable per-case jobs rather than a loop that only changes filenames.

1. Read [the workflow contract](references/workflow.md). Confirm parameter meanings, units, geometry, named boundary regions, output quantities and an appropriate study size. Preserve the user's solver and scope.
2. Copy `assets/sweep.json` into the project. The included adapter is an elastic B21 cantilever; use [the adapter contract](references/adapters.md) for other mechanics. Do not run actual research specimen defaults as a teaching demo.
3. Run `python <skill-dir>/scripts/prepare_sweep.py <sweep.json> --out <new-run-dir> --max-cases 16`. Inspect `manifest.json` and each case's selected node IDs and INP. Changing length also changes the named TIP region in this adapter. Cases/configuration/helper hashes are frozen.
4. Preview execution with `python <skill-dir>/scripts/run_sweep.py <manifest.json> --max-jobs 2`. It reports the bounded queue without launching Abaqus. When solver execution is requested or authorized, add `--execute --abaqus <launcher>`.
5. The runner checks completion records and actual ODB histories, not only return code. Read per-case `status.json`, console logs and `summary.csv`. A failed job stops the default queue. If a restart is appropriate, use `--resume`; failed or interrupted cases additionally require `--retry-failed`. It refuses changed frozen input/config/helper hashes and skips completed cases only after evidence-integrity checks.
6. Compare registered quantities and mesh/loading sensitivity before interpreting a physical trend. Parameter sensitivity is not parameter identification; fitted cases are not holdout predictions. Keep numerical quality failures in the summary.

For a GUI-generated study, export its JSON and pass it through the same planner. The interface preview is analytical; it does not contain an FE solution. Contact, nonlinear materials, periodic constraints, static Riks and branch switching need a separately implemented project adapter.
