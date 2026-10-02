# Reusable sweep contract

The transferable habits are a frozen plan, bounded queue, stable identity, per-case evidence, explicit failures and auditable resume. The helper defaults are illustrative and configurable, not universal execution limits.

1. Freeze the full configuration, axes and adapter hashes before running. A case ID derives from canonical JSON, so an identical configuration has the same ID.
2. Resolve named boundary sets from the generated geometry and record actual selected IDs. Counts alone do not guarantee physical selection.
3. Prepare all inputs before consuming solver licenses. Launch cases serially within `--max-jobs`; a failure stops the queue unless an explicit continuation policy is selected.
4. A completed analysis has success text in its STA, a readable expected ODB step, aligned finite histories and the requested end time. A passed quality audit is a separate result.
5. Preserve both failures and successes. Resume requires frozen input, config and helper identity; completed evidence hashes must match. Failed/interrupted retry does not overwrite an old run: the runner uses a new attempt directory.
6. Summarize status, parameters, final displacement/reaction, energy ratios and evidence paths. Numerical final-reaction checks do not validate buckling or physical experiments.

JSON: `base` is the supported beam config; `axes` maps allowed parameter paths to finite lists. Allowed paths: geometry.length/width/thickness/elements, material.E/nu/density, duration and tip_displacement. Empty axes means one base case. A duplicate axis value is rejected. The planner adjusts ROOT/TIP endpoint selectors for this adapter; custom selectors or BC changes belong in a new adapter.

`manifest.json` is the frozen plan; each case directory holds `config.json`, `registration.json`, INP and `status.json`. Run artifacts live under `attempts/001/` etc. Do not edit files under a frozen plan to rescue a failed result. Prepare a new plan when the problem changes.
