#!/usr/bin/env python3
"""Report selected local EEG capabilities without accessing EEG data."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import struct
import sys
import sysconfig
from importlib import metadata
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "1.2.0"
SUPPORTED_PYTHON = ">=3.10,<3.15"

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
    "numpy",
    "pandas",
    "pip",
    "pybids",
    "pyedflib",
    "pyhealth",
    "pymatreader",
    "scipy",
    "torch",
    "torchaudio",
    "torcheeg",
)

COMMANDS = (
    "apptainer",
    "bids-validator",
    "bids-validator-deno",
    "conda",
    "datalad",
    "deno",
    "git",
    "git-annex",
    "matlab",
    "mamba",
    "micromamba",
    "openneuro",
    "rsync",
    "singularity",
    "uv",
)

INTENTS = {
    "accession-acquire": {
        "packages": ("datalad", "eegdash"),
        "commands": ("datalad", "git", "git-annex", "openneuro", "rsync"),
    },
    "bids-conformance": {
        "packages": (),
        "commands": ("bids-validator", "bids-validator-deno", "deno"),
    },
    "bids-query": {
        "packages": ("mne-bids", "pybids"),
        "commands": (),
    },
    "framework-cache": {
        "packages": ("braindecode", "pyhealth", "torcheeg"),
        "commands": (),
    },
    "matlab-eeglab": {
        "packages": (),
        "commands": ("matlab",),
    },
    "native-edf": {
        "packages": ("mne", "pyedflib"),
        "commands": (),
    },
    "python-preprocess": {
        "packages": ("autoreject", "braindecode", "mne", "mne-icalabel"),
        "commands": (),
    },
    "runtime-compat": {
        "packages": PYTHON_DISTRIBUTIONS,
        "commands": (
            "apptainer",
            "conda",
            "mamba",
            "micromamba",
            "singularity",
            "uv",
        ),
    },
}


def _distribution_record(name: str) -> dict[str, Any]:
    try:
        version = metadata.version(name)
    except metadata.PackageNotFoundError:
        return {"available": False, "version": None}
    return {"available": True, "version": version}


def _command_record(name: str) -> dict[str, Any]:
    path = shutil.which(name)
    return {"available": path is not None, "path": path}


def _runtime_record() -> dict[str, Any]:
    libc_name, libc_version = platform.libc_ver()
    marker = Path(sysconfig.get_path("stdlib")) / "EXTERNALLY-MANAGED"
    return {
        "python": platform.python_version(),
        "skill_python_window": SUPPORTED_PYTHON,
        "within_skill_python_window": (3, 10) <= sys.version_info[:2] < (3, 15),
        "implementation": platform.python_implementation(),
        "compiler": platform.python_compiler(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "sysconfig_platform": sysconfig.get_platform(),
        "pointer_bits": struct.calcsize("P") * 8,
        "libc": {"name": libc_name or None, "version": libc_version or None},
        "executable": sys.executable,
        "prefix": sys.prefix,
        "base_prefix": sys.base_prefix,
        "in_virtual_environment": sys.prefix != sys.base_prefix,
        "externally_managed_marker": str(marker) if marker.is_file() else None,
    }


def collect_capabilities(
    python_distributions: Iterable[str] = PYTHON_DISTRIBUTIONS,
    commands: Iterable[str] = COMMANDS,
) -> dict[str, Any]:
    """Collect a non-invasive inventory for only the requested candidates."""

    selected_packages = tuple(dict.fromkeys(python_distributions))
    selected_commands = tuple(dict.fromkeys(commands))
    return {
        "schema_version": SCHEMA_VERSION,
        "probe_scope": "current process environment only",
        "runtime": _runtime_record(),
        "python_distributions": {
            name: _distribution_record(name) for name in selected_packages
        },
        "commands": {name: _command_record(name) for name in selected_commands},
        "interpretation": (
            "Availability only. Verify source/release coverage, signatures, "
            "read/write scope, side effects, and endpoint fit before selection. "
            "Probe each WSL, container, scheduler, notebook, or remote runtime "
            "that will actually execute the phase. MATLAB command availability "
            "does not prove EEGLAB or plugin availability in its active session. "
            "Distribution metadata does not prove resolver, wheel, ABI, external "
            "binary, accelerator, or operation-level compatibility. This probe "
            "does not import packages or install, remove, or upgrade anything."
        ),
    }


def resolve_selection(
    intents: Iterable[str] = (),
    tools: Iterable[str] = (),
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Resolve intent presets and explicit names to package/command probes."""

    requested_intents = tuple(intents)
    requested_tools = tuple(tools)
    if not requested_intents and not requested_tools:
        return PYTHON_DISTRIBUTIONS, COMMANDS

    packages: list[str] = []
    commands: list[str] = []
    for intent in requested_intents:
        packages.extend(INTENTS[intent]["packages"])
        commands.extend(INTENTS[intent]["commands"])
    for tool in requested_tools:
        if tool in PYTHON_DISTRIBUTIONS:
            packages.append(tool)
        if tool in COMMANDS:
            commands.append(tool)
        if tool not in PYTHON_DISTRIBUTIONS and tool not in COMMANDS:
            raise ValueError(f"unknown tool: {tool}")
    return tuple(dict.fromkeys(packages)), tuple(dict.fromkeys(commands))


def _split_tools(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(
        name.strip()
        for value in values
        for name in value.split(",")
        if name.strip()
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--intent",
        action="append",
        choices=tuple(INTENTS),
        default=[],
        help="Probe a small preset; repeat to combine intents.",
    )
    parser.add_argument(
        "--tools",
        action="append",
        default=[],
        metavar="NAME[,NAME]",
        help="Probe exact distribution or command names; repeat or comma-separate.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Emit compact JSON instead of indented JSON.",
    )
    args = parser.parse_args(argv)
    try:
        packages, commands = resolve_selection(args.intent, _split_tools(args.tools))
    except ValueError as exc:
        parser.error(str(exc))
    result = collect_capabilities(packages, commands)
    result["requested_intents"] = args.intent
    indent = None if args.compact else 2
    print(json.dumps(result, indent=indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
