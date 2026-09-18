import contextlib
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "career-strategy-coach" / "scripts" / "career_workspace.py"
SKILL_ROOT = ROOT / "career-strategy-coach"

MODULE_SPEC = importlib.util.spec_from_file_location("career_workspace", SCRIPT)
assert MODULE_SPEC is not None and MODULE_SPEC.loader is not None
career_workspace = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(career_workspace)


def run_cli(*args):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


class CareerWorkspaceCliTests(unittest.TestCase):
    def test_init_creates_expected_workspace_structure(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "new-workspace"
            result = run_cli("init", "--path", str(target))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                sorted(path.relative_to(target).as_posix() for path in target.rglob("*")),
                [
                    "career-profile.md",
                    "career-strategy.md",
                    "decisions",
                    "plans",
                    "reviews",
                ],
            )
            self.assertTrue((target / "career-profile.md").is_file())
            self.assertTrue((target / "career-strategy.md").is_file())
            self.assertTrue((target / "plans").is_dir())
            self.assertTrue((target / "reviews").is_dir())
            self.assertTrue((target / "decisions").is_dir())

    def test_relative_path_is_rejected(self):
        result = run_cli("init", "--path", "relative-target")

        self.assertEqual(result.returncode, 2)
        self.assertIn("absolute path", result.stderr.lower())

    def test_existing_target_is_rejected_without_removing_marker(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "existing-workspace"
            target.mkdir()
            marker = target / "keep.md"
            marker.write_text("keep this marker", encoding="utf-8")

            result = run_cli("init", "--path", str(target))

            self.assertEqual(result.returncode, 2)
            self.assertTrue(marker.is_file())
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep this marker")

    def test_target_inside_skill_root_is_rejected_and_remains_absent(self):
        with tempfile.TemporaryDirectory(dir=SKILL_ROOT) as temp_dir:
            target = Path(temp_dir) / "blocked-target"
            self.assertFalse(target.exists())

            result = run_cli("init", "--path", str(target))

            self.assertEqual(result.returncode, 2)
            self.assertFalse(target.exists())

    def test_overlap_guard_rejects_equal_descendant_and_ancestor_but_allows_sibling(self):
        with self.assertRaises(ValueError):
            career_workspace.ensure_outside_skill(SKILL_ROOT, SKILL_ROOT)
        with self.assertRaises(ValueError):
            career_workspace.ensure_outside_skill(SKILL_ROOT / "nested", SKILL_ROOT)
        with self.assertRaises(ValueError):
            career_workspace.ensure_outside_skill(SKILL_ROOT.parent, SKILL_ROOT)
        career_workspace.ensure_outside_skill(SKILL_ROOT.parent / "sibling", SKILL_ROOT)

        if os.name == "nt":
            with self.assertRaises(ValueError):
                career_workspace.ensure_outside_skill(
                    Path(str(SKILL_ROOT).swapcase()), SKILL_ROOT
                )

    def test_overlap_guard_resolves_existing_symlink_when_supported(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            link = Path(temp_dir) / "skill-link"
            try:
                os.symlink(SKILL_ROOT, link, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("directory symlinks are unavailable")

            with self.assertRaises(ValueError):
                career_workspace.ensure_outside_skill(link, SKILL_ROOT)

    def test_validate_empty_target_reports_missing_profile(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "empty-workspace"
            target.mkdir()

            result = run_cli("validate", "--path", str(target))

            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")
            self.assertIn("career-profile.md", result.stderr)

    def test_validate_initialized_target_succeeds(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "initialized-workspace"
            initialized = run_cli("init", "--path", str(target))
            self.assertEqual(initialized.returncode, 0, initialized.stderr)

            result = run_cli("validate", "--path", str(target))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validate_rejects_linked_entries_when_supported(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            temp_root = Path(temp_dir)
            target = temp_root / "workspace"
            initialized = run_cli("init", "--path", str(target))
            self.assertEqual(initialized.returncode, 0, initialized.stderr)

            external_file = temp_root / "external.md"
            external_file.write_text("not a profile", encoding="utf-8")
            external_dir = temp_root / "external-dir"
            external_dir.mkdir()
            (target / "career-profile.md").unlink()
            shutil.rmtree(target / "plans")
            try:
                os.symlink(external_file, target / "career-profile.md")
                os.symlink(external_dir, target / "plans", target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("file or directory symlinks are unavailable")

            result = run_cli("validate", "--path", str(target))

            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")
            self.assertIn("career-profile.md", result.stderr)
            self.assertIn("plans", result.stderr)

    def test_validate_rejects_linked_workspace_root_when_supported(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            temp_root = Path(temp_dir)
            target = temp_root / "workspace"
            initialized = run_cli("init", "--path", str(target))
            self.assertEqual(initialized.returncode, 0, initialized.stderr)
            linked_target = temp_root / "workspace-link"
            try:
                os.symlink(target, linked_target, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("directory symlinks are unavailable")

            result = run_cli("validate", "--path", str(linked_target))

            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")
            self.assertIn("linked", result.stderr.lower())

    def test_initialize_copy_failure_leaves_target_absent(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "copy-failure"
            with mock.patch.object(
                career_workspace.shutil, "copyfile", side_effect=OSError("copy failed")
            ):
                with contextlib.redirect_stderr(io.StringIO()) as error:
                    result = career_workspace.initialize_workspace(target, SKILL_ROOT)

            self.assertEqual(result, 2)
            self.assertFalse(target.exists())
            self.assertIn("copy failed", error.getvalue())

    def test_initialize_cleanup_failure_preserves_original_error(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "cleanup-failure"
            with mock.patch.object(
                career_workspace.shutil, "copyfile", side_effect=OSError("copy failed")
            ), mock.patch.object(
                career_workspace.shutil, "rmtree", side_effect=OSError("cleanup failed")
            ):
                with contextlib.redirect_stderr(io.StringIO()) as error:
                    result = career_workspace.initialize_workspace(target, SKILL_ROOT)

            self.assertEqual(result, 2)
            self.assertFalse(target.exists())
            self.assertIn("copy failed", error.getvalue())
            self.assertIn("cleanup failed", error.getvalue())
            self.assertNotIn("Traceback", error.getvalue())

    def test_initialize_keyboard_interrupt_leaves_target_absent(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "interrupt"
            with mock.patch.object(
                career_workspace.shutil,
                "copyfile",
                side_effect=KeyboardInterrupt(),
            ):
                with contextlib.redirect_stderr(io.StringIO()) as error:
                    result = career_workspace.initialize_workspace(target, SKILL_ROOT)

            self.assertEqual(result, 130)
            self.assertFalse(target.exists())
            self.assertIn("interrupted", error.getvalue().lower())
            self.assertNotIn("Traceback", error.getvalue())

    def test_main_converts_path_errors_and_keyboard_interrupt(self):
        absolute_target = str(ROOT.parent / "safe-sibling")
        for failure in (OSError("path failed"), RuntimeError("path failed")):
            with self.subTest(failure=type(failure).__name__):
                with mock.patch.object(
                    career_workspace, "resolve_absolute", side_effect=failure
                ):
                    with contextlib.redirect_stderr(io.StringIO()) as error:
                        result = career_workspace.main(
                            ["validate", "--path", absolute_target]
                        )
                self.assertEqual(result, 2)
                self.assertIn("path failed", error.getvalue())
                self.assertNotIn("Traceback", error.getvalue())

        with mock.patch.object(
            career_workspace, "resolve_absolute", side_effect=KeyboardInterrupt()
        ):
            with contextlib.redirect_stderr(io.StringIO()) as error:
                result = career_workspace.main(["validate", "--path", absolute_target])
        self.assertEqual(result, 130)
        self.assertIn("interrupted", error.getvalue().lower())
        self.assertNotIn("Traceback", error.getvalue())


if __name__ == "__main__":
    unittest.main()
