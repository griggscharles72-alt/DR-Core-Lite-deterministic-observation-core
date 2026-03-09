#!/usr/bin/env python3

"""
DR Core Lite — Database Storage Layer

Purpose
-------
Provide controlled access to database storage operations.

Responsibilities
----------------
- Initialize database
- Register observation runs
- Store parsed records
- Track artifacts
"""

from __future__ import annotations

from typing import List, Dict

from dr_core_lite.helpers.sqlite_utils import (
    init_schema,
    execute
)

from dr_core_lite.helpers.time_utils import utc_now


def init_database() -> None:
    """
    Ensure database schema exists.
    """

    init_schema()


def create_run() -> None:
    """
    Register a new observation run.
    """

    execute(
        "INSERT INTO runs (timestamp) VALUES (?)",
        (utc_now(),)
    )


def store_records(records: List[Dict]) -> None:
    """
    Store parsed records into appropriate tables.

    Parameters
    ----------
    records : list of dict
        Parsed records produced by parser modules.
    """

    for record in records:

        rtype = record.get("type")

        if rtype == "interface":

            execute(
                """
                INSERT INTO interfaces (name,address,state)
                VALUES (?,?,?)
                """,
                (
                    record.get("name"),
                    record.get("address"),
                    record.get("state"),
                ),
            )

        elif rtype == "access_point":

            execute(
                """
                INSERT INTO access_points (ssid,bssid,channel,signal)
                VALUES (?,?,?,?)
                """,
                (
                    record.get("ssid"),
                    record.get("bssid"),
                    record.get("channel"),
                    record.get("signal"),
                ),
            )

        elif rtype == "artifact":

            execute(
                """
                INSERT INTO artifacts (path,created_at)
                VALUES (?,?)
                """,
                (
                    record.get("path"),
                    utc_now(),
                ),
            )
