# PARN Copilot Agent — beta 0.8.0 release baseline

**Date:** 2026-10-15  
**Status:** Proposed / not deployed by this repository  
**Origin:** Consolidated from PARN candidate instructions and validation artifacts dated 2026-10-13. The prior report identifies saved Copilot agent v9 and a candidate v10. These are **Copilot edit versions**, not directly equivalent to GitHub release versions.

## Scope

- Three copy-ready outputs: PARN, Suggested Internal Notes, and Client Follow-Up Email.
- Fidelity to technician dictation, chronology, literal technical evidence, state of work, and actual outcomes.
- Internal/public routing for single notes and bounded sections.
- Screenshots and logs as evidence without assuming who performed an action.
- Context-aware terminology using a separately maintained approved table.
- Optional SharePoint/Teams knowledge research and public vendor research, each confined to internal suggestions.
- Privacy-aware searches and no assumption that skill files grant access or permissions.

## Repository artifacts

- `agent/ConnectWise_PARN_Agent_Instructions_Condensed.md` — current **candidate** agent instructions; 8,000-character limit applies to deployed Copilot instructions.
- `agent/knowledge/PARN_Terminology_Table.txt` — approved terminology reference.
- `skills/parn-internal-knowledge-review/SKILL.md` — internal knowledge workflow.
- `skills/it-deep-vendor-research/SKILL.md` and `references/vendor-sources.md` — public/vendor research instructions and a **sanitized, curated** vendor index.
- `tests/PARN_Test_Report.md` — historical manual dry runs; 22 example cases with bracketed synthetic identifiers. **Not** agent knowledge.
- `tests/validate_parn_examples.py` — deterministic checks for instruction limits and selected synthetic output patterns.
- `config.example.yaml` — documentation-only placeholder inventory (not parsed by Copilot).

## Verification

The October 13 report describes 22 cases: three full-output examples and 19 focused cases. Static checks can verify known strings and formatting, **not** genuine live model behavior.

**Not yet verified live:** Copilot import, repeated run consistency, actual attachment OCR, knowledge retrieval and source permissions, skill invocation, client-specific access rules, and vendor browsing.

## Release controls

1. Back up the live agent and settings independently. This repository does not contain a live environment backup.
2. Review privacy before merging or packaging skill files. Do not add customer material or secret values to the repository.
3. Run `python3 tests/validate_parn_examples.py`.
4. Build and upload skills only in a **test copy** of Copilot.
5. Collect and review real test-environment outputs with **synthetic** samples before approving deployment.

**Release decision:** A source-controlled candidate baseline is established on a review branch, not a claim of production acceptance.
