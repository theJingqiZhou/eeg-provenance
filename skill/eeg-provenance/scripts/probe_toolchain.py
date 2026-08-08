#!/usr/bin/env python3
"""Report local EEG toolchain capabilities without accessing EEG data.

This probe is deliberately descriptive: installation does not make a tool
appropriate for a dataset or endpoint. Use the result with the phase-level
selection procedure in references/toolchain-selection.md.
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys
from importlib import metadata
from typing import Any


SCHEMA_VERSION = "1.0.0"

PYTHON_DISTRIBUTIONS = (
    "autoreject",
    "braindecode",
    "datalad",
    "eegdash",
    "h5io",
    "h5py",
    "mne",
    "mne-bids",
    "mne-icalabel",
    "moabb",
    "pybids",
    "pyedflib",
    "pyhealth",
    "pymatreader",
    "scipy",
    "torcheeg",
)

COMMANDS = (
    "bids-validator",
    "bids-validator-deno",
    "datalad",
    "deno",
    "git",
    "git-annex",
    "matlab",
    "openneuro",
    "rsync",
)


def _distribution_record(name: str) -> dict[str, Any]:
    try:
        version = metadata.version(name)
    except metadata.PackageNotFoundError:
        return {"available": False, "version": None}
    return {"available": True, "version": version}


def _command_record(name: str) -> dict[str, Any]:
    path = shutil.which(name)
    return {"available": path is not None, "path": path}


def collect_capabilities() -> dict[str, Any]:
    """Collect non-invasive runtime, distribution, and command facts."""

    return {
        "schema_version": SCHEMA_VERSION,
        "probe_scope": "current process environment only",
        "runtime": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "executable": sys.executable,
        },
        "python_distributions": {
            name: _distribution_record(name) for name in PYTHON_DISTRIBUTIONS
        },
        "commands": {name: _command_record(name) for name in COMMANDS},
        "interpretation": (
            "Availability only. Verify candidate version, source/release coverage, "
            "read/write scope, and endpoint fit before selection. MATLAB command "
            "availability does not prove that EEGLAB or a required plugin is on "
            "the active MATLAB session path. Rerun this probe inside each WSL, "
            "container, scheduler, notebook, or remote runtime that will execute "
            "a phase."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Emit compact JSON instead of indented JSON.",
    )
    args = parser.parse_args(argv)
    indent = None if args.compact else 2
    print(json.dumps(collect_capabilities(), indent=indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
