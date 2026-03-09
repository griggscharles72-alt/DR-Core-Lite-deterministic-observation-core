#!/usr/bin/env python3

"""
DR Core Lite — Ethtool Tool Runner

Purpose
-------
Execute `ethtool` to collect network driver information.

Responsibilities
----------------
- detect network interfaces
- run ethtool for each interface
- capture output
- store raw artifact
"""

from __future__ import annotations

from dr_core_lite.helpers.subprocess_safe import run_command
from dr_core_lite.helpers.paths import RAW_DIR, LOGS_DIR
from dr_core_lite.helpers.time_utils import run_id
from dr_core_lite.helpers.log_utils import log_line


def get_interfaces() -> list[str]:
    """
    Detect interfaces using `ip -o link`.
    """

    result = run_command(["ip", "-o", "link"])

    interfaces = []

    for line in result.stdout.splitlines():
        parts = line.split(":")
        if len(parts) > 1:
            iface = parts[1].strip()
            if iface != "lo":
                interfaces.append(iface)

    return interfaces


def run_ethtool() -> str:
    """
    Execute ethtool for detected interfaces.
    """

    interfaces = get_interfaces()

    combined_output = []

    for iface in interfaces:

        command = ["ethtool", "-i", iface]

        result = run_command(command)

        combined_output.append(f"Interface: {iface}\n")
        combined_output.append(result.stdout)
        combined_output.append("\n")

    raw_output = "".join(combined_output)

    artifact_dir = RAW_DIR / "ethtool"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    artifact_path = artifact_dir / f"{run_id()}_ethtool.txt"

    with artifact_path.open("w", encoding="utf-8") as f:
        f.write(raw_output)

    log_line(LOGS_DIR / "core.log", "tool_ethtool executed")

    return raw_output
