from __future__ import annotations

import sys
from pathlib import Path


def package_root() -> Path:
    """Return the application root, supporting PyInstaller bundles."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent


def default_db_path() -> Path:
    return package_root() / "data" / "functions.db"


def user_data_dir() -> Path:
    if sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support" / "FunctionSearch"
    elif sys.platform == "win32":
        base = Path.home() / "AppData" / "Local" / "FunctionSearch"
    else:
        base = Path.home() / ".local" / "share" / "function-search"
    base.mkdir(parents=True, exist_ok=True)
    return base
