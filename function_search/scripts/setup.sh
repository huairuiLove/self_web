#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 -m venv .venv
source .venv/bin/activate
pip install -q -r requirements.txt -e .

if ! python3 -c "import tkinter" 2>/dev/null; then
  echo "Tip: install GUI support with: brew install python-tk@3.14"
fi

export PYTHONPATH="$ROOT/src:${PYTHONPATH:-}"
if python3 -c "import torch" 2>/dev/null; then
  python3 -m function_search.build_index
else
  python3 -m function_search.build_index --no-pytorch
fi

echo "Setup complete. Try: function-search search torch.nn.Linear"
