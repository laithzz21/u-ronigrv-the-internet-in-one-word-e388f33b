#!/usr/bin/env python3
"""One-word entry for make.fun bounty u-ronigrv-the-internet-in-one-word-e388f33b.

Brief: describe the whole internet in a SINGLE WORD.
Entry: "doomscrolling" — the internet, distilled: an endless feed you
came to check for five minutes and somehow never left.

The program prints exactly that one word to stdout with NO trailing
newline, and also writes it (no trailing newline) to a file under
$MAKEFUN_OUTPUT_DIR, else $MAKEFUN_OUTPUT, else a per-entry /tmp path.
Deterministic, stdlib only, no network, no clock, no randomness.
It never writes into the repository directory.
"""

import os
import sys

WORD = "doomscrolling"

FALLBACK_DIR = "/tmp/u-ronigrv-the-internet-in-one-word-e388f33b"


def validate_word(word: str) -> None:
    """The entry must be exactly one word: non-empty, no whitespace,
    a single alphabetic token in lowercase (no digits, punctuation,
    hyphens, or mixed case that would read as more than one word)."""
    if not word:
        raise ValueError("entry word is empty")
    if any(ch.isspace() for ch in word):
        raise ValueError(f"entry must be a single word, got: {word!r}")
    if not word.isalpha():
        raise ValueError(f"entry must be letters only, got: {word!r}")
    if word != word.lower():
        raise ValueError(f"entry must be lowercase, got: {word!r}")


def resolve_output_path() -> str:
    """Resolve where the entry file goes.

    $MAKEFUN_OUTPUT_DIR (a directory) wins, then $MAKEFUN_OUTPUT —
    treated as a file path when it ends in ".txt" (the per-run
    verification layout, e.g. .../run1/entry.txt), otherwise as a
    directory — then the per-entry /tmp path.
    """
    output_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "").strip()
    if output_dir:
        return os.path.join(output_dir, "entry.txt")
    output = (os.environ.get("MAKEFUN_OUTPUT") or "").strip()
    if output:
        if output.endswith(".txt"):
            return output
        return os.path.join(output, "entry.txt")
    return os.path.join(FALLBACK_DIR, "entry.txt")


def write_entry(path: str) -> str:
    """Write WORD to path (no trailing newline) and verify by reading back.

    Refuses to write inside the repository directory: the grader's
    checkout is read-only, so a repo-relative path would fail there
    even when a local run passes.
    """
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(path).startswith(repo_dir + os.sep):
        raise OSError(f"refusing to write inside repository directory: {path!r}")
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(WORD)
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != WORD:
        raise ValueError(
            f"verification failed: expected {WORD!r}, read back {written!r}"
        )
    return path


def main() -> int:
    validate_word(WORD)
    path = resolve_output_path()
    try:
        write_entry(path)
    except OSError:
        # Fall back to the per-entry /tmp path if the primary location
        # is not writable (e.g. a read-only checkout or missing parent).
        fallback = os.path.join(FALLBACK_DIR, "entry.txt")
        if fallback != path:
            write_entry(fallback)
        else:
            raise
    sys.stdout.write(WORD)
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
