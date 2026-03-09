#!/usr/bin/env python3

"""
DR Core Lite — IW Tool Runner

Purpose
-------
Execute the Linux `iw` command to collect wireless scan data.

Responsibilities
----------------
- detect wireless interface
- run wireless scan
- capture output
- store raw artifact
"""

from __future__ import annotations

from pathlib import Path

from dr_core_lite.helpers.subprocess_safe import run_command
from dr_core_lite.helpers.paths import RAW_DIR, LOGS_DIR
from dr_core_lite.helpers.time_utils import run_id
from dr_core_lite.helpers.log_utils import log_line


def detect_interface() -> str | None:
    """
    Detect wireless interface using `iw dev`.
    """

    result = run_command(["iw", "dev"])

    lines = result.stdout.splitlines()

    for line in lines:
        line = line.strip()

        if line.startswith("Interface"):
            return line.split()[1]

    return None


def run_iw() -> str:
    """
    Execute wireless scan and return raw output.
    """

    interface = detect_interface()

    if not interface:
        log_line(LOGS_DIR / "core.log", "tool_iw no interface detected")
        return ""

    command = ["iw", "dev", interface, "scan"]

    result = run_command(command)

    raw_output = result.stdout

    artifact_dir = RAW_DIR / "iw"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    artifact_path = artifact_dir / f"{run_id()}_iw_scan.txt"

    with artifact_path.open("w", encoding="utf-8") as f:
        f.write(raw_output)

    log_line(LOGS_DIR / "core.log", f"tool_iw executed on {interface}")

    return raw_output
