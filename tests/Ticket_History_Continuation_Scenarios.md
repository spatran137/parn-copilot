# Same-ticket PARN history preservation (issue #3; PR #10 pre-merge regression)

These are **fictional test fixtures**, not observed Copilot results. Use a separate test agent configured with the exact candidate instructions. Each numbered scenario starts a new conversation; stage 2 happens **in the SAME conversation** as stage 1. For tests expecting an email, explicitly include a `Draft client email` instruction in the dictation; otherwise email is not requested. The agent must not ask Yes/No or technical depth.

## 1. VPN installation followed by database callback — retain both stages

### Stage 1 dictation
I called the client and connected to their test workstation. I installed and configured the VPN. I asked another technician for advice about a firewall error, then I corrected the account's group membership myself. The client and I tested the VPN together, and the client confirmed access to the required applications. Draft client email.

### Stage 2 dictation (same conversation)
Add to ticket notes: The client called back and reported that she couldn't access an internal database. I reviewed her VPN profile and found that the required networks were missing. I added the appropriate networks, and the client confirmed she could access the database successfully. No further action required. Closing the ticket.

### Expected cumulative PARN
- Problem retains the original need for VPN access **and** the later inaccessible database.
- Action retains all original work **in order**: contact client, connect to workstation, install VPN, configure VPN, consult colleague, correct group membership, test VPN with client, client confirms application access.
- Action **appends** the later callback, profile review, missing-network finding, and network addition.
- Resolution reflects the final client-confirmed database and application access; it must not invent independent technician retesting.
- Next Steps says `Closing ticket` without claiming the ticket was already closed.
- The previously dictated **email request** persists and the style is automatically **Standard**, without questions. The updated email must describe the new issue without inventing group testing.
- **FAIL:** the updated Action has only database callback steps and silently drops earlier VPN installation/configuration/testing; or it says `Retested access with client` after the callback.

## 2. Mixed server maintenance results followed by callback — keep historical failures

### Stage 1 dictation
I ran maintenance against [SERVER_A] and [SERVER_B]. On [SERVER_A] the disk scan completed with no errors. On [SERVER_B] the WMI check failed with [EXACT_WMI_ERROR]. I will revisit [SERVER_B] tomorrow.

### Stage 2 dictation (same conversation)
Add to ticket notes: I called the site contact and confirmed [SERVER_B] remains online. I have not rerun the WMI check. I will retry it next week.

### Expected cumulative PARN
- Action retains both original checks, with [SERVER_A] success and [SERVER_B] failure/error text, then adds the call.
- Resolution does not turn [SERVER_B] WMI failure into success merely because the server is online.
- Next Steps updates the explicit plan from tomorrow to next week if the later statement supersedes it. Do not simultaneously claim both plans remain active.
- **FAIL:** only the callback survives, or the unperformed WMI retest is claimed complete.

## 3. Changed result — preserve chronology without leaving stale Resolution

### Stage 1 dictation
I installed the application, but it returned error [ERROR_A]. The issue is unresolved.

### Stage 2 dictation (same conversation)
Add to ticket notes: I corrected the configuration and tried launching the application again. It opened successfully. The client confirmed they can sign in.

### Expected cumulative PARN
- Action retains initial installation and the original error as historical evidence, plus configuration repair and successful subsequent launch.
- Resolution reflects the latest confirmed working state, NOT the earlier unresolved state.
- Do not infer that the technician personally tested the client's login.

## 4. New unrelated ticket — prevent history contamination

### Stage 1 dictation
I configured the VPN for the client. Email needed: No.

### Stage 2 dictation (separate unrelated ticket, same conversation)
New unrelated ticket: The printer is offline. I restarted the printer and it came online. Email needed: Yes.

### Expected PARN
- The new printer ticket starts fresh; no VPN actions or context leak into it.
- Explicit new-ticket `Email needed: Yes` triggers a Standard draft; `Email needed: No` suppresses one. No question is asked.

## 5. Prior notes unavailable — do not reconstruct or silently replace

### Stage 1 dictation
Start this test in a **fresh conversation with no previous ticket context**.

### Stage 2 dictation
Add to ticket notes: The database is now accessible after I added the missing networks. Keep the earlier VPN work in the ticket.

### Expected behavior
- Ask for earlier ticket notes or original actions if they are not available in context.
- Do not fabricate previous VPN installation, account group changes, old tests or client confirmations.
- Do not silently output a callback-only replacement that purports to preserve an unseen original ticket.

## Verification guidance

Evaluate the **complete revised PARN**, not just the last email. Count retained actions against both stages. A fixture passing static source checks does **not** establish that Copilot maintained conversational state in practice.
