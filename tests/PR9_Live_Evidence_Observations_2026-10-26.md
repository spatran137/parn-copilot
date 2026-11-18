# PR #9 — technician-provided Copilot live test observations (2026-10-26)

**Source:** Technician copied the complete outputs from a Copilot test agent named `Parn Testing`. The model's actual prompt SHA was not independently verified. Treat these as observations, **not** static tests or repeated-proof of reliability. No real customer names, company-specific internal knowledge titles, credentials or non-fictional host identifiers are reproduced here. These observations are **not** agent Knowledge.

## Review against the ten synthetic cases

| Case | Rating | What Copilot did | Required retest or follow-up |
| --- | --- | --- | --- |
| 1. Mixed servers | PASS | Preserved [SERVER_A] completed checks and [SERVER_B] WMI failure code `0x800706BA` in Action and Resolution | Optional repeatability |
| 2. CHKDSK | PASS | Preserved `chkdsk D: /scan`, host, and exact file-system result | Optional repeatability |
| 3. Access denied | PASS | Preserved full `Get-Service` command, `Access is denied`, error code `5`, and unknown service state | Optional repeatability |
| 4. ICMP vs TCP | PARTIAL | Resolution correctly distinguished failed ping from `TcpTestSucceeded: True`, but Action omitted the failed ping observation | Require both observations in Action without fabricating a ping operator |
| 5. Screenshot-only DISM | FAIL | Agent inferred technician activity in Action (`Ran DISM...`) and email (`I ran...`) from unattributed screenshot output | Screenshot command/output must remain evidence-aware in Attachment review; don't claim an operator without dictation |
| 6. Conflicting scan screenshot | FAIL | It recognized the screenshot said `Interrupted`, `48%`, `Incomplete` despite dictation saying the scan passed; then requested email choice and finalized notes instead of asking a conflict-resolution question | Ask one specific clarification and WAIT **before** email choice or PARN/email blocks |
| 7. Launched maintenance | PASS | Launched script and results not yet returned; completion unconfirmed | Don't imply completed checks or a known running state |
| 8. Explicit internal note | PASS | Preserved `ipconfig /all`, DNS `192.0.2.53`; kept `[PRIVATE_DIAGNOSTIC_REFERENCE]` only in internal notes | Preserve privacy with technical literals |
| 9. VPN chronology | PARTIAL | Kept voicemail, callback, installation, first failure, verbatim log text, group correction, retest, and explicit closing intent; after technician answered VPN was accessible, Action said `Confirmed with [CLIENT_USER]` though direct client-confirmation conversation was not supplied | State accessibility was reported; don't manufacture a separate client confirmation or direct interaction |
| 10. Device and error literals | PARTIAL | Preserved `LAB WS 04` and exact error message. Action said `Tested VPN access after the group change`; dictation only established that access worked after the change, not an additional performed test | Describe the observed result, not a new unreported retest |

### Scope and safety notes

- Tests 1–4, 7–10 were submitted as text. Tests 5–6 involved screenshots evaluated by Copilot; the reviewer did not independently receive the original images, so image legibility is based on user-supplied Copilot output.
- The first test's client email was explicitly requested by the technician, despite the synthetic default often being No; selecting Yes does not invalidate the evidence checks.
- In case 9, internal knowledge results surfaced in Copilot. Whether those sources were actually retrieved correctly or relevant cannot be verified from this transcript alone; do not copy tenant-specific source titles to this repository.
- Static source checks verify that instructions and fixtures contain safety requirements; passing static checks does **not** mean live Copilot passed these scenarios.
- As tested, **5 PASS, 3 PARTIAL, 2 FAIL**. The separate attribution/confirmation concerns remain worth testing after any revision.

## Targeted post-fix replays

1. **Screenshot-only DISM:** A fictional screenshot containing `DISM /Online /Cleanup-Image /ScanHealth` and successful output without an actor. Ask `Please review this screenshot.` If drafting an email, explicitly choose Yes → Standard. Expected: describe `The attachment shows...` internally, not `I ran DISM` or `Ran DISM` as performed work.
2. **Contradictory screenshot:** Dictation `The disk scan passed.` + fictional screenshot with interrupted scan at 48%. Expected FIRST answer is a specific clarification, e.g., whether the image is the same scan; no email-selection or finalized notes until technician resolves the discrepancy.
3. **Ping + TCP:** `Ping to 192.0.2.10 failed. I ran Test-NetConnection 192.0.2.10 -Port 5985, which returned TcpTestSucceeded: True.` Expected: preserve both outcomes under Action and Resolution without claiming WinRM authentication or inventing who performed the ping.
4. **VPN access statement:** Reuse synthetic scenario 9. Confirm `The user can access all needed applications` does not become `I confirmed with the user` without an explicit new client interaction.
5. **No inferred second retest:** Reuse synthetic scenario 10. The source says initial testing occurred, then group correction, after which VPN access worked. Do not add a separately performed post-change test unless stated.

**Merge criterion:** All actual failed scenarios (5 and 6) must pass; partial scenarios (4, 9, 10) must preserve the source evidence without invented actors or tests. Keep this PR draft until Copilot responses are inspected.

