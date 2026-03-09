#!/usr/bin/env bash

# DR Core Lite — Environment Verification Script

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "DR Core Lite Environment Verification"
echo "Repository: $REPO_ROOT"
echo ""

# --------------------------------------------------
# Python check
# --------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 not found"
    exit 1
fi

echo "Python: $(python3 --version)"

# --------------------------------------------------
# Virtual environment check
# --------------------------------------------------

if [ -d "$REPO_ROOT/.venv" ]; then
    echo "Virtual environment: OK"
else
    echo "WARNING: .venv not found"
fi

# --------------------------------------------------
# Required tools
# --------------------------------------------------

echo ""
echo "Checking required tools..."

TOOLS=(
ip
iw
rfkill
nmcli
ethtool
sqlite3
)

for tool in "${TOOLS[@]}"; do

    if command -v "$tool" >/dev/null 2>&1; then
        echo "OK: $tool"
    else
        echo "ERROR: missing tool -> $tool"
        exit 1
    fi

done

# --------------------------------------------------
# Directory structure
# --------------------------------------------------

echo ""
echo "Checking directories..."

DIRS=(
data
data/db
data/artifacts
data/artifacts/raw
data/artifacts/parsed
data/artifacts/reports
data/logs
)

for dir in "${DIRS[@]}"; do

    if [ -d "$REPO_ROOT/$dir" ]; then
        echo "OK: $dir"
    else
        echo "ERROR: missing directory -> $dir"
        exit 1
    fi

done

# --------------------------------------------------
# Database location
# --------------------------------------------------

DB_FILE="$REPO_ROOT/data/db/core.db"

touch "$DB_FILE" 2>/dev/null || {
    echo "ERROR: cannot write database file"
    exit 1
}

echo ""
echo "Database location writable"

# --------------------------------------------------
# Finished
# --------------------------------------------------

echo ""
echo "Environment verification complete"
echo "System ready to run"
