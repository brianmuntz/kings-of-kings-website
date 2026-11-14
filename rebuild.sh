#!/bin/sh
set -eu
PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$PROJECT_ROOT"
KOK_PYTHON="${KOK_PYTHON:-python3}"
"$KOK_PYTHON" website/tools/build.py
"$KOK_PYTHON" website/tools/check.py
if command -v node >/dev/null 2>&1; then node --check website/assets/site.js; fi
