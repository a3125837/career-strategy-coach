from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Sequence


EXPECTED_FILES = ("career-profile.md", "career-strategy.md")
EXPECTED_DIRS = ("plans", "reviews", "decisions")


def resolve_absolute(raw_path: str | Path) -> Path:
    """Resolve a user-supplied path, requiring an absolute path first."""
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        raise ValueError("an absolute path is required")
    return path.resolve(strict=False)


def is_relative_to(candidate: Path, parent: Path) -> bool:
    """Return whether candidate is parent or is nested below parent."""
    try:
        candidate.relative_to(parent)
        return True
    except ValueError:
        return False


def ensure_outside_skill(target: Path, skill_root: Path) -> None:
    """Reject workspaces that overlap the packaged Skill directory."""
    if is_relative_to(target, skill_root):
        raise ValueError("career workspace must be outside the Skill directory")


def _target_exists(target: Path) -> bool:
    """Include dangling symlinks when deciding whether a target exists."""
    return target.exists() or target.is_symlink() or os.path.lexists(str(target))


def initialize_workspace(target: Path, skill_root: Path) -> int:
    ensure_outside_skill(target, skill_root)
    if _target_exists(target):
        print(f"target already exists: {target}", file=sys.stderr)
        return 2

    template_root = skill_root / "assets" / "workspace-template"
    missing_templates = [
        name for name in EXPECTED_FILES if not (template_root / name).is_file()
    ]
    if missing_templates:
        print(
            "missing packaged templates: " + ", ".join(missing_templates),
            file=sys.stderr,
        )
        return 2

    created_target = False
    try:
        target.mkdir(parents=True, exist_ok=False)
        created_target = True
        for directory in EXPECTED_DIRS:
            (target / directory).mkdir()
        for filename in EXPECTED_FILES:
            shutil.copyfile(template_root / filename, target / filename)
    except Exception as exc:
        if created_target and _target_exists(target):
            shutil.rmtree(target)
        print(f"initialization failed: {exc}", file=sys.stderr)
        return 2

    print(f"initialized career workspace: {target}")
    for filename in EXPECTED_FILES:
        print(f"created file: {target / filename}")
    for directory in EXPECTED_DIRS:
        print(f"created directory: {target / directory}")
    return 0


def validate_workspace(target: Path, skill_root: Path) -> int:
    ensure_outside_skill(target, skill_root)
    if not target.is_dir():
        print(f"workspace directory not found: {target}")
        return 1

    problems: list[str] = []
    for filename in EXPECTED_FILES:
        if not (target / filename).is_file():
            problems.append(f"missing or wrong file: {filename}")
    for directory in EXPECTED_DIRS:
        if not (target / directory).is_dir():
            problems.append(f"missing or wrong directory: {directory}")

    if problems:
        for problem in problems:
            print(problem)
        return 1

    print(f"valid career workspace: {target}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage a private Markdown career workspace."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("init", "validate"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("--path", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    skill_root = Path(__file__).resolve().parents[1]
    try:
        target = resolve_absolute(args.path)
        if args.command == "init":
            return initialize_workspace(target, skill_root)
        return validate_workspace(target, skill_root)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
