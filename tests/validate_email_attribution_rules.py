"""Static checks of email attribution source rules; NOT a live Copilot evaluation."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
prompt = (root / "agent" / "ConnectWise_PARN_Agent_Instructions_Condensed.md").read_text()
cases = (root / "tests" / "Email_Attribution_Scenarios.md").read_text()
rules = next((line for line in prompt.splitlines() if line.startswith("- Match tech's voice.")), "")
checks = {
    "LF instruction length": len(prompt) <= 8000,
    "CRLF instruction length": len(prompt.replace("\n", "\r\n")) <= 8000,
    "Explicit solo attribution": "Use `I` for solo work" in rules,
    "Explicit collaborative attribution": "`we` only for proven joint work" in rules,
    "Mixed actions have independent actors": "Attribute mixed-ticket actions separately" in rules,
    "Consultation is not shared performance": "Advice isn't joint execution" in rules,
    "Unattributed actions use neutral language": "unknown actors stay neutral" in rules,
    "Attachment does not imply actor": "Attachment output does not prove who performed work" in prompt,
    "Internal routing remains present": "marked text goes only under `Technician note`" in prompt,
    "Client voice rule retained": "Match tech's voice" in rules,
    "Eight synthetic scenarios": all(f"### {i}. " in cases for i in range(1, 9)),
    "Solo and shared fixture": "Solo plus technician collaboration" in cases,
    "Consultation fixture": "Advice is not shared execution" in cases,
    "Client joint fixture": "Technician and client joint action" in cases,
    "Unknown actor fixture": "Unknown actor, attachment only" in cases,
    "Explicit plural fixture": "Dictated plural without named contributors" in cases,
    "Internal-only fixture": "[INTERNAL_CASE_ID]" in cases,
    "Full-ticket mixed actor fixture": "Multiple actor changes across one ticket" in cases,
}
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
print(f"{sum(checks.values())}/{len(checks)} static checks passed; Copilot behavior not tested.")
raise SystemExit(0 if all(checks.values()) else 1)
