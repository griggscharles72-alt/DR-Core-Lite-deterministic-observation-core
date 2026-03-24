#!/usr/bin/env python3
from dr_core_lite.helpers.paths import RAW_DIR, PARSED_DIR
import os, json

def parse_rfkill():
    raw_file = os.path.join(RAW_DIR, "rfkill_raw.txt")
    parsed_file = os.path.join(PARSED_DIR, "radio_state.json")

    parsed = []
    current_dev = {}
    if os.path.exists(raw_file):
        with open(raw_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and ":" in line and not line.startswith(("Soft", "Hard")):
                    if current_dev:
                        parsed.append(current_dev)
                    parts = line.split(":")
                    current_dev = {"index": parts[0], "name": parts[1].strip()}
                elif current_dev and "Soft blocked" in line:
                    current_dev["soft_blocked"] = line.split(":")[1].strip()
                elif current_dev and "Hard blocked" in line:
                    current_dev["hard_blocked"] = line.split(":")[1].strip()
            if current_dev:
                parsed.append(current_dev)

    os.makedirs(PARSED_DIR, exist_ok=True)
    with open(parsed_file, "w") as f:
        json.dump(parsed, f, indent=2)
    return parsed

if __name__ == "__main__":
    parse_rfkill()
