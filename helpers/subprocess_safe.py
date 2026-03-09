#!/usr/bin/env python3

"""
DR Core Lite — Safe Subprocess Execution

Purpose
-------
Execute external programs safely and deterministically.

Responsibilities
----------------
- Run system commands
- Capture stdout and stderr
- Apply timeouts
- Provide structured result objects
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import List, Optional


DEFAULT_TIMEOUT = 30


@dataclass
class CommandResult:
    command: List[str]
    returncode: int
    stdout: str
    stderr: str


def run_command(
    command: List[str],
    timeout: Optional[int] = DEFAULT_TIMEOUT
) -> CommandResult:
    """
    Execute a system command safely.

    Parameters
    ----------
    command : list[str]
        Command and arguments
    timeout : int
        Execution timeout in seconds

    Returns
    -------
    CommandResult
    """

    try:
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )

        return CommandResult(
            command=command,
            returncode=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr
        )

    except subprocess.TimeoutExpired as exc:

        return CommandResult(
            command=command,
            returncode=-1,
            stdout=exc.stdout or "",
            stderr=f"TimeoutExpired: {exc}"
        )
