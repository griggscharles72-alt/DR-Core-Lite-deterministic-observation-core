#!/usr/bin/env python3

"""
DR Core Lite — NMCLI Output Parser

Purpose
-------
Parse NetworkManager device output into structured records.
"""

from __future__ import annotations

from typing import List, Dict


def parse_nmcli(raw_output: str) -> List[Dict]:
    """
    Parse nmcli device output into structured records.
    """

    records: List[Dict] = []

    lines = raw_output.splitlines()

    for line in lines:

        if not line.strip():
            continue

        parts = line.split(":")

        if len(parts) < 4:
            continue

        device = parts[0]
        dev_type = parts[1]
        state = parts[2]
        connection = parts[3] if parts[3] else None

        record = {
            "type": "network_device",
            "device": device,
            "device_type": dev_type,
            "state": state,
            "connection": connection,
        }

        records.append(record)

    return records
