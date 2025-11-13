#!/usr/bin/env python
"""Watch for source changes and rerun the CLI command."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from watchfiles import run_process

SOURCE_DIR = Path("/app/src")


def launch() -> None:
    """Run the CLI with the provided arguments."""
    cmd = ["python", "-m", "src.cli", *sys.argv[1:]]
    subprocess.run(cmd, check=False)


def main() -> None:
    run_process(str(SOURCE_DIR), target=launch)


if __name__ == "__main__":
    main()


