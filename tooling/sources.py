"""Tooling price sources: public storefront feeds only (Shopify /products.json, WooCommerce Store API).

Every source was checked on 2026-11-26: robots.txt allows the feed for a generic crawler, the feed answers
without a login, captcha or bot challenge. Sites that answered 403 / bot walls are listed in BLOCKED and
are never fetched.
"""

SOURCES = [
    # --- Québec ------------------------------------------------------------
    {"id": "airtek", "name": "Airtek", "platform": "shopify", "host": "airtekltd.com", "lang_path": "/fr", "verify_pages": True,
     "city": "Saint-Laurent (Montréal)", "province": "QC", "country": "CA", "currency": "CAD", "max_pages": 80},
    {"id": "groupe-mortier", "name": "Groupe Mortier", "platform": "shopify", "host": "groupemortier.ca",
     "city": "", "province": "QC", "country": "CA", "currency": "CAD", "max_pages": 40},
    {"id": "oxypro", "name": "Oxypro", "platform": "shopify", "host": "oxypro-inc.com",
     "city": "", "province": "QC", "country": "CA", "currency": "CAD", "max_pages": 4},
    {"id": "fabtooling", "name": "Fabtooling", "platform": "shopify", "host": "fabtooling.ca",
     "city": "Lévis", "province": "QC", "country": "CA", "currency": "CAD", "max_pages": 4},
    {"id": "sharpex", "name": "Sharpex", "platform": "woo", "host": "sharpex.ca", "variations": True,
     "city": "", "province": "QC", "country": "CA", "currency": "CAD", "max_pages": 2},
    # --- Rest of Canada ----------------------------------------------------
    {"id": "glcs", "name": "Great Lakes Carbide Supply", "platform": "woo", "host": "glcs.shop",
     "city": "Kitchener", "province": "ON", "country": "CA", "currency": "CAD",
     # category id -> pages of 100 to read (the store has 45 000+ items; we sample the main families)
     "categories": {2010: 3, 2013: 1, 2007: 2, 1994: 2, 2003: 1, 1987: 2, 1984: 1, 1988: 1, 1989: 1, 2034: 1,
                    2020: 3, 2021: 2, 1964: 1, 1963: 1, 1912: 3, 2031: 2, 1803: 2, 1804: 2, 1805: 1,
                    1880: 1, 1898: 1, 2015: 1, 1997: 1, 2026: 1}},
    {"id": "accusize", "name": "Accusize Industrial Tools", "platform": "shopify", "host": "accusizetools.com",
     "city": "Markham", "province": "ON", "country": "CA", "currency": "CAD", "max_pages": 8},
    {"id": "busybee", "name": "Busy Bee Tools", "platform": "shopify", "host": "www.busybeetools.com",
     "city": "Concord", "province": "ON", "country": "CA", "currency": "CAD", "max_pages": 20},
    {"id": "wiseline", "name": "Wise Line Tools", "platform": "shopify", "host": "wiselinetools.ca",
     "city": "", "province": "ON", "country": "CA", "currency": "CAD", "max_pages": 45},
    {"id": "cncrouterstore", "name": "CNC Router Store", "platform": "shopify", "host": "www.cncrouterstore.ca",
     "city": "", "province": "ON", "country": "CA", "currency": "CAD", "max_pages": 26},
    {"id": "superior-tool", "name": "Superior Tool Supply", "platform": "shopify", "host": "superiortoolsupply.ca",
     "city": "Cambridge", "province": "ON", "country": "CA", "currency": "CAD", "max_pages": 2},
    {"id": "machinists-vault", "name": "Machinist’s Vault", "platform": "shopify", "host": "machinistsvault.com",
     "city": "", "province": "ON", "country": "CA", "currency": "CAD", "max_pages": 6},
    {"id": "canadian-woodworker", "name": "Canadian Woodworker", "platform": "woo", "host": "www.canadianwoodworker.com",
     "city": "Winnipeg", "province": "MB", "country": "CA", "currency": "CAD",
     "categories": {392: 1, 323: 1, 304: 1, 169: 1}},
    # --- United States, ships to Canada (USD converted at the site’s Bank of Canada rate) ----------------
    {"id": "langmuir", "name": "Langmuir Systems", "platform": "shopify", "host": "www.langmuirsystems.com",
     "city": "Texas", "province": "", "country": "US", "currency": "USD", "max_pages": 3},
    {"id": "benchmark-abrasives", "name": "Benchmark Abrasives", "platform": "shopify", "host": "benchmarkabrasives.com",
     "city": "Arizona", "province": "", "country": "US", "currency": "USD", "max_pages": 6},
    {"id": "red-label-abrasives", "name": "Red Label Abrasives", "platform": "shopify", "host": "www.redlabelabrasives.com",
     "city": "Michigan", "province": "", "country": "US", "currency": "USD", "max_pages": 4},
]

