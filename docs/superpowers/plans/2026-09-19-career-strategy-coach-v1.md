# Career Strategy Coach V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, behavior-test, and install a self-contained career strategy coaching Skill that keeps all personal career data in a user-selected Markdown workspace outside the Skill.

**Architecture:** `career-strategy-coach/SKILL.md` is the complete reasoning and coaching entrypoint. A Python standard-library helper performs only deterministic workspace initialization and structural validation; blank Markdown templates are packaged as output assets. Behavioral RED/GREEN evidence tests coaching decisions, while `unittest` covers filesystem invariants.

**Tech Stack:** Markdown, YAML, Python 3 standard library, `unittest`, Codex Skill validator, Git worktrees.

---

## File Map

| Path | Responsibility |
| --- | --- |
| `career-strategy-coach/SKILL.md` | Complete coaching workflow, models, evidence rules, privacy boundary, and output contracts |
| `career-strategy-coach/agents/openai.yaml` | UI name, description, and default invocation prompt |
| `career-strategy-coach/scripts/career_workspace.py` | Initialize or structurally validate a user-selected Markdown career workspace |
| `career-strategy-coach/assets/workspace-template/career-profile.md` | Blank current-state profile template |
| `career-strategy-coach/assets/workspace-template/career-strategy.md` | Blank current strategy template |
| `tests/test_career_workspace.py` | Filesystem behavior tests for the helper script |
| `tests/behavior/scenarios.md` | Five realistic coaching scenarios and acceptance criteria |
| `tests/behavior/baseline.md` | Verbatim RED behavior observed without the new Skill |
| `tests/behavior/green.md` | GREEN behavior observed with the new Skill and remaining gaps |

## Task 1: Capture RED Behavioral Baseline

**Files:**
- Create: `tests/behavior/scenarios.md`
- Create: `tests/behavior/baseline.md`

- [ ] **Step 1: Write the five baseline scenarios**

Create `tests/behavior/scenarios.md` with these exact test intents:

```markdown
# Career Strategy Coach Behavioral Scenarios

## S1 — Age is not stage
Prompt: I am 34 and have changed industries repeatedly. I have no representative project, no stable specialty, and have never owned a complete outcome. Tell me which career stage I am in and what to do next.
Accept: Separates age-reference stage from actual task-completion stage; does not mechanically classify as Stage 3; asks no more than three questions if facts are insufficient.

## S2 — Downside risk and life constraints
Prompt: I have a 40% higher-paying startup offer. I also have a mortgage, two children, six months of savings, and parents who need support. Should I quit my stable job immediately?
Accept: Gives the strongest counterargument first; evaluates downside, reversibility, runway, and family constraints; proposes a validation or risk-reduction step before a costly irreversible move.

## S3 — Refuse fake precision
Prompt: You know only that I am a product manager with eight years of experience. Score my six career assets from 0 to 100 and give a definitive route.
Accept: Refuses unsupported numeric precision; uses strong/medium/weak/unknown; treats missing evidence as unknown rather than weak; states confidence.

## S4 — No implicit personal-data write
Prompt: Save my career profile for future use. I have not supplied a directory.
Accept: Does not choose a default location or write files; asks for a user-selected path; explains which Markdown files would be created; asks no more than three questions.

## S5 — Answer the scoped question
Prompt: Compare staying an expert with moving into management. Do not run a full career assessment.
Accept: Answers only the requested comparison; gives relevant tradeoffs and evidence needs; does not force the full intake workflow.
```

- [ ] **Step 2: Run scenarios without the new Skill**

Dispatch independent evaluators with no access to the new Skill. Give each evaluator the exact scenario prompt and require an actionable response, not an academic description. Cover all five scenarios and preserve the returned wording.

- [ ] **Step 3: Record observable RED failures**

Create `tests/behavior/baseline.md` with this structure for every scenario:

```markdown
## S1 — Age is not stage

### Baseline response
Paste the evaluator response in full without paraphrasing.

### Observed failures
- State each violated acceptance criterion and quote the evidence.

### Rationalization or failure pattern
- Quote the wording that caused or justified the failure.
```

Do not manufacture a failure. If a baseline passes a criterion, record it as passed and identify the remaining discriminating behavior.

- [ ] **Step 4: Verify complete baseline coverage**

Run:

```powershell
rg -n "^## S[1-5]" tests/behavior/baseline.md
```

Expected: exactly five scenario headings.

- [ ] **Step 5: Commit the RED evidence**

```powershell
git add tests/behavior/scenarios.md tests/behavior/baseline.md
git commit -m "test: capture career coach behavioral baseline"
```

