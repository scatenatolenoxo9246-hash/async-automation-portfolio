#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECK_FILES = [
    ROOT / "output" / "outreach_drafts.md",
    *sorted(ROOT.glob("send_batch_*.md")),
]

FORBIDDEN_PATTERNS = [
    re.compile(r"\[[^\]]+\]"),
    re.compile(r"Hi\s+\[Name\]", re.IGNORECASE),
    re.compile(r"\[portfolio link\]", re.IGNORECASE),
    re.compile(r"your\.email@gmail\.com", re.IGNORECASE),
    re.compile(r"your-github-username", re.IGNORECASE),
]


def main() -> None:
    errors: list[str] = []
    for path in CHECK_FILES:
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{path.relative_to(ROOT)}:{line}: {match.group(0)}")

    if errors:
        print("Send-ready validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Send-ready validation passed.")


if __name__ == "__main__":
    main()