# Checked 2026-11-26 and NOT fetched (bot wall, robots.txt, or no public price feed).
BLOCKED = [
    {"name": "CSL Industriel", "host": "cslindustriel.com", "province": "QC", "why_fr": "Réponse 403 (pare-feu anti-robots) — prix visibles seulement dans un navigateur.", "why_en": "HTTP 403 (bot firewall) — prices only visible in a browser."},
    {"name": "Cantin et fils (catalogue)", "host": "catalogue.cantinindustriel.com", "province": "QC", "why_fr": "Réponse 403 (pare-feu anti-robots).", "why_en": "HTTP 403 (bot firewall)."},
    {"name": "Pronet Distribution", "host": "pronetindustriel.com", "province": "QC", "why_fr": "Réponse 403 (pare-feu anti-robots).", "why_en": "HTTP 403 (bot firewall)."},
    {"name": "Meunier Outillage Industriel", "host": "outillagemeunier.com", "province": "QC", "why_fr": "Réponse 403 (pare-feu anti-robots).", "why_en": "HTTP 403 (bot firewall)."},
    {"name": "Outils Pierre Berger", "host": "outilspierreberger.com", "province": "QC", "why_fr": "Réponse 403 (pare-feu anti-robots).", "why_en": "HTTP 403 (bot firewall)."},
    {"name": "Les Attaches Richard", "host": "lesattachesrichard.com", "province": "QC", "why_fr": "robots.txt interdit l’exploration.", "why_en": "robots.txt disallows crawling."},
    {"name": "Groupe Sabec", "host": "sabec.ca", "province": "QC", "why_fr": "Site injoignable depuis notre robot (erreur de certificat).", "why_en": "Unreachable from our fetcher (certificate error)."},
    {"name": "Outillage Industriel Québec", "host": "quebecindustriel.com", "province": "QC", "why_fr": "Catalogue sans prix affichés.", "why_en": "Catalogue shows no prices."},
    {"name": "Drillmex", "host": "drillmex.com", "province": "QC", "why_fr": "Prix sur soumission seulement.", "why_en": "Quote only."},
    {"name": "Cobalt Industrial", "host": "cobaltindustrial.ca", "province": "AB", "why_fr": "robots.txt interdit l’exploration.", "why_en": "robots.txt disallows crawling."},
    {"name": "Infinity Industrial", "host": "shop.infinityindustrial.ca", "province": "ON", "why_fr": "Réponse 403 (pare-feu anti-robots).", "why_en": "HTTP 403 (bot firewall)."},
    {"name": "Machinery Canada (Techleader)", "host": "shop.machinerycanada.com", "province": "ON", "why_fr": "Page de vérification anti-robots (202).", "why_en": "Bot-check page (HTTP 202)."},
    {"name": "Toolup", "host": "toolup.com", "province": "", "why_fr": "Réponse 403 (pare-feu anti-robots).", "why_en": "HTTP 403 (bot firewall)."},
    {"name": "Lakeshore Carbide", "host": "lakeshorecarbide.com", "province": "", "why_fr": "Erreur serveur 500 au relevé.", "why_en": "Server error 500 when checked."},
    {"name": "Travers Tool", "host": "travers.com", "province": "", "why_fr": "robots.txt interdit l’exploration.", "why_en": "robots.txt disallows crawling."},
    {"name": "Shars, ToolsToday, Maritool, Precise Bits", "host": "", "province": "", "why_fr": "Pas de flux public structuré ; non relevés pour l’instant.", "why_en": "No structured public feed; not recorded yet."},
]
