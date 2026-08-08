#!/usr/bin/env python3
"""Probe a MATLAB MCP server through initialize, tools/list, and evaluation."""

from __future__ import annotations

import argparse
import json
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, TextIO


class MCPProbe:
    def __init__(self, command: list[str], timeout: float) -> None:
        self.timeout = timeout
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        self.messages: queue.Queue[dict[str, Any]] = queue.Queue()
        self.stderr: list[str] = []
        assert self.process.stdout is not None
        assert self.process.stderr is not None
        threading.Thread(target=self._read_stdout, args=(self.process.stdout,), daemon=True).start()
        threading.Thread(target=self._read_stderr, args=(self.process.stderr,), daemon=True).start()
        self.next_id = 1

    def _read_stdout(self, stream: TextIO) -> None:
        for line in stream:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                message = json.loads(stripped)
            except json.JSONDecodeError:
                self.stderr.append(f"non-JSON stdout: {stripped}")
                continue
            if isinstance(message, dict):
                self.messages.put(message)

    def _read_stderr(self, stream: TextIO) -> None:
        for line in stream:
            self.stderr.append(line.rstrip())

    def send(self, message: dict[str, Any]) -> None:
        if self.process.stdin is None:
            raise RuntimeError("MCP stdin is unavailable")
        self.process.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
        self.process.stdin.flush()

    def request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        request_id = self.next_id
        self.next_id += 1
        self.send({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}})
        deadline = time.monotonic() + self.timeout
        deferred: list[dict[str, Any]] = []
        try:
            while time.monotonic() < deadline:
                if self.process.poll() is not None and self.messages.empty():
                    raise RuntimeError(
                        f"MCP server exited with {self.process.returncode}: " + "\n".join(self.stderr[-20:])
                    )
                remaining = max(0.05, deadline - time.monotonic())
                try:
                    message = self.messages.get(timeout=min(0.5, remaining))
                except queue.Empty:
                    continue
                if message.get("id") == request_id:
                    if "error" in message:
                        raise RuntimeError(f"MCP {method} error: {message['error']}")
                    return message
                deferred.append(message)
            raise TimeoutError(f"timed out waiting for MCP response to {method}")
        finally:
            for message in deferred:
                self.messages.put(message)

    def close(self) -> None:
        if self.process.stdin is not None:
            self.process.stdin.close()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)


def _evaluation_arguments(tool: dict[str, Any], workdir: Path) -> dict[str, str]:
    properties = tool.get("inputSchema", {}).get("properties", {})
    arguments: dict[str, str] = {}
    code = "disp(jsonencode(struct('eeg_provenance_mcp',true,'matlab_version',version)))"
    for name in properties:
        lowered = name.casefold()
        if lowered in {"code", "matlab_code"}:
            arguments[name] = code
        elif lowered in {"project_path", "working_directory", "working_folder", "path"}:
            arguments[name] = str(workdir)
    return arguments


def run_probe(server: Path, matlab_root: Path, workdir: Path, timeout: float) -> dict[str, Any]:
    command = [
        str(server),
        "--matlab-root",
        str(matlab_root),
        "--matlab-display-mode",
        "nodesktop",
        "--matlab-session-mode",
        "auto",
        "--disable-telemetry",
        "true",
        "--initial-working-folder",
        str(workdir),
    ]
    probe = MCPProbe(command, timeout)
    try:
        initialized = probe.request(
            "initialize",
            {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "eeg-provenance-verifier", "version": "1.0.0"},
            },
        )
        probe.send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
        listed = probe.request("tools/list")
        tools = listed.get("result", {}).get("tools", [])
        evaluation = next((tool for tool in tools if tool.get("name") == "evaluate_matlab_code"), None)
        if evaluation is None:
            raise RuntimeError("evaluate_matlab_code is not exposed by the MATLAB MCP server")
        arguments = _evaluation_arguments(evaluation, workdir)
        required = set(evaluation.get("inputSchema", {}).get("required", []))
        if not required <= arguments.keys():
            missing = sorted(required - arguments.keys())
            raise RuntimeError(f"probe does not know how to populate required evaluation fields: {missing}")
        evaluated = probe.request(
            "tools/call",
            {"name": "evaluate_matlab_code", "arguments": arguments},
        )
        result = evaluated.get("result", {})
        if result.get("isError") is True:
            raise RuntimeError(f"MATLAB evaluation returned an MCP tool error: {result}")
        return {
            "protocol_version": initialized.get("result", {}).get("protocolVersion"),
            "server_info": initialized.get("result", {}).get("serverInfo"),
            "tool_count": len(tools),
            "tool_names": sorted(tool.get("name", "") for tool in tools),
            "evaluation_result": result,
            "stderr_tail": probe.stderr[-10:],
        }
    finally:
        probe.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server", type=Path, required=True)
    parser.add_argument("--matlab-root", type=Path, required=True)
    parser.add_argument("--workdir", type=Path, default=Path.cwd())
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args(argv)
    try:
        report = run_probe(args.server.resolve(), args.matlab_root.resolve(), args.workdir.resolve(), args.timeout)
    except (OSError, RuntimeError, TimeoutError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
