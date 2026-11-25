#!/usr/bin/env python3
"""Write one word describing the whole internet to entry.txt.

Deterministic, Python 3 stdlib only. Output location fallback order:
OUTPUT_DIR, _OUTPUT_DIR, MAKEFUN_OUTPUT_DIR, /output, ./output,
current working directory.
"""

import os
from pathlib import Path

WORD = "spaghetti"


def validate_word(word):
    """Gate: one token, 1-30 chars, UTF-8, not whitespace-only."""
    assert isinstance(word, str) and word, "word must be non-empty"
    assert 1 <= len(word) <= 30, f"word length out of range: {len(word)}"
    assert word == word.strip(), "word must not have surrounding whitespace"
    assert len(word.split()) == 1, "word must be a single token"
    word.encode("utf-8")
    return word


def find_output_dir():
    for env in ("OUTPUT_DIR", "_OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        value = os.environ.get(env)
        if value:
            return Path(value)
    for candidate in (Path("/output"), Path("./output"), Path.cwd()):
        if candidate.is_dir():
            return candidate
    return Path("/output")


def main():
    word = validate_word(WORD)
    out_dir = find_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "entry.txt"
    path.write_text(word + "\n", encoding="utf-8")
    text = path.read_text(encoding="utf-8")
    assert text == word + "\n", f"unexpected entry.txt content: {text!r}"
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