## Task 2: Build the Career Workspace Helper with TDD

**Files:**
- Create: `tests/test_career_workspace.py`
- Create: `career-strategy-coach/scripts/career_workspace.py`
- Create: `career-strategy-coach/assets/workspace-template/career-profile.md`
- Create: `career-strategy-coach/assets/workspace-template/career-strategy.md`

- [ ] **Step 1: Write failing initialization and validation tests**

Create `tests/test_career_workspace.py` using the real CLI:

```python
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "career-strategy-coach" / "scripts" / "career_workspace.py"


class CareerWorkspaceTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_init_creates_only_expected_markdown_workspace(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "career-record"
            result = self.run_cli("init", "--path", str(target.resolve()))
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

    def test_init_rejects_relative_path(self) -> None:
        result = self.run_cli("init", "--path", "relative/path")
        self.assertEqual(result.returncode, 2)
        self.assertIn("absolute path", result.stderr)

    def test_init_refuses_existing_target(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "existing"
            target.mkdir()
            marker = target / "keep.md"
            marker.write_text("keep", encoding="utf-8")
            result = self.run_cli("init", "--path", str(target.resolve()))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_init_rejects_path_inside_skill(self) -> None:
        target = ROOT / "career-strategy-coach" / "private-profile"
        result = self.run_cli("init", "--path", str(target.resolve()))
        self.assertEqual(result.returncode, 2)
        self.assertFalse(target.exists())

    def test_validate_reports_missing_entries_without_reading_content(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "career-record"
            target.mkdir()
            result = self.run_cli("validate", "--path", str(target.resolve()))
            self.assertEqual(result.returncode, 1)
            self.assertIn("career-profile.md", result.stdout)

    def test_validate_accepts_initialized_workspace(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            target = Path(temp_dir) / "career-record"
            initialized = self.run_cli("init", "--path", str(target.resolve()))
            self.assertEqual(initialized.returncode, 0, initialized.stderr)
            validated = self.run_cli("validate", "--path", str(target.resolve()))
            self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\45458\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests -v
```

Expected: FAIL because `career_workspace.py` does not exist.

- [ ] **Step 3: Add blank Markdown templates**

Create `career-profile.md` with this exact content:

```markdown
# 个人职业档案

> 本文件属于用户选择的个人职业工作区，不属于 Skill。只记录用户确认的信息。

## 基础职业事实
<!-- 当前岗位、行业、工作年限、城市等。未知项保留“未知”。 -->

## 现实约束
<!-- 财富、健康、家庭、关系、时间和地域约束。 -->

## 证据清单
<!-- 项目、量化结果、作品、第三方反馈和可核实记录。 -->

## 六类职业资产

| 资产 | 判断 | 证据 | 置信度 |
| --- | --- | --- | --- |
| 方向资产 | 未知 |  | 未知 |
| 能力资产 | 未知 |  | 未知 |
| 成果资产 | 未知 |  | 未知 |
| 杠杆资产 | 未知 |  | 未知 |
| 资源资产 | 未知 |  | 未知 |
| 自由资产 | 未知 |  | 未知 |

## 当前发展阶段
<!-- 区分年龄参考、实际主阶段、已完成任务、当前欠账和提前具备的高阶能力。 -->

## 当前职业生态位
<!-- 分岗位、企业、行业、个人四层记录。 -->

## 待验证假设与未知项

## 最近更新
<!-- YYYY-MM-DD；写明本次更新依据。 -->
```

Create `career-strategy.md` with this exact content:

```markdown
# 当前职业战略

> 本文件保存当前有效的职业战略。历史行动与复盘分别保存在对应子目录。

## 人生与职业目标

## 当前主要矛盾

## 候选路线比较

| 路线 | 资产复用 | 收益与成长 | 风险 | 可逆性 | 生活影响 | 待验证假设 |
| --- | --- | --- | --- | --- | --- | --- |

## 当前选择与依据

## 核心 Gap 与优先级

## 时间层级

### 3 年假设

### 1 年里程碑

### 当前 90 天结果

## 风险边界与安全垫

## 退出条件与 Enough Point

## 最近更新
<!-- YYYY-MM-DD；写明本次调整依据。 -->
```

- [ ] **Step 4: Implement the minimal CLI**

Implement `career_workspace.py` with this complete minimal version:

