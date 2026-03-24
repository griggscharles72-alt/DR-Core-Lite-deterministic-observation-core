````markdown
# DR-Core-Lite-deterministic-observation-core

## DR Core Lite

**Deterministic Observation Core – Lite Version**

DR Core Lite is a lean deterministic system for collecting, parsing, and reporting system and network observations using native Linux tools and Python scripts. It prioritizes transparency, reproducibility, and minimal hidden logic.

---

## Architecture Principles

* Deterministic behavior – same input environment produces identical outputs.
* Tool transparency – every external program executed in isolation.
* Minimal hidden logic – explicit scripts and readable code.
* Fast rebuild – database and artifacts can be recreated quickly.
* Explicit artifact generation – structured JSON + human-readable reports.

---

## Design Philosophy

### Deterministic Execution

Pipeline stages:

**Tool Execution → Parsing → Storage → Reporting**

Each stage is isolated and inspectable.

### One Script per Tool

Dedicated scripts for each external program:

* `tool_ip.py`
* `tool_iw.py`
* `tool_rfkill.py`
* `tool_nmcli.py`
* `tool_ethtool.py`

Benefits:

* Simplifies debugging and verification
* Reduces risk of cross-script contamination
* Serves as a learning platform for system diagnostics

### Thin Wrapper Orchestration

The wrapper orchestrates execution:

```bash
dr-core-lite doctor
dr-core-lite collect
dr-core-lite report
dr-core-lite all
````

### Minimal Abstraction

* Python + SQLite + native Linux commands
* Avoids heavy frameworks or hidden automation
* Focus on clarity, control, and reproducibility

---

## System Pipeline

### 1. Tool Execution

Collect environment data via system tools:

* `ip` – network interfaces and IPs
* `iw` – wireless scan info
* `rfkill` – soft/hard block states
* `nmcli` – connections and devices
* `ethtool` – driver and interface info

Optional capture tools:

* `tcpdump`, `dumpcap`, `tshark`

Raw outputs stored in `data/artifacts/raw/`.

---

### 2. Parsing

Dedicated parsers convert raw output into deterministic JSON:

* `parse_ip.py` → `interfaces.json`
* `parse_iw.py` → `wireless.json`
* `parse_rfkill.py` → `radio_state.json`
* `parse_nmcli.py` → `connections.json`
* `parse_ethtool.py` → `driver_info.json`

---

### 3. Storage

SQLite database stores observations and run metadata:

**Tables:**

* `interfaces` – network interfaces
* `wireless` – scanned access points
* `radio_state` – soft/hard blocked states
* `connections` – active connections
* `driver_info` – driver metadata

Run IDs link artifacts and observations.

---

### 4. Reporting

Reports summarize stored observations:

* `summary.txt` – human-readable overview
* `summary.json` – structured JSON report
* `doctor.txt` – environment validation report

Reports are deterministic functions of the stored database state.

---

## Repository Structure

```
dr-core-lite/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── bin/dr-core-lite
├── config/
│   ├── system.yaml
│   ├── tags.yaml
│   └── thresholds.yaml
├── data/
│   ├── db/core.db
│   ├── artifacts/
│   │   ├── raw/
│   │   ├── parsed/
│   │   └── reports/
│   └── logs/core.log
├── docs/
│   ├── architecture.md
│   ├── tool_map.md
│   ├── artifact_model.md
│   └── runbook.md
├── src/dr_core_lite/
│   ├── main_wrapper.py
│   ├── doctor_env.py
│   ├── db_store.py
│   ├── report_summary.py
│   ├── tag_rules.py
│   ├── tools/
│   │   ├── tool_ip.py
│   │   ├── tool_iw.py
│   │   ├── tool_rfkill.py
│   │   ├── tool_nmcli.py
│   │   └── tool_ethtool.py
│   ├── parsers/
│   │   ├── parse_ip.py
│   │   ├── parse_iw.py
│   │   ├── parse_rfkill.py
│   │   ├── parse_nmcli.py
│   │   └── parse_ethtool.py
│   └── helpers/
│       ├── paths.py
│       ├── subprocess_safe.py
│       ├── jsonio.py
│       ├── sqlite_utils.py
│       ├── time_utils.py
│       └── log_utils.py
├── tests/
│   ├── test_tools.py
│   ├── test_parsers.py
│   ├── test_db.py
│   └── test_reports.py
└── scripts/
    ├── bootstrap.sh
    └── verify_env.sh
```

---

## Core Commands

### `doctor`

Validates environment and database accessibility:

```bash
dr-core-lite doctor
```

### `collect`

Runs all observation tools:

```bash
dr-core-lite collect
```

### `report`

Generates deterministic summary reports:

```bash
dr-core-lite report
```

### `all`

Runs full deterministic pipeline:

```bash
dr-core-lite all
# doctor → collect → parse → store → report
```

---

## Installation

```bash
git clone <repo-ssh>
cd DR-Core-Lite-deterministic-observation-core
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./bin/dr-core-lite doctor
```

---

## Intended Use

* Deterministic baseline observation
* Transparent system diagnostics
* Learning platform for Linux networking and tools
* Trusted fallback architecture

---

## License

Open architecture reference implementation.

```
```
