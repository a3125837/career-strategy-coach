from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "career-strategy-coach"


def level_two_section(markdown: str, title: str) -> str | None:
    marker = f"## {title}"
    if markdown.count(marker) != 1:
        return None
    section_start = markdown.index(marker) + len(marker)
    remaining = markdown[section_start:]
    next_section = remaining.find("\n## ")
    if next_section != -1:
        remaining = remaining[:next_section]
    return remaining.strip()


def frontmatter_description(markdown: str) -> str | None:
    if not markdown.startswith("---\n"):
        return None
    parts = markdown.split("---", 2)
    if len(parts) != 3:
        return None
    descriptions = [
        line.partition(":")[2].strip()
        for line in parts[1].splitlines()
        if line.startswith("description:")
    ]
    if len(descriptions) != 1:
        return None
    return descriptions[0]


def yaml_quoted_value(text: str, key: str) -> str | None:
    prefix = f"  {key}: "
    matches = [line[len(prefix) :] for line in text.splitlines() if line.startswith(prefix)]
    if len(matches) != 1:
        return None
    value = matches[0].strip()
    if len(value) < 2 or value[0] != '"' or value[-1] != '"':
        return None
    return value[1:-1]


class SkillDiscoveryTests(unittest.TestCase):
    def test_skill_uses_official_repository_location(self):
        self.assertTrue((SKILL_ROOT / "SKILL.md").is_file())
        self.assertFalse((REPO_ROOT / "career-strategy-coach").exists())

    def test_project_alias_routes_to_the_skill(self):
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        route = level_two_section(agents, "职业战略教练调用")

        self.assertIsNotNone(route)
        route = route or ""
        self.assertIn("/ZhiYeJiaoLian", route)
        self.assertIn(".agents/skills/career-strategy-coach/SKILL.md", route)
        self.assertRegex(route, r"项目级文本(?:触发)?(?:别名|约定)")
        self.assertRegex(route, r"不是\s*Codex\s*原生(?:自定义裸)?斜杠命令")

    def test_project_alias_arguments_and_alias_only_behavior_are_declared(self):
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        route = level_two_section(agents, "职业战略教练调用")

        self.assertIsNotNone(route)
        route = route or ""
        self.assertRegex(
            route,
            r"/ZhiYeJiaoLian[^\n]*后有文本时[^\n]*后续文本[^\n]*作为[^\n]*职业问题",
        )
        self.assertRegex(
            route,
            r"只有别名本身时[^\n]*只询问[^\n]*本次[^\n]*职业问题",
        )

    def test_natural_language_trigger_and_private_root_are_declared(self):
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        route = level_two_section(agents, "职业战略教练调用")
        skill_file = SKILL_ROOT / "SKILL.md"
        self.assertTrue(skill_file.is_file())
        skill = skill_file.read_text(encoding="utf-8")
        description = frontmatter_description(skill)

        self.assertIsNotNone(route)
        route = route or ""
        self.assertIsNotNone(description)
        self.assertIn("analyze a career path", (description or "").lower())
        self.assertIn("/ZhiYeJiaoLian", description or "")
        self.assertIn("帮我分析一下职业路径", skill)
        self.assertIn("分析职业路径", route)
        for trigger in ("职业发展", "跳槽", "转型"):
            self.assertIn(trigger, route)
        self.assertIn("career-profiles/", route)
        self.assertIn("career-profiles", skill)
        self.assertIn("明确确认", skill)

    def test_skill_entry_declares_alias_as_project_text_not_native_slash(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        entry = level_two_section(skill, "项目入口")

        self.assertIsNotNone(entry)
        entry = entry or ""
        self.assertIn("/ZhiYeJiaoLian", entry)
        self.assertRegex(entry, r"项目(?:内|级)文本别名")
        self.assertRegex(entry, r"不是\s*Codex\s*原生(?:自定义裸)?斜杠命令")

    def test_openai_prompt_exposes_project_alias_without_native_claim(self):
        manifest = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        prompt = yaml_quoted_value(manifest, "default_prompt")

        self.assertIsNotNone(prompt)
        prompt = prompt or ""
        self.assertIn("/ZhiYeJiaoLian", prompt)
        self.assertRegex(prompt, r"项目(?:内|级)文本别名")
        self.assertNotRegex(prompt, r"原生(?:自定义裸)?斜杠命令")

    def test_profile_workflow_requires_propose_output_and_confirmation_before_init(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        gate = level_two_section(skill, "隐私与职业工作区闸门")

        self.assertIsNotNone(gate)
        gate = gate or ""
        propose = (
            "python scripts/career_workspace.py propose --root <absolute-root> "
            "--name <single-folder-name>"
        )
        init = "python scripts/career_workspace.py init --path <absolute-path>"
        self.assertIn(propose, gate)
        self.assertIn("目标路径与五项", gate)
        self.assertIn("等待用户明确确认", gate)
        self.assertRegex(gate, r"不得[^\n]*手工拼接[^\n]*替代\s*`propose`")
        self.assertIn(init, gate)
        self.assertLess(gate.index(propose), gate.index("等待用户明确确认"))
        self.assertLess(gate.index("等待用户明确确认"), gate.index(init))

    def test_private_profiles_are_gitignored(self):
        ignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("career-profiles/", ignore.splitlines())


if __name__ == "__main__":
    unittest.main()
