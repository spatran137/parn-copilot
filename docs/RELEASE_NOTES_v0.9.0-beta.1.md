# PARN Copilot Agent — v0.9.0-beta.1

**Expanded Testing Release**

PARN is a Microsoft Copilot agent that turns technician dictation and screenshots into structured ConnectWise PARN notes (Problem, Action, Resolution, Next Steps), suggested internal notes, and optional client email drafts.

## New Features
- On-demand client follow-up emails, triggered directly through technician dictation.
- Email requests and cancellations supported during the same ticket conversation.

## Improvements
- Better preservation of technical details, troubleshooting results, and ticket history.
- Improved internal evidence handling and more natural client communication.

## Fixes
- Stronger safeguards against invented technician actions, retests, and client confirmations.
- Improved handling of conflicting evidence and failed checks.
- Email-only requests no longer rewrite existing ticket notes in the targeted tests.

## Known Issues
- Beta testing is ongoing; internal knowledge retrieval and less common dictation scenarios need wider validation.
- Generated documentation requires technician review. The agent does not submit tickets or send emails automatically.

**Recommended test configuration:** Think deeper.
