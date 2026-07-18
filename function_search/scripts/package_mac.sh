#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d ".venv" ]]; then
  echo "==> Creating virtual environment"
  python3 -m venv .venv
fi
source .venv/bin/activate

echo "==> Installing dependencies"
pip install -q -r requirements.txt -e .

if ! python3 -c "import tkinter" 2>/dev/null; then
  echo "WARNING: tkinter is not available. GUI will not work until you install it:"
  echo "  brew install python-tk@3.14"
  echo "CLI search still works via: function-search search <query>"
fi

echo "==> Building search index"
export PYTHONPATH="$ROOT/src:${PYTHONPATH:-}"

if python3 -c "import torch" 2>/dev/null; then
  python3 -m function_search.build_index
else
  echo "PyTorch not installed. Building Python + backend index only."
  echo "For full PyTorch index: pip install torch && python3 -m function_search.build_index"
  python3 -m function_search.build_index --no-pytorch
fi

DB_PATH="$ROOT/src/function_search/data/functions.db"
if [[ ! -f "$DB_PATH" ]]; then
  echo "Index build failed: $DB_PATH not found" >&2
  exit 1
fi

COUNT=$(python3 - <<PY
import sqlite3
conn = sqlite3.connect("$DB_PATH")
print(conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0])
conn.close()
PY
)
echo "==> Index ready: $COUNT entries"

if ! python3 -c "import tkinter" 2>/dev/null; then
  echo "==> Skipping .app packaging (tkinter required for GUI bundle)"
  exit 0
fi

echo "==> Packaging macOS app with PyInstaller"
pip install -q pyinstaller
pyinstaller --noconfirm function_search.spec

APP_PATH="$ROOT/dist/FunctionSearch.app"
if [[ -d "$APP_PATH" ]]; then
  echo "==> Done: $APP_PATH"
  echo "    Run: open \"$APP_PATH\""
else
  echo "Build finished. Check dist/ directory." >&2
  exit 1
fi
