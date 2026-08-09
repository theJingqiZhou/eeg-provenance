from __future__ import annotations

import json

from scripts import probe_toolchain


def test_probe_reports_packages_and_commands_without_executing_them(
    monkeypatch,
) -> None:
    versions = {"mne": "1.12.1", "pybids": "0.22.0"}
    calls: list[str] = []

    def fake_version(name: str) -> str:
        calls.append(f"package:{name}")
        if name in versions:
            return versions[name]
        raise probe_toolchain.metadata.PackageNotFoundError(name)

    def fake_which(name: str) -> str | None:
        calls.append(f"command:{name}")
        return f"/tools/{name}" if name in {"git", "matlab"} else None

    monkeypatch.setattr(probe_toolchain.metadata, "version", fake_version)
    monkeypatch.setattr(probe_toolchain.shutil, "which", fake_which)

    result = probe_toolchain.collect_capabilities()

    assert result["schema_version"] == "1.2.0"
    assert result["probe_scope"] == "current process environment only"
    assert result["python_distributions"]["mne"] == {
        "available": True,
        "version": "1.12.1",
    }
    assert result["python_distributions"]["braindecode"] == {
        "available": False,
        "version": None,
    }
    assert result["commands"]["matlab"] == {
        "available": True,
        "path": "/tools/matlab",
    }
    assert result["commands"]["openneuro"] == {
        "available": False,
        "path": None,
    }
    assert {
        "compiler",
        "skill_python_window",
        "within_skill_python_window",
        "machine",
        "sysconfig_platform",
        "pointer_bits",
        "libc",
        "prefix",
        "base_prefix",
        "in_virtual_environment",
        "externally_managed_marker",
    } <= result["runtime"].keys()
    assert result["runtime"]["skill_python_window"] == ">=3.10,<3.15"
    assert len(calls) == len(probe_toolchain.PYTHON_DISTRIBUTIONS) + len(
        probe_toolchain.COMMANDS
    )


def test_probe_cli_emits_machine_readable_json(capsys) -> None:
    assert probe_toolchain.main(["--compact"]) == 0
    parsed = json.loads(capsys.readouterr().out)
    assert {"runtime", "python_distributions", "commands"} <= parsed.keys()


def test_intent_resolves_only_decision_relevant_capabilities() -> None:
    packages, commands = probe_toolchain.resolve_selection(("bids-query",), ())
    assert packages == ("mne-bids", "pybids")
    assert commands == ()


def test_probe_cli_filters_explicit_tools(capsys) -> None:
    assert probe_toolchain.main(["--tools", "mne,pyedflib", "--compact"]) == 0
    parsed = json.loads(capsys.readouterr().out)
    assert set(parsed["python_distributions"]) == {"mne", "pyedflib"}
    assert parsed["commands"] == {}
    assert parsed["requested_intents"] == []


def test_runtime_intent_inventories_stack_and_environment_managers() -> None:
    packages, commands = probe_toolchain.resolve_selection(("runtime-compat",), ())
    for package in (
        "numpy",
        "scipy",
        "pandas",
        "mne",
        "mne-bids",
        "pybids",
        "eegdash",
        "moabb",
        "braindecode",
        "pyhealth",
        "torcheeg",
        "torch",
        "pip",
    ):
        assert package in packages
    for command in ("conda", "mamba", "micromamba", "uv", "apptainer"):
        assert command in commands
