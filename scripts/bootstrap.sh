#!/usr/bin/env bash

# DR Core Lite — Environment Bootstrap Script

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "DR Core Lite Bootstrap"
echo "Repository: $REPO_ROOT"
echo ""

# --------------------------------------------------
# Verify Python
# --------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 not installed"
    exit 1
fi

echo "Python found: $(python3 --version)"

# --------------------------------------------------
# Create Virtual Environment
# --------------------------------------------------

echo ""
echo "Creating virtual environment..."

python3 -m venv "$REPO_ROOT/.venv"

source "$REPO_ROOT/.venv/bin/activate"

echo "Virtual environment activated"

# --------------------------------------------------
# Upgrade pip
# --------------------------------------------------

echo ""
echo "Upgrading pip..."

pip install --upgrade pip setuptools wheel

# --------------------------------------------------
# Install dependencies
# --------------------------------------------------

echo ""
echo "Installing project dependencies..."

pip install -r "$REPO_ROOT/requirements.txt"

# --------------------------------------------------
# Verify required system tools
# --------------------------------------------------

echo ""
echo "Checking system tools..."

TOOLS=(
python3
sqlite3
ip
iw
rfkill
nmcli
ethtool
)

for tool in "${TOOLS[@]}"; do

    if command -v "$tool" >/dev/null 2>&1; then
        echo "OK: $tool"
    else
        echo "ERROR: required tool missing -> $tool"
        exit 1
    fi

done

# --------------------------------------------------
# Prepare directories
# --------------------------------------------------

echo ""
echo "Preparing directories..."

mkdir -p "$REPO_ROOT/data/db"
mkdir -p "$REPO_ROOT/data/artifacts/raw"
mkdir -p "$REPO_ROOT/data/artifacts/parsed"
mkdir -p "$REPO_ROOT/data/artifacts/reports"
mkdir -p "$REPO_ROOT/data/logs"

echo "Directory structure ready"

# --------------------------------------------------
# Finish
# --------------------------------------------------

echo ""
echo "Bootstrap complete"
echo ""
echo "Next step:"
echo "chmod +x bin/dr-core-lite"
echo "bin/dr-core-lite doctor"
