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
        self.assertIn("帮我分析一下职业路径", skill)
        self.assertIn("分析职业路径", route)
        self.assertIn("career-profiles/", route)
        self.assertIn("career-profiles", skill)
        self.assertIn("明确确认", skill)

    def test_private_profiles_are_gitignored(self):
        ignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("career-profiles/", ignore.splitlines())


if __name__ == "__main__":
    unittest.main()
