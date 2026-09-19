# Career Coach Invocation and Profile Defaults Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the career coach automatically discoverable inside this F-drive repository, support the project-level `/ZhiYeJiaoLian` alias and natural-language career-path triggers, and safely propose a named personal archive under `career-profiles/` without writing before confirmation.

**Architecture:** Move the authoritative Skill into the official repository discovery tree at `.agents/skills/career-strategy-coach`. Keep routing policy in root `AGENTS.md`, deterministic folder-name validation in `career_workspace.py`, and private archive contents in an ignored `career-profiles/` directory. Preserve the separate F-drive installation as a physical copy synchronized only after proving it has not been modified.

**Tech Stack:** Markdown Skill instructions, YAML UI metadata, Python 3 standard library, `unittest`, Git, PowerShell, official `quick_validate.py`.

---

## File map

- Move: `career-strategy-coach/` → `.agents/skills/career-strategy-coach/` — authoritative repository Skill.
- Modify: `AGENTS.md` — project-level `/ZhiYeJiaoLian` routing and default archive root.
- Modify: `.gitignore` — exclude `career-profiles/`.
- Modify: `.agents/skills/career-strategy-coach/SKILL.md` — natural-language triggers and default archive workflow.
- Modify: `.agents/skills/career-strategy-coach/agents/openai.yaml` — default prompt aligned with the shortcut.
- Modify: `.agents/skills/career-strategy-coach/scripts/career_workspace.py` — read-only `propose` command and safe single-folder-name validation.
- Modify: `tests/test_career_workspace.py` — TDD coverage for `propose`.
- Create: `tests/test_skill_discovery.py` — repository discovery, alias, natural-language triggers, and Git-ignore checks.
- Create: `tests/behavior/invocation-profile-baseline.md` — RED evidence.
- Create: `tests/behavior/invocation-profile-green.md` — GREEN evidence.
- External physical copy: `F:\AIPro\Codex\skills\career-strategy-coach` — synchronized after repository verification; never committed.

### Task 1: Create an isolated worktree and capture RED behavior

**Files:**
- Create: `tests/behavior/invocation-profile-baseline.md`
- Create: `tests/test_skill_discovery.py`
- Modify: `tests/test_career_workspace.py`

- [ ] **Step 1: Create the F-drive worktree**

Run from the repository root:

```powershell
git worktree add "F:\AIPro\Career Strategy Coach  职业战略教练\.worktrees\career-coach-invocation" -b codex/career-coach-invocation
```

Expected: the new worktree is based on `master`, and both worktrees are clean.

- [ ] **Step 2: Record the three RED scenarios**

Create `tests/behavior/invocation-profile-baseline.md` with verbatim baseline responses and explicit criteria for:

```text
/ZhiYeJiaoLian
```

```text
帮我分析一下职业路径
```

```text
为我创建个人职业档案。我还没有起档案名称。
```

Expected RED failures:

- no explicit project-level alias contract;
- natural-language activation is not stated in the Skill description;
- no deterministic default-root/name proposal exists.

- [ ] **Step 3: Add failing repository-discovery tests**

Create `tests/test_skill_discovery.py`:

```python
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "career-strategy-coach"


class SkillDiscoveryTests(unittest.TestCase):
    def test_skill_uses_official_repository_location(self):
        self.assertTrue((SKILL_ROOT / "SKILL.md").is_file())
        self.assertFalse((REPO_ROOT / "career-strategy-coach").exists())

    def test_project_alias_routes_to_the_skill(self):
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("/ZhiYeJiaoLian", agents)
        self.assertIn(".agents/skills/career-strategy-coach/SKILL.md", agents)

    def test_natural_language_trigger_and_private_root_are_declared(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("帮我分析一下职业路径", skill)
        self.assertIn("career-profiles", skill)
        self.assertIn("明确确认", skill)

    def test_private_profiles_are_gitignored(self):
        ignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("career-profiles/", ignore.splitlines())
```

- [ ] **Step 4: Add failing `propose` CLI tests**

Extend `CareerWorkspaceCliTests` with subprocess calls that expect:

```python
def test_propose_returns_target_and_five_items_without_writing(self):
    root = self.temp_root / "career-profiles"
    result = self.run_cli("propose", "--root", str(root), "--name", "2026职业规划")
    self.assertEqual(0, result.returncode, result.stderr)
    self.assertIn(str(root / "2026职业规划"), result.stdout)
    for name in ("career-profile.md", "career-strategy.md", "plans", "reviews", "decisions"):
        self.assertIn(name, result.stdout)
    self.assertFalse(root.exists())

def test_propose_rejects_unsafe_single_folder_names(self):
    root = self.temp_root / "career-profiles"
    for name in ("", ".", "..", "a/b", r"a\b", "CON", "nul.txt"):
        with self.subTest(name=name):
            result = self.run_cli("propose", "--root", str(root), "--name", name)
            self.assertEqual(2, result.returncode)
            self.assertFalse(root.exists())
```

- [ ] **Step 5: Run RED tests and preserve evidence**

