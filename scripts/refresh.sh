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
for a in "$@"; do if [ "$a" = "--weekly" ]; then ARGS+=("--with-bars"); elif [ "$a" = "--tooling" ]; then :; else ARGS+=("$a"); fi; done
"$PY" prices/fetch_prices.py "${ARGS[@]}"
"$PY" -m used.fetch_listings
# Tooling prices (/outillage/): weekly (Mondays or --weekly); ~20 public storefront feeds, ~15 min, polite 1 req/s.
# A failing source keeps its previous rows, and a failed run never blocks the daily build.
if [ "$(TZ=America/Toronto date +%u)" = "1" ] || printf '%s\n' "$@" | grep -qx -- "--weekly\|--tooling"; then
  "$PY" -m tooling.fetch_tooling || echo "WARN: tooling fetch failed; keeping data/tooling/prices.json"
fi
# Hot news JSON (data/news/latest.json): worldwide CNC / machining / laser / plasma / fabrication
# industry RSS (headline, date, source, short excerpt only). Never invents items or copies full articles.
# Homepage and /nouvelles/ are rebuilt from this file.
"$PY" -m news.build || echo "WARN: news.build failed; keeping data/news/latest.json"
python3 build.py > /dev/null
python3 scripts/deploy_manifest.py
# Stage the refreshed data and every generated page (all index.html, sitemap, JSON/CSV exports) so the
# tree ends clean; hand-edited source (*.py, sitekit/, content/, css/, js/) is left alone on purpose.
git add -A data/prices data/used data/tooling data/news prix pieces outillage occasions nouvelles en/sheet-prices en/parts en/tooling en/used-equipment en/news \
  sitemap.xml 404.html guides/recherche.json en/guides/search.json >/dev/null 2>&1 || true
git add -A -- ':(glob)**/index.html' >/dev/null 2>&1 || true
git commit -q -m "prix et occasions: relevé $(TZ=America/Toronto date +%F)" >/dev/null 2>&1 || true
echo "OK: built. Deploy: see scripts/deploy_manifest.py (Vercel connector, team micro-bot, project coupefab)."
