from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".venv", "venv", "env", ".git"}

TARGETS = [
    ROOT / ".pytest_cache",
    ROOT / ".ruff_cache",
    ROOT / "allure-results",
    ROOT / "allure-report",
]


def remove_pycache(path: Path) -> None:
    for child in path.rglob("__pycache__"):
        if any(part in SKIP_DIRS for part in child.parts):
            continue
        shutil.rmtree(child, ignore_errors=True)


def main() -> None:
    for target in TARGETS:
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target, ignore_errors=True)
            else:
                target.unlink(missing_ok=True)
    remove_pycache(ROOT)
    print("Cache cleaned.")


if __name__ == "__main__":
    main()
