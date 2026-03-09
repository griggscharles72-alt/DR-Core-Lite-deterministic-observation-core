#!/usr/bin/env python3

"""
DR Core Lite — IP Output Parser

Purpose
-------
Parse raw `ip addr` output into structured interface records.
"""

from __future__ import annotations

import re
from typing import List, Dict


INTERFACE_PATTERN = re.compile(r"^\d+:\s+([a-zA-Z0-9_\-]+):\s+<(.+?)>")
IP_PATTERN = re.compile(r"inet\s+(\d+\.\d+\.\d+\.\d+)")


def parse_ip(raw_output: str) -> List[Dict]:
    """
    Parse `ip addr` output into interface records.
    """

    records = []

    current_iface = None
    current_state = None
    current_ip = None

    lines = raw_output.splitlines()

    for line in lines:

        iface_match = INTERFACE_PATTERN.match(line)

        if iface_match:

            if current_iface:
                records.append(
                    {
                        "type": "interface",
                        "name": current_iface,
                        "address": current_ip,
                        "state": current_state,
                    }
                )

            current_iface = iface_match.group(1)
            flags = iface_match.group(2)

            current_state = "UP" if "UP" in flags else "DOWN"
            current_ip = None

            continue

        ip_match = IP_PATTERN.search(line)

        if ip_match:
            current_ip = ip_match.group(1)

    if current_iface:
        records.append(
            {
                "type": "interface",
                "name": current_iface,
                "address": current_ip,
                "state": current_state,
            }
        )

    return records