Run with `TEMP`, `TMP`, `PYTHONDONTWRITEBYTECODE`, and `PYTHONUTF8` explicitly placed on F:

```powershell
py -3.11 -m unittest tests.test_skill_discovery -v
py -3.11 -m unittest tests.test_career_workspace.CareerWorkspaceCliTests.test_propose_returns_target_and_five_items_without_writing -v
```

Expected: failures caused by the missing official location and missing `propose` subcommand, not test errors.

- [ ] **Step 6: Commit RED tests**

```powershell
git add tests/behavior/invocation-profile-baseline.md tests/test_skill_discovery.py tests/test_career_workspace.py
git commit -m "test: define career coach invocation and profile defaults"
```

### Task 2: Move the Skill and add invocation routing

**Files:**
- Move: `career-strategy-coach/` → `.agents/skills/career-strategy-coach/`
- Modify: `AGENTS.md`
- Modify: `.gitignore`
- Modify: `tests/test_career_workspace.py`
- Modify: `.agents/skills/career-strategy-coach/SKILL.md`
- Modify: `.agents/skills/career-strategy-coach/agents/openai.yaml`

- [ ] **Step 1: Move the authoritative Skill without changing content**

```powershell
New-Item -ItemType Directory -Path '.agents\skills' -Force | Out-Null
git mv career-strategy-coach .agents/skills/career-strategy-coach
```

Update the existing test constants at the same time:

```python
ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / ".agents" / "skills" / "career-strategy-coach"
SCRIPT = SKILL_ROOT / "scripts" / "career_workspace.py"
```

Verify `git diff --summary` reports renames rather than duplicate source trees and run the existing unit suite before making behavioral edits.

- [ ] **Step 2: Add project routing to `AGENTS.md`**

Append:

```markdown
## 职业战略教练调用

- `/ZhiYeJiaoLian` 是项目级文本触发别名，不是 Codex 原生斜杠命令。
- 用户输入 `/ZhiYeJiaoLian`，或明确要求分析职业路径、职业发展、职业规划、跳槽、转型、职业路线比较或职业复盘时，读取并使用 `.agents/skills/career-strategy-coach/SKILL.md`。
- `/ZhiYeJiaoLian` 后有文本时，将后续文本作为职业问题；只有别名本身时，只询问本次希望解决的职业问题。
- 新建职业档案的默认基础目录是本项目根目录下的 `career-profiles/`；必须先取得用户提供的单层档案名称并完成写入确认闸门。
```

- [ ] **Step 3: Protect private archives**

Append exactly one entry to `.gitignore`:

```gitignore
career-profiles/
```

- [ ] **Step 4: Update Skill discovery metadata**

Replace the frontmatter description with a trigger-only description under 500 characters:

```yaml
description: Use when a user enters /ZhiYeJiaoLian or asks to analyze a career path, career development, career planning, job change, career transition, professional assets, route comparison, action planning, or recurring career review.
```

Add an invocation section that states the alias and natural-language examples, and update the archive gate so that missing explicit paths use `career-profiles/<用户起的名字>` only after collecting and validating a single folder name. Preserve explicit alternative absolute paths and the confirmation gate.

- [ ] **Step 5: Update the default UI prompt**

Set `default_prompt` in `agents/openai.yaml` to:

```yaml
default_prompt: "使用 $career-strategy-coach 分析我的职业路径或决策；也可输入 /ZhiYeJiaoLian。信息不足时每轮最多问三个问题。"
```

- [ ] **Step 6: Run discovery tests**

```powershell
py -3.11 -m unittest tests.test_skill_discovery -v
```

Expected: all repository discovery and routing tests pass.

- [ ] **Step 7: Commit the move and routing**

```powershell
git add AGENTS.md .gitignore .agents tests/test_skill_discovery.py tests/test_career_workspace.py
git commit -m "feat: add career coach project shortcut"
```

### Task 3: Implement safe archive-path proposal

**Files:**
- Modify: `.agents/skills/career-strategy-coach/scripts/career_workspace.py`
- Modify: `tests/test_career_workspace.py`

- [ ] **Step 1: Implement single-name validation**

Add:

```python
WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


def validate_workspace_name(raw_name: str) -> str:
    name = raw_name.strip()
    if not name or name in {".", ".."}:
        raise WorkspaceError("a non-empty single folder name is required")
    if "/" in name or "\\" in name:
        raise WorkspaceError("workspace name must be a single folder name")
    device_stem = name.rstrip(" .").split(".", 1)[0].upper()
    if device_stem in WINDOWS_RESERVED_NAMES:
        raise WorkspaceError("workspace name is reserved on Windows")
    if name.endswith((" ", ".")):
        raise WorkspaceError("workspace name cannot end with a space or period")
    return name
```

- [ ] **Step 2: Implement the read-only proposal**

Add:

