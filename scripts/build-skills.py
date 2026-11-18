#!/usr/bin/env python3
"""Build Agent Builder skill ZIPs from the source files listed below."""

import argparse
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent.parent
SKILLS = {
    "it-deep-vendor-research": ("SKILL.md", "references/vendor-sources.md"),
    "parn-internal-knowledge-review": ("SKILL.md",),
}


def build_archive(name, members):
    source = ROOT / "skills" / name
    instructions = (source / "SKILL.md").read_text(encoding="utf-8")
    lines = instructions.split("\n", 4)
    if len(lines) != 5:
        raise ValueError(f"{name}: missing SKILL.md front matter or instructions")
    opening, title, description, closing, body = lines
    if opening != "---" or closing != "---" or not body.strip():
        raise ValueError(f"{name}: invalid SKILL.md front matter or missing instructions")
    if title != f"name: {name}" or not description.startswith("description: "):
        raise ValueError(f"{name}: expected a matching name and description in SKILL.md")
    if not description.removeprefix("description: ").strip():
        raise ValueError(f"{name}: skill description is empty")
    if len(body) >= 20_000:
        raise ValueError(f"{name}: keep skill instructions under 20,000 characters")

    buffer = BytesIO()
    with ZipFile(buffer, mode="w") as archive:
        for member in members:
            # A fixed timestamp and uncompressed entries keep checked-in ZIPs reproducible.
            data = (source / member).read_bytes()
            data = data.replace(b"\r\n", b"\n")
            archive.writestr(ZipInfo(member), data)
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--refresh", action="store_true", help="update the checked-in downloads")
    modes.add_argument("--check", action="store_true", help="verify the checked-in downloads")
    options = parser.parse_args()

    output = ROOT / ("packages" if options.refresh or options.check else "dist")
    try:
        for name, members in SKILLS.items():
            package = output / f"{name}.zip"
            archive = build_archive(name, members)
            if options.check:
                if not package.is_file() or package.read_bytes() != archive:
                    parser.error(f"{package.relative_to(ROOT)} is out of date. Run with --refresh.")
                print(f"Verified {package.relative_to(ROOT)}")
            else:
                output.mkdir(exist_ok=True)
                package.write_bytes(archive)
                print(f"Built {package.relative_to(ROOT)}")
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
