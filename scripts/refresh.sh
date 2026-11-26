#!/usr/bin/env bash
# Daily CoupeFab price refresh: fetch -> build -> deploy manifest -> local commit.
# Usage: scripts/refresh.sh [--only metalsrus mercier40 ...]
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${COUPEFAB_PY:-/workspace/coupefab-venv-tools/bin/python}"   # needs requests, beautifulsoup4, lxml
[ -x "$PY" ] || PY=python3
"$PY" prices/fetch_prices.py "$@"
python3 build.py > /dev/null
python3 scripts/deploy_manifest.py > /tmp/coupefab-deploy.json
git add -A data/prices prix en/sheet-prices sitemap.xml >/dev/null 2>&1 || true
git commit -q -m "prix: relevé $(TZ=America/Toronto date +%F)" >/dev/null 2>&1 || true
echo "OK: built. Deploy with the Vercel connector using /tmp/coupefab-deploy.json (create_deployment, team micro-bot)."
