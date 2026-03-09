#!/usr/bin/env python3

"""
DR Core Lite — Ethtool Output Parser

Purpose
-------
Parse `ethtool -i` output into structured driver records.
"""

from __future__ import annotations

from typing import List, Dict


def parse_ethtool(raw_output: str) -> List[Dict]:
    """
    Parse ethtool output into driver records.
    """

    records: List[Dict] = []

    current_iface = None
    driver = None
    version = None
    firmware = None
    bus_info = None

    lines = raw_output.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith("Interface:"):

            if current_iface:
                records.append(
                    {
                        "type": "driver_info",
                        "interface": current_iface,
                        "driver": driver,
                        "version": version,
                        "firmware": firmware,
                        "bus_info": bus_info,
                    }
                )

            current_iface = line.split(":", 1)[1].strip()
            driver = None
            version = None
            firmware = None
            bus_info = None

            continue

        if line.startswith("driver:"):
            driver = line.split(":", 1)[1].strip()

        elif line.startswith("version:"):
            version = line.split(":", 1)[1].strip()

        elif line.startswith("firmware-version:"):
            firmware = line.split(":", 1)[1].strip()

        elif line.startswith("bus-info:"):
            bus_info = line.split(":", 1)[1].strip()

    if current_iface:
        records.append(
            {
                "type": "driver_info",
                "interface": current_iface,
                "driver": driver,
                "version": version,
                "firmware": firmware,
                "bus_info": bus_info,
            }
        )

    return records
