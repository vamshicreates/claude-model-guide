#!/usr/bin/env python3
"""Manage only Model Guide's marked block in global Claude Code instructions (CLAUDE.md)."""
import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys
import uuid

START = b"<!-- claude-model-guide:start -->"
END = b"<!-- claude-model-guide:end -->"
SEP = b"\n\n"


def default_home():
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")


def locate(data):
    if START not in data and END not in data:
        return None
    if data.count(START) != 1 or data.count(END) != 1:
        raise ValueError("Ambiguous markers; review CLAUDE.md manually before continuing.")
    start = data.index(START)
    end = data.index(END) + len(END)
    if end < start:
        raise ValueError("Invalid marker order; review CLAUDE.md manually.")
    return start, end


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "uninstall", "status"])
    parser.add_argument("--claude-home", type=Path, default=default_home(),
                        help="Claude Code config dir (default: $CLAUDE_CONFIG_DIR or ~/.claude)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.claude_home.expanduser().resolve()
    target = root / "CLAUDE.md"
    if target.is_symlink():
        raise ValueError("CLAUDE.md is a symlink; manage its destination explicitly.")
    data = target.read_bytes() if target.exists() else b""
    span = locate(data)
    if args.action == "status":
        print(f"{'Enabled' if span else 'Not enabled'}: {target}")
        return
    if args.action == "install":
        policy = (Path(__file__).resolve().parents[1] / "policy.md").read_bytes().rstrip()
        block = START + b"\n\n" + policy + b"\n" + END
        if span:
            updated = data[:span[0]] + block + data[span[1]:]
        else:
            # Exactly SEP before the block and one newline after, so uninstall can reverse it.
            updated = data + (SEP if data else b"") + block + b"\n"
    else:
        if span:
            before, after = data[:span[0]], data[span[1]:]
            if after.startswith(b"\n"):
                after = after[1:]
            if before.endswith(SEP):
                before = before[: -len(SEP)]
            updated = before + after
        else:
            updated = data
    if updated == data:
        print(f"No change needed: {target}")
        return
    if args.dry_run:
        print(f"Would {args.action} Model Guide in {target}")
        if args.action == "install":
            print(policy.decode())
        return
    root.mkdir(parents=True, exist_ok=True)
    if target.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup = root / f"CLAUDE.md.model-guide-backup-{stamp}-{uuid.uuid4().hex[:8]}"
        shutil.copy2(target, backup)
        print(f"Backup: {backup}")
    target.write_bytes(updated)
    print(f"{args.action.capitalize()} complete: {target}")
    print("Start a new Claude Code session (or run /clear) to load the updated instructions.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
