#!/usr/bin/env python3
"""Validate the repository's Podkop skill structure and metadata."""

from pathlib import Path
import re
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
SKILL_DIRS = sorted(ROOT.glob("podkop-*"))


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path}: missing YAML frontmatter")

    parts = text.split("---\n", 2)
    if len(parts) != 3:
        fail(f"{path}: unterminated YAML frontmatter")

    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        fail(f"{path}: frontmatter must be a mapping")
    if set(data) != {"name", "description"}:
        fail(f"{path}: frontmatter must contain only name and description")
    return data


def validate_skill(directory: Path) -> None:
    skill_file = directory / "SKILL.md"
    agent_file = directory / "agents" / "openai.yaml"

    if not skill_file.is_file():
        fail(f"{directory}: missing SKILL.md")
    if not agent_file.is_file():
        fail(f"{directory}: missing agents/openai.yaml")

    metadata = parse_frontmatter(skill_file)
    name = metadata["name"]
    description = metadata["description"]

    if name != directory.name:
        fail(f"{skill_file}: name must match directory")
    if not NAME_RE.fullmatch(name):
        fail(f"{skill_file}: invalid skill name")
    if not isinstance(description, str) or not description.strip():
        fail(f"{skill_file}: description must be non-empty")

    agent = yaml.safe_load(agent_file.read_text(encoding="utf-8"))
    interface = agent.get("interface", {}) if isinstance(agent, dict) else {}
    prompt = interface.get("default_prompt", "")
    if f"${name}" not in prompt:
        fail(f"{agent_file}: default_prompt must mention ${name}")

    text = skill_file.read_text(encoding="utf-8")
    for target in re.findall(r"\]\((references/[^)]+)\)", text):
        if not (directory / target).is_file():
            fail(f"{skill_file}: broken reference {target}")

    if "TODO" in text:
        fail(f"{skill_file}: unresolved TODO")

    print(f"OK: {name}")


def main() -> None:
    if len(SKILL_DIRS) != 5:
        fail(f"expected 5 podkop skills, found {len(SKILL_DIRS)}")
    for directory in SKILL_DIRS:
        validate_skill(directory)


if __name__ == "__main__":
    main()

