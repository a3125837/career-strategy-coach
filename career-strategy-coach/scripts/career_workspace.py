from __future__ import annotations

import argparse
import os
import stat
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Sequence


EXPECTED_FILES = ("career-profile.md", "career-strategy.md")
EXPECTED_DIRS = ("plans", "reviews", "decisions")


def resolve_absolute(raw_path: str | Path) -> Path:
    """Resolve a user-supplied path, requiring an absolute path first."""
    path = Path(raw_path)
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
    canonical_target = target.resolve(strict=False)
    canonical_skill_root = skill_root.resolve(strict=False)
    if is_relative_to(canonical_target, canonical_skill_root) or is_relative_to(
        canonical_skill_root, canonical_target
    ):
        raise ValueError("career workspace must be outside the Skill directory")


def _target_exists(target: Path) -> bool:
    """Include dangling symlinks when deciding whether a target exists."""
    return target.exists() or target.is_symlink() or os.path.lexists(str(target))


def _is_link_or_reparse(path: Path) -> bool:
    try:
        details = path.lstat()
    except FileNotFoundError:
        return False
    if stat.S_ISLNK(details.st_mode):
        return True
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(getattr(details, "st_file_attributes", 0) & reparse_flag)


def _path_has_link_or_reparse(path: Path) -> bool:
    current = path
    while True:
        if _is_link_or_reparse(current):
            return True
        parent = current.parent
        if parent == current:
            return False
        current = parent


def _cleanup_staging(staging: Path | None) -> BaseException | None:
    if staging is None:
        return None
    try:
        if _target_exists(staging):
            shutil.rmtree(staging)
    except BaseException as cleanup_error:
        return cleanup_error
    return None


def _report_initialization_failure(
    error: BaseException, cleanup_error: BaseException | None = None
) -> None:
    if isinstance(error, KeyboardInterrupt):
        message = "initialization interrupted"
    else:
        message = f"initialization failed: {error}"
    if cleanup_error is not None:
        message += f"; cleanup failed: {cleanup_error}"
    print(message, file=sys.stderr)


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

    staging: Path | None = None
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(
            tempfile.mkdtemp(
                prefix=f".{target.name}.staging-", dir=str(target.parent)
            )
        )
        for directory in EXPECTED_DIRS:
            (staging / directory).mkdir()
        for filename in EXPECTED_FILES:
            shutil.copyfile(template_root / filename, staging / filename)
        if _target_exists(target):
            raise FileExistsError(f"target appeared during initialization: {target}")
        staging.replace(target)
        staging = None
    except KeyboardInterrupt as exc:
        cleanup_error = _cleanup_staging(staging)
        _report_initialization_failure(exc, cleanup_error)
        return 130
    except Exception as exc:
        cleanup_error = _cleanup_staging(staging)
        _report_initialization_failure(exc, cleanup_error)
        return 2

    print(f"initialized career workspace: {target}")
    for filename in EXPECTED_FILES:
        print(f"created file: {target / filename}")
    for directory in EXPECTED_DIRS:
        print(f"created directory: {target / directory}")
    return 0


def validate_workspace(
    target: Path, skill_root: Path, input_path: Path | None = None
) -> int:
    ensure_outside_skill(target, skill_root)
    workspace_path = input_path or target
    if _path_has_link_or_reparse(workspace_path):
        print(f"linked or reparse workspace path: {workspace_path}", file=sys.stderr)
        return 1
    if not target.is_dir():
        print(f"workspace directory not found: {target}", file=sys.stderr)
        return 1

    problems: list[str] = []
    for filename in EXPECTED_FILES:
        entry = target / filename
        if _is_link_or_reparse(entry):
            problems.append(f"linked or reparse path: {filename}")
        elif not entry.is_file():
            problems.append(f"missing or wrong file: {filename}")
    for directory in EXPECTED_DIRS:
        entry = target / directory
        if _is_link_or_reparse(entry):
            problems.append(f"linked or reparse path: {directory}")
        elif not entry.is_dir():
            problems.append(f"missing or wrong directory: {directory}")

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
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
    try:
        input_path = Path(args.path)
        target = resolve_absolute(input_path)
        skill_root = Path(__file__).resolve().parents[1]
        if args.command == "init":
            return initialize_workspace(target, skill_root)
        lexical_path = Path(os.path.abspath(input_path))
        return validate_workspace(target, skill_root, lexical_path)
    except KeyboardInterrupt as exc:
        _report_initialization_failure(exc)
        return 130
    except (OSError, RuntimeError) as exc:
        print(f"path operation failed: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