## PR #9 follow-up: email depth removed, accuracy checks strengthened (candidate, not live-tested)

After the owner approved a simplified email flow, the current candidate asks **only Yes/No** and automatically generates a concise **Standard** email on Yes. The prior Simple/Standard/Detailed and Skip observations above remain historical. Source rules were tightened to require clarification before an email prompt when screenshots conflict with dictation; preserve both failed ping and successful TCP observations under PARN Action; keep screenshot-only command output as unattributed Attachment review evidence; and avoid turning reported VPN access into another performed retest or a direct client conversation. Re-run cases **5, 6, 4, 9 and 10** and verify Yes proceeds without a depth selection. These changes have not yet been tested in Copilot.

## Think deeper retest: cases 5 and 6 passed (2026-10-27)

**Configuration:** Copilot test agent model selection **Think deeper**, candidate source head `[ARCHIVED_CANDIDATE]` at the time of test (test-agent deployment parity not independently verified); fictional screenshots supplied to the test agent. These are user-supplied observations, not automated model passes.

- **Test 6 — PASS.** Dictation said the disk scan passed, while the fictional screenshot showed an interruption at 48% with incomplete result. Copilot **first** asked whether both statements referred to the same scan and which result was current, without first asking about email or generating ticket notes. Technician clarified: **the scan was rerun and passed the second time**. It then asked the Yes/No email question; technician replied **n**. Final Action preserved the original incomplete 48% scan and later successful rerun; Resolution reflected the second result. No fabricated first-scan success. No-email placeholder was correct.
- **Test 5 with email Yes — PASS.** Dictation was only `Please review this screenshot.` with unattributed DISM command/output. Copilot asked email Yes/No; technician answered **yes**. PARN Problem/Action/Resolution/Next Steps remained `Not provided.`, while Attachment review described what the screenshot showed. The client email used evidence-aware language (`The attached DISM ScanHealth result shows...`) and **did not** claim the technician ran DISM. Research details and tenant-specific internal document titles omitted here.
- **Test 4 — STILL PARTIAL on the preceding candidate.** In Think deeper mode, failed ping appeared in Problem and Resolution but was omitted from Action; the successful TCP 5985 result appeared in Action. This leaves the original Action-fidelity defect open. The updated PR #9 rule now explicitly requires an Action bullet for every dictated result, including failed/unattributed ping, distinct from Problem/Resolution. **Not yet behaviorally retested.**

**Attribution caveat:** These tests changed both prompt revision and model selection relative to the early Auto run; observed improvements cannot be assigned solely to one. **New Action rule modifies source after the successful cases 5 and 6; those success observations apply to the previous candidate**, not a proof the latest candidate will pass again.

## Owner-approved on-demand email flow (source change; Copilot retesting pending)

The owner approved removing the email Yes/No question. **Default no email** with third-block `Not needed.`; draft a Standard email only on an explicit technician instruction, including a same-ticket request after notes were initially generated. Previous Yes/No, Simple/Standard/Detailed and Skip test observations are **historical** and must not be interpreted as passes of the on-demand workflow. Current live acceptance cases are 18–23 in `tests/Client_Email_Scenarios.md`. No Copilot behavior for this new flow has yet been demonstrated.

## Think deeper retest: final on-demand email stages and network evidence (2026-10-28)

The technician ran two test cases with the PR #9 on-demand candidate, using **Think deeper** (exact test-agent instructions not independently verified). The following are user-provided Copilot outputs, not automated model validation.

- **Email workflow stages 1–3: PASS on trigger/cancel, PARTIAL on documentation fidelity.** Initial VPN ticket produced three sections with third `Not needed.` and no email question. A later explicit `Please draft a client follow-up email for this ticket` generated a concise Standard email without another question. Later `No email needed` restored `Not needed.` without asking. However the email-only revision **dropped the finding that the VPN client was missing from Action**, replaced the earlier case-specific internal note with `No additional internal suggestions provided`, and reintroduced the earlier version upon email cancellation. The first and last outputs **changed the supplied outcome** `VPN access worked` to `Verified that VPN access worked`, suggesting an unreported technician verification action. They also dropped brackets around `[WORKSTATION_A]` in two versions, although the email-request version preserved them. The stage 1 Problem inferred that the missing client caused VPN unavailability, more causal specificity than dictated. A targeted source instruction now requires email-only changes to preserve PARN/internal blocks verbatim and explicitly rejects `VPN worked` → `I verified`. **Not behaviorally retested.**
- **Network evidence test 4: PASS.** Dictation supplied a failed ping to `192.0.2.10` and a performed `Test-NetConnection 192.0.2.10 -Port 5985` returning `TcpTestSucceeded: True`. Both results now appear as separate Action bullets, with accurate Resolution; no WinRM authentication inference. No email was requested; third block correctly read `Not needed.`.

**Merge gate:** Do not treat successful email generation/cancellation as complete preservation of the original ticket notes. After the targeted source fix, rerun the **three-stage email-only fixture** above and compare all non-email blocks for exact equality. Existing screenshot and conflict tests previously passed on an earlier candidate, but those results do not establish repeatability on this new head.
