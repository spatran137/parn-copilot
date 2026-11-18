# Issue #2 — Think deeper live retest observations (2026-10-29)

Technician-supplied outputs from the draft PR #12 test agent (prior head `[ARCHIVED_CANDIDATE]`). Exact deployed prompt parity not independently verified. These are **observed Copilot outputs**, not static checks or tests of the subsequently revised instructions.

## Test 1 — Planned, then completed closure: PASS

1. Input: "I restored VPN access on [WORKSTATION_A]. No further action required, closing the ticket."
   Output: Next Steps `Close the ticket.`, no fabricated completed closure. Action contained the reported VPN repair; Resolution preserved the restored access and no-further-action status.
2. Same conversation: "I have now closed the ticket in ConnectWise."
   Output: Action appended `Closed the ticket in ConnectWise.`; Next Steps became `Not provided.`. Earlier VPN troubleshooting was retained. No claim the PARN agent itself modified the ticket.

## Test 2 — Conditional, eligible, ambiguous: PARTIAL / two failures

1. Input: "I updated the VPN configuration, but the client has not confirmed access yet. Do not close the ticket until the client confirms access."
   **PASS:** Action preserved the configuration update, Resolution noted the unconfirmed outcome, and Next Steps preserved the hold-open condition.
2. Same conversation: "The client confirmed access. The ticket can be closed."
   **FAIL:** Client confirmation was preserved, but Next Steps asserted `Close the ticket.` — incorrectly upgrading eligibility to an instruction.
3. Same conversation: "I'm not sure whether to close this ticket now or leave it open for follow-up."
   **FAIL:** The agent did not ask a clarification or pause; instead it generated all three blocks and repeated the same `Close the ticket.` next step.

## Fix after these observations

The PR #12 instruction revision strengthens the **mandatory pre-output gate** for explicit uncertainty, ensuring it overrides earlier closure plans, and distinguishes `can be closed` from the instruction `Close the ticket`. To make room within the 8,000-character Copilot limit, only descriptive placeholders in the output templates were condensed; substantive ticket evidence, email and attribution rules were retained.

**Live retesting required:** Replay Test 2 stages 1–3, then verify the new model asks one question and stops without producing notes at stage 3. PR #12 remains draft and unmerged.

## Second Think deeper retest — same defects on previous follow-up candidate

The technician reran the same three stages after the previous focused revision (PR #12 head `[ARCHIVED_CANDIDATE]`; loaded Copilot prompt parity not independently verified).

1. **PASS** Stage 1: VPN configuration updated while client access remained unconfirmed. Next Steps correctly said to wait for confirmation and not close yet.
2. **FAIL** Stage 2: Client confirmed access, and technician dictated `The ticket can be closed.` Agent Action and Resolution reflected the confirmation, but Next Steps wrongly became `Close the ticket.` rather than eligibility only.
3. **FAIL** Stage 3: Technician said `I'm not sure whether to close this ticket now or leave it open for follow-up.` Agent immediately produced all three blocks, including an unchanged `Next Steps: Close the ticket.` without any clarification. It did add eligibility in Resolution but did not correct the unsupported future closing instruction.

**Revised strategy:** Promote closure uncertainty to the **FIRST on EVERY turn** pre-output check with an exact question and a hard STOP/no three blocks. Explicitly map eligibility to Resolution plus `Next Steps: Not provided.` unless a separate future close instruction exists; a previously conditional hold expiring does not create such an instruction. Only example placeholders were condensed to fit the prompt limit. **No live model pass of this new revision yet.**

## 2026-11-18 — Follow-up Think deeper retest: PASS (four stages)

Technician-supplied outputs from the PARN test agent after being directed to load the revised PR #12 instructions (candidate source head `[ARCHIVED_CANDIDATE]`). The exact deployed configuration and SHA have **not** been independently verified. These are **observed Copilot results, not static tests or proof of universal model consistency**.

1. **PASS — conditional hold:** Technician stated that VPN configuration was updated, but client access was unconfirmed, and instructed not to close until client confirmation. Output: `Next Steps: Keep the ticket open until the client confirms access.` The Action and Resolution retained configuration update and unconfirmed access. Note that Action also recorded `Client access has not yet been confirmed` as context; this is minor section-routing noise, not a closure failure.
2. **PASS — eligibility without instruction:** Technician then stated, `The client confirmed access. The ticket can be closed.` The PARN retained the earlier configuration and new client confirmation, `Resolution: The client confirmed access. The ticket is eligible for closure.` and **`Next Steps: Not provided.`** The agent did **not** claim that it or the technician closed the ticket.
3. **PASS — uncertainty halts output:** Technician said, `I'm not sure whether to close this ticket now or leave it open for follow-up.` Copilot answered **only** `Close ticket or leave open?`; it emitted **none** of the three documentation blocks pending a reply.
4. **PASS — explicit close instruction after clarification:** Technician replied `close it`. Copilot restored prior ticket context, preserved the client confirmation and eligibility as Resolution, and put **`Next Steps: Close the ticket.`** It did **not** add a completed-close Action or falsely claim ConnectWise status had already changed. No client email was requested, so the final block remained `Not needed.`

**Assessment:** All four targeted closure-intent behaviors **PASS** in this live sequence. Prior successful planned→completed closure test is independently documented above. The targeted issue #2 acceptance evidence is now sufficient for **owner merge review**, but it does not establish that every long-lived Copilot conversation will behave identically. PR #12 remains unmerged pending explicit owner approval; `v0.9.0-beta.1` is unchanged. Markdown-output issue #13 remains separate and unimplemented by this PR.