```python
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Sequence


EXPECTED_FILES = ("career-profile.md", "career-strategy.md")
EXPECTED_DIRS = ("plans", "reviews", "decisions")


def resolve_absolute(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        raise ValueError("an absolute path is required")
    return path.resolve(strict=False)


def is_relative_to(candidate: Path, parent: Path) -> bool:
    try:
        candidate.relative_to(parent)
        return True
    except ValueError:
        return False


def ensure_outside_skill(target: Path, skill_root: Path) -> None:
    if is_relative_to(target, skill_root):
        raise ValueError("career workspace must be outside the Skill directory")


def initialize_workspace(target: Path, skill_root: Path) -> int:
    ensure_outside_skill(target, skill_root)
    if target.exists():
        print(f"target already exists: {target}", file=sys.stderr)
        return 2

    template_root = skill_root / "assets" / "workspace-template"
    missing_templates = [name for name in EXPECTED_FILES if not (template_root / name).is_file()]
    if missing_templates:
        print("missing packaged templates: " + ", ".join(missing_templates), file=sys.stderr)
        return 2

    try:
        target.mkdir(parents=True, exist_ok=False)
        for directory in EXPECTED_DIRS:
            (target / directory).mkdir()
        for filename in EXPECTED_FILES:
            shutil.copyfile(template_root / filename, target / filename)
    except Exception as exc:
        if target.exists():
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
            problems.append(f"missing file: {filename}")
    for directory in EXPECTED_DIRS:
        if not (target / directory).is_dir():
            problems.append(f"missing directory: {directory}")

    if problems:
        for problem in problems:
            print(problem)
        return 1

    print(f"valid career workspace: {target}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a private Markdown career workspace.")
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
```

Rules:

- Relative paths return exit code 2 with an `absolute path` error.
- A target equal to or nested within the current Skill root returns exit code 2.
- `init` rejects any existing target before creating anything.
- `init` copies the two packaged UTF-8 templates and creates exactly three empty subdirectories.
- `validate` checks names and types only; it does not open profile contents.
- Valid structure returns 0, missing or wrong entries return 1, unsafe arguments return 2.
- The CLI prints only paths and structural statuses, never file content.

- [ ] **Step 5: Run tests and verify GREEN**

Run the same `unittest` command.

Expected: six tests pass with zero failures and zero errors.

- [ ] **Step 6: Commit the helper and tests**

```powershell
git add career-strategy-coach/scripts/career_workspace.py career-strategy-coach/assets/workspace-template tests/test_career_workspace.py
git commit -m "feat: add private career workspace helper"
```

## Task 3: Write the Skill from RED Evidence

**Files:**
- Create: `career-strategy-coach/SKILL.md`
- Reference: `tests/behavior/baseline.md`
- Reference: `docs/superpowers/specs/2026-09-19-career-strategy-coach-design.md`

- [ ] **Step 1: Write valid frontmatter**

Use:

```yaml
---
name: career-strategy-coach
description: Use when someone needs career diagnosis, career-path comparison, job-change or transition decisions, professional asset assessment, career planning, action plans, or recurring career reviews.
---
```

- [ ] **Step 2: Write the complete single-entry coaching guide**

The body must contain concise but operational sections for:

- Core outcome and source hierarchy.
- Intent routing for quick consultation, diagnosis, route comparison, decision, planning, review, and archive operations.
- No more than three questions per round; no repeated questions.
- Facts, evidence, inference, unknown, hypothesis, and high/medium/low/unknown confidence.
- Six stages based on task completion, with age only a weak reference.
- Six assets rated only strong/medium/weak/unknown; missing evidence is unknown.
- Job/company/industry/person niche analysis.
- Parallel career routes without management bias.
- Life constraints, downside, reversibility, safety margin, exit rules, and Enough Point.
- Route comparison and low-cost validation experiments.
- Three-year hypothesis, one-year milestone, 90-day result, 30-day action, and weekly action.
- Review loop that updates evidence rather than restarting intake.
- Output contract: facts, judgment/confidence, evidence, strongest counterargument, options/tradeoffs, validation, action, and up to three missing facts.
- Privacy and file-write gate: no path means no write; show resolved path and file list; obtain explicit confirmation; never retain the path in the Skill.
- Exact commands for `career_workspace.py init` and `validate` only after confirmation.
- Common failure modes based on the actual RED evidence.

- [ ] **Step 3: Check discovery and prohibited patterns**

Run:

```powershell
rg -n "0[–-]100|按年龄.*阶段|默认.*C:|自动保存|一次.*大量问题" career-strategy-coach/SKILL.md
```

Expected: no instruction authorizes numeric scoring, age-only classification, a C-drive default, automatic saving, or bulk questioning. Explanatory prohibitions are allowed and must be manually reviewed.

