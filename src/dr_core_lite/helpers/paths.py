import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/artifacts"))
RAW_DIR = os.path.join(BASE_DIR, "raw")
PARSED_DIR = os.path.join(BASE_DIR, "parsed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/logs"))

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/db"))
DB_FILE = os.path.join(DB_DIR, "core.db")

# Ensure directories exist
for d in [RAW_DIR, PARSED_DIR, REPORTS_DIR, LOGS_DIR, DB_DIR]:
    os.makedirs(d, exist_ok=True)
