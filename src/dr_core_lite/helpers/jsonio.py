#!/usr/bin/env python3

"""
DR Core Lite — JSON Utilities

Purpose
-------
Provide consistent JSON read and write functions.

Responsibilities
----------------
- Deterministic JSON output
- Safe file writing
- UTF-8 encoding
- Pretty formatted artifacts
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_json(path: Path, data: Any) -> None:
    """
    Write JSON to disk with deterministic formatting.
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            sort_keys=True,
            ensure_ascii=False
        )
        f.write("\n")


def read_json(path: Path) -> Any:
    """
    Load JSON from disk.
    """

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
