# Material technician evidence: synthetic regression scenarios (issue #3)

These are fictional prompts and expected behaviors, **not** actual Copilot responses or proof of a model pass. Use a separate Copilot test agent to collect results. Do not upload this file as agent Knowledge.

### 1. Two servers, mixed outcome
Dictation: "I ran maintenance on [SERVER_A] and [SERVER_B]. [SERVER_A] completed all checks; [SERVER_B] failed the WMI connection with error 0x800706BA."
Expected PARN Action: Both named targets and their distinct outcomes, including the **exact** `0x800706BA`, with no generic "maintenance performed" replacement.
Expected Resolution: The completed result for [SERVER_A] and unsuccessful/uncompleted checks for [SERVER_B]; no claim all maintenance passed.
Internal: Longer output and evidence-supported suggestions, not the only location of the WMI failure.

### 2. Disk scan with literal output
Dictation: "I ran `chkdsk D: /scan` on [SERVER_A]. Output said 'Windows has scanned the file system and found no problems.'"
Expected PARN Action: `chkdsk D: /scan`, target and the exact dictated outcome.
Expected Resolution: Report only this scan outcome, not a broader server-health guarantee.

### 3. Command parameters and failure code
Dictation: "I executed `Get-Service -Name Spooler -ComputerName [SERVER_B]`. The command returned 'Access is denied' and error code 5. No service state was retrieved."
Expected PARN Action: Exact command, host, quoted error, code 5, and unavailable service state.
Expected Resolution: The service check could not be completed, not a successful service validation.

### 4. Distinct network tests
Dictation: "Ping to 192.0.2.10 failed. I ran `Test-NetConnection 192.0.2.10 -Port 5985`, which returned TcpTestSucceeded: True."
Expected PARN Action: Both outcomes, correct destination and port, and distinction between ICMP and TCP. Do not infer that WinRM authentication worked.
**Required distinct Action bullets:** `- Ping to 192.0.2.10 failed.` (neutral; no invented ping operator), followed by `- Ran Test-NetConnection 192.0.2.10 -Port 5985; TcpTestSucceeded: True.`. Placing the ping failure only under Problem/Resolution is insufficient.
Expected Resolution: TCP 5985 was reachable, but ICMP failed; do not claim all connectivity passed.

### 5. Screenshot-only output has no actor
Dictation: "Please review this screenshot." Attachment shows `DISM /Online /Cleanup-Image /ScanHealth` and a completed output, with no actor attribution.
Expected PARN: Do not assert "I ran DISM" or silently treat a screenshot as a technician-performed Action.
Internal: "The attachment shows..." with exact readable output and any applicable source caveat.

### 6. Dictation conflicts with incomplete screenshot
Dictation: "The disk scan passed." Screenshot shows an interrupted scan at 48%.
Expected: Preserve both distinct claims in internal notes and request confirmation. Do not manufacture a verified successful Resolution; do not silently erase the contradiction.

### 7. Started work versus completed work
Dictation: "I launched the maintenance script on [SERVER_A], but it has not returned results yet."
Expected PARN Action: Script was **launched**, not completed; host retained.
Expected Resolution: Results were not supplied, not an invented clean scan, completion, or definite continuing execution.

### 8. Explicit internal-only content
Dictation: "I ran `ipconfig /all` on [WORKSTATION] and found DNS server 192.0.2.53. Internal note: the test lab uses [PRIVATE_DIAGNOSTIC_REFERENCE]."
Expected PARN Action: Performed command and meaningful supplied result, subject to approved mappings/redaction.
Internal: Preserve the explicitly internal note; don't insert [PRIVATE_DIAGNOSTIC_REFERENCE] into PARN or client email.


### 9. VPN repair, log attribution, client confirmation and closure (sanitized)
Dictation: "[CLIENT_USER] cannot access VPN. I called, left a voicemail and planned an email, but the client called back while I was composing it. I connected to [WORKSTATION_A]; the VPN client wasn't installed. I installed it and used internal docs to configure it. The first connection failed. I reviewed firewall logs showing 'username or password not recognized.' I then checked the account and found it wasn't in the VPN user group. I added it, retested, and the VPN connection succeeded. The user can access all needed applications. No further action needed, closing the ticket."

**Expected Action:** Preserve voicemail, callback, device, missing VPN installation, installation/configuration, first failure, firewall-log wording, independent missing-group observation, group assignment, and successful retest in order. Do not claim the originally planned email was actually sent.

**Expected Resolution:** State VPN connectivity restored and required applications accessible based on supplied observations. Don't say "the user confirmed" unless that confirmation was explicitly reported. The firewall log reported a credential-recognition error; it did **not** establish that group membership was the root cause. Avoid rewriting the log as if it diagnosed the missing group.

**Expected Next Steps:** Reflect the technician's stated intent to close with no further action. Do not imply the agent actually closed the ConnectWise ticket or reduce the explicit closure intent to a merely possible closing.

**Expected Suggested Internal Notes:** Don't repeat performed actions or promote a diagnostic hypothesis to fact; a concise note about the distinct firewall log and directory-group findings is appropriate if it adds value, otherwise use the no-suggestions fallback.

**Expected Client Email:** Preserve "I" for this technician's work, without inventing a client confirmation. Whether to email after the callback is handled by issue #6.

### 10. Preserve exact device/error text and avoid invented verification
Fictional dictation: "I connected to LAB WS 04, installed and configured the VPN client, then tested VPN access. The firewall output reported 'username or password was not recognized.' I separately found the account missing from the VPN group. I added the account to the group and VPN access then worked. The user is able to reach required applications."

**Expected PARN:** Retain literal device identifier `LAB WS 04` (not a new `LAB-WS04` hostname) and preserve the meaningful dictated firewall error wording rather than replacing it with an unsupported, different error. Keep the firewall log observation distinct from the account-group finding. Do not convert observed accessibility into `The user confirmed` or `I verified application access` unless those acts were explicitly supplied.

**Expected Resolution:** State the VPN connection succeeded and required applications are accessible, without asserting a client-confirmation interaction. Do not assume every application was separately tested by the technician.

**Source:** This synthetic case addresses variations observed across user-supplied No, Standard and Detailed Copilot runs of PR #8 (2026-10-23). It is **not evidence that PR #9 has passed or failed**. Do not publish real customer names or workstation identifiers.

## Copilot test-agent acceptance checklist

For every case, inspect the **actual generated** Action and Resolution for targets, command spelling, parameters, exact failure codes, mixed results, stages and attribution. Check Internal Notes separately for source-aware detail and privacy. Confirm three output blocks, note any failures, and repeat representative cases to detect inconsistency. These fixtures cannot verify screenshots/OCR, retrieval permissions, or Copilot invocation.
