# DR-Core-Lite-deterministic-observation-core

## DR Core Lite

**Deterministic Observation Core**

DR Core Lite is a lean deterministic system for collecting, parsing, and reporting system and network environment observations using stable, proven operating-system tools.

The system is intentionally minimal and transparent. Each external program is executed by its own script, each parser is isolated, and a thin wrapper orchestrates the full run sequence.

### Architecture Principles

* Deterministic behavior
* Tool transparency
* Minimal hidden logic
* Easy rebuild and debugging
* Explicit artifact generation

DR Core Lite is designed as a trusted baseline observation system that can be inspected, modified, or rebuilt quickly.

---

## Design Philosophy

### Deterministic Execution

The system produces identical outputs given the same environment and configuration.
Pipeline stages are:

**Tool Execution → Parsing → Storage → Reporting**

Each stage is isolated and inspectable.

---

### One Program per Script

Every external program runs in its own dedicated script:

* `tool_ip.py`
* `tool_iw.py`
* `tool_rfkill.py`
* `tool_nmcli.py`
* `tool_ethtool.py`

Benefits:

* Clear understanding of each tool
* Easier debugging and testing
* Safer refactoring
* Learning platform for system tools

---

### Thin Wrapper Architecture

A single wrapper provides entry points without altering individual scripts:

```bash
dr-core-lite doctor
dr-core-lite collect
dr-core-lite report
dr-core-lite all
```

The wrapper orchestrates execution of all scripts while preserving isolation.

---

### Minimal Abstraction

The system avoids complex frameworks or hidden automation.

Technologies used:

* Python
* SQLite
* Native Linux tools

Focus is on clarity, control, and reproducibility.

---

## System Pipeline

### 1. Tool Execution

External programs gather environment data. Examples:

* `ip`
* `iw`
* `rfkill`
* `nmcli`
* `ethtool`

Optional capture tools are used if enabled.
Outputs are stored as raw artifacts.

---

### 2. Parsing

Dedicated parser modules convert raw tool output into structured data.

Examples:

* `parse_iw.py`
* `parse_nmcli.py`
* `parse_rfkill.py`

Parsers generate deterministic JSON records.

---

### 3. Storage

Parsed observations are stored in SQLite:

* Run history
* Tool outputs
* Parsed observations
* Artifact references

Enables historical analysis and comparisons.

---

### 4. Reporting

Reports summarize stored observations:

* Environment summaries
* Tool output summaries
* Structured JSON
* Human-readable summaries

Reports are deterministic functions of stored state.

---

## Repository Structure

```
dr-core-lite/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── bin/
│   └── dr-core-lite
│
├── config/
│   ├── system.yaml
│   ├── tags.yaml
│   └── thresholds.yaml
│
├── data/
│   ├── db/
│   │   └── core.db
│   ├── artifacts/
│   │   ├── raw/
│   │   ├── parsed/
│   │   └── reports/
│   └── logs/
│       └── core.log
│
├── docs/
│   ├── architecture.md
│   ├── tool_map.md
│   ├── artifact_model.md
│   └── runbook.md
│
├── src/
│   └── dr_core_lite/
│       ├── main_wrapper.py
│       ├── doctor_env.py
│       ├── db_store.py
│       ├── report_summary.py
│       ├── tag_rules.py
│       │
│       ├── tools/
│       │   ├── tool_ip.py
│       │   ├── tool_iw.py
│       │   ├── tool_rfkill.py
│       │   ├── tool_nmcli.py
│       │   ├── tool_ethtool.py
│       │   ├── tool_tcpdump.py
│       │   ├── tool_dumpcap.py
│       │   └── tool_tshark.py
│       │
│       ├── parsers/
│       │   ├── parse_ip.py
│       │   ├── parse_iw.py
│       │   ├── parse_rfkill.py
│       │   ├── parse_nmcli.py
│       │   ├── parse_ethtool.py
│       │   └── parse_tshark.py
│       │
│       └── helpers/
│           ├── paths.py
│           ├── subprocess_safe.py
│           ├── jsonio.py
│           ├── sqlite_utils.py
│           ├── time_utils.py
│           └── log_utils.py
│
├── tests/
│   ├── test_tools.py
│   ├── test_parsers.py
│   ├── test_db.py
│   └── test_reports.py
│
└── scripts/
    ├── bootstrap.sh
    └── verify_env.sh
```

---

## Core Commands

### `doctor`

Validates environment:

* Required programs
* Python version
* Directory structure
* Database accessibility

```bash
dr-core-lite doctor
```

---

### `collect`

Executes observation tools and collects raw artifacts:

* `ip`
* `rfkill`
* `iw`
* `nmcli`
* `ethtool`

Optional capture tools may also run.

```bash
dr-core-lite collect
```

---

### `report`

Generates summaries from stored observations:

* JSON summary
* Text report
* Artifact references

```bash
dr-core-lite report
```

---

### `all`

Runs the full deterministic pipeline:

```bash
dr-core-lite all
# doctor → collect → parse → store → report
```

---

## System Programs Used

**Required:**

* python3
* sqlite3
* ip
* iw
* rfkill
* nmcli
* ethtool

**Optional Capture Tools:**

* tcpdump
* dumpcap
* tshark

---

## Artifact Model

**Raw Artifacts:**
Direct output from system tools:

```
data/artifacts/raw/ip/
data/artifacts/raw/iw/
data/artifacts/raw/rfkill/
```

**Parsed Artifacts:**
Structured JSON representations:

```
interfaces.json
wireless_scan.json
radio_state.json
driver_info.json
```

**Reports:**
Human-readable summaries:

```
summary.txt
summary.json
doctor.txt
```

---

## Database Model

SQLite stores observations and run metadata.

**Core tables:**

* runs
* tool_runs
* interfaces
* access_points
* radio_state
* driver_info
* artifacts
* tags

The database links each observation to the producing run.

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

DR Core Lite is:

* A deterministic observation baseline
* A transparent system diagnostics tool
* A learning platform for system tools
* A trusted fallback architecture

Emphasizes reliability, clarity, and reproducibility over automation complexity.

---

## License

Open architecture reference implementation.
