#!/usr/bin/env python3

"""
DR Core Lite — Time Utilities

Purpose
-------
Provide standardized timestamp and run identifier utilities.

Responsibilities
----------------
- Generate ISO timestamps
- Generate run IDs
- Provide deterministic time formatting
"""

from __future__ import annotations

from datetime import datetime
import uuid


def utc_now() -> str:
    """
    Return the current UTC timestamp in ISO format.
    """

    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def run_id() -> str:
    """
    Generate a unique run identifier.

    Format:
    run-<timestamp>-<short-uuid>
    """

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    short_uuid = uuid.uuid4().hex[:8]

    return f"run-{timestamp}-{short_uuid}"
