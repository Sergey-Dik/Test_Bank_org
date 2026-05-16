#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ -x ".venv/Scripts/python.exe" ]]; then
  PY=".venv/Scripts/python.exe"
elif command -v py >/dev/null 2>&1; then
  PY="py -3.12"
else
  PY="python3"
fi

exec "$PY" -m pytest "$@"
