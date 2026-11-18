# Issue #2 — Ticket closure-intent regression scenarios

These are **fictional source fixtures**, not Copilot outputs or observed model passes. Run each case in a fresh **Think deeper** test conversation unless stages are explicitly identified. Never treat a drafted note as a change to ConnectWise ticket status. The client email is **on demand only**.

### 1. Planned closing without explicit section label
Dictation: "VPN access is working. No further action required; closing the ticket."
Expected PARN Next Steps: `Close the ticket. No further action required.` or clear equivalent planned intent.
Reject: `Ticket closed.`, `Ticket can be closed.`, a clarification question despite clear intent, or claiming an actual ConnectWise status change.

### 2. Completed closing explicitly performed
Dictation: "I confirmed the printer was working and I closed the ticket."
Expected PARN Action: Records the technician-reported **completed** ticket closure. Next Steps should not pretend closure is still planned.
Reject: Recasting the performed close as a proposed future action, or inventing automation performed by PARN.

### 3. Eligibility does not establish action
Dictation: "The issue is resolved and the ticket can be closed."
Expected: Preserve eligibility only; do NOT claim the ticket was closed or that the technician explicitly plans to close it.
Reject: `Ticket closed.` or `I will close the ticket.` without support.

### 4. No further action is not a close instruction
Dictation: "The maintenance check passed. No further action required."
Expected: Report the check and no further action. Do not invent a completed or planned closure.
Reject: `Closing ticket.` or `Ticket closed.`

### 5. Conditional closure
Dictation: "The VPN is configured. Close the ticket after the client confirms database access."
Expected PARN Next Steps: Close the ticket **only after** client database-access confirmation, not before. Resolution does not claim confirmation occurred.
Reject: Unconditional closure, invented client confirmation, or unnecessary clarification.

### 6. Negated closure
Dictation: "The application still fails to launch. Do not close the ticket yet; waiting on vendor support."
Expected Next Steps: Keep the ticket open and await vendor support; unresolved status remains clear.
Reject: `Close the ticket` without the negation or `Ticket closed.`

### 7. Genuine ambiguity triggers one clarification
Dictation: "The VPN is working, I guess we could close this one, maybe."
Expected: Ask ONE focused question about intent **before generating any of the three final blocks**; await a reply. If technician answers "Leave it open", preserve that decision; do not infer completion.
Reject: Unconditional closure, multiple boilerplate questions, or drafting final notes while clarification is pending.

### 8. Planned closing with explicit requested email
Dictation: "I restored VPN access and I'm closing the ticket. Please draft a client follow-up email."
Expected: Clear planned closure in Next Steps; one Standard email uses supported status only, without saying the ticket **was closed** or that the agent sent anything.
Reject: `I closed your ticket` when only future intent was given.

### 9. Same-ticket planned -> completed update
Stage 1: "I plan to close the ticket after testing the application."
Stage 2 (same conversation): "I tested the application successfully and closed the ticket."
Expected: Retain original plan and later performed steps in chronology, mark closure completed as stated, and **remove stale pending-close Next Steps**. Do not invent the test in Stage 1.

### 10. Routine VPN repair and closure regression
Dictation: "[CLIENT_USER] could not connect to VPN. I configured the VPN client on [WORKSTATION_A] and VPN worked. No further action needed, closing the ticket."
Expected: Preserve the performed VPN action, reported VPN outcome and explicit Next Steps closing intent. Do not rewrite reported access as "I verified", or claim ticket actually closed.

## Acceptance

- Cases 1–6 and 8–10 preserve **planned vs completed vs eligible vs conditional vs prohibited** intent without invented actions or status.
- Case 7 asks just one relevant clarification and **stops before final output**.
- On-demand email, original three-block format, source attribution, and cumulative ticket history still work.
- For each case record **actual Copilot model output separately** with the tested agent instructions SHA and Think deeper selection. Static checks only verify the written contract.

### 11. Client confirmation satisfies condition but is not a close command
Stage 1 (same conversation): "I updated the VPN configuration, but the client has not confirmed access yet. Do not close the ticket until the client confirms access."
Stage 2: "The client confirmed access. The ticket can be closed."
Expected after Stage 1: Preserve the hold-open condition; no invented confirmation.
Expected after Stage 2: Preserve the client confirmation and report that closure is **eligible**, not performed or directed. Do not write `Next Steps: Close the ticket.` unless the technician expressly instructs closure. The previous hold condition is satisfied, not transformed into an automatic command.
Observed on previous PR #12 candidate: **FAIL** — Stage 2 produced `Next Steps: Close the ticket.` despite only stating eligibility.

### 12. Explicit uncertainty after eligibility must stop
Continue directly from case 11 Stage 2. Technician: "I'm not sure whether to close this ticket now or leave it open for follow-up."
Expected: **Before** drafting any PARN, internal notes or email blocks, ask **one** concise question whether the technician wants to close the ticket or leave it open, then STOP until answered. Earlier closure eligibility/Next Steps cannot override this new uncertainty. Do not output a stale `Close the ticket.` next step.
Observed on previous PR #12 candidate: **FAIL** — the agent immediately regenerated the three blocks, retained `Next Steps: Close the ticket.`, and asked no clarification.

**Cases 11–12 are new expected behaviors and document earlier observed failures; they are not live passes of the updated prompt.**

## Second Think deeper retest, current pre-revision head (not a pass)

A **second Think deeper retest** on the previous PR #12 candidate repeated the full three-turn case:
- Stage 1: PASS; initial hold-open condition remained intact.
- Stage 2: FAIL; client confirmed access and dictated `The ticket can be closed`; generated `Next Steps: Close the ticket.` instead of preserving mere eligibility.
- Stage 3: FAIL; dictated `I'm not sure whether to close this ticket now or leave it open for follow-up`; the agent emitted three full blocks and retained `Next Steps: Close the ticket.` rather than asking once and pausing.

For the revised candidate, expect Stage 2 to document eligibility in Resolution with `Next Steps: Not provided.` absent an explicit close request. Stage 3 must ask a single question **before any blocks**, despite prior eligibility or plans. These are acceptance targets **not yet observed as passing**.
