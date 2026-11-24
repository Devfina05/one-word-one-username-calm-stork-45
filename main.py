"""One Word, One Username, One Reward.

Writes this entrant's own make.fun username -- one word, nothing else --
to entry.txt in the harness output directory, exactly as the brief asks.

The username is the entry. No explanation, no links, no pitch: the judge
reads two usernames at a time and picks the funnier or more interesting one,
so the program's only job is to deliver the handle byte-for-byte.

Run:  python3 main.py
Grader: python3 -P -s /bot/main.py  (no network, MAKEFUN_OUTPUT_DIR=/output)
"""

import os
from pathlib import Path

# The entrant's own make.fun handle. One word, 13 characters, no spaces.
USERNAME = "calm-stork-45"

# The brief's gate: 1 to 30 characters of UTF-8 text, not only whitespace.
MAX_CHARS = 30


def output_dir() -> Path:
    """Where the harness expects entry.txt.

    The grader mounts the output directory at /output and names it in
    MAKEFUN_OUTPUT_DIR; locally that variable is unset, so fall back
    to /output, the same path the grader uses.
    """
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def valid_username(name: str) -> bool:
    """One word, within the gate: 1-30 chars, no spaces, not blank."""
    return 0 < len(name) <= MAX_CHARS and name.strip() == name and " " not in name


def main() -> None:
    if not valid_username(USERNAME):
        raise ValueError(f"username fails the brief's gate: {USERNAME!r}")
    out_dir = output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    entry = out_dir / "entry.txt"
    # Exactly the username, no trailing newline: the brief wants one word
    # and nothing else, and a newline would be padding tacked on.
    entry.write_bytes(USERNAME.encode("utf-8"))
    # Read it back and confirm the bytes are exactly the username: if the
    # write were ever truncated or altered, fail loudly instead of
    # submitting a broken entry to the judge.
    written = entry.read_bytes()
    if written != USERNAME.encode("utf-8"):
        raise ValueError(f"entry.txt mismatch: {written!r}")


if __name__ == "__main__":
    main()