```python
def propose_workspace(root_value: str, raw_name: str) -> Path:
    root = resolve_absolute(root_value)
    name = validate_workspace_name(raw_name)
    target = root / name
    reject_skill_overlap(target)
    print(f"proposed career workspace: {target}")
    print(f"file: {target / 'career-profile.md'}")
    print(f"file: {target / 'career-strategy.md'}")
    for directory in ("plans", "reviews", "decisions"):
        print(f"directory: {target / directory}")
    return target
```

Register an argparse `propose` subcommand requiring `--root` and `--name`. It must not call `mkdir`, copy templates, or read profile contents.

- [ ] **Step 3: Run targeted tests**

```powershell
py -3.11 -m unittest tests.test_career_workspace.CareerWorkspaceCliTests.test_propose_returns_target_and_five_items_without_writing -v
py -3.11 -m unittest tests.test_career_workspace.CareerWorkspaceCliTests.test_propose_rejects_unsafe_single_folder_names -v
```

Expected: both tests pass and the proposed root remains absent.

- [ ] **Step 4: Run the complete unit suite**

```powershell
py -3.11 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: all executable tests pass; the existing three symlink tests may skip when Windows denies symlink creation.

- [ ] **Step 5: Commit the proposal command**

```powershell
git add .agents/skills/career-strategy-coach/scripts/career_workspace.py tests/test_career_workspace.py
git commit -m "feat: propose named career profile workspaces"
```

### Task 4: Run GREEN behavior and validate the repository Skill

**Files:**
- Create: `tests/behavior/invocation-profile-green.md`
- Modify if needed: `.agents/skills/career-strategy-coach/SKILL.md`

- [ ] **Step 1: Re-run the exact three RED prompts with the Skill**

Record complete responses, per-criterion PASS/FAIL, and reproducibility limitations. Requirements:

- `/ZhiYeJiaoLian` loads the career coach and asks only what the user wants to solve when no problem follows;
- “帮我分析一下职业路径” activates the Skill without requiring the alias;
- archive creation asks for one folder name, proposes the absolute `career-profiles/<name>` path and five items, and waits for explicit confirmation.

- [ ] **Step 2: Close only observed loopholes**

If a criterion fails, make the smallest corresponding `SKILL.md` or `AGENTS.md` correction and re-run only affected scenarios. Do not weaken acceptance criteria.

- [ ] **Step 3: Validate the Skill and repository**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONUTF8='1'
py -3.11 C:\Users\45458\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents\skills\career-strategy-coach
py -3.11 -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
git status --short
```

Expected: `Skill is valid!`, no test failures, and only intended files changed.

- [ ] **Step 4: Commit GREEN evidence**

```powershell
git add tests/behavior/invocation-profile-green.md AGENTS.md .agents/skills/career-strategy-coach/SKILL.md
git commit -m "test: verify career coach shortcut behavior"
```

### Task 5: Safely synchronize the F-drive installation

**Files:**
- External update: `F:\AIPro\Codex\skills\career-strategy-coach`

- [ ] **Step 1: Prove the current installation is unmodified**

Compare its five files against the pre-change `master` Skill blobs. If any file differs, stop and report the conflict; never silently overwrite.

- [ ] **Step 2: Synchronize the verified source**

Copy the five authoritative files from `.agents/skills/career-strategy-coach` to the existing F-drive installation. Do not copy the parent directory as an extra nesting layer.

- [ ] **Step 3: Verify source/install parity**

Compute manifests keyed by relative path and SHA-256. Expected:

```text
SourceFiles: 5
InstalledFiles: 5
PathDifferences: 0
HashDifferences: 0
ReparseEntries: 0
```

- [ ] **Step 4: Run installed-copy smoke tests**

Use a unique F-drive temporary directory. Verify:

```powershell
py -3.11 F:\AIPro\Codex\skills\career-strategy-coach\scripts\career_workspace.py propose --root <F-temp-root> --name 2026职业规划
py -3.11 F:\AIPro\Codex\skills\career-strategy-coach\scripts\career_workspace.py init --path <F-temp-root>\2026职业规划
py -3.11 F:\AIPro\Codex\skills\career-strategy-coach\scripts\career_workspace.py validate --path <F-temp-root>\2026职业规划
```

Expected: `propose` creates nothing, `init` creates exactly five root items, and `validate` succeeds. Verify exact boundaries and contents before deleting each known file and empty directory non-recursively.

- [ ] **Step 5: Final verification and commit state**

Run the full unit suite, source and install validators, behavior scans, privacy scans, SHA-256 comparison, `git diff --check`, and `git status --porcelain=v1`. Expected: clean branch, no unresolved failures, and no C-drive output.

### Task 6: Review, merge, and cleanup

**Files:** none unless review finds a defect.

- [ ] **Step 1: Request specification and quality review**

Review against the approved design, with special attention to truthful slash-command wording, default-path privacy, name traversal, confirmation gates, and installation parity.

- [ ] **Step 2: Fix and re-review any blocking findings**

Use TDD for behavior or script defects. Re-synchronize the installation only after proving it remains unmodified.

- [ ] **Step 3: Merge after user selection**

After all verification passes, offer the standard branch completion options. Do not merge, push, delete, or discard without the corresponding user choice.
