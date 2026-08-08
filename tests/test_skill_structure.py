import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def test_local_markdown_links_resolve() -> None:
    errors: list[str] = []
    for path in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]:
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_RE.findall(text):
            if "://" in target or target.startswith(("mailto:", "#")):
                continue
            relative = target.split("#", 1)[0]
            if not relative:
                continue
            resolved = (path.parent / relative).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)} -> {target}")
    assert errors == []


def test_skill_frontmatter_and_ui_metadata() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\n")
    _, frontmatter_text, _ = text.split("---", 2)
    frontmatter = yaml.safe_load(frontmatter_text)
    assert set(frontmatter) == {"name", "description"}
    assert frontmatter["name"] == "eeg-provenance"
    assert len(text.splitlines()) < 500

    metadata = yaml.safe_load((ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    interface = metadata["interface"]
    assert 25 <= len(interface["short_description"]) <= 64
    assert "$eeg-provenance" in interface["default_prompt"]
    assert metadata["policy"]["allow_implicit_invocation"] is True


def test_legacy_mirrors_and_duplicate_skill_creator_are_absent() -> None:
    assert not (ROOT / "README.md").exists()
    assert not (ROOT / ".agents").exists()
    assert not (ROOT / ".claude").exists()
    assert not (ROOT / "references" / "MNE Resources").exists()
    assert not (ROOT / "references" / "NumPy Resources").exists()
    assert not (ROOT / "references" / "SciPy Resources").exists()
