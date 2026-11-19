"""Static source-contract checks for issue #3; NOT Copilot behavioral tests."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
prompt = (root / "agent" / "ConnectWise_PARN_Agent_Instructions_Condensed.md").read_text()
cases = (root / "tests" / "Performed_Evidence_Scenarios.md").read_text()
live_observations = (root / "tests" / "PR9_Live_Evidence_Observations_2026-10-26.md").read_text()

action = next((line for line in prompt.splitlines() if line.startswith("- Action:")), "")
resolution = next((line for line in prompt.splitlines() if line.startswith("- Resolution:")), "")
checks = {
    "LF instruction length <= 8,000": len(prompt) <= 8000,
    "CRLF instruction length <= 8,000": len(prompt.replace("\n", "\r\n")) <= 8000,
    "Three output blocks retained": "return all three sections in order" in prompt,
    "Attachment evidence is supplementary": "Performed results belong in PARN; raw logs stay internal" in prompt,
    "Every dictated test/result is an Action bullet": "Bullet EVERY dictated step/result" in action,
    "Action retains performed target and technical literals": all(
        value in action for value in ["target", "tool/command", "parameters", "path/address", "version", "observed result", "exact error/code", "pass/fail per target"]
    ),
    "Action avoids generic descriptions": "Never generalize results" in action,
    "Resolution records partial or failed checks": "incomplete/failed checks per target" in resolution,
    "Missing scan results are not assumed passed": "Missing scan results are unknown, not passed" in resolution,
    "Screenshot-only output is not attributed": "Attachment output does not prove who performed work" in prompt,
    "Dictation/evidence conflict is not silently resolved": "If attachment and dictation conflict" in prompt,
    "Internal routing/privacy kept": "marked text goes only under" in prompt and "Redact passwords" in prompt,
    "Ten synthetic scenarios": all(f"### {i}. " in cases for i in range(1, 11)),
    "WMI code preserved in fixture": "0x800706BA" in cases,
    "Command parameters preserved in fixture": "chkdsk D: /scan" in cases and "-Port 5985" in cases,
    "Network pass/fail distinction recorded": "ICMP failed" in cases and "TcpTestSucceeded: True" in cases,
    "Unattributed screenshot fixture": "Screenshot-only output has no actor" in cases,
    "Conflicting incomplete-output fixture": "interrupted scan at 48%" in cases,
    "Internal-only fixture": "[PRIVATE_DIAGNOSTIC_REFERENCE]" in cases,
    "Log error does not prove cause": "no inferred cause" in resolution,
    "Technician observation is not client confirmation": "client confirmation ONLY if stated" in resolution,
    "Sanitized VPN case": "VPN repair, log attribution, client confirmation and closure" in cases,
    "VPN case preserves raw log discrepancy": "username or password not recognized" in cases,
    "VPN case preserves closure intention": "Do not imply the agent actually closed the ConnectWise ticket" in cases,
    "Exact fictional workstation spelling fixture": "LAB WS 04" in cases and "LAB-WS04" in cases,
    "Raw credential error must not be invented": "username or password was not recognized" in cases,
    "Unattributed client confirmation rejected": "The user confirmed" in cases and "I verified application access" in cases,
    "Screenshot-only test forbids inferred technician action": "Screenshot-only command/results:" in prompt and "`Attachment review` ONLY" in prompt and "not technician Action" in prompt,
    "Contradictory screenshot blocks email choice": "For dictated vs screenshot conflict" in prompt and "STOP before final notes" in prompt,
    "Conflicting evidence requires confirmation before final output": "If attachment and dictation conflict, keep both internally; request confirmation and STOP." in prompt,
    "Failed ping observation retained without invented operator": "including failed or unattributed tests" in action and "never invent a ping operator" in action,
    "No invented client confirmation or retest": "Never invent work, retests, client contact" in prompt,
    "Reported access is not client conversation": "`user can access` isn\u0027t `confirmed with client`" in prompt,
    "Outcome is not performed second test": "`VPN worked` isn\u0027t `I verified` or a new test" in prompt,
    "Failed ping stays in Action": "Failed ping AND passed TCP belong in Action, not only Problem/Resolution" in action,
    "Live Copilot observations explicitly separated": "technician-provided Copilot live test observations" in live_observations and "not" in live_observations.lower() and "Static source checks" in live_observations,
    "Failed and partial live cases tracked": all(f"| {n}." in live_observations for n in [4, 5, 6, 9, 10]),
}
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
print(f"{sum(checks.values())}/{len(checks)} source checks passed; model behavior not tested.")
raise SystemExit(0 if all(checks.values()) else 1)
