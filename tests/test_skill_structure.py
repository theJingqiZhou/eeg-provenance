import re
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skill" / "eeg-provenance"
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
REFERENCE_LINK_RE = re.compile(r"\((references/[^)#]+\.md)(?:#[^)]+)?\)")


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


def test_every_reference_is_directly_discoverable() -> None:
    skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    linked = set(REFERENCE_LINK_RE.findall(skill_text))
    expected = {
        f"references/{path.name}"
        for path in (SKILL_ROOT / "references").glob("*.md")
    }
    assert linked == expected


def test_long_references_have_contents_navigation() -> None:
    for path in (SKILL_ROOT / "references").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if len(text.splitlines()) > 100:
            assert re.search(r"^## (?:Contents|Table of contents)$", text, re.MULTILINE), path


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
