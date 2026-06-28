#!/usr/bin/env bash
set -euo pipefail
python --version
python - <<'PYCHECK'
import importlib.util
for pkg in ['django','rest_framework','psycopg']:
    print(pkg, 'ok' if importlib.util.find_spec(pkg) else 'missing')
PYCHECK
python manage.py check
