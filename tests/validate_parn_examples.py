"""Static checks of manually generated examples, NOT a model/Copilot test."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
prompt = (root / 'agent' / 'ConnectWise_PARN_Agent_Instructions_Condensed.md').read_text()
report = (root / 'tests' / 'PARN_Test_Report.md').read_text()
table = (root / 'agent' / 'knowledge' / 'PARN_Terminology_Table.txt').read_text()
checks = []
def check(label, condition):
    checks.append((label, bool(condition)))

check('Prompt <=8000 LF characters', len(prompt) <= 8000)
check('Prompt <=8000 CRLF characters', len(prompt.replace('\n', '\r\n')) <= 8000)
check('Prompt references exact table filename', 'PARN_Terminology_Table.txt' in prompt)
check('Attachment review output category exists', 'Technician note, Attachment review, Internal knowledge' in prompt)
check('Ticket attachments default to internal review', 'Route all readable ticket-relevant content to `Attachment review` by default' in prompt)
check('Relevant attachment evidence may enter PARN', 'directly supports public technician notes' in prompt and 'proper PARN section' in prompt)
check('Attachment output is not assumed technician work', 'does not prove who performed work' in prompt)
check('Unreadable attachment text is not guessed', 'Do not guess unreadable/cropped content' in prompt)
check('Conflicting attachment evidence is flagged', 'attachment and dictation conflict' in prompt and 'request confirmation' in prompt)
check('Internal knowledge skill is explicitly invoked', 'Invoke `parn-internal-knowledge-review` after drafting' in prompt)
check('Internal knowledge trigger includes technical signals', all(term in prompt for term in ['product/device', 'version', 'error', 'event ID', 'alert', 'log/command output', 'symptom', 'procedure']))
check('Internal knowledge skill owns retrieval safeguards', all(term in prompt for term in ['SharePoint/Teams search', 'citations', 'privacy', 'failures', 'routing']))
action_rule = next((line for line in prompt.splitlines() if line.startswith('- Action:')), '')
check('Action rule preserves material technical details', all(term in action_rule for term in ['stage', 'target', 'tool/command', 'parameters', 'path/address', 'version', 'observed result']))
rows = [s.split(' | ') for s in table.splitlines() if ' | antivirus | ' in s]
check('Three unique approved aliases', len(rows) == 3 and len({r[0].casefold() for r in rows}) == 3)
check('No hardcoded SentinelOne mapping remains in prompt', 'SentinelOne' not in prompt)
blocks = re.findall(r'```text\n(.*?)\n```', report, re.S)
check('Three complete examples with three blocks each', len(blocks) == 9)
for i in range(3):
    parn, internal, email = blocks[3*i:3*i+3]
    check(f'Example {i+1} PARN heading order', bool(re.match(r'Problem:\n.*?\nAction:\n.*?\nResolution:\n.*?\nNext Steps:\n', parn, re.S)))
    actions = parn.split('Action:\n')[1].split('\n\nResolution:')[0].splitlines()
    check(f'Example {i+1} Action bullets', all(s.startswith('- ') for s in actions))
    check(f'Example {i+1} Internal heading', internal.startswith('Suggested Internal Notes:\n'))
    check(f'Example {i+1} Email body without greeting/signoff', email.startswith('Client Follow-Up Email:\nSubject:') and not re.search(r'(?im)^(hello|hi|dear|thank you|regards)\b', email))
check('Maintenance site-loading note stays internal', 'loading parts of the site' in blocks[1] and 'loading parts of the site' not in blocks[0] + blocks[2])
check('No unconfirmed ongoing scan assertion', 'still running' not in blocks[0] + blocks[2])
check('Attachment not asserted complete', 'Attached' not in blocks[0])
check('Script completion retained', 'script completed' in blocks[0])
for literal in [r'C:\ProgramData\SentinelOne\Logs\agent.log', r'\\[FILE_SERVER]\IT\S1-report.txt', '[EXAMPLE_IP_C]', '26.1.2', '"SentinelOne service unavailable"']:
    check('Literal retained: ' + literal, literal in blocks[3])
check('Prose mapping applied', 'Checked antivirus' in blocks[3])
check('Block content not leaked', all(s not in blocks[6] + blocks[8] for s in ['console', 'renewal']))
check('Dictated timeline retained', 'tomorrow' in blocks[8])
check('Twenty-two documented cases', len(re.findall(r'^## Case [123] |^### (?:[4-9]|1[0-9]|2[0-2])\.', report, re.M)) == 22)
check('Unrelated screenshot details remain internal', 'Screenshot details unrelated to the public note' in report and 'all readable ticket-relevant attachment details stay internal' in report)
check('Relevant screenshot details retain command and result', '`Test-NetConnection [DOMAIN_CONTROLLER] -Port 5985`' in report and '`TcpTestSucceeded : True`' in report)
check('Screenshot-only output is not attributed', 'Screenshot output without action attribution' in report and 'does not claim that the technician ran the command' in report)
check('Unreadable screenshot text is not reconstructed', 'no path is guessed or reconstructed' in report)
check('Conflicting values are preserved for confirmation', 'both values are retained internally' in report)
check('Routine maintenance may skip knowledge lookup', 'Routine maintenance does not force knowledge lookup' in report and 'skill is skipped' in report)
check('Technical signals trigger cited internal lookup', 'Technical signal invokes internal knowledge review' in report and 'Source: Exact returned title - direct returned link' in report)
check('No-match lookup does not invent documentation status', 'No relevant knowledge result' in report and 'does not claim that no documentation exists' in report)
check('Permission or readiness failure is reported', 'Knowledge source permission or readiness failure' in report and 'confirm source readiness' in report)
check('Conflicting internal sources are not silently selected', 'Conflicting internal sources' in report and 'does not silently choose a procedure' in report)
for label, passed in checks:
    print(('PASS' if passed else 'FAIL') + ': ' + label)
print(f'LF characters: {len(prompt)}; CRLF characters: {len(prompt.replace(chr(10), chr(13)+chr(10)))}')
print(f'{sum(p for _,p in checks)}/{len(checks)} static checks passed. Model behavior not measured.')
raise SystemExit(0 if all(p for _,p in checks) else 1)