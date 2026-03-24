#!/usr/bin/env python3
from dr_core_lite.helpers.paths import RAW_DIR
import subprocess, os, shutil

def run_command(cmd):
    if shutil.which(cmd[0]) is None:
        return f"[!] Command not found: {cmd[0]}\n"
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return result.stdout
    except Exception as e:
        return f"[!] Error running {cmd}: {e}\n"

def run():
    os.makedirs(RAW_DIR, exist_ok=True)
    cmd = ['sudo','ethtool','-i','lo']
    output = run_command(cmd)
    raw_path = os.path.join(RAW_DIR, 'ethtool_raw.txt')
    with open(raw_path, 'w') as f:
        f.write(output)
    return output

if __name__ == "__main__":
    run()
