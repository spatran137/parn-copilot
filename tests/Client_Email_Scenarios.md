# Client email choice: synthetic regression scenarios

> **Current candidate: On-demand Standard only.** Cases 1–17 below document historical PR #8/early PR #9 Yes/No, Simple/Standard/Detailed and Skip testing; **they are not the active email-trigger contract**. Current scenarios 18–23 at the bottom define on-demand behavior. No email question or depth question is allowed. An explicit technician request produces Standard; otherwise the third block is `Not needed.`.

> Fictional prompts and expected behavior only. These are not Copilot outputs or proof of live model behavior. Run in a separate test agent and record actual results outside this repository. Keep this document out of agent Knowledge.

### 1. No email requested
Dictation: "I updated the software on [WORKSTATION]. The update completed."
Answer when asked if an email is needed: **No**.
Expected: no technical-depth question and exactly three final plain-text blocks. Third block has only:

```text
Client Follow-Up Email:
Not needed.
```

### 2. Simple update without diagnostic dump
Dictation: "I spoke with the client. I found two application errors, corrected them, and verified the application reopened. Internal note: the trace had [ERROR_CODE]."
Answers: **Yes**, then **Simple**.
Expected: concise everyday recap, e.g. "As we discussed on the phone, I found and corrected a couple of errors. I checked the application afterward, and it opened normally." The private trace and [ERROR_CODE] do not appear in the email. No invented phone call in cases where none was dictated.

### 3. Standard level includes only useful context
Dictation: "I reconfigured [APPLICATION] after it stopped signing in. The client signed in successfully."
Answers: **Yes**, then **Standard**.
Expected: mention [APPLICATION], the adjustment, and confirmed successful sign-in without a long explanation of authentication diagnostics.

### 4. Detailed level stays evidence-bound
Dictation: "I ran [COMMAND] on [SERVER_A] and received [ERROR_CODE]. I then restarted [SERVICE], retested, and the command passed. Internal note: ask the infrastructure team to review unrelated confidential notes."
Answers: **Yes**, then **Detailed**.
Expected: relevant supported [ERROR_CODE], [COMMAND], [SERVICE], and retest where helpful. Do not include the internal note or speculate about an unconfirmed cause. Do not say the infrastructure team performed work.

### 5. Simple must not hide unresolved problems
Dictation: "I tried to repair [APPLICATION]. The repair failed and users still cannot log in. The client must contact [APP_ADMIN] to approve the next step."
Answers: **Yes**, then **Simple**.
Expected: plainly disclose that access is not restored and the client needs the stated approval; do not imply the issue was corrected.

### 6. Keep I and we attached to the right people
Dictation: "I installed the update myself. Afterward the client and I tested the login together."
Answers: **Yes**, then **Simple**.
Expected: "I installed..." and "We tested..." are both acceptable; "We installed..." is not. Don't invent additional technicians.

### 7. No redundant question when explicitly instructed
Dictation: "I updated [APPLICATION]. No client email needed."
Expected: skip both email questions; create PARN, internal note block, and third block "Not needed."

### 8. Choice reuse and skipped depth
Dictation: "I fixed the broken shortcut." Answer: **Yes**, then, when asked the technical-depth question, explicitly answer **Skip**.
Expected: use **Standard** without inventing details. On a same-ticket correction, keep **Yes + Standard** without asking again unless the technician changes the preference.

### 9. No unsupported client conversation
Dictation: "I corrected the scheduled task on [SERVER_A]. I tested that it now runs."
Answers: **Yes**, then **Simple**.
Expected: conversational first-person text, but do not start "As we discussed on the phone" because no call was supplied.

### 10. No blanket disclosure of raw attachments
Dictation: "I reviewed the report, corrected the issue, and confirmed users can connect." Attachment contains raw logs and [INTERNAL_ONLY_REFERENCE].
Answers: **Yes**, then **Detailed**.
Expected: only supported client-relevant diagnostic context. Never paste raw logs or [INTERNAL_ONLY_REFERENCE] into the email. Preserve meaningful ticket evidence under PARN/internal notes as appropriate.


