# Validation report / 实测验证报告

Measured on 2026-10-02, Windows, portable Python 3.12.14. Licensed execution used Abaqus/Explicit 3DEXPERIENCE R2019x and its Python 2.7.3 ODB reader. This report separates deterministic helper behavior from scientific and agent-level effectiveness.

## Portable checks

- 38 local unittest checks passed, including informative negative controls for leakage, unbounded novelty, invented ledger IDs, missing passages, missing figures, modified evidence, wrong boundary nodes/DOFs, excessive inertia and incomplete jobs.
- All four SKILL.md files passed the bundled skill-creator quick validator; UI descriptions/default prompts and local reference links were inspected. UTF-8 mode was needed for that bundled validator on a Windows GBK-default shell.
- Complete-directory installation was tested in an isolated destination, including non-overwrite behavior. An installed helper was executed successfully. No claim is made that a cached app discovered the skills without a fresh task/turn.
- The portable end-to-end demo ran all four workflows and generated an annotated writing draft, evidence map, prospective significance contract, synthetic literature ledger, registered Explicit deck and exact normal-form outputs.
- Fold/pitchfork sampled equilibria had residuals below 1e-12 and the expected tangent signs. These are exact known scalar branches, not an FE continuation test.

## Real Explicit execution

Each case has a completed STA record, a readable expected LOAD ODB step and 501 exported time-history samples. The histories and source hashes are stored under [beam-cases](../validation/research-v0.1.0/beam-cases/). Binary ODBs and full local console files are retained in the local working directory, not uploaded. Published INPs/configs let others reproduce the runs with their own licensed solver.

The reference tip displacement is −0.1 mm and the small-deformation Euler–Bernoulli reaction is −0.0525 N. All cases used double precision, automatic stable time increments and no mass scaling. Ratios below concern t/T∈[0.5,1] with an internal-energy mask of 1% of peak IE; full-history meaningful-window maxima are also recorded in JSON.

| Case | Elements | Duration/s | Final RF2/N | Reaction error | Max KE/IE in window | Event candidates |
|---|---:|---:|---:|---:|---:|---:|
| n10_t025 | 10 | 0.25 | -0.05252707 | 0.05156% | 0.08011% | 0 |
| n20_t025 | 20 | 0.25 | -0.05250386 | 0.00736% | 0.07953% | 0 |
| n20_t050 | 20 | 0.50 | -0.05250374 | 0.00713% | 0.01988% | 0 |

Final prescribed U2 in all three runs was −0.10000000149 mm at ODB output precision. ALLAE was zero for this beam. The final-reaction mesh sensitivity (10 → 20 elements) was 0.04420% and loading-duration sensitivity (0.25 → 0.50 s at 20 elements) was 0.000227%. These are two-setting sensitivity checks on one elastic observable, not a convergence-order proof.

## Failures observed and retained

The first single-precision run completed, but its final U2 was −0.10039236 mm, approximately 0.39% away from the prescribed value. The audit rejected it; see [the retained rejection](../validation/research-v0.1.0/single-precision-rejected.json). A double-precision rerun passed the same criteria. This is an observed numerical issue for this example, not a blanket claim about all single-precision Explicit jobs.

The first ODB extractor assumed `.log` existed and then assumed ordinary dictionary membership for an Abaqus repository. Actual interactive R2019x execution exposed both assumptions. The shipped version handles absent interactive logs, uses repository keys, casts ODB scalars to Python float and checks the produced history artifact. The launcher returned 0 despite extraction tracebacks, confirming why artifacts and completion evidence must be checked separately.

One default displacement-boundary warning was reviewed: the deck prescribes a single smooth ramp and no intended inter-step jump. Its local data and console records preserve the warning.

## What remains unverified

No independent Codex-model A/B experiment, blinded writing assessment or real-literature novelty evaluation was run. [CODEX_VALIDATION](CODEX_VALIDATION.md) gives an explicit protocol for that next level. The writing and gap helpers verify structure/provenance; they cannot certify the meanings of claims or the scientific quality of prose.

No contact specimen, material nonlinearity, periodic metamaterial, full FE bifurcation, branch switching, dynamic snap landing or robot hardware was validated by the beam runs. The adapter/reference contracts describe how to extend the package without silently claiming those capabilities.

## Reproduce

```bash
python -m unittest discover -s tests -v
python tools/run_demo.py --out local-runs/demo-new
python tools/run_abaqus_smoke.py --abaqus abaqus --out local-runs/explicit-new --sensitivity
```

Use a licensed Abaqus launcher; select its absolute `.bat` path on Windows if needed. Optional solver execution is not part of GitHub Actions. CI runs only portable tests and the synthetic demo.
