#!/usr/bin/env python3

"""
DR Core Lite — IP Tool Runner

Purpose
-------
Execute the Linux `ip` command to collect interface information.

Responsibilities
----------------
- run the ip command
- capture command output
- store raw artifact
- return output for parsing
"""

from __future__ import annotations

from pathlib import Path

from dr_core_lite.helpers.subprocess_safe import run_command
from dr_core_lite.helpers.paths import RAW_DIR
from dr_core_lite.helpers.time_utils import run_id
from dr_core_lite.helpers.log_utils import log_line
from dr_core_lite.helpers.paths import LOGS_DIR


def run_ip() -> str:
    """
    Execute `ip addr` and return the raw output.
    """

    command = ["ip", "addr"]

    result = run_command(command)

    raw_output = result.stdout

    artifact_dir = RAW_DIR / "ip"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    artifact_path = artifact_dir / f"{run_id()}_ip.txt"

    with artifact_path.open("w", encoding="utf-8") as f:
        f.write(raw_output)

    log_line(LOGS_DIR / "core.log", "tool_ip executed")

    return raw_output
