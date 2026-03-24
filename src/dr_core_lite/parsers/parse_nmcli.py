#!/usr/bin/env python3
from dr_core_lite.helpers.paths import RAW_DIR, PARSED_DIR
import os, json

def parse_nmcli():
    raw_file = os.path.join(RAW_DIR, "nmcli_raw.txt")
    parsed_file = os.path.join(PARSED_DIR, "connections.json")

    parsed = []
    if os.path.exists(raw_file):
        with open(raw_file, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:  # skip header
                line = line.strip()
                if line:
                    parts = line.split()
                    parsed.append({
                        "device": parts[0],
                        "type": parts[1],
                        "state": parts[2],
                        "connection": parts[3] if len(parts) > 3 else ""
                    })

    os.makedirs(PARSED_DIR, exist_ok=True)
    with open(parsed_file, "w") as f:
        json.dump(parsed, f, indent=2)
    return parsed

if __name__ == "__main__":
    parse_nmcli()
