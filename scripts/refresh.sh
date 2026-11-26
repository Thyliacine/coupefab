#!/usr/bin/env bash
# Daily CoupeFab price + used-equipment refresh: fetch -> build -> deploy manifest -> local commit.
# Usage: scripts/refresh.sh            daily: sheet & plate of every supplier + the small Shopify stores
#                                      (Aluminox, Forces Inc, Valmont, WeMachine, Smith Metal Shop, OptiKutz,
#                                      Canadian Laser Supply); weekly rows are kept from the last weekly run
#        scripts/refresh.sh --weekly   weekly: also bar/tube/pipe/angle (Metals 'R' Us collections, Metals Depot
#                                      39 categories, Acier Terrebonne WooCommerce variations)
#        scripts/refresh.sh --only metalsrus mercier40   only those suppliers
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${COUPEFAB_PY:-/workspace/coupefab-venv-tools/bin/python}"   # needs requests, beautifulsoup4, lxml
[ -x "$PY" ] || PY=python3
ARGS=()
for a in "$@"; do if [ "$a" = "--weekly" ]; then ARGS+=("--with-bars"); else ARGS+=("$a"); fi; done
"$PY" prices/fetch_prices.py "${ARGS[@]}"
"$PY" -m used.fetch_listings
python3 build.py > /dev/null
python3 scripts/deploy_manifest.py
git add -A data/prices prix en/sheet-prices sitemap.xml >/dev/null 2>&1 || true
git add data/used occasions en/used-equipment css/occasions.css js/occasions.js >/dev/null 2>&1 || true
git commit -q -m "prix et occasions: relevé $(TZ=America/Toronto date +%F)" >/dev/null 2>&1 || true
echo "OK: built. Deploy: see scripts/deploy_manifest.py (Vercel connector, team micro-bot, project coupefab)."
