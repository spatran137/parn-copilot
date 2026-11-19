# Output format live regression scenarios

Use a separate Microsoft Copilot test agent in **Think deeper** with the candidate instructions and the existing approved knowledge and skills. Start a new conversation for each numbered case. Keep messages in the same conversation when a case has multiple turns. Record the tested commit, configuration, actual output, and pass, fail, or blocked status using synthetic data only.

## Markdown mode

Leave the first instruction line set to `OUTPUT_FORMAT: markdown` for cases 1–7.

- A full response has `## PARN Note`, `## Suggested Internal Notes`, and `## Client Follow-Up Email` in that order. PARN uses `### Problem`, `### Action`, `### Resolution`, and `### Next Steps` in order, with ordered-in-time `- ` Action bullets.
- Explicit single-output requests show only that deliverable. A request to include a draft still returns all three sections.
- Each deliverable has its own Markdown code block and copy control. Copilot may render a preview inside a block. Headings rendered directly in the chat without a dedicated copy control fail, as does a single combined code block. The full response, including fences, stays within 8,000 characters.
- Use each block’s Copy control and paste into a plain-text editor first. Expect the Markdown source, including heading markers, without the outer fences or other sections. If Copilot offers **Show code**, try Copy in the default view first, then switch to **Show code** and repeat. Record which view gives you literal headings and list markers. If only **Show code** works, record the extra step. If neither view works, mark the copy check as failed.
- Preview the copied PARN and internal notes in a test ConnectWise ticket and a Teams draft. Paste the email subject and body into their fields in an unsent draft. Record the Copilot surface, whether each block copied independently, and how each destination handled line breaks and literal evidence.

## 1. Resolved ticket and PARN-only output

> The user reported their label printer was offline. I reconnected its loose USB cable and printed a test label successfully. The printer worked afterward. No further action is needed.

Expect all three sections immediately. A closure question fails this case. Action captures the cable reconnection and the successful test print. Resolution records restored printing. Next Steps may report that no further action is needed. It must not imply closure. The email section says `Not needed.` without a question.

Then send:

> Return only the PARN Note for this ticket.

Expect one copyable code block with the same four headings and facts. The copied source starts with `## PARN Note` and includes `### Action` and its `- ` bullets. If other sections appear, record which headings appeared in chat and which came through Copy. For a direct comparison, run the initial prompt in both production and the test agent and record which views expose independent copy controls.

In one reported test run, the initial printer prompt triggered `Close ticket or leave open?`. An explicit `close` reply then produced planned closure, and the single-section follow-up displayed only PARN. Repeat the original prompt in a fresh chat and confirm it drafts immediately. Verify Copy separately.

## 2. VPN closure and clarification

Send each message in sequence:

1. “I updated the VPN configuration. The client has not confirmed access. Do not close the ticket until the client confirms access.”
2. “The client confirmed access. The ticket can be closed.”
3. “I'm not sure whether to close this ticket now or leave it open for follow-up.”
4. “Close it.”
5. “I closed the ticket.”

Expect Next Steps to retain the hold in turn 1. Turn 2 records the client's confirmation and eligibility in Resolution. Next Steps is `Not provided.` Turn 3 returns only `Close ticket or leave open?` without a heading. Turn 4 puts planned closure in Next Steps. Turn 5 records the reported completed closure in Action and clears the stale plan. All final outputs retain prior performed work. No turn claims the agent closed the ticket, invents a retest, or drafts an unsolicited email.

Also rerun the remaining [closure-intent scenarios](Ticket_Closure_Intent_Scenarios.md) against this candidate for negative, conditional, and unambiguous planned closure.

## 3. App repair with a command and multiline logs

Paste this entire prompt:

~~~text
LedgerDesk 3.2 would not launch on LAB-WS04. I ran Repair-App -Name LedgerDesk -Mode Repair on LAB-WS04. The repair returned exit code 0, and I reopened LedgerDesk successfully. Include these exact log lines in Suggested Internal Notes as repair evidence:
08:00:01 [INFO] Component=LedgerDesk_Core
08:00:02 [WARN] Cache entry <missing>; rebuilt
~~~

Expect Action to retain the exact command in inline code, device, version, result and subsequent retest. Expect the exact multiline log inside a tilde fence in the copied Suggested Internal Notes Markdown. The inner fence must stay intact and the outer block must remain copyable. Verify that `<missing>` is literal evidence, underscores survive, no raw logs appear in PARN or email, and no client confirmation is invented.

The fence must contain exactly two lines. Keep exit code 0 in Action because it was stated in prose. Adding a third log line for that result fails this test, even if a previous conversation used a longer excerpt.


### Test 3 control

Start a new conversation with the same agent instructions and paste:

~~~text
AsterDesk 4.1 would not launch on LAB-WS19. I ran Repair-App -Name AsterDesk -Mode Repair on LAB-WS19. It returned exit code 0, and I reopened AsterDesk successfully. Copy these two exact lines into Suggested Internal Notes as repair evidence:
14:27:51 [INFO] Component=AsterDesk_Shell
14:27:56 [WARN] Slot <blank>; rebuilt
~~~

Expect exactly those two lines, in order, inside the fence and exit code 0 in Action. If any line is added, record it verbatim alongside the loaded instruction revision.

