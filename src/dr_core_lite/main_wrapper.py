#!/usr/bin/env python3
import sys
import os
import subprocess

TOOLS_DIR = os.path.join(os.path.dirname(__file__), "tools")
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/artifacts")

def run_tool(tool_name):
    tool_path = os.path.join(TOOLS_DIR, f"tool_{tool_name}.py")
    if os.path.exists(tool_path):
        subprocess.run([sys.executable, tool_path])
    else:
        print(f"[!] Tool {tool_name} not found")

def doctor():
    print("[*] Running environment validation (doctor)")
    for tool in ["ip", "iw", "rfkill", "nmcli", "ethtool"]:
        if subprocess.run(["which", tool], capture_output=True).returncode != 0:
            print(f"[!] Required command '{tool}' not found")
        else:
            print(f"[+] Found {tool}")

def collect():
    print("[*] Collecting artifacts...")
    for tool_file in os.listdir(TOOLS_DIR):
        if tool_file.startswith("tool_") and tool_file.endswith(".py"):
            subprocess.run([sys.executable, os.path.join(TOOLS_DIR, tool_file)])

def report():
    print("[*] Generating report")
    print(f"[+] Reports would be saved in {DATA_DIR}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main_wrapper.py [doctor|collect|report|all]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "doctor":
        doctor()
    elif cmd == "collect":
        collect()
    elif cmd == "report":
        report()
    elif cmd == "all":
        doctor()
        collect()
        report()
    else:
        print(f"[!] Unknown command: {cmd}")
