#!/usr/bin/env python3

"""
DR Core Lite — Main Wrapper

Purpose
-------
Top-level command interface for the deterministic observation system.

This wrapper orchestrates execution of the individual system scripts.

It intentionally contains minimal logic and only coordinates the pipeline.

Pipeline
--------
doctor → collect → report
"""

import argparse
import sys

from dr_core_lite.doctor_env import run_doctor
from dr_core_lite.tools.tool_ip import run_ip
from dr_core_lite.tools.tool_iw import run_iw
from dr_core_lite.tools.tool_rfkill import run_rfkill
from dr_core_lite.tools.tool_nmcli import run_nmcli
from dr_core_lite.tools.tool_ethtool import run_ethtool

from dr_core_lite.parsers.parse_ip import parse_ip
from dr_core_lite.parsers.parse_iw import parse_iw
from dr_core_lite.parsers.parse_rfkill import parse_rfkill
from dr_core_lite.parsers.parse_nmcli import parse_nmcli
from dr_core_lite.parsers.parse_ethtool import parse_ethtool

from dr_core_lite.db_store import store_records
from dr_core_lite.report_summary import generate_report


def run_collect():
    """
    Executes tool pipeline and stores parsed results.
    """

    print("Running system observation tools...")

    raw_ip = run_ip()
    raw_iw = run_iw()
    raw_rfkill = run_rfkill()
    raw_nmcli = run_nmcli()
    raw_ethtool = run_ethtool()

    print("Parsing tool outputs...")

    parsed_records = []

    parsed_records.extend(parse_ip(raw_ip))
    parsed_records.extend(parse_iw(raw_iw))
    parsed_records.extend(parse_rfkill(raw_rfkill))
    parsed_records.extend(parse_nmcli(raw_nmcli))
    parsed_records.extend(parse_ethtool(raw_ethtool))

    print("Storing records...")

    store_records(parsed_records)

    print("Collection complete.")


def run_all():
    """
    Executes full pipeline.
    """

    run_doctor()
    run_collect()
    generate_report()


def main():

    parser = argparse.ArgumentParser(description="DR Core Lite CLI")

    parser.add_argument(
        "command",
        choices=["doctor", "collect", "report", "all"],
        help="Command to execute"
    )

    args = parser.parse_args()

    if args.command == "doctor":
        run_doctor()

    elif args.command == "collect":
        run_collect()

    elif args.command == "report":
        generate_report()

    elif args.command == "all":
        run_all()

    else:
        print("Unknown command")
        sys.exit(1)


if __name__ == "__main__":
    main()
