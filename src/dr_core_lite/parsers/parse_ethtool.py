#!/usr/bin/env python3
from dr_core_lite.helpers.paths import RAW_DIR, PARSED_DIR
import os, json

def parse_ethtool():
    raw_file = os.path.join(RAW_DIR, "ethtool_raw.txt")
    parsed_file = os.path.join(PARSED_DIR, "driver_info.json")

    parsed = {}
    if os.path.exists(raw_file):
        with open(raw_file, "r") as f:
            for line in f:
                line = line.strip()
                if ":" in line:
                    k, v = line.split(":", 1)
                    parsed[k.strip()] = v.strip()

    os.makedirs(PARSED_DIR, exist_ok=True)
    with open(parsed_file, "w") as f:
        json.dump(parsed, f, indent=2)
    return parsed

if __name__ == "__main__":
    parse_ethtool()
