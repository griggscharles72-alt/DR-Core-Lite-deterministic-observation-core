#!/usr/bin/env python3

"""
DR Core Lite — RFKill Tool Runner

Purpose
-------
Execute the Linux `rfkill` command to inspect radio blocking state.

Responsibilities
----------------
- run rfkill list
- capture output
- store raw artifact
- return output for parsing
"""

from __future__ import annotations

from dr_core_lite.helpers.subprocess_safe import run_command
from dr_core_lite.helpers.paths import RAW_DIR, LOGS_DIR
from dr_core_lite.helpers.time_utils import run_id
from dr_core_lite.helpers.log_utils import log_line


def run_rfkill() -> str:
    """
    Execute `rfkill list` and return raw output.
    """

    command = ["rfkill", "list"]

    result = run_command(command)

    raw_output = result.stdout

    artifact_dir = RAW_DIR / "rfkill"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    artifact_path = artifact_dir / f"{run_id()}_rfkill.txt"

    with artifact_path.open("w", encoding="utf-8") as f:
        f.write(raw_output)

    log_line(LOGS_DIR / "core.log", "tool_rfkill executed")

    return raw_output
