#!/usr/bin/env python3

"""
DR Core Lite — RFKill Output Parser

Purpose
-------
Parse `rfkill list` output into structured radio state records.
"""

from __future__ import annotations

from typing import List, Dict


def parse_rfkill(raw_output: str) -> List[Dict]:
    """
    Parse rfkill output into structured records.
    """

    records: List[Dict] = []

    current_device = None
    current_type = None
    soft_block = None
    hard_block = None

    lines = raw_output.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if ":" in line and line[0].isdigit():

            if current_device is not None:
                records.append(
                    {
                        "type": "radio_state",
                        "device": current_device,
                        "radio_type": current_type,
                        "soft_blocked": soft_block,
                        "hard_blocked": hard_block,
                    }
                )

            parts = line.split(":", 2)

            device_id = parts[0]
            remainder = parts[2].strip()

            pieces = remainder.split()

            current_device = pieces[-1]
            current_type = " ".join(pieces[:-1])

            soft_block = None
            hard_block = None

            continue

        if line.startswith("Soft blocked:"):
            value = line.split(":")[1].strip()
            soft_block = value.lower() == "yes"

        if line.startswith("Hard blocked:"):
            value = line.split(":")[1].strip()
            hard_block = value.lower() == "yes"

    if current_device is not None:
        records.append(
            {
                "type": "radio_state",
                "device": current_device,
                "radio_type": current_type,
                "soft_blocked": soft_block,
                "hard_blocked": hard_block,
            }
        )

    return records