## 4. Evidence-heavy internal-only output

Create a screenshot of this synthetic Portainer display with the three lines visible:

```text
Container: lab-web_01
Image: lab/web:2.4
Health: unhealthy
```

Attach the screenshot with this message:

> The lab demo web app timed out once. I reviewed the attached Portainer screenshot but have not run any tests, restarted anything, or identified a cause. Return only Suggested Internal Notes. Suggest one next check based on the screenshot.

Expect just the internal heading with readable evidence and exact identifiers. It should connect the timeout and unhealthy state as observations, offer a case-specific check clearly marked not performed, and avoid inventing what caused the timeout or who ran a command. If the screenshot is unreadable, it should say which evidence cannot be verified.

## 5. On-demand email, three detail levels and attribution

Start with:

> LedgerDesk 3.2 did not start on the client's test workstation. I checked the LedgerDesk service and found it stopped. A coworker suggested starting it, and I started it myself. My coworker and I then opened the app together and verified that it loaded. The client has not verified access yet. Next step is for the client to try it and let me know if it still fails. Internal note: LAB-CASE-04 is our tracking reference. I previously emailed the client about the appointment.

Expect `Not needed.` with no email question. Send each follow-up in sequence:

| Prompt | Expected |
| --- | --- |
| Please draft a client follow-up email for this ticket. | Full response with a Standard draft using the prior facts. PARN and internal text stay identical. |
| Return only a Simple client follow-up email for this ticket. | Email section only. Plain language explains the work and requests client verification. |
| Return only a Standard client follow-up email for this ticket. | Email section only. Natural work, outcome, and follow-up paragraphs with enough context for the client. |
| Return only a Detailed client follow-up email for this ticket. | Email section only. Mention the supplied LedgerDesk 3.2 service finding and what was tested. Keep client verification pending. |
| The client confirmed LedgerDesk opened. Update the ticket. | Full response. Detailed email preference carries forward. Capture client confirmation without inventing a new technician retest. |
| Return only a Standard client follow-up email again. | Email section only. Explicit Standard replaces the retained Detailed preference. |
| No email for this ticket. Keep the existing notes. | Full response. Email says `Not needed.`; other sections are unchanged. |
| New unrelated ticket. I replaced a faulty mouse and verified the replacement worked. | Fresh PARN and internal sections with no carryover; email says `Not needed.`. |

At every level, use `I` for the solo service check and start. If the shared verification is mentioned in first person, use `we` for that action. A coworker's suggestion alone never makes the start joint work. Exclude the internal reference, raw logs, greetings, signatures, and any claim the agent sent a message. Drafts use a plain subject line and natural paragraphs. Bullets are optional. The copyable code block is the only fence for email.

## 6. Named-resource ambiguity gate

> The client could not access the payroll database. I later heard all apps were accessible. Return only the PARN Note.

Expect one question asking whether the payroll database can be accessed now, with no final headings. Reply “Yes, the client confirmed access to the payroll database.” Expect just the requested PARN section with accurate confirmation and no invented retest or closure.

## 7. Internal knowledge and vendor research

With an authorized synthetic SharePoint test procedure titled **PARN Lab VPN Runbook** and a known test item URL, send:

> The fictional LAB-VPN endpoint stopped connecting after a client update. Check authorized internal knowledge for PARN Lab VPN Runbook. Return only Suggested Internal Notes.

Expect a relevant finding with exact returned title and accessible URL inside the internal section. If lookup fails or is unavailable, expect a truthful limitation with no fabricated result. Verify against the actual item and record any available invocation evidence separately.

In a new conversation, send:

> On a fictional Windows test workstation, Windows Update reported 0x80070002. I have not tried a fix. Look up official Microsoft guidance and include the findings with the PARN response. Draft a Standard client follow-up email.

Expect a verified, relevant official source and any proposed steps labeled not performed in the internal section. PARN and email use only ticket facts. If approved web access is unavailable or no official source can be verified, record the outcome rather than scoring retrieval as passed. [Issue #2](https://github.com/spatran137/parn-copilot/issues/2) covers broader knowledge and skill validation.

## 8. Plain-text mode

In the test agent's Instructions, change only the first line to `OUTPUT_FORMAT: plain_text` and save. Start a fresh chat for each rerun.

| Rerun | What to check after Copy |
| --- | --- |
| Case 1, full response and PARN only | The full response has three independent blocks. The follow-up has one. The PARN block starts with `PARN Note:` and has `Problem:`, `Action:`, `Resolution:`, and `Next Steps:`, with `- ` Action bullets. The no-email block says `Not needed.` |
| Case 3, app repair | The command is literal and the two supplied log lines keep their exact characters, order, and line breaks inside Suggested Internal Notes. |
| Case 5, requested email | Copy a Standard draft and an email-only reply. The email retains the subject line, paragraph breaks, and I/we attribution. |
| Case 6, access clarification | The question appears by itself. After the reply, only the PARN block appears, still in plain text. |

Paste into a plain-text editor and then the intended ticket or email editor. Check that copied blocks have no added Markdown heading markers, inline backticks, inner fences, or escapes. Keep any punctuation that is part of supplied evidence. Record the Copilot surface and the result for each editor.
