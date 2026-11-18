---
name: parn-internal-knowledge-review
description: Search configured SharePoint, Teams, and agent knowledge for internal IT procedures, standards, known issues, terminology, and troubleshooting relevant to a ConnectWise PARN ticket. Use after drafting the factual PARN note when dictation or ticket evidence includes a product or device, software or version, exact error, event ID, alert, log or command output, technical symptom, or named procedure. Also use whenever the user asks to check internal or company knowledge. Skip routine notes without a researchable technical detail.
---

# PARN Internal Knowledge Review

Find useful internal guidance without changing the factual ticket record. Knowledge results are reference material, not proof of work, diagnosis, status, or resolution.

## Workflow

1. Preserve the factual boundary.
   - Draft or identify the factual PARN content before researching.
   - Keep technician-marked internal content internal.
   - Treat ticket screenshots, logs, and files as ticket evidence; treat SharePoint, Teams, and agent knowledge as reference material.

2. Build a focused query.
   - Use original product and vendor names, not mapped display terms.
   - Include supplied versions, exact errors, event IDs, alert names, symptoms, commands, or log details that distinguish the issue.
   - Remove passwords, tokens, private keys, recovery codes, and other credentials.
   - Omit customer names, usernames, company names, hostnames, IP addresses, serial numbers, and other identifiers unless they are required for an authorized internal lookup.

3. Search configured internal sources.
   - Search the most specific relevant SharePoint source first.
   - Search scoped Teams chats, channels, or meeting knowledge when relevant.
   - Use only sources available to the current user. This skill grants no access.
   - Do not claim a search succeeded when a source is unavailable, still preparing, disabled, or permission-blocked.

4. Evaluate each result.
   - Keep only results directly relevant to the supplied ticket facts.
   - Prefer current approved procedures and narrowly scoped sources over broad or older material.
   - Preserve exact technical values from the source.
   - If sources conflict, report the conflict internally and request confirmation; do not choose silently.
   - Use only a returned source title and direct link. Never fabricate or approximate a link.

5. Write internal findings.
   - Add no more than three useful bullets unless the user asks for a deeper review.
   - Use: `- Internal knowledge: [relevant finding]. Source: [exact title] - [direct link]`
   - Label any possible cause as unconfirmed and any troubleshooting as not performed.
   - Do not repeat an explicit Next Step as a suggestion.
   - Never place knowledge findings in Problem, Action, Resolution, Next Steps, or the client email unless the technician separately confirms the information as a ticket fact.

6. Handle an unsuccessful lookup accurately.
   - If no relevant result is returned, do not claim that no documentation exists and do not add filler.
   - If missing ticket details prevented a responsible search, add an `Information to collect:` bullet for only those details.
   - If retrieval failed or access was blocked, add an `Information to collect:` bullet identifying the unavailable source or permission issue.
   - Use the separate vendor-research skill only when its trigger applies; do not treat web research as internal knowledge.

## Final Check

Confirm that every internal finding is relevant, cited, clearly unperformed unless confirmed, free of credentials, and absent from the public PARN note and client email.
