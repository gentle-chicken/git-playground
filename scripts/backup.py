#!/usr/bin/env python3
import os
import shutil
from datetime import datetime
from pathlib import Path

SOURCE_DIR = Path.home() / "Documents" / "backup-source"   # we will create this
BACKUP_ROOT = Path.cwd() / "backups"
LOG_FILE = Path.cwd() / "logs" / "backup.log"

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
        print("Create it and add a few files, then run again.")
        return

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = BACKUP_ROOT / stamp
    dest.mkdir(parents=True, exist_ok=True)

    copied = 0
    for item in SOURCE_DIR.iterdir():
        if item.is_file():
            shutil.copy2(item, dest / item.name)
            copied += 1

    log(f"OK: copied {copied} file(s) from {SOURCE_DIR} to {dest}")
    print(f"Backup complete: {copied} file(s) -> {dest}")

if __name__ == "__main__":
    main()
