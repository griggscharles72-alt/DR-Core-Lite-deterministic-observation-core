#!/usr/bin/env python3
from dr_core_lite.helpers.paths import RAW_DIR, PARSED_DIR
import os, json

def parse_ip():
    raw_file = os.path.join(RAW_DIR, "ip_raw.txt")
    parsed_file = os.path.join(PARSED_DIR, "interfaces.json")

    parsed = []
    if os.path.exists(raw_file):
        with open(raw_file, "r") as f:
            current_iface = {}
            for line in f:
                line = line.strip()
                if line and line[0].isdigit():
                    parts = line.split(":")
                    current_iface = {"index": parts[0], "name": parts[1].strip()}
                    parsed.append(current_iface)
                elif current_iface and line.startswith("inet "):
                    current_iface["ipv4"] = line.split()[1]
                elif current_iface and line.startswith("inet6 "):
                    current_iface["ipv6"] = line.split()[1]

    os.makedirs(PARSED_DIR, exist_ok=True)
    with open(parsed_file, "w") as f:
        json.dump(parsed, f, indent=2)
    return parsed

if __name__ == "__main__":
    parse_ip()
