# Open-source influences and provenance

These are commit-pinned sources inspected while designing this package. The helpers and domain contracts in this repository were newly implemented; no upstream code module or full skill text was vendored. Links document influences and make the comparison reproducible, rather than implying endorsement or universal portability.

| Source | Pinned commit / license | Used here |
|---|---|---|
| [K-Dense hypothesis-generation](https://github.com/K-Dense-AI/scientific-agent-skills/tree/91497e335489dcb544ec8ddc8f6b7ce5fd6d1121/skills/hypothesis-generation) | `91497e335489dcb544ec8ddc8f6b7ce5fd6d1121` / MIT | rival hypotheses, operational predictions, evidence-bounded planning |
| [K-Dense scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/tree/91497e335489dcb544ec8ddc8f6b7ce5fd6d1121/skills/scientific-writing) | same commit / MIT | claim/source linkage and manuscript consistency |
| [FEMIS](https://github.com/test1card/femis-skill/tree/ceff46782f8379425162f7de42a46312f07704a5) | `ceff46782f8379425162f7de42a46312f07704a5` / Apache-2.0 | numerical V&V and energy/convergence discipline |
| [CAE-Agent-Hub](https://github.com/Cai-aa/CAE-Agent-Hub/tree/194ef498e6efb1984cd65325e21e71087588a581) | `194ef498e6efb1984cd65325e21e71087588a581` / MIT | Abaqus model, execution and postprocessing separation |
| [UCL-ERL paper/code consistency](https://github.com/UCL-ERL/skills/tree/9d50603850b661a1da175ef3e330ba0b52e3efe9/skills/evaluation/paper-code-consistency-auditor) | `9d50603850b661a1da175ef3e330ba0b52e3efe9` / MIT | inspect scientific claims against actual execution evidence |

Domain additions come from generalized research-workflow observations: boundary-condition registration, calibration/holdout separation, contact release versus later fold/jump, and preservation of Main/SI evidence across revisions. Original private cases and text are excluded.

## What was measured upstream

An earlier local audit of these pinned sources on Windows ran the FEMIS `test_scripts` suite: 59 tests passed. The K-Dense hypothesis-generation suite recorded 25 passed, 1 failed and 1 skipped (plus 7 subtests); the failure concerned a POSIX file-permission expectation on Windows, and the skip concerned unavailable symlinks. The failing test was not silently counted as a pass.

Those results establish execution of the particular checked helpers on that machine. They do not certify the whole repositories, all their instructions or agent reasoning quality. The newly inspected scientific-writing source and UCL-ERL auditor were used as design references; their complete upstream suites were not run in this package's validation. CAE-Agent-Hub guidance was consulted while developing an independently executed beam adapter.

Robotics context: [official MuJoCo skills](https://github.com/google-deepmind/mujoco/tree/56aeb7c4b9138861d47305f03195dfa6ef3067da/doc/skills), Apache-2.0, were previously inspected with real small control/contact/rendering smoke checks. A documented binding convenience call did not work on the installed MuJoCo 3.14.0 API and required adaptation. This four-skill package does not vendor a robotics executor or claim hardware validation.

## Primary format and solver sources

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills): structured entrypoints, optional runnable resources and discovery paths.
- [OpenAI: Plugin packaging](https://developers.openai.com/plugins/build/plugins): root `plugin.json` plus fixed `skills/` component layout.
- [OpenAI: Skill installer](https://github.com/openai/skills/blob/main/skills/.system/skill-installer/SKILL.md): install a GitHub path as a complete directory.
- [SIMULIA: Quasi-static Explicit](https://docs.software.vt.edu/abaqusv2025/English/SIMACAEGSARefMap/simagsa-m-Quasi-sb.htm): inertia and loading-time considerations.
- [SIMULIA: Unstable collapse and postbuckling](https://docs.software.vt.edu/abaqusv2025/English/SIMACAEANLRefMap/simaanl-c-postbuckling.htm): equilibrium path analysis and Riks scope.

Documentation was inspected on 2026-10-02. The installed R2019x solver, rather than the linked 2025 manual, establishes the measured execution environment.
