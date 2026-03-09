#!/usr/bin/env python3

"""
DR Core Lite — Report Generator

Purpose
-------
Generate human-readable and JSON summaries from stored observation data.
"""

from __future__ import annotations

from pathlib import Path

from dr_core_lite.helpers.sqlite_utils import fetch_all
from dr_core_lite.helpers.paths import REPORTS_DIR
from dr_core_lite.helpers.jsonio import write_json
from dr_core_lite.helpers.time_utils import utc_now


def generate_report() -> None:
    """
    Generate summary reports from the database.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    interfaces = fetch_all("SELECT * FROM interfaces")
    access_points = fetch_all("SELECT * FROM access_points")
    artifacts = fetch_all("SELECT * FROM artifacts")

    summary = {
        "generated_at": utc_now(),
        "interface_count": len(interfaces),
        "access_point_count": len(access_points),
        "artifact_count": len(artifacts),
        "interfaces": [dict(row) for row in interfaces],
        "access_points": [dict(row) for row in access_points],
    }

    json_path = REPORTS_DIR / "summary.json"
    txt_path = REPORTS_DIR / "summary.txt"

    write_json(json_path, summary)

    with txt_path.open("w", encoding="utf-8") as f:

        f.write("DR Core Lite Observation Summary\n")
        f.write("--------------------------------\n\n")

        f.write(f"Generated: {summary['generated_at']}\n\n")

        f.write(f"Interfaces detected: {summary['interface_count']}\n")
        f.write(f"Access points detected: {summary['access_point_count']}\n")
        f.write(f"Artifacts recorded: {summary['artifact_count']}\n\n")

        f.write("Interfaces\n")
        f.write("----------\n")

        for iface in summary["interfaces"]:
            f.write(
                f"{iface.get('name')} "
                f"{iface.get('address')} "
                f"{iface.get('state')}\n"
            )

        f.write("\nAccess Points\n")
        f.write("-------------\n")

        for ap in summary["access_points"]:
            f.write(
                f"{ap.get('ssid')} "
                f"{ap.get('bssid')} "
                f"ch:{ap.get('channel')} "
                f"signal:{ap.get('signal')}\n"
            )

    print("Report generated:")
    print(json_path)
    print(txt_path)
