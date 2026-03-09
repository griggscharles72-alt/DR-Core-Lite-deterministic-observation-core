#!/usr/bin/env python3

"""
DR Core Lite — Path Definitions

Purpose
-------
Centralized filesystem paths used across the project.

All scripts should import paths from this module instead of hardcoding
directory locations.

The repository root is detected automatically.
"""

from pathlib import Path


# ------------------------------------------------------------
# Repository Root
# ------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]


# ------------------------------------------------------------
# Data Directories
# ------------------------------------------------------------

DATA_DIR = REPO_ROOT / "data"

DB_DIR = DATA_DIR / "db"

ARTIFACTS_DIR = DATA_DIR / "artifacts"

RAW_DIR = ARTIFACTS_DIR / "raw"

PARSED_DIR = ARTIFACTS_DIR / "parsed"

REPORTS_DIR = ARTIFACTS_DIR / "reports"

LOGS_DIR = DATA_DIR / "logs"


# ------------------------------------------------------------
# Database
# ------------------------------------------------------------

DB_FILE = DB_DIR / "core.db"


# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------

def ensure_directories():
    """
    Ensure all required directories exist.
    """

    dirs = [
        DATA_DIR,
        DB_DIR,
        ARTIFACTS_DIR,
        RAW_DIR,
        PARSED_DIR,
        REPORTS_DIR,
        LOGS_DIR,
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
