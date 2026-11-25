"""Unsent micro-confession entry.

The program has one job: put the two-part confession -- a To: line naming
who the message was meant for, then the unsent line itself, exactly as it
was typed -- into entry.txt where the harness grades it.

The same bytes come out on every run. There is no input, no clock, no
network and no randomness anywhere in here, so the grader's two runs
always agree with each other.
"""

import os
from pathlib import Path

ADDRESSEE = "Mum"

CONFESSION = (
    "The rent money you sent went to pay off a loan I never told you "
    "about, and this is the third time I've rewritten this because "
    "every version sounds like I'm asking you for more."
)


def build_text() -> str:
    """Join the two parts with a single newline, nothing after the line."""
    return "To: " + ADDRESSEE + "\n" + CONFESSION


def validate(text: str) -> None:
    """Guard the two-part shape before anything is written out."""
    parts = text.split("\n")
    if len(parts) != 2:
        raise ValueError("entry must be exactly two lines")
    if not parts[0].startswith("To: "):
        raise ValueError("first line must be the To: line")
    if not parts[1].strip():
        raise ValueError("second line must hold the unsent message")
    if len(text) > 260:
        raise ValueError("entry exceeds the 260-char gate")


def destination() -> Path:
    """Where the harness wants the entry: its env var, else /output."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(wanted) / "entry.txt"


def run() -> int:
    text = build_text()
    validate(text)
    target = destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    print("wrote " + str(len(text)) + " chars to " + str(target))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
