# Search and gap contract

Use several query families as the topic requires: mechanism synonyms, application synonyms, closest methodological approach, and an adversarial query targeting the proposed novelty. Do not invent a fixed paper count as a quality certificate.

Capability assessment should concern mechanisms and scope: equilibrium branch discovery, contact feasibility, physical dynamic landing, transfer without refitting, matched-density comparison, continuum homogenization, or hardware closure. A new specimen count or unused parameter value is rarely sufficient by itself.

`gap.json` fields: `domain`, `gap_statement`, `search_scope`, `cutoff_date` (ISO date), `claim_type` (`bounded` or `universal`), `counterexample_queries` (queries actually run), `nearest_studies` (study_id plus capability, unresolved, assessment=`absent|partial|unknown|present`), `decisive_test`. Use ledger study IDs for references. A `present` record should cause revision if it resolves the entire gap; Codex must judge overlap, because the script has no semantic evaluator.

CSV columns: `study_id,query,engine,searched_on,title,url,doi,decision,passage,capability_note`. One row per assessed retrieved study; repeat study IDs across queries if needed. No-hit queries belong in `search_scope` with engine/date/result and can be linked separately. Excluded studies need a reason in `capability_note`.

DOI normalization removes common DOI resolver prefixes and case differences, but does not merge distinct preprint and journal records automatically. That needs human/agent inspection. The helper catches citation-less included records, unknown IDs, future/out-of-scope dates and duplicate DOI identities. It does not search, download papers or determine novelty.
