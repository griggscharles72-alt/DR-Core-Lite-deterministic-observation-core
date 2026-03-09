#!/usr/bin/env python3

"""
DR Core Lite — Environment Doctor

Purpose
-------
Validate the local runtime environment before collection begins.

Checks
------
- Python version
- Required external programs
- Required directories
- SQLite availability
- Basic write access

This module is intentionally simple and deterministic.
"""

from __future__ import annotations

import os
import shutil
import sqlite3
import sys
from pathlib import Path
from typing import List, Tuple

from dr_core_lite.helpers.paths import (
    REPO_ROOT,
    DATA_DIR,
    DB_DIR,
    ARTIFACTS_DIR,
    RAW_DIR,
    PARSED_DIR,
    REPORTS_DIR,
    LOGS_DIR,
)
from dr_core_lite.helpers.log_utils import log_line


REQUIRED_PROGRAMS = [
    "python3",
    "sqlite3",
    "ip",
    "iw",
    "rfkill",
    "nmcli",
    "ethtool",
]

OPTIONAL_PROGRAMS = [
    "tcpdump",
    "dumpcap",
    "tshark",
]

MIN_PYTHON = (3, 10)


def _check_python_version() -> Tuple[bool, str]:
    current = sys.version_info[:2]
    ok = current >= MIN_PYTHON
    msg = f"Python version: detected {current[0]}.{current[1]}, required >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]}"
    return ok, msg


def _check_program_exists(name: str) -> Tuple[bool, str]:
    path = shutil.which(name)
    ok = path is not None
    msg = f"{name}: {'FOUND' if ok else 'MISSING'}" + (f" at {path}" if path else "")
    return ok, msg


def _ensure_directory(path: Path) -> Tuple[bool, str]:
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True, f"Directory OK: {path}"
    except Exception as exc:
        return False, f"Directory ERROR: {path} :: {exc}"


def _check_write_access(path: Path) -> Tuple[bool, str]:
    probe = path / ".write_test"
    try:
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return True, f"Write OK: {path}"
    except Exception as exc:
        return False, f"Write ERROR: {path} :: {exc}"


def _check_sqlite() -> Tuple[bool, str]:
    test_db = DB_DIR / "doctor_test.db"
    try:
        conn = sqlite3.connect(str(test_db))
        conn.execute("CREATE TABLE IF NOT EXISTS doctor_probe (id INTEGER PRIMARY KEY, note TEXT)")
        conn.commit()
        conn.close()
        test_db.unlink(missing_ok=True)
        return True, "SQLite OK"
    except Exception as exc:
        return False, f"SQLite ERROR :: {exc}"


def _print_result(ok: bool, message: str) -> None:
    prefix = "[OK]" if ok else "[FAIL]"
    print(f"{prefix} {message}")


def run_doctor() -> None:
    """
    Run all environment checks and exit with a failure code if required checks fail.
    """

    print("== DR Core Lite :: doctor ==")
    print(f"Repo root: {REPO_ROOT}")

    failures: List[str] = []

    checks: List[Tuple[bool, str]] = []

    checks.append(_check_python_version())

    for program in REQUIRED_PROGRAMS:
        checks.append(_check_program_exists(program))

    for directory in [DATA_DIR, DB_DIR, ARTIFACTS_DIR, RAW_DIR, PARSED_DIR, REPORTS_DIR, LOGS_DIR]:
        checks.append(_ensure_directory(directory))
        checks.append(_check_write_access(directory))

    checks.append(_check_sqlite())

    print("\nRequired checks:")
    for ok, msg in checks:
        _print_result(ok, msg)
        log_line(LOGS_DIR / "core.log", f"doctor :: {msg}")
        if not ok:
            failures.append(msg)

    print("\nOptional tools:")
    for program in OPTIONAL_PROGRAMS:
        ok, msg = _check_program_exists(program)
        _print_result(ok, msg)
        log_line(LOGS_DIR / "core.log", f"doctor_optional :: {msg}")

    if failures:
        print("\nDoctor result: FAILED")
        for item in failures:
            print(f" - {item}")
        raise SystemExit(1)

    print("\nDoctor result: OK")
