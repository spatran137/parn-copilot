# Set up and test PARN Copilot Agent

Start with the [README](../README.md#set-up-the-agent) to create a test agent in Microsoft 365 Copilot Agent Builder. If you already have a working agent, save its instruction text, skill ZIPs, knowledge sources, and sharing settings somewhere private before replacing anything. Keep the test agent separate until you're happy with its output.

## Set up knowledge and research

- **Terminology.** Upload the [terminology table](../agent/knowledge/PARN_Terminology_Table.txt) under **Knowledge** if your tenant supports it. Check what the embedded file contains before sharing the agent, since Microsoft shares embedded files with users who acquire it.
- **Internal knowledge.** Upload the [internal knowledge skill](../packages/parn-internal-knowledge-review.zip) and point the agent at a small, approved SharePoint or Teams scope. Start with a fictional procedure you can recognize in the response. The skill uses access already granted in your tenant.
- **Vendor research.** Upload the [vendor research skill](../packages/it-deep-vendor-research.zip) and enable web search if permitted. Keep `references/vendor-sources.md` inside the archive. Check that the returned source is official, that the link opens, and that the advice matches your test product or version.
- **Deployment record.** Copy [config.example.yaml](../config.example.yaml) to `config.local.yaml` if you want a local checklist. Its values are examples and Copilot reads its settings from Agent Builder. Keep credentials in your approved secret store.

Microsoft documents the options in [knowledge setup](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agent-builder-add-knowledge) and [skill setup](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agent-builder-add-skills). This guide covers Microsoft 365 Copilot Agent Builder.

## Try these in Copilot

Use a fresh chat for each scenario and keep the follow-up turns together where specified. Use fictional names, screenshots, and logs. If your tenant offers **Think deeper**, select it and record it with the results.

| Check | What to look for |
| --- | --- |
| [Ticket closure and VPN](../tests/Ticket_Closure_Intent_Scenarios.md) | A pending client confirmation keeps the ticket open. Eligibility to close and a direction to close have different wording. An undecided technician gets a clarification before notes are drafted. |
| [Performed work and attachments](../tests/Performed_Evidence_Scenarios.md) | Each dictated action and result stays intact. Unattributed screenshot evidence goes into internal notes. A material conflict triggers a question. |
| [Email on demand](../tests/Client_Email_Scenarios.md) | The email block says `Not needed.` by default. An explicit request gets a Standard draft unless Simple or Detailed is specified. Cancellation restores `Not needed.` while preserving the other notes. |
| [Email attribution](../tests/Email_Attribution_Scenarios.md) | The email uses “I” for solo work, “we” for confirmed shared work, and neutral wording if the actor is unknown. |
| [Same-ticket history](../tests/Ticket_History_Continuation_Scenarios.md) | A follow-up retains earlier actions and appends the new ones. A fresh ticket starts without the previous email request. |
| Internal knowledge | An explicit request about a fictional procedure returns a relevant finding and an exact internal link in Suggested Internal Notes. A blocked lookup is described accurately. |
| Vendor research | A fictional ticket with a product and version or error produces a source-backed internal suggestion. The web query uses generic technical facts and omits customer identifiers and credentials. |

Also check that the terminology table changes prose only, with original product names or technical literals still available where required. Review generated output before using it in a real ticket and keep actual customer transcripts out of the repository.

## Check both output formats

Use the [output format live scenarios](../tests/Markdown_Output_Scenarios.md) to verify each copy control, single-section requests, and paste behavior in the intended editors. Start with `OUTPUT_FORMAT: markdown`, then switch the first line of the test agent's instructions to `OUTPUT_FORMAT: plain_text` and start a fresh chat. Run the closure scenarios against the same candidate and record the setting and actual output.

## Check the source and downloads

From the repository root, run these commands with Python 3:

```sh
python3 scripts/build-skills.py --check
python3 tests/validate_parn_examples.py
python3 tests/validate_email_rules.py
python3 tests/validate_email_attribution_rules.py
python3 tests/validate_ticket_history_rules.py
python3 tests/validate_performed_evidence_rules.py
python3 tests/validate_ticket_closure_rules.py
python3 tests/validate_markdown_output_rules.py
```

After editing a skill, run `python3 scripts/build-skills.py --refresh` and include the updated ZIP in the same change. Each ZIP has `SKILL.md` at the root, plus any listed resources. The local checks validate the source and package structure. The Copilot trials above verify upload, skill use, citations, permissions, and response quality in your tenant.

Before rolling the change out, record the repository commit, Copilot mode, date, and results from the test agent. If a check fails, fix the test agent first. If an already-published rollout needs to be rolled back, restore the saved instructions, skill packages, and configuration.
