"""Static source contract checks for issue #2, NOT live Copilot tests."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
prompt = (root / "agent" / "ConnectWise_PARN_Agent_Instructions_Condensed.md").read_text()
cases = (root / "tests" / "Ticket_Closure_Intent_Scenarios.md").read_text()
next_steps = next((line for line in prompt.splitlines() if line.startswith("- Next Steps:")), "")
checks = {
    "LF <= 8,000 characters": len(prompt) <= 8000,
    "CRLF <= 8,000 characters": len(prompt.replace("\n", "\r\n")) <= 8000,
    "Three output blocks": "return exactly three plain-text code blocks" in prompt,
    "Closing is future intent": "`Closing ticket` is intent, NEVER `ticket closed` or `can close`" in next_steps,
    "Completed close is distinct": "`I closed` = completed Action" in next_steps,
    "Eligible close is distinct": "`can be closed` = eligible only" in next_steps,
    "Eligibility is never closure instruction": "(NOT `Close the ticket`)" in next_steps,
    "Eligibility output goes in Resolution": "Resolution notes eligibility" in next_steps,
    "No invented future action for eligibility": "`Next Steps: Not provided.` unless explicit close request" in next_steps,
    "Prior hold expiring is not close instruction": "even if prior hold condition met" in next_steps,
    "Explicit uncertainty overrides prior eligibility/plan": "FIRST on EVERY turn" in prompt.split("# Required Output",1)[0] and "If technician is unsure whether to close vs leave open" in prompt and "override prior closure eligibility/plan" in prompt,
    "No further action not a close": "`No further action` isn't closure" in next_steps,
    "Conditional and negative closure": all(t in next_steps for t in ["`close after X`","`do not close`"]),
    "Uncertain closure asks one question before blocks": "Ask ONLY `Close ticket or leave open?`" in prompt and "STOP without ANY three blocks" in prompt and prompt.index("FIRST on EVERY turn") < prompt.index("# Required Output"),
    "No ticket automation": "never close tickets" in next_steps,
    "On-demand email unchanged": "Draft Standard ONLY on explicit tech request" in prompt,
    "Mandatory evidence contradiction gate": "STOP before final notes" in prompt,
    "Twelve targeted scenarios": all(f"### {i}. " in cases for i in range(1, 13)),
    "Eligibility after condition test": "### 11. Client confirmation satisfies condition but is not a close command" in cases,
    "Ambiguity after eligibility test": "### 12. Explicit uncertainty after eligibility must stop" in cases,
    "Observed second failure recorded": "second Think deeper retest" in cases,
    "Future and completed timeline included": "Same-ticket planned -> completed update" in cases,
    "First-output regression included": "No further action required; closing the ticket" in cases,
    "Client email still factual": "without saying the ticket **was closed**" in cases,
    "Fixtures not claimed live": "not Copilot outputs or observed model passes" in cases,
}
for label, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + label)
print(f"{sum(checks.values())}/{len(checks)} closure source checks passed. Copilot behavior NOT tested.")
raise SystemExit(0 if all(checks.values()) else 1)
