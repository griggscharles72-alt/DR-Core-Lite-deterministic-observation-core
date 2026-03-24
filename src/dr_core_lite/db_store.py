#!/usr/bin/env python3
import sqlite3
import json
import os
import datetime
import shutil

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/artifacts"))
PARSED_DIR = os.path.join(BASE_DIR, "parsed")
DB_FILE = os.path.join(BASE_DIR, "db", "core.db")

# Ensure directories exist
os.makedirs(PARSED_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

# Fix JSON artifacts: rename "index" keys to "iface_index"
for filename in os.listdir(PARSED_DIR):
    if filename.endswith(".json"):
        path = os.path.join(PARSED_DIR, filename)
        try:
            with open(path, "r") as f:
                data_list = json.load(f)
            if isinstance(data_list, list):
                for item in data_list:
                    if "index" in item:
                        item["iface_index"] = item.pop("index")
            with open(path, "w") as f:
                json.dump(data_list, f, indent=2)
        except Exception as e:
            print(f"[!] Error fixing {filename}: {e}")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS interfaces (
            run_id INTEGER,
            iface_index TEXT,
            name TEXT,
            ipv4 TEXT,
            ipv6 TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS wireless (
            run_id INTEGER,
            name TEXT,
            mac TEXT,
            type TEXT,
            txpower TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS radio_state (
            run_id INTEGER,
            iface_index TEXT,
            name TEXT,
            soft_blocked TEXT,
            hard_blocked TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS connections (
            run_id INTEGER,
            device TEXT,
            type TEXT,
            state TEXT,
            connection TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS driver_info (
            run_id INTEGER,
            key TEXT,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("[+] Database initialized.")

def store_json(json_path, table_name, run_id):
    if not os.path.exists(json_path):
        return
    with open(json_path, "r") as f:
        try:
            data_list = json.load(f)
        except json.JSONDecodeError:
            print(f"[!] Invalid JSON in {json_path}, skipping.")
            return
    if not isinstance(data_list, list):
        print(f"[!] JSON in {json_path} is not a list, skipping.")
        return
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for data in data_list:
        if not isinstance(data, dict):
            continue
        cols = ",".join(f'"{k}"' for k in data.keys())
        placeholders = ",".join("?" for _ in data)
        values = list(data.values())
        try:
            c.execute(f'INSERT INTO {table_name} (run_id, {cols}) VALUES (?, {placeholders})', (run_id, *values))
        except sqlite3.OperationalError as e:
            print(f"[!] SQLite error inserting into {table_name}: {e}")
    conn.commit()
    conn.close()

def run_db_store():
    init_db()
    run_id = int(datetime.datetime.utcnow().timestamp())
    artifact_mapping = [
        ("interfaces.json", "interfaces"),
        ("wireless.json", "wireless"),
        ("radio_state.json", "radio_state"),
        ("connections.json", "connections"),
        ("driver_info.json", "driver_info")
    ]
    for json_file, table in artifact_mapping:
        path = os.path.join(PARSED_DIR, json_file)
        store_json(path, table, run_id)
    print(f"[+] Stored run_id {run_id} into database.")
    return run_id

if __name__ == "__main__":
    run_db_store()
