import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/subagent-routing/scripts/setup.py"
AGENTS = ROOT / "skills/subagent-routing/agents"
ROLES = {"extractor", "analyst", "judge", "synthesizer"}


def run(root, action, *extra, env=None):
    args = [sys.executable, str(SCRIPT), action]
    if root is not None:
        args += ["--claude-home", str(root)]
    return subprocess.run(args + list(extra), capture_output=True, text=True, env=env)


class AgentDefinitionTests(unittest.TestCase):
    def frontmatter(self, path):
        text = path.read_text()
        match = re.match(r"---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(match, path.name)
        return dict(line.split(": ", 1) for line in match.group(1).splitlines())

    def test_all_roles_present_with_valid_frontmatter(self):
        self.assertEqual({p.stem for p in AGENTS.glob("*.md")}, ROLES)
        for path in AGENTS.glob("*.md"):
            meta = self.frontmatter(path)
            self.assertEqual(meta["name"], path.stem)
            self.assertTrue(meta["description"])
            self.assertIn(meta["model"], {"haiku", "sonnet", "opus"})
            self.assertIn(meta["effort"], {"low", "medium", "high", "xhigh"})
            self.assertIn(b"claude-model-guide:subagent-routing", path.read_bytes())

    def test_judge_and_synthesizer_never_use_cheap_models(self):
        for role in ("judge", "synthesizer"):
            self.assertEqual(self.frontmatter(AGENTS / f"{role}.md")["model"], "opus")


class InstallerTests(unittest.TestCase):
    def test_install_status_uninstall(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.assertEqual(run(root, "install").returncode, 0)
            self.assertEqual({p.stem for p in (root / "agents").glob("*.md")}, ROLES)
            self.assertEqual(run(root, "status").stdout.count("Installed:"), 4)
            self.assertEqual(run(root, "install").returncode, 0)
            self.assertEqual(list((root / "agents").glob("*backup*")), [])
            self.assertEqual(run(root, "uninstall").returncode, 0)
            self.assertEqual(list((root / "agents").glob("*.md")), [])

    def test_existing_user_agent_is_never_overwritten_or_removed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "agents").mkdir()
            mine = root / "agents" / "judge.md"
            mine.write_bytes(b"---\nname: judge\n---\nMy own judge.\n")
            result = run(root, "install")
            self.assertEqual(result.returncode, 0)
            self.assertIn("Skipped judge", result.stdout)
            self.assertEqual(mine.read_bytes(), b"---\nname: judge\n---\nMy own judge.\n")
            self.assertTrue((root / "agents" / "analyst.md").exists())
            run(root, "uninstall")
            self.assertTrue(mine.exists())
            self.assertFalse((root / "agents" / "analyst.md").exists())

    def test_modified_installed_agent_is_backed_up_on_reinstall(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            run(root, "install")
            target = root / "agents" / "analyst.md"
            target.write_bytes(target.read_bytes() + b"\nlocal tweak\n")
            run(root, "install")
            self.assertEqual(len(list((root / "agents").glob("analyst.md.model-guide-backup-*"))), 1)
            self.assertNotIn(b"local tweak", target.read_bytes())

    def test_dry_run_creates_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "new-home"
            self.assertEqual(run(root, "install", "--dry-run").returncode, 0)
            self.assertFalse(root.exists())

    def test_honors_claude_config_dir(self):
        with tempfile.TemporaryDirectory() as d:
            env = dict(os.environ, CLAUDE_CONFIG_DIR=d)
            self.assertEqual(run(None, "install", env=env).returncode, 0)
            self.assertTrue((Path(d) / "agents" / "judge.md").exists())


if __name__ == "__main__":
    unittest.main()
