import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "career-strategy-coach" / "scripts" / "career_workspace.py"
PYTHON = Path(
    r"C:\Users\45458\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
)


def run_cli(*args):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [str(PYTHON), str(SCRIPT), *args],
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
                {item.name for item in target.iterdir()},
                {"career-profile.md", "career-strategy.md", "plans", "reviews", "decisions"},
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
        target = ROOT / "career-strategy-coach" / "blocked-target"
        self.assertFalse(target.exists())

        result = run_cli("init", "--path", str(target))

        self.assertEqual(result.returncode, 2)
        self.assertFalse(target.exists())

    def test_validate_empty_target_reports_missing_profile(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "empty-workspace"
            target.mkdir()

            result = run_cli("validate", "--path", str(target))

            self.assertEqual(result.returncode, 1)
            self.assertIn("career-profile.md", result.stdout)

    def test_validate_initialized_target_succeeds(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "initialized-workspace"
            initialized = run_cli("init", "--path", str(target))
            self.assertEqual(initialized.returncode, 0, initialized.stderr)

            result = run_cli("validate", "--path", str(target))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
