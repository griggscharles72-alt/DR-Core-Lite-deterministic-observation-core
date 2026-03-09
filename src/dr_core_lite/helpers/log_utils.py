#!/usr/bin/env python3

"""
DR Core Lite — Logging Utilities

Purpose
-------
Provide simple deterministic logging for the system.

Responsibilities
----------------
- append log lines
- attach timestamps
- ensure log directory exists
"""

from __future__ import annotations

from pathlib import Path

from dr_core_lite.helpers.time_utils import utc_now


def log_line(log_path: Path, message: str) -> None:
    """
    Append a timestamped line to a log file.

    Parameters
    ----------
    log_path : Path
        Path to the log file
    message : str
        Log message
    """

    log_path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = utc_now()

    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {message}\n")
