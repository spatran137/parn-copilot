"""Check the Markdown prompt contract. These checks do not run Copilot."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
prompt = (root / "agent" / "ConnectWise_PARN_Agent_Instructions_Condensed.md").read_text()
output = prompt.split("# Required Output\n", 1)[1].split("# Accuracy and Safety\n", 1)[0]
email = prompt.split("# Client Email Rules\n", 1)[1].split("# Research Skill\n", 1)[0]
headings = re.findall(r"^#{2,3} .+$", output, re.M)

checks = {
    "Markdown section and subsection order": headings == [
        "## PARN Note",
        "### Problem",
        "### Action",
        "### Resolution",
        "### Next Steps",
        "## Suggested Internal Notes",
        "## Client Follow-Up Email",
    ],
    "Markdown headings have blank-line separation": all(
        f"\n\n{heading}\n\n" in output for heading in headings
    ),
    "Explicit single-section requests omit other sections": "unless asked to omit others" in output,
    "Each deliverable gets its own Markdown code block": (
        "Put each section in its own backtick fence (3+) labeled markdown" in output
    ),
    "No text outside deliverable fences and no HTML": "no text outside fences" in output
    and "No HTML" in output,
    "Portable list and paragraph formatting": "`- ` bullets" in output
    and "short paragraphs" in output and "Escape prose markup" in output,
    "Inline literals and verbatim multiline evidence": "inline code for literals" in output
    and "tilde fences for multiline commands/logs" in output
    and "Fences exceed inner runs" in output,
    "Quoted logs contain only supplied lines": "Copy designated lines only, excluding prior logs/prose." in output,
    "Check and correct exact log quotes before output": "Match fence to source line for line; recopy on mismatch." in output,
    "Email subject and body are separated": "`Subject: ...`, blank line, then body" in output,
    "No-email marker is retained": "Without a draft: `Not needed.`" in output,
    "Email body uses restrained formatting": "Conversational paragraphs; bullets only if helpful" in email
    and "No body headings/fences" in email,
    "Standard default and explicit levels": "Standard default" in email
    and "Use explicit Simple (plain language), Standard or Detailed (relevant technical specifics)" in email,
    "Closure clarification exits without deliverable blocks": (
        "STOP without output sections" in prompt.split("# Required Output", 1)[0]
    ),
    "8,000-character response budget includes markup": "Max 8,000 characters including markup" in output,
    "Both skill invocations retained": all(
        f"Invoke `{skill}`" in prompt for skill in (
            "parn-internal-knowledge-review", "it-deep-vendor-research"
        )
    ),
}

for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
print(f"{sum(checks.values())}/{len(checks)} static Markdown checks passed. Copilot behavior not tested.")
raise SystemExit(0 if all(checks.values()) else 1)
