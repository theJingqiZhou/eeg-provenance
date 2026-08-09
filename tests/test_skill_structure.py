import re
import tomllib
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skill" / "eeg-provenance"
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
REFERENCE_LINK_RE = re.compile(r"\((references/[^)#]+\.md)(?:#[^)]+)?\)")
LOCAL_REFERENCE_LINK_RE = re.compile(r"\(([^/)#]+\.md)(?:#[^)]+)?\)")


def test_local_markdown_links_resolve() -> None:
    errors: list[str] = []
    paths = [
        SKILL_ROOT / "SKILL.md",
        *sorted((SKILL_ROOT / "references").glob("*.md")),
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_RE.findall(text):
            if "://" in target or target.startswith(("mailto:", "#")):
                continue
            relative = target.split("#", 1)[0]
            if not relative:
                continue
            resolved = (path.parent / relative).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(SKILL_ROOT)} -> {target}")
    assert errors == []


def test_skill_frontmatter_and_ui_metadata() -> None:
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\n")
    _, frontmatter_text, _ = text.split("---", 2)
    frontmatter = yaml.safe_load(frontmatter_text)
    assert set(frontmatter) == {"name", "description"}
    assert frontmatter["name"] == "eeg-provenance"
    assert len(text.splitlines()) < 500

    metadata = yaml.safe_load(
        (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )
    interface = metadata["interface"]
    assert 25 <= len(interface["short_description"]) <= 64
    assert "$eeg-provenance" in interface["default_prompt"]
    assert metadata["policy"]["allow_implicit_invocation"] is True


def test_installable_skill_has_only_canonical_entries() -> None:
    assert SKILL_ROOT.name == "eeg-provenance"
    entries = {path.name for path in SKILL_ROOT.iterdir()}
    assert entries == {"SKILL.md", "agents", "assets", "references", "scripts"}
    assert not (REPO_ROOT / "SKILL.md").exists()
    assert not (REPO_ROOT / "agents").exists()
    assert not (REPO_ROOT / "assets").exists()
    assert not (REPO_ROOT / "references").exists()
    assert not (REPO_ROOT / "scripts").exists()


def _reference_graph() -> tuple[set[str], dict[str, set[str]]]:
    skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    roots = {
        Path(target).name
        for target in REFERENCE_LINK_RE.findall(skill_text)
    }
    graph: dict[str, set[str]] = {}
    for path in (SKILL_ROOT / "references").glob("*.md"):
        graph[path.name] = set(LOCAL_REFERENCE_LINK_RE.findall(
            path.read_text(encoding="utf-8")
        ))
    return roots, graph


def test_reference_graph_is_bounded_reachable_and_acyclic() -> None:
    roots, graph = _reference_graph()
    assert roots == {
        "dataset-intake.md",
        "pipeline.md",
        "runtime-compatibility.md",
        "provenance-ledger.md",
        "evidence-register.md",
    }

    distance = {name: 1 for name in roots}
    frontier = list(roots)
    while frontier:
        parent = frontier.pop(0)
        for child in graph[parent]:
            assert child in graph, f"unknown reference target: {parent} -> {child}"
            if child not in distance:
                distance[child] = distance[parent] + 1
                frontier.append(child)
    assert set(distance) == set(graph)
    assert max(distance.values()) <= 2

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str) -> None:
        assert name not in visiting, f"reference cycle reaches {name}"
        if name in visited:
            return
        visiting.add(name)
        for child in graph[name]:
            visit(child)
        visiting.remove(name)
        visited.add(name)

    for name in graph:
        visit(name)


def test_top_level_routes_have_explicit_activation_conditions() -> None:
    skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    resource_map = skill_text.split("## Resource map", 1)[1].split(
        "## Stop conditions", 1
    )[0]
    assert "Load only a resource whose condition is true" in resource_map
    for target in REFERENCE_LINK_RE.findall(resource_map):
        assert resource_map.count(f"]({target})") == 1


def test_long_references_have_contents_navigation() -> None:
    for path in (SKILL_ROOT / "references").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if len(text.splitlines()) > 100:
            assert re.search(r"^## (?:Contents|Table of contents)$", text, re.MULTILINE), path


def test_bids_contract_has_version_pinned_public_sources() -> None:
    contract = (SKILL_ROOT / "references" / "bids-eeg-1.11.1.md").read_text(
        encoding="utf-8"
    )
    evidence = (SKILL_ROOT / "references" / "evidence-register.md").read_text(
        encoding="utf-8"
    )
    for text in (contract, evidence):
        assert "bids-specification.readthedocs.io/en/v1.11.1/" in text
        assert "bids-specification.readthedocs.io/en/stable/" not in text
        assert "PDF pp." not in text
    assert "supplied 805-page" not in contract
    assert "## Normative source map" in contract


def test_legacy_skill_mirrors_are_absent() -> None:
    assert not (SKILL_ROOT / "README.md").exists()
    assert not (REPO_ROOT / ".agents").exists()
    claude_root = REPO_ROOT / ".claude"
    if claude_root.exists():
        local_files = {
            path.relative_to(claude_root)
            for path in claude_root.rglob("*")
            if path.is_file()
        }
        assert local_files <= {Path("settings.local.json")}
    assert not (SKILL_ROOT / "references" / "MNE Resources").exists()
    assert not (SKILL_ROOT / "references" / "NumPy Resources").exists()
    assert not (SKILL_ROOT / "references" / "SciPy Resources").exists()


def test_optional_framework_contracts_have_isolated_ci_lanes() -> None:
    framework_workflow = yaml.safe_load(
        (REPO_ROOT / ".github" / "workflows" / "framework-contracts.yml").read_text(
            encoding="utf-8"
        )
    )
    jobs = framework_workflow["jobs"]
    assert {
        "braindecode-contract",
        "moabb-contract",
        "pyhealth-contract",
    } <= set(jobs)
    commands = {
        name: "\n".join(
            step.get("run", "") for step in job["steps"] if "run" in step
        )
        for name, job in jobs.items()
    }
    assert "--group braindecode --locked" in commands["braindecode-contract"]
    assert "--group adapters --locked" in commands["moabb-contract"]
    assert "--only-group pyhealth --locked" in commands["pyhealth-contract"]

    core_workflow = (
        REPO_ROOT / ".github" / "workflows" / "ci.yml"
    ).read_text(encoding="utf-8")
    for marker in ("not adapters", "not braindecode", "not pyhealth"):
        assert marker in core_workflow

    project = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert "pyhealth==2.0.1" in project["dependency-groups"]["pyhealth"]
    assert project["tool"]["uv"]["sources"]["torch"] == {
        "index": "pytorch-cpu"
    }
