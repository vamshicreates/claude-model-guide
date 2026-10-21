import os
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/model-guide/scripts/setup.py"


class SetupTests(unittest.TestCase):
    def run_setup(self, root, action, *extra, env=None):
        args = [sys.executable, str(SCRIPT), action]
        if root is not None:
            args += ["--claude-home", str(root)]
        return subprocess.run(args + list(extra), capture_output=True, text=True, env=env)

    def roundtrip(self, original):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "CLAUDE.md"
            target.write_bytes(original)
            self.assertEqual(self.run_setup(root, "install").returncode, 0)
            installed = target.read_bytes()
            self.assertTrue(installed.startswith(original))
            self.assertIn(b"claude-model-guide:start", installed)
            self.assertEqual(self.run_setup(root, "install").returncode, 0)
            self.assertEqual(target.read_bytes(), installed)
            self.assertEqual(len(list(root.glob("CLAUDE.md.model-guide-backup-*"))), 1)
            self.assertEqual(self.run_setup(root, "uninstall").returncode, 0)
            self.assertEqual(target.read_bytes(), original)

    def test_preservation_idempotence_and_removal(self):
        self.roundtrip(b"# Personal rules\r\nPreserve my files.")

    def test_roundtrip_with_trailing_newlines(self):
        self.roundtrip(b"# Rules\n- be brief\n")
        self.roundtrip(b"# Rules\n\n")

    def test_dry_run_does_not_create_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "new-home"
            self.assertEqual(self.run_setup(root, "install", "--dry-run").returncode, 0)
            self.assertFalse(root.exists())

    def test_fresh_install_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertIn("Not enabled", self.run_setup(root, "status").stdout)
            self.assertEqual(self.run_setup(root, "install").returncode, 0)
            self.assertIn("Enabled:", self.run_setup(root, "status").stdout)
            self.assertEqual(self.run_setup(root, "uninstall").returncode, 0)
            self.assertEqual((root / "CLAUDE.md").read_bytes(), b"")

    def test_honors_claude_config_dir(self):
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, CLAUDE_CONFIG_DIR=directory)
            self.assertEqual(self.run_setup(None, "install", env=env).returncode, 0)
            self.assertTrue((Path(directory) / "CLAUDE.md").exists())

    def test_malformed_markers_are_not_modified(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = b"Keep this. <!-- claude-model-guide:start -->"
            target = root / "CLAUDE.md"
            target.write_bytes(original)
            self.assertNotEqual(self.run_setup(root, "install").returncode, 0)
            self.assertEqual(target.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
