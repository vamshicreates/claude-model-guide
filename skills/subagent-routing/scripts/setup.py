#!/usr/bin/env python3
"""Install, inspect, or remove Model Guide's role subagents in ~/.claude/agents."""
import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys

MARKER = b"<!-- claude-model-guide:subagent-routing -->"
SOURCE = Path(__file__).resolve().parents[1] / "agents"


def default_home():
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")


def owned(path):
    return path.exists() and not path.is_symlink() and MARKER in path.read_bytes()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "uninstall", "status"])
    parser.add_argument("--claude-home", type=Path, default=default_home(),
                        help="Claude Code config dir (default: $CLAUDE_CONFIG_DIR or ~/.claude)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    dest = args.claude_home.expanduser().resolve() / "agents"
    sources = sorted(SOURCE.glob("*.md"))
    if not sources:
        raise ValueError(f"No agent files found in {SOURCE}")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    skipped = 0
    for src in sources:
        target = dest / src.name
        name = src.stem
        if args.action == "status":
            if owned(target):
                state = "Installed"
            elif target.exists() or target.is_symlink():
                state = "Name taken by another file"
            else:
                state = "Not installed"
            print(f"{state}: {target}")
        elif args.action == "install":
            if target.is_symlink() or (target.exists() and not owned(target)):
                print(f"Skipped {name}: {target} exists and was not installed by Model Guide.")
                skipped += 1
                continue
            data = src.read_bytes()
            if target.exists() and target.read_bytes() == data:
                print(f"No change needed: {target}")
                continue
            if args.dry_run:
                print(f"Would install {name} -> {target}")
                continue
            dest.mkdir(parents=True, exist_ok=True)
            if target.exists():
                backup = dest / f"{src.name}.model-guide-backup-{stamp}"
                shutil.copy2(target, backup)
                print(f"Backup: {backup}")
            target.write_bytes(data)
            print(f"Installed {name}: {target}")
        else:
            if not (target.exists() or target.is_symlink()):
                continue
            if not owned(target):
                print(f"Left alone {name}: {target} was not installed by Model Guide.")
                continue
            if args.dry_run:
                print(f"Would remove {target}")
                continue
            target.unlink()
            print(f"Removed {name}: {target}")
    if args.action != "status" and not args.dry_run:
        print("Start a new Claude Code session to load the updated agents.")
    if skipped:
        print(f"{skipped} file(s) skipped to protect your existing agents; rename or move them to install.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
