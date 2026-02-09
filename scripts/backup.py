#!/usr/bin/env python3
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

SOURCE_DIR = Path.home() / "Documents" / "backup-source"
BACKUP_ROOT = Path.cwd() / "backups"
LOG_FILE = Path.cwd() / "logs" / "backup.log"

DRY_RUN = "--dry-run" in sys.argv

def log(msg: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}\n"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)

def main() -> None:
    if not SOURCE_DIR.exists():
        log(f"ERROR: source folder not found: {SOURCE_DIR}")
        print(f"Source folder not found: {SOURCE_DIR}")
        return

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = BACKUP_ROOT / stamp

    if DRY_RUN:
        print("[DRY-RUN] No files will be copied.")
    else:
        dest.mkdir(parents=True, exist_ok=True)

    copied = 0
    for item in SOURCE_DIR.iterdir():
        if item.is_file():
            if DRY_RUN:
                print(f"[DRY-RUN] Would copy: {item.name}")
            else:
                shutil.copy2(item, dest / item.name)
                copied += 1

    if DRY_RUN:
        log("DRY-RUN: backup simulated")
        print("[DRY-RUN] Done.")
    else:
        log(f"OK: copied {copied} file(s) from {SOURCE_DIR} to {dest}")
        print(f"Backup complete: {copied} file(s) -> {dest}")

if __name__ == "__main__":
    main()
