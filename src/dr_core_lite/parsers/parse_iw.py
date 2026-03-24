#!/usr/bin/env python3
from dr_core_lite.helpers.paths import RAW_DIR, PARSED_DIR
import os, json

def parse_iw():
    raw_file = os.path.join(RAW_DIR, "iw_raw.txt")
    parsed_file = os.path.join(PARSED_DIR, "wireless.json")

    parsed = []
    if os.path.exists(raw_file):
        with open(raw_file, "r") as f:
            current_iface = {}
            for line in f:
                line = line.strip()
                if line.startswith("Interface"):
                    current_iface = {"name": line.split()[1]}
                    parsed.append(current_iface)
                elif line.startswith("addr") and current_iface:
                    current_iface["mac"] = line.split()[1]
                elif line.startswith("type") and current_iface:
                    current_iface["type"] = line.split()[1]
                elif line.startswith("txpower") and current_iface:
                    current_iface["txpower"] = line.split()[1]

    os.makedirs(PARSED_DIR, exist_ok=True)
    with open(parsed_file, "w") as f:
        json.dump(parsed, f, indent=2)
    return parsed

if __name__ == "__main__":
    parse_iw()