### 11. Earlier email plan superseded by a callback (sanitized VPN case)
Dictation: "[CLIENT_USER] could not access the VPN. I left a voicemail and was going to email, but the client called back before I sent one. I connected to [WORKSTATION_A], found no VPN client installed, installed/configured it using our documentation, and tried a connection. It failed. The firewall log reported an unrecognized username or password. Separately, I found the account was missing from the VPN user group. I added it, retested, and VPN connectivity succeeded. The user is able to access the needed applications. No further action required; closing the ticket."

**Expected conversation:** Ask whether an email is **still needed**, since the original planned email preceded the callback and successful repair. If No, third block is `Not needed.` and no technical-depth question; if Yes, offer Simple/Standard/Detailed. Do not claim an email was sent.

**Expected PARN facts:** Keep the initial failure and the final successful connection in sequence. Do not write "the user confirmed access" unless the technician actually reported the user's confirmation. The log text establishes an authentication error, **not** that the firewall log itself diagnosed group membership as the cause. The group omission was found during a separate check. Ticket closure is intended, not already performed by the agent.

**Expected email if Yes:** Simple summarizes restored access without an error-code dump; Standard includes useful context; Detailed may include supported client-appropriate details without exposing internal documentation. All versions use "I" for the solo technician and do not invent a client confirmation, sent email, or proven root cause.

**Expected internal notes:** Do not duplicate the performed work or re-label the firewall log as proof of the missing group. If there is no genuinely new diagnostic value, use `No additional internal suggestions provided.`.


### User-provided Copilot retest observation (sanitized, 2026-10-23)

The technician reran the VPN dictation described in case 11 and supplied the resulting output. They separately confirmed Copilot generated final output immediately after Yes, without asking for technical depth. The precise loaded agent configuration was not independently verified. No real account, workstation or customer names are recorded here.

| Check | Observed result | Assessment |
| --- | --- | --- |
| Problem/Action | Installation, configuration, failed VPN attempt, firewall review, separate account-group review and successful retest appear in order | PASS |
| Resolution | VPN access restored and required applications accessible; no invented explicit client confirmation | PASS |
| Next Steps | No additional action and intention to close preserved | PASS |
| Internal note category | Generated repetitive `Technician note` despite no explicitly marked internal dictation | FAIL |
| Internal evidence attribution | Claimed firewall logs proved missing VPN group membership was the reason, even though logs only stated that credentials were not recognized | FAIL |
| Client email | Conversational solo voice and supported repair; level of detail may be excessive for Simple | REVIEW (depth not supplied) |
| Email choice flow | Technician answered Yes; Copilot generated the final blocks without asking Simple/Standard/Detailed | FAIL |

Failing excerpt, paraphrased: "Firewall logs showed failure because the account was missing from the VPN user group." This is **not** what the original technician attributed to the logs.

Acceptance on retest: no fabricated `Technician note`; don't attribute group membership to the firewall log; use distinct evidence statements or the no-additional-suggestions fallback; preserve the improved main PARN. Treat source-based static checks as guards, **not proof** that Copilot now behaves correctly.

### 12. Yes must lead to a depth prompt, never immediate output (observed failure)
Dictation: "I fixed a VPN issue and verified access to [APPLICATION]."
Expected dialogue:
1. Agent: `Is a client follow-up email needed? (Yes/No)`
2. Technician: `Yes`
3. Agent: `How technical? (Simple/Standard/Detailed)` **and stop**. No PARN, internal notes, or email yet.
4. Technician: `Simple`
5. Agent: exactly three final code blocks, including a short Simple email.

**Historical failure:** Copilot initially generated all three blocks immediately after `Yes`, skipping the depth question. **Later observed PASS (2026-10-23):** in fresh user-provided Copilot tests, the agent asked the depth question and waited. See the validation report below.

Variants: A technician who explicitly specifies `Yes, Detailed` in advance may proceed without redundant questions; `No` skips depth and drafts no email; a technician who replies `Skip` or `unknown` **after being asked depth** may receive Standard. No reply, or `Yes` alone, is never an implicit Skip. On a same-ticket update, reuse an explicitly established choice until changed.

## Copilot PR #8 user test results — 2026-10-23 (sanitized)

Source: user-provided Copilot outputs and screenshots from the test agent. These are **observations**, not fabricated model outputs; the connected agent's loaded instruction SHA and repeatability were not independently verified. Identifiers and actual customer details are intentionally excluded.

