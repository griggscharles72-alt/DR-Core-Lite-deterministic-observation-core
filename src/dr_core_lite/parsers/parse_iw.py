#!/usr/bin/env python3

"""
DR Core Lite — IW Scan Parser

Purpose
-------
Parse wireless scan output produced by the `iw` command.

Produces structured access point records.
"""

from __future__ import annotations

import re
from typing import List, Dict


BSS_PATTERN = re.compile(r"BSS\s+([0-9a-fA-F:]{17})")
SSID_PATTERN = re.compile(r"SSID:\s+(.*)")
SIGNAL_PATTERN = re.compile(r"signal:\s+(-?\d+\.?\d*)")
CHANNEL_PATTERN = re.compile(r"DS Parameter set:\s+channel\s+(\d+)")


def parse_iw(raw_output: str) -> List[Dict]:
    """
    Parse iw scan output into access point records.
    """

    records: List[Dict] = []

    current_bssid = None
    current_ssid = None
    current_channel = None
    current_signal = None

    lines = raw_output.splitlines()

    for line in lines:

        line = line.strip()

        bss_match = BSS_PATTERN.search(line)

        if bss_match:

            if current_bssid:
                records.append(
                    {
                        "type": "access_point",
                        "ssid": current_ssid,
                        "bssid": current_bssid,
                        "channel": current_channel,
                        "signal": current_signal,
                    }
                )

            current_bssid = bss_match.group(1)
            current_ssid = None
            current_channel = None
            current_signal = None

            continue

        ssid_match = SSID_PATTERN.search(line)

        if ssid_match:
            current_ssid = ssid_match.group(1)

        signal_match = SIGNAL_PATTERN.search(line)

        if signal_match:
            current_signal = int(float(signal_match.group(1)))

        channel_match = CHANNEL_PATTERN.search(line)

        if channel_match:
            current_channel = int(channel_match.group(1))

    if current_bssid:
        records.append(
            {
                "type": "access_point",
                "ssid": current_ssid,
                "bssid": current_bssid,
                "channel": current_channel,
                "signal": current_signal,
            }
        )

    return records
