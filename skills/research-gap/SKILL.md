---
name: research-gap
description: Find and test bounded research gaps using a reproducible search ledger, primary-paper capability matrix, counterexample search and falsifiable gap statements. Use for literature-backed novelty assessment, not unsupported first-ever claims.
license: MIT
---


# Research gap

Find what the closest work has not resolved within an explicit problem domain.

1. Read [the search and gap contract](references/search-contract.md). State the intended mechanism, geometry family, boundary protocol, observable and method. Search synonyms and the closest competing approaches, not only the user's phrasing. Browse and open primary sources; titles or snippets do not prove capabilities.
2. Copy `assets/search-ledger.csv` and `assets/gap.json` into the project. They are templates, not literature evidence. Replace demo records. Log query, engine, date, URL/DOI, inclusion decision, and the supporting passage location for each capability assessment.
3. Build the nearest-work matrix: study → solved capability → scope/control → unresolved capability → direct source. Label unknown full-text access as `unknown`, not `absent`.
4. Actively search for a paper that would invalidate the proposed gap. Narrow or retire a contradicted claim. A finite search cannot establish universal absence.
5. Run `python <skill-dir>/scripts/audit_gap.py <project>/gap.json <project>/search-ledger.csv --out <project>/gap-audit.json`. Report search coverage and deduplication, not an automatic novelty verdict.
6. Deliver two or three bounded gap candidates with scientific consequence, closest counterexample and cheapest decisive test; recommend one based on the actual evidence and feasibility.

Useful handoff: a gap says what remains unresolved; significance says why resolving it matters; the test states what outcome would disprove the proposed contribution. If the user's question is already covered, say so and identify the residual issue.
