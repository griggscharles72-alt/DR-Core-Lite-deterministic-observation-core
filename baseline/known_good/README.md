# DR-Core-Lite-deterministic-observation-core
:::writing{variant=“standard” id=“40271”}

DR Core Lite

Deterministic Observation Core

DR Core Lite is a lean deterministic system for collecting, parsing, and reporting system and network environment observations using proven operating-system tools.

The system is intentionally minimal and transparent. Every external program is executed by its own script, every parser is isolated, and a single wrapper orchestrates the full run sequence.

The architecture emphasizes:
	•	deterministic behavior
	•	tool transparency
	•	minimal hidden logic
	•	easy rebuild and debugging
	•	explicit artifact generation

DR Core Lite is designed as a trusted baseline observation system that can be inspected, modified, or rebuilt quickly.

⸻

Design Philosophy

The project follows several strict design principles.

Deterministic Execution

Given the same environment and configuration, the system should produce identical outputs.

The pipeline is structured as:

Tool Execution → Parsing → Storage → Reporting

Each stage is isolated and inspectable.

⸻

One Program per Script

Each external system program is executed by its own script.

Examples:

tool_ip.py
tool_iw.py
tool_rfkill.py
tool_nmcli.py
tool_ethtool.py

This allows:
	•	clear understanding of each tool
	•	easier debugging
	•	safer refactoring
	•	easier learning of system tools

⸻

Thin Wrapper Architecture

The wrapper provides a single entry point while leaving individual scripts intact.

dr-core-lite doctor
dr-core-lite collect
dr-core-lite report
dr-core-lite all

Internally, the wrapper simply orchestrates the scripts.

⸻

Minimal Abstraction

The system avoids complex frameworks or hidden automation.

Instead it uses:
	•	Python
	•	SQLite
	•	native Linux tools

The goal is clarity and control rather than abstraction.

⸻

System Pipeline

The execution pipeline follows four stages.

1. Tool Execution

External programs gather environment data.

Examples:
	•	ip
	•	iw
	•	rfkill
	•	nmcli
	•	ethtool

Optional capture tools may also be used.

The output of each program is stored as a raw artifact.

⸻

2. Parsing

Dedicated parser modules transform raw program output into structured data.

Each parser is specific to one tool.

Example:

parse_iw.py
parse_nmcli.py
parse_rfkill.py

Parsers convert raw output into deterministic JSON records.

⸻

3. Storage

Parsed observations are stored in SQLite.

The database preserves:
	•	run history
	•	tool outputs
	•	parsed observations
	•	artifact references

This allows later analysis and comparisons.

⸻

4. Reporting

Reports are generated from stored observations.

Reports include:
	•	environment summaries
	•	tool output summaries
	•	structured JSON data
	•	human-readable reports

Reports are deterministic functions of stored state.

⸻

Repository Structure

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


⸻

Core Commands

doctor

Performs environment validation.

Checks:
	•	required system programs
	•	Python version
	•	directory structure
	•	database accessibility

Example:

dr-core-lite doctor


⸻

collect

Executes all observation tools and collects raw artifacts.

The collect command runs the following programs:
	•	ip
	•	rfkill
	•	iw
	•	nmcli
	•	ethtool

Optional capture tools may also run.

Example:

dr-core-lite collect


⸻

report

Generates summaries from stored observations.

Outputs include:
	•	JSON summary
	•	text report
	•	artifact references

Example:

dr-core-lite report


⸻

all

Runs the full pipeline.

doctor → collect → parse → store → report

Example:

dr-core-lite all


⸻

System Programs Used

The baseline system relies on a small set of stable Linux utilities.

Required Programs

python3
sqlite3
ip
iw
rfkill
nmcli
ethtool

Optional Capture Tools

tcpdump
dumpcap
tshark

These tools are used only if capture analysis is enabled.

⸻

Artifact Model

Artifacts are stored under the data/artifacts directory.

Raw Artifacts

Outputs directly captured from system tools.

Example:

data/artifacts/raw/ip/
data/artifacts/raw/iw/
data/artifacts/raw/rfkill/


⸻

Parsed Artifacts

Structured JSON representations of raw tool output.

Example:

interfaces.json
wireless_scan.json
radio_state.json
driver_info.json


⸻

Reports

Human-readable summaries.

Example:

summary.txt
summary.json
doctor.txt


⸻

Database Model

The system uses a small SQLite database.

Core tables include:

runs
tool_runs
interfaces
access_points
radio_state
driver_info
artifacts
tags

The database records the relationship between observations and the runs that produced them.

⸻

Installation

Clone the repository and install dependencies.

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Verify environment:

./bin/dr-core-lite doctor


⸻

Intended Use

DR Core Lite is designed as:
	•	a deterministic observation baseline
	•	a transparent system diagnostics tool
	•	a learning platform for system tools
	•	a trusted fallback architecture

It prioritizes reliability and clarity over automation complexity.

⸻

License

Open architecture reference implementation.
:::
