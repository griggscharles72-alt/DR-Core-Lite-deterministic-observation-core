#!/usr/bin/env python3

"""
DR Core Lite — Tag Rules

Purpose
-------
Apply deterministic tags to observed objects.

This module performs lightweight classification only.
"""

from __future__ import annotations

from typing import Dict, List


def tag_interface(record: Dict) -> List[str]:
    """
    Apply tags to interface records.
    """

    tags = []

    name = record.get("name")

    if name and name.startswith("eth"):
        tags.append("ethernet_interface")

    if name and name.startswith("wlan"):
        tags.append("wireless_interface")

    if record.get("state") == "UP":
        tags.append("interface_up")

    return tags


def tag_access_point(record: Dict) -> List[str]:
    """
    Apply tags to wireless access point records.
    """

    tags = []

    signal = record.get("signal")

    if signal is not None:

        if signal > -50:
            tags.append("strong_signal")

        elif signal < -75:
            tags.append("weak_signal")

    ssid = record.get("ssid")

    if not ssid:
        tags.append("hidden_network")

    return tags


def tag_radio_state(record: Dict) -> List[str]:
    """
    Apply tags to radio state records.
    """

    tags = []

    if record.get("soft_blocked"):
        tags.append("radio_soft_blocked")

    if record.get("hard_blocked"):
        tags.append("radio_hard_blocked")

    return tags


def apply_tags(record: Dict) -> Dict:
    """
    Apply tagging rules to a record.
    """

    rtype = record.get("type")

    tags: List[str] = []

    if rtype == "interface":
        tags = tag_interface(record)

    elif rtype == "access_point":
        tags = tag_access_point(record)

    elif rtype == "radio_state":
        tags = tag_radio_state(record)

    record["tags"] = tags

    return record
