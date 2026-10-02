---
name: research-evidence-handoff
description: Package research claims with traceable figures, source data, code, solver inputs/results, frozen versions and rerun instructions. Use when consolidating research versions, preparing Main/SI, or handing reproducible work to another researcher.
---

Inventory existing results before rerunning or rewriting. Establish one canonical case/figure/claim index and retain prior versions through explicit supersession. Recover valuable analysis from older drafts; do not discard it because the newest draft is shorter.

Map each proposed claim to a quantitative result, figure, raw source, processing code, solver input/output when relevant, and verification boundary. Distinguish fitted cases, held-out predictions, discrete solver agreement, mesh convergence, diagnostic mechanisms and unsupported hypotheses. Maintain failed cases in the index. A figure's visual similarity does not substitute for numerical comparison.

Use `python scripts/check_evidence.py manifest.json root-directory` to hash declared relative artifacts and reject missing files or prediction claims supported only by calibration data. The supported manifest is `{ "claims": [{"id":"...", "claim_type":"prediction", "dataset_role":"holdout", "artifacts":[{"path":"relative/file.csv"}]}] }`. Optional `sha256` locks an artifact version. This validates traceability and simple role consistency, not scientific truth. Give each claim its actual evidence limitations and metric/tolerance outside this minimal integrity schema.

For paper assembly, keep the decisive physical explanation and evidence in Main; put reproducible derivation and complementary diagnostics in SI. Define each coordinate and matrix at first use and use the same registered sample through equations and figures. Preserve article-specific style and journal requirements; do not force a universal word count or figure count.

Deliver an entry point, manifest, source/code/data directories as appropriate, an exact rerun command with dependency versions, and a list of unresolved comparisons. Share only the requested distributable scope; sanitize private histories, credentials, personal paths and unpublished data unless the user requests their inclusion.