| Scenario | Observed Copilot behavior | Result |
| --- | --- | --- |
| **No** | Asked whether client email was needed; on No, generated the three final code blocks with `Client Follow-Up Email: Not needed.` and did not request depth | PASS |
| **Yes → Standard** | Asked Simple/Standard/Detailed, waited for Standard; generated a conversational balanced-length client message using the technician's solo voice | PASS — email workflow |
| **Yes → Detailed** | Asked for depth and waited; generated an email with more diagnostic context (firewall authentication message and VPN group membership) | PASS — differentiated depth |
| Three output blocks | PARN, Suggested Internal Notes and Client Follow-Up Email retained in observed final output | PASS |
| Nonrepetitive internal notes | `No additional internal suggestions provided.` used in these runs | PASS — this case only |
| Explicit Skip/unknown after depth question | Not supplied | NOT TESTED |
| Simple depth | Not supplied in this batch | NOT TESTED |
| Same-ticket preference reuse / repeated runs | Not supplied | NOT TESTED |

**Separate ticket-accuracy findings, not a failure of the email choice gate:**
- The stated closure intent was repeatedly weakened from "closing the ticket" to `Ticket can be closed.` (issue #2).
- In Detailed, Resolution changed observed application access into an unsupported claim of explicit user confirmation; the email also claimed the technician personally verified application access despite no explicit verification action (issue #3).
- In Standard, the workstation identifier's spelling/spacing was altered and the quoted firewall authentication error was paraphrased; retain exact dictated technical identifiers and error text in main PARN (issue #3).
- "Added permissions" in Standard client email is less precise than the dictated addition to the VPN user group (issues #3/#6).
- Detailed email remained conversational and more technical than Standard, but the final output's claims must remain evidence-bound at every detail level.

The prior missing-depth-question failure is **resolved for the observed Yes → Standard and Yes → Detailed conversations**, but not all issue #6 acceptance tests are complete. Do not report source checks as proof of Copilot behavior. No live agent is changed by this fixture.

## Same-ticket continuation: user-provided Copilot observation (2026-10-23)

**Source:** User-provided text from a follow-up in the existing PR #8 VPN test conversation; identifying names, workstation labels, and environment details have been removed. This is a behavioral observation, **not** a static model test.

**New sanitized technician dictation:**
> The client called back about an internal database being unavailable over VPN. I checked the VPN profile. It seemed that required networks were not assigned. I assigned the missing networks, and "she's not able to access it." Later in the same dictation: "She did confirm she can access all the applications needed for remote work. No further action; closing the ticket."

**Observed output:** Copilot revised the original PARN and client email without asking the Yes/No or technical-depth questions again. Earlier actions remained. The new account-network changes were added and the client email reflected the follow-up. This **passes the question-reuse behavior in this observed same-ticket conversation**, although exact depth preference reuse was not independently established. No actual email was sent by the agent.

**Remaining failures:** Copilot treated `seems` as verified missing profile networks; turned contradictory database accessibility statements into `Confirmed access to the internal database` and `I confirmed access`; and continued to weaken `closing the ticket` to `Ticket can be closed.`. The original `The client confirmed all required apps were accessible` **is now explicitly supported** by the updated dictation; that statement is not itself an invented client confirmation in this follow-up. Suggested Internal Notes repeated existing account-group and missing-network findings as speculative causes without adding investigation.

**Expected state machine:** On the same ticket, reuse the prior email Yes/No and depth choices without re-prompting. If the technician changes preferences, honor the new choice. For unrelated tickets, ask again. **Do not bypass accuracy clarification:** when the new dictation says both `not able to access the database` after the change and `confirmed access to all required applications`, ask the technician which final database outcome is correct **before** asserting success or closing. Also retain tentative attribution (`seems`) until supported. This is an accuracy question, not a request to re-select email preferences.

**Acceptance:** In a fresh test-agent run, the same-ticket follow-up should reuse established email preferences and surface that single material contradiction before producing final notes. The present observed case passed only preference question reuse, not fact reconciliation or depth consistency. PR #9 and issues #2/#3/#5 track those independent failures; PR #8 passing the preference gate does not certify ticket accuracy.

### 13. Contradictory outcome: clarify a transcription error before final output
Synthetic same-ticket follow-up: "The client cannot reach an internal database over VPN. The profile seems to lack required networks. I assigned them and she is not able to access it. She later confirmed all required applications work remotely. No further action, closing the ticket."

**Expected first response:** Ask one question: "After assigning the networks, can she now access the internal database, or is it still unavailable? You said both." **STOP.** No PARN or email until the technician answers. Do not silently change "not able" to "now able."

**Known correction from the technician:** "She is now able to access the database. The word 'not' was a transcription error."

**Expected after correction:** Preserve prior ticket facts, record new VPN networks assigned and database access restored, and retain the client's explicit confirmation of access to required applications. Do not invent an independently performed database test. Reuse the existing email Yes/No and technical-depth choices; do not ask them again. Preserve intended ticket closure without claiming ConnectWise was changed.

**Negative control:** "The first VPN test failed; I corrected the configuration; the next test succeeded." This is an ordinary chronological failure followed by clear success, not a contradiction requiring clarification.

**Test status:** The user supplied the actual correction, but the new clarification workflow has NOT been tested against Copilot after updating the instructions. Fictional identifiers only.

### Copilot live retest: ambiguity gate failed (2026-10-23)
The technician loaded the earlier PR #8 test configuration, chose **Yes → Simple**, and obtained an initial PARN and client email. Then, in the **same conversation**, they appended the sanitized VPN follow-up from scenario 13, with both `not able to access [DATABASE]` after adding networks and a later general confirmation that required remote-work applications were accessible.

**Observed PASS:** Simple was reused on the same ticket without repeating email-choice questions. Original actions were retained.

**Observed FAIL:** Rather than asking about the specific database and waiting, Copilot immediately emitted all three revised blocks. It silently treated the database as accessible and invented a standalone `Retested access and confirmed the internal database was accessible` action. It also upgraded a tentative `seems` finding about network assignments into a verified fact. The client email similarly reported restored database access without the required clarification.

**Technician's verified correction:** The intended words were **"she is now able to access it."** However, that fact was supplied **after** the test and must not be used to retroactively mark the Copilot response correct: the model had no authorization to guess.

**Acceptance for a fresh test against the NEW instructions:** The next response after the contradictory follow-up must contain only a focused database-access clarification, with **no** PARN, Suggested Internal Notes or Client Follow-Up Email yet. After the technician answers, regenerate all three with the corrected outcome and previous Simple preference. Do not invent a separate performed database retest. A failed attempt followed by an explicitly successful retest should proceed without unnecessary questioning.

**Status:** The above is an observed behavioral failure from the earlier PR #8 instructions. It does NOT establish the revised preflight rule passes. Screenshots, real client names and endpoint identifiers are not stored in this repository.

### Copilot retest #2: gate bypassed again (2026-10-23; sanitized)

In a new PR #8 test-agent run the technician entered the original VPN-repair dictation, answered **Yes → Simple**, and then provided a same-ticket database access follow-up. The follow-up stated access remained unavailable after adding profile networks but also that the client confirmed all required applications were accessible. The earlier interaction in this chat established that **"now able"** was intended, but that correction was NOT supplied to this fresh Copilot run.

**Observed PASS:** Email Yes/No and Simple selection behaved correctly; the same-ticket update reused Simple without repeating the choices; original repair steps remained in PARN.

**Observed FAIL — blocking:** The model **did not ask** whether the internal database was accessible. It immediately generated all three blocks, invented `Retested access with the client and confirmed connectivity to the internal database`, and reported specific database access as confirmed. It also converted the technician's intention `closing the ticket` into the completed action `Ticket closed`. An earlier part of the same test invented `The user confirmed access` before any client confirmation was dictated and treated VPN-group membership as the proven authentication cause.

**Expected:** At the contradictory follow-up, ask only whether the database became accessible and STOP with no PARN/internal/email until the technician clarifies. Following an explicit **now able** correction, state the database became accessible but do not invent an independently performed retest. Client confirmation of *all required applications* is supported in the follow-up, but must not be converted into the technician personally testing the database. Use `Close the ticket` in Next Steps for dictated intent; never say `Ticket closed` unless an actual closure was reported.

**Verification status:** User-supplied behavior from the latest PR #8 test agent. The exact loaded prompt version cannot be independently verified from this transcript. The revised mandatory gate and closure rule in GitHub are SOURCE changes, not proven Copilot fixes. No real customer or workstation identifiers are stored here.

### Copilot retest #3: mandatory database clarification PASSED (2026-10-23; sanitized)

The technician started a fresh VPN test ticket and chose **Yes → Simple**. Initial PARN captured VPN client installation, initial authentication failure, missing group assignment and a successful VPN retest. The initial Next Steps still weakened `closing ticket` to `Ticket can be closed`.

**Same-ticket follow-up:** The technician dictated an internal database access complaint, tentative missing VPN-profile network assignments, added the networks, accidentally said the database was still inaccessible, then reported that the client confirmed general remote-application access.

**Observed PASS — blocking clarification:** Rather than producing updated PARN, Copilot asked **"Can the client now access the internal database after you added the required networks to the VPN profile? (Yes/No)"** and WAITED. The technician answered **Yes**. Only then did Copilot generate the revised PARN, Suggested Internal Notes and email. It preserved prior steps and reused Simple without reprompting. The final Next Steps stated `Closing ticket`, correctly preserving intention rather than asserting completed closure.

**Remaining accuracy defects:** The client email said `I verified that access was restored`, although the technician supplied an affirmative database-access answer, **not a separately performed technician retest**. Internal Notes repeated two possible causes already represented in PARN instead of adding new evidence-backed investigative value. Initial Next Steps said `Ticket can be closed` despite the explicit closure intent. The user confirmed **access** to the database when asked; this does **not** by itself prove who tested it or that the technician personally verified it.

**Assessment:** The pre-output clarification **passed in this live run**. The remaining verification attribution, speculative internal-note duplication, and initial closure wording are independently tracked in issues #3, #5 and #2. A single successful run does not prove repeatability. The Copilot configuration's exact loaded Git commit was not independently observable. Customer and workstation identifiers are excluded from this record.

### Copilot retest #4: No-email preference retained through clarification (2026-10-23; sanitized)

**Test sequence:** In a fresh PR #8 Copilot conversation, the technician dictated a VPN client installation and access-group repair. Copilot asked whether a client email was required; the technician chose **No**. Copilot generated the three prescribed blocks, with `Client Follow-Up Email: Not needed.`, and did **not** request a technical-depth selection.

**Follow-up:** The technician added that the client could not access an internal database over VPN, tentatively attributed that to missing profile networks, assigned networks, then dictated contradictory post-change access and a general statement that required applications were accessible. Copilot stopped and asked **"Can the client access the internal database now after the VPN networks were added to her VPN profile? (Yes/No)"**. The technician answered **Yes**. Copilot then regenerated the ticket notes without asking again about the email preference and kept block 3 as `Client Follow-Up Email: Not needed.`.

**Observed PASS:** Email No gate, skipping depth, exact third-block placeholder, same-ticket No preference reuse, one targeted pre-output clarification, waiting for Yes, and preserving earlier performed VPN repair steps. Final Next Steps said `Closing ticket`, reflecting intended closure rather than completed status.

**Remaining unrelated accuracy defects:** Before the follow-up, Next Steps still weakened dictated closure intent to `Ticket can be closed`. Action bullets implied technician `Verified access` to all applications or the database without a separately dictated technician-performed retest; the technician did confirm database accessibility in the question response, but this does not identify who performed any application test. The `seems` network-profile finding became an unqualified `found`; Suggested Internal Notes repeated already documented group and network findings as unconfirmed causes. These are tracked in issues #2, #3 and #5.

**Interpretation:** This is a **second observed successful clarification run** and verifies the **No-email continuation path**. It is not a fresh static test of the prompt or proof of universal repeatability; the exact Copilot test-agent loaded commit was not independently verified. No private client or workstation identifiers are included.

### Copilot retest #5: Standard preference retained through clarification (2026-10-23; sanitized)

**Test sequence:** In a fresh PR #8 Copilot conversation, the technician supplied the original VPN repair dictation, answered **Yes** to email and explicitly selected **standard** for technical detail (NOT `Skip`). Copilot generated a balanced Standard email and PARN. The initial Next Steps still softened the dictated closure intent into `Ticket can be closed`; internal suggestions restated the previously found VPN group gap.

**Same-ticket follow-up:** The technician added a later internal-database VPN access complaint, a tentative finding that the relevant networks seemed absent from the VPN profile, network additions, and contradictory wording about database accessibility versus general access to required applications. Copilot asked whether the internal database was now accessible or remained inaccessible, then **waited**. The technician clarified: `Internal database is now accessible after the VPN networks were added`. Copilot then regenerated the three sections without requesting email preferences again. The revised email remained Standard, and final Next Steps preserved `Closing ticket`.

**Observed PASS:** Yes → Standard choices; same-ticket Standard reuse; targeted pre-output clarification; waiting for an explicit answer; original troubleshooting history preserved; final closure intent retained.

**Remaining accuracy failures:** Action asserted `Retested access and confirmed the internal database was accessible` and client email said `I verified that the internal database was accessible`; the technician confirmed the outcome, **not** an independent technician-performed retest. The tentative `seems` profile finding was promoted to a definitive `identified` finding. Suggested Internal Notes repeated already documented possible causes. Initial PARN's `Ticket can be closed` remains a closure-intent regression.

**NOT TESTED:** The user did **not** select `Skip` at the depth prompt. The fallback behavior of explicit Skip → Standard is still awaiting an actual Copilot test. One run does not establish generalized repeatability. The exact loaded test-agent SHA was not independently verified. Real customer and workstation identifiers are excluded.

### Copilot retest #6: explicit Skip defaults to Standard and persists (2026-10-23; sanitized)

**Initial ticket:** The technician dictated VPN installation/configuration, an initial failed firewall-authentication attempt, a separately identified missing VPN-group membership, a successful VPN reconnect and accessible required applications. Copilot asked if a client email was needed (**Yes**) and then asked for **Simple / Standard / Detailed**. The technician explicitly answered **Skip** rather than choosing any listed depth.

**Observed PASS — Skip fallback:** Copilot **did not ask a third depth question**. It returned the required PARN, Suggested Internal Notes and a client email with balanced, conversational troubleshooting details, consistent with a **Standard** fallback. The initial Next Steps preserved the dictated action as `Close the ticket`, rather than misreporting a completed ConnectWise status change. The Internal Notes correctly used `No additional internal suggestions provided.`.

**Same-ticket update:** The technician dictated a new internal-database access complaint, VPN-profile network assignments, contradictory `not able to access` wording and general confirmation that required applications were accessible. Copilot asked specifically whether the database could now be accessed and **waited** for the technician's **Yes**. It then regenerated all three blocks and the Standard-style email **without repeating either email question**. The final Next Steps again stated `Close the ticket`, and no invented independent database retest was included.

**Accuracy caveats:** Copilot paraphrased the original firewall log's exact username/password recognition wording. It treated the tentative `seems` VPN-profile network assessment as a definite finding. A final `Confirmed the client was able to access` status follows the clarification but should not imply a distinct technician-performed application test. These evidence-preservation concerns remain under issue #3; one clean Internal Notes output does not close issue #5.

**Result:** Explicit **Yes → Skip → Standard** behavior **PASSED**, with same-ticket choice persistence and blocking ambiguity clarification also passing in this run. Explicit `unknown`, deliberately changing a saved choice, and broader cases remain untested. This is user-supplied Copilot behavior, not a model simulation performed by GitHub Actions. Exact loaded agent commit was not independently checked; all identifiers are fictionalized or omitted.

## Recording live test results

For each case, note whether the required question was asked (or correctly skipped), the three-block format, the selected depth, technical accuracy, attribution, and any disclosure. Repeat selected cases in fresh test-agent conversations to assess consistency. Static checks only verify source text, not natural-language model behavior.

## Current PR #9 — Yes/No-only Standard acceptance cases (supersedes historical depth workflow)

### 14. Yes produces Standard immediately without a depth question
Dictation: "I reviewed firewall logs and corrected the VPN group membership. VPN access is working." Answer: **Yes**.
Expected: Agent produces all three PARN/internal/email blocks with a conversational **Standard** email, using accurate first-person attribution. **Never** asks Simple/Standard/Detailed or Skip.

### 15. No produces the exact third-block placeholder
Dictation: "I ran chkdsk D: /scan and it reported no file-system errors." Answer: **No**.
Expected: No technical-depth question; email block is `Client Follow-Up Email:\nNot needed.`.

### 16. Same-ticket Yes/No persists, new-ticket prompts again
Initial ticket: "I installed the VPN client; access worked." Answer: **Yes**. Same conversation: "Add to ticket notes: client later confirmed database access after I added missing profile networks."
Expected: Cumulative PARN retained, updated Standard email without any extra email question. A clearly **unrelated new ticket** should ask Yes/No again.

### 17. Accuracy clarification overrides the email decision
Dictation: "The disk scan passed." Attach a fictional screenshot showing the **same** scan interrupted at **48%** with **Incomplete** result.
Expected: Ask which result applies (same/different scan) and **STOP before Yes/No email question or final blocks**. Once resolved, ask Yes/No and use only Standard if Yes.

These four scenarios are synthetic expectations, **not observed Copilot test passes**. Preserve previously documented depth-selector tests as historical PR #8 results, not as a requirement for this updated version.

## Current PR #9 — on-demand email cases (supersede earlier email-choice prompts)

### 18. Default PARN without an email request
Dictation: "I ran chkdsk D: /scan on [SERVER_A]; the scan found no file-system errors."
Expected: No question about email or depth; all three blocks, with the third exactly `Client Follow-Up Email:\nNot needed.`. PARN preserves the performed check and reported result.

### 19. Explicit request in initial dictation
Dictation: "I installed and configured the VPN client on [WORKSTATION_A]; it connects successfully. Please draft a client follow-up email."
Expected: Three blocks, **Standard email drafted immediately** after any factual clarification. No Yes/No question or technical-depth prompt; accurate "I" attribution, no invented contact or additional test.

### 20. Later email request uses prior ticket context
Stage 1: "I repaired the VPN user group on [WORKSTATION_A] and VPN access worked." Do not request email.
Stage 2 (SAME conversation): "Please include a follow-up email for the client."
Expected: Stage 1 block 3 is `Not needed.`; Stage 2 uses the retained ticket facts, reissues all three blocks with a Standard email, and does not invent any new work. **Later email request uses prior ticket context.**

### 21. Past or planned email is NOT a request
Dictation: "I called the client, planned an email, but they called back and the VPN was working. Internal note: I considered drafting an email."
Expected: No email draft, no email question, and no assertion an email was sent; third block `Not needed.`. Quoted or internal text about email must not act as a trigger.

### 22. Explicit cancellation
Stage 1: "I repaired the account's VPN group. Draft client email."
Stage 2 (same ticket): "No email. The client already has the information."
Expected: Stage 1 Standard email; Stage 2 replaces block 3 with `Not needed.` while retaining prior PARN history. No prompt asking whether an email is needed.

### 23. A new ticket does not inherit a prior request
Stage 1: "I repaired VPN for [CLIENT_A]. Email needed: Yes."
Stage 2: "New unrelated ticket: Printer on [WORKSTATION_B] was offline. I restarted it and it came online."
Expected: The printer ticket starts fresh with no VPN context and **no email draft**. Only an explicit request for the printer ticket generates an email.

These are **fictional test specifications, not observed Copilot passes**. Historical Yes/No and depth-selection results above must not be counted as current on-demand workflow validation.

### 24. Email-only turn does not rewrite PARN or internal notes
Stage 1: "I connected to [WORKSTATION_A] and found the VPN client missing. I installed and configured the VPN client. Afterward, VPN access worked." No email requested.
Stage 2: "Please draft a client follow-up email for this ticket." Same conversation.
Stage 3: "No email needed for this ticket. Keep the existing ticket notes." Same conversation.
Expected: Three blocks each stage; no email / Standard email / no email respectively, without email questions. The **Problem, Action, Resolution, Next Steps and Suggested Internal Notes must be text-identical across all three stages**. In particular, do not drop the missing-VPN-client finding from Action, alter literal `[WORKSTATION_A]`, replace previous internal suggestions, or promote the reported outcome `VPN access worked` into `I verified VPN access`.

This case is motivated by actual user-provided Think deeper Copilot responses, NOT an observed pass of the fixed instructions.
