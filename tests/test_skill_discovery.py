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
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        skill_file = SKILL_ROOT / "SKILL.md"
        self.assertTrue(skill_file.is_file())
        skill = skill_file.read_text(encoding="utf-8")

        self.assertIn("帮我分析一下职业路径", skill)
        self.assertIn("职业路径", agents)
        self.assertIn("career-profiles/", agents)
        self.assertIn("career-profiles", skill)
        self.assertIn("明确确认", skill)

    def test_private_profiles_are_gitignored(self):
        ignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("career-profiles/", ignore.splitlines())


if __name__ == "__main__":
    unittest.main()
