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

    assert result["schema_version"] == "1.0.0"
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
    assert len(calls) == len(probe_toolchain.PYTHON_DISTRIBUTIONS) + len(
        probe_toolchain.COMMANDS
    )


def test_probe_cli_emits_machine_readable_json(capsys) -> None:
    assert probe_toolchain.main(["--compact"]) == 0
    parsed = json.loads(capsys.readouterr().out)
    assert {"runtime", "python_distributions", "commands"} <= parsed.keys()
