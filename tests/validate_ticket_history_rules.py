"""Static contract checks for cumulative same-ticket PARN history; not a Copilot evaluation."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
prompt = (root / "agent" / "ConnectWise_PARN_Agent_Instructions_Condensed.md").read_text()
cases = (root / "tests" / "Ticket_History_Continuation_Scenarios.md").read_text()
workflow = prompt.split("# Workflow and Follow-Up", 1)[-1]
checks = {
    "Prompt within 8000 LF": len(prompt) <= 8000,
    "Prompt within 8000 CRLF": len(prompt.replace("\n", "\r\n")) <= 8000,
    "Same-ticket retention explicitly required": "Same ticket:" in workflow and "prior Problem" in workflow,
    "All earlier action/results retained": "every Action/result" in workflow,
    "Prior internal notes retained": "internal notes" in workflow,
    "Chronological append": "append new steps in order" in workflow,
    "Resolution and next steps updated": "Update Resolution/Next Steps" in workflow,
    "Callback-only replacement forbidden": "Never replace history with callback-only notes" in workflow,
    "Missing prior context prompts request": "ask for them; don't guess" in workflow,
    "New-ticket context separation": "New ticket starts fresh" in workflow,
    "Retest safety preserved": "client confirmation is NOT a technician retest" in prompt,
    "Explicit on-demand request retained": "Carry request on same ticket until changed" in prompt,
    "Email-only output does not rewrite history": "Email-only turns must preserve PARN/internal blocks verbatim" in prompt,
    "Five synthetic scenarios": all(f"## {n}. " in cases for n in range(1, 6)),
    "VPN callback history": "VPN installation followed by database callback" in cases and "drops earlier VPN" in cases,
    "Partial server failure history": "[EXACT_WMI_ERROR]" in cases and "have not rerun the WMI check" in cases,
    "Superseded resolution history": "Changed result" in cases and "earlier unresolved state" in cases,
    "Unrelated ticket isolation": "New unrelated ticket" in cases,
    "Context unavailable fallback": "Prior notes unavailable" in cases,
}
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
print(f"{sum(checks.values())}/{len(checks)} static source checks passed. Copilot behavior not tested.")
raise SystemExit(0 if all(checks.values()) else 1)
