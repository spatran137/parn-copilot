"""Static source contract checks for issue #2, NOT live Copilot tests."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
prompt = (root / "agent" / "ConnectWise_PARN_Agent_Instructions_Condensed.md").read_text()
cases = (root / "tests" / "Ticket_Closure_Intent_Scenarios.md").read_text()
preflight = prompt.split("# Required Output", 1)[0]
next_steps = next((line for line in prompt.splitlines() if line.startswith("- Next Steps:")), "")
checks = {
    "LF <= 8,000 characters": len(prompt) <= 8000,
    "CRLF <= 8,000 characters": len(prompt.replace("\n", "\r\n")) <= 8000,
    "Three output blocks": "return all three sections in order" in prompt,
    "Closing is future intent": "`Closing ticket` is intent, NEVER `ticket closed` or `can close`" in next_steps,
    "Completed close is distinct": "`I closed` = completed Action" in next_steps,
    "Eligible close is distinct": "`can be closed` = eligible only" in next_steps,
    "Eligibility is never closure instruction": "(NOT `Close the ticket`)" in next_steps,
    "Eligibility output goes in Resolution": "Resolution notes eligibility" in next_steps,
    "No invented future action for eligibility": "`Not provided.` in Next Steps unless explicit close request" in next_steps,
    "Prior hold expiring is not close instruction": "even if prior hold condition met" in next_steps,
    "Only explicit uncertainty triggers the closure gate": (
        "FIRST on EVERY turn" in preflight
        and "For explicit closure indecision only, override prior eligibility/plan" in preflight
    ),
    "No further action triggers neither closure nor clarification": (
        "`No further action` alone means no closure or question." in preflight
        and "Draft immediately without a closure question." in cases
    ),
    "Conditional and negative closure": all(t in next_steps for t in ["`close after X`","`do not close`"]),
    "Uncertain closure asks one question before blocks": "ask ONLY `Close ticket or leave open?`" in preflight and "STOP without output sections" in preflight,
    "No ticket automation": "never close tickets" in next_steps,
    "On-demand email unchanged": "Draft ONLY on explicit tech request" in prompt,
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