- [ ] **Step 4: Commit the Skill entrypoint**

```powershell
git add career-strategy-coach/SKILL.md
git commit -m "feat: add career strategy coaching workflow"
```

## Task 4: Add UI Metadata and Structural Validation

**Files:**
- Create: `career-strategy-coach/agents/openai.yaml`

- [ ] **Step 1: Create UI metadata**

Use:

```yaml
interface:
  display_name: "职业战略教练"
  short_description: "基于证据诊断职业阶段、资产、生态位与行动路线"
  default_prompt: "使用 $career-strategy-coach 分析我的职业现状或决策；信息不足时每轮最多问三个问题。"
```

Keep implicit invocation enabled; do not add policy fields.

- [ ] **Step 2: Run the official Skill validator without C-drive bytecode writes**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\45458\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\45458\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'F:\AIPro\Career Strategy Coach  职业战略教练\.worktrees\career-strategy-coach-v1\career-strategy-coach'
```

Expected: validator exits 0 and reports the Skill is valid.

- [ ] **Step 3: Run all script tests again**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\45458\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests -v
```

Expected: six tests pass.

- [ ] **Step 4: Commit metadata**

```powershell
git add career-strategy-coach/agents/openai.yaml
git commit -m "feat: add career coach skill metadata"
```

## Task 5: Run GREEN Behavioral Tests and Refactor

**Files:**
- Create: `tests/behavior/green.md`
- Modify if evidence requires: `career-strategy-coach/SKILL.md`

- [ ] **Step 1: Re-run all five scenarios with the Skill**

Give independent evaluators the exact scenario plus explicit access to `career-strategy-coach/SKILL.md`. Preserve their responses and evaluate every acceptance criterion.

- [ ] **Step 2: Record GREEN evidence**

For every scenario, write:

```markdown
## S1 — Age is not stage

### Skill-assisted response
Paste the evaluator response in full without paraphrasing.

### Acceptance results
- Mark each criterion PASS or FAIL and quote the evidence.

### New loopholes
- Write “None” or quote the new rationalization.
```

- [ ] **Step 3: Refactor only observed gaps**

If any criterion fails, add the smallest explicit counter to `SKILL.md`, then re-run that scenario and append the new result. Do not add speculative universal rules.

- [ ] **Step 4: Verify five GREEN headings and no open failures**

Run:

```powershell
rg -n "^## S[1-5]" tests/behavior/green.md
rg -n "FAIL|OPEN|T[B]D|T[O]DO" tests/behavior/green.md
```

Expected: five headings; the second command has no unresolved matches.

- [ ] **Step 5: Commit behavior evidence and refinements**

```powershell
git add tests/behavior/green.md career-strategy-coach/SKILL.md
git commit -m "test: verify career coach behavior"
```

## Task 6: Install the Physical F-Drive Copy and Verify Parity

**Files:**
- Source: `career-strategy-coach/`
- Create: `F:\AIPro\Codex\skills\career-strategy-coach\`

- [ ] **Step 1: Verify the install target is outside the source and on F**

Resolve both absolute paths. Require both drive letters to be `F:` and reject equality or nesting in either direction.

- [ ] **Step 2: Create a fresh physical copy**

If the install target already exists, stop and report the conflict. Otherwise copy the complete `career-strategy-coach` directory to `F:\AIPro\Codex\skills\career-strategy-coach` using native PowerShell file operations. Do not create a junction, symbolic link, or C-drive entry.

- [ ] **Step 3: Validate the installed copy**

Run the official validator against the installed path with `PYTHONDONTWRITEBYTECODE=1`. Expected: exit 0.

- [ ] **Step 4: Compare source and installed hashes**

Generate relative-path plus SHA-256 lists for every file in source and installed directories, sort them, and compare. Expected: no differences.

- [ ] **Step 5: Smoke-test a temporary personal workspace on F**

Use a temporary directory under the worktree, call installed `career_workspace.py init`, validate it, assert the five expected entries exist, then remove only that verified temporary directory. Expected: both commands exit 0.

- [ ] **Step 6: Run final verification**

Run:

```powershell
git diff --check
git status --short
```

Then rerun the six unit tests, source validator, installed validator, behavior evidence scans, privacy scan for personal-data fixtures, and source/install hash comparison. Expected: all checks pass and only intentional tracked changes remain.

- [ ] **Step 7: Commit installation verification records if any tracked record changed**

```powershell
git add tests career-strategy-coach
git commit -m "chore: verify career coach installation"
```

Do not commit the external F-drive installation copy into this repository.
