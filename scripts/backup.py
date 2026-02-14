#!/usr/bin/env python3
import argparse
import shutil
from datetime import datetime
from pathlib import Path

LOG_FILE = Path.cwd() / "logs" / "backup.log"

def log(msg: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}\n"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)

def parse_args():
    p = argparse.ArgumentParser(description="Simple backup script")
    p.add_argument("--source", default=str(Path.home() / "Documents" / "backup-source"),
                   help="Source directory to back up")
    p.add_argument("--dest", default="backups",
                   help="Destination root folder (inside repo or absolute path)")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would happen, but don't copy files")
    return p.parse_args()

def main() -> None:
    args = parse_args()
    source_dir = Path(args.source).expanduser()
    backup_root = Path(args.dest).expanduser()

    if not source_dir.exists():
        log(f"ERROR: source folder not found: {source_dir}")
        print(f"Source folder not found: {source_dir}")
        return

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = backup_root / stamp

    if args.dry_run:
        print("[DRY-RUN] No files will be copied.")
    else:
        dest.mkdir(parents=True, exist_ok=True)

    copied = 0
    for item in source_dir.iterdir():
        if item.is_file():
            if args.dry_run:
                print(f"[DRY-RUN] Would copy: {item.name}")
            else:
                shutil.copy2(item, dest / item.name)
                copied += 1

    if args.dry_run:
        log(f"DRY-RUN: simulated backup from {source_dir} to {backup_root}")
        print("[DRY-RUN] Done.")
    else:
        log(f"OK: copied {copied} file(s) from {source_dir} to {dest}")
        print(f"Backup complete: {copied} file(s) -> {dest}")

if __name__ == "__main__":
    main()

