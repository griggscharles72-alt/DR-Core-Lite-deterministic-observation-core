#!/usr/bin/env python3

"""
DR Core Lite — SQLite Utilities

Purpose
-------
Centralized helper functions for interacting with SQLite.

Responsibilities
----------------
- Open database connections
- Initialize schema
- Execute safe queries
- Simplify inserts and reads
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Any

from dr_core_lite.helpers.paths import DB_FILE


def get_connection() -> sqlite3.Connection:
    """
    Open a SQLite connection using the configured database path.
    """

    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_schema() -> None:
    """
    Initialize the database schema if it does not exist.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tool_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id INTEGER,
        tool TEXT,
        status INTEGER,
        artifact_path TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS interfaces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        state TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS access_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ssid TEXT,
        bssid TEXT,
        channel INTEGER,
        signal INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS artifacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        object_type TEXT,
        object_id TEXT,
        tag TEXT
    )
    """)

    conn.commit()
    conn.close()


def execute(query: str, params: Iterable[Any] = ()) -> None:
    """
    Execute a SQL statement without returning results.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(query, params)

    conn.commit()
    conn.close()


def fetch_all(query: str, params: Iterable[Any] = ()) -> list[sqlite3.Row]:
    """
    Execute a query and return all rows.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(query, params)

    rows = cur.fetchall()

    conn.close()

    return rows
