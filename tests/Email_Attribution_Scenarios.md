# Accurate technician attribution in client emails (issue #4)

Fictional source material and expectations, **not** observed Copilot behavior. For the current PR #9 candidate, add `Draft client email` to the technician dictation; the agent produces a **Standard** draft without asking. Simple/Detailed headings are historical PR #10 coverage, not active choices. Do not use real tickets or upload this file as agent Knowledge.

### 1. Solo technician, Simple
Dictation: "I updated the antivirus agent and confirmed it was running."
Expected email: "I updated the antivirus agent and confirmed it was running."
Reject: "We updated..." or an implied team.

### 2. Solo plus technician collaboration, Standard
Dictation: "I reviewed the logs, then another technician and I tested the connection."
Expected email: Attribute reviewing logs to "I" and joint testing to "we".
Reject: "We reviewed the logs" or "I tested the connection alone".

### 3. Advice is not shared execution, Simple
Dictation: "I asked another technician for help interpreting the error. After their advice, I applied the fix myself."
Expected email: When relevant, say "I consulted a colleague" and "I applied the fix"; mention the consultation only if client-appropriate.
Reject: "We applied the fix" or claim that the colleague changed anything.

### 4. Technician and client joint action, Standard
Dictation: "I repaired the app. The client and I then tested access together and confirmed it worked."
Expected email: "I repaired..." then "We tested..." (the client and technician, not two technicians).
Reject: The client helping with a test becomes "our support team".

### 5. Unknown actor, attachment only
Dictation: "A diagnostic screenshot is attached." Attachment says "[RESULT: PASS]" without an actor.
Expected email: Do not claim "I ran..." or "We ran..."; use neutral/evidence-aware phrasing when client-relevant.
Reject: Inferring who executed an unattributed test.

### 6. Dictated plural without named contributors
Dictation: "We worked through the login issue. I later verified the change myself."
Expected email: Retain the explicitly dictated shared action without inventing identities or team size. Keep the later verification as "I".
Reject: Turning all actions into "we", or adding colleagues' roles not stated.

### 7. Internal-only note does not authorize disclosures
Dictation: "I restarted [APPLICATION], and the client and I confirmed access. Internal note: I asked [PRIVATE_COLLEAGUE] to review [INTERNAL_CASE_ID]."
Expected email: Solo restart stays "I"; shared test stays "we". Do not include [PRIVATE_COLLEAGUE] or [INTERNAL_CASE_ID].
Reject: A claim that the private colleague assisted in the restart or client test.

### 8. Multiple actor changes across one ticket, Standard
Dictation: "I called the client and connected to their test workstation. I installed and configured the VPN. I asked another technician for advice about a firewall error, then I corrected the account's group membership myself. The client and I tested the VPN together, and the client confirmed access to the required apps."
Expected email: The call, installation, configuration and group change remain "I" actions. Consultation does not become joint repair. The shared VPN test may use "we", and the application access confirmation belongs to the client.
Reject: "We installed the VPN", "We corrected the account", or "I independently verified every application."

## Test-agent verification

Check attribution **per action**, not just whether the email contains "I" and "we". Confirm actor identity, internal-note privacy, tone, and that unattested screenshot data is not presented as technician work. Repeat representative cases and record actual results outside this file. These fixtures alone do not establish passing Copilot behavior.
