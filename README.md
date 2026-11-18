# PARN Copilot Agent

> **Beta.** PARN is still a work in progress. You may run into rough edges, especially with screenshots, follow-up replies, or the way Copilot formats your notes. Thanks for trying it and for being patient while I work through those issues. Give every draft a quick read before you paste it into a ticket or email. If something looks off, open an issue with a fictional example that shows what happened.

I built PARN for the part of an IT ticket that comes after the troubleshooting. You can dictate what happened, add a screenshot if it helps, and get a draft you can review and paste into ConnectWise. PARN stands for **Problem, Action, Resolution, and Next Steps**.

The agent drafts three copy-ready blocks:

- **PARN Note** records what was reported, what you did, what you confirmed, and what still needs to happen.
- **Suggested Internal Notes** captures useful attachment details, source links, and ideas you haven't tested yet.
- **Client Follow-Up Email** gives you a subject and body when you ask for a draft. Otherwise it says `Not needed.`

You review the output, then copy it into your ticket or email. There's no ConnectWise integration to install.

## What you'll need

- Microsoft 365 Copilot with access to **Agent Builder**. Look for **Skills** on the **Configure** tab if you plan to upload the research skills.
- Permission to use any SharePoint or Teams sources you add. Your Microsoft 365 licensing and tenant policy determine which knowledge features are available.
- A fictional ticket to try first. You can start documenting tickets before connecting internal knowledge or turning on web search.

## Set up the agent

1. In Microsoft 365 Copilot, choose **New agent** and **Skip to configure**. Name it **PARN Copilot Agent**.
2. Open the [agent instructions](agent/ConnectWise_PARN_Agent_Instructions_Condensed.md), select **Raw**, and paste the entire text into **Instructions**.
3. Under **Knowledge**, upload the [terminology table](agent/knowledge/PARN_Terminology_Table.txt) if your tenant supports embedded files. Review the table first. It maps SentinelOne to “antivirus” in prose. If your team uses different terms, adjust the table before uploading it.
4. Under **Skills**, choose **Add** and upload the ZIPs you want to use, one at a time. On GitHub, open each ZIP and select **Download raw file**. Upload the ZIP as downloaded.

   | Skill ZIP | What to configure |
   | --- | --- |
   | [parn-internal-knowledge-review.zip](packages/parn-internal-knowledge-review.zip) | Add the SharePoint or Teams sources your audience is allowed to use. |
   | [it-deep-vendor-research.zip](packages/it-deep-vendor-research.zip) | Enable web search if your tenant allows it. The skill ships with a list of official vendor sources. |

5. Open **Try it** and run the example below. If **Think deeper** is available, use it for testing. If Skills isn't available, try the basic drafting flow and leave the research checks for a tenant with skill support.

For the Microsoft screens and tenant options, see [Agent Builder setup](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agent-builder-build-agents), [knowledge sources](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agent-builder-add-knowledge), and [skill upload](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agent-builder-add-skills).

## Try it with a ticket

Paste this into a fresh conversation:

> The user reported that the label printer was offline. I reconnected the loose USB cable and printed a test label successfully. The printer worked afterward. No further action is needed.

Check that **Action** includes the cable reconnection and test print, **Resolution** reflects the working printer, and **Client Follow-Up Email** says `Not needed.` In the same conversation, say `Please draft a client follow-up email for this ticket.` The agent should now draft an email in the technician's voice and preserve the notes it already wrote. Start a fresh conversation for an unrelated ticket.

Use `Internal note:` for one technician-only thought. Put longer private dictation between `Begin internal section:` and `End internal section:`. Review those boundaries before pasting anything into a customer-facing field. If the client still needs to confirm VPN access, say so and give the next step explicitly.

## Test or update an install

- [Deployment and validation guide](docs/DEPLOYMENT_AND_VALIDATION.md) covers testing skills, deciding what to share, and backing up an existing agent.
- [Ticket scenarios](tests/Ticket_Closure_Intent_Scenarios.md) and [email scenarios](tests/Client_Email_Scenarios.md) give you more prompts to try.
- [Latest public beta](https://github.com/spatran137/parn-copilot/releases/tag/v0.9.0-beta.2) has both skill ZIPs ready to download. Get the instructions, terminology table, and ZIPs from the same revision when setting up a new agent.

If you're editing a skill, change its source under [skills](skills/). Run `python3 scripts/build-skills.py` to build both ZIPs into `dist/`. Maintainers can run `python3 scripts/build-skills.py --refresh` to update the checked-in downloads and `python3 scripts/build-skills.py --check` to verify them. The packaging script uses Python's standard library.

Use fictional data in examples and bug reports. Keep customer tickets, screenshots, credentials, and tenant configuration in your approved systems. [config.example.yaml](config.example.yaml) is a reference checklist for your installation.

## License

PARN is available under the [MIT License](LICENSE).
