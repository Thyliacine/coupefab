"""Coolant (cutting fluid) mixing calculator: /outils/calculateur-liquide-de-coupe/ (FR) and /en/tools/coolant-calculator/ (EN).

Machine tank capacities come from data/coolant-machines.json (every figure has a source URL; null = not published).
All math runs client-side in js/liquide-math.js (tested by tests/test_liquide_math.js); js/liquide.js drives the UI.
Also publishes the database as /outils/machines-liquide-de-coupe.json (CC BY 4.0).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "coolant-machines.json"
FR_PATH = "/outils/calculateur-liquide-de-coupe/"
EN_PATH = "/en/tools/coolant-calculator/"
PUBLIC_JSON = ROOT / "outils" / "machines-liquide-de-coupe.json"
GUIDE_FR = "/guides/arrosage-fluides-de-coupe/"
GUIDE_EN = "/en/guides/coolant-cutting-fluids/"
QA_PRODUCTS = "https://qalube.com/soluble-oil-coolants"
QA_BROCHURE = "https://qalube.com/QA-Coolant-Basics-Training-Brochure.pdf"

TYPES = {  # id: (fr, en)
    "vmc": ("Centre d’usinage vertical", "Vertical machining centre"),
    "hmc": ("Centre d’usinage horizontal", "Horizontal machining centre"),
    "5ax": ("Centre 5 axes", "5-axis machining centre"),
    "lathe": ("Tour CNC", "CNC lathe"),
    "millturn": ("Tour à outils motorisés / axe Y", "Mill-turn / Y-axis lathe"),
    "vtl": ("Tour vertical", "Vertical turning centre"),
    "boring": ("Aléseuse horizontale", "Horizontal boring mill"),
    "router": ("Routeur portique", "Gantry router"),
}


def esc(s) -> str:
    return (str(s if s is not None else "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def ver(rel: str) -> int:
    p = ROOT / rel
    return p.stat().st_mtime_ns // 1000 if p.exists() else 0


def nfr(x, d=0):
    s = f"{x:,.{d}f}"
    return s.replace(",", "\u202f").replace(".", ",")


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def write_public(d):
    PUBLIC_JSON.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_JSON.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def compact(d):
    """Rows for the page script: [brand, model, type, liters, gal, source, note_fr, note_en, variants]."""
    rows = []
    for m in d["machines"]:
        rows.append([m["brand"], m["model"], m["type"], m.get("liters"), m.get("us_gal"), m.get("source"),
                     m.get("note_fr") or "", m.get("note_en") or "",
                     [[v["label_fr"], v["label_en"], v["liters"], v["us_gal"]] for v in m.get("variants", [])]])
    return rows


def render(site="https://coupefab.ca"):
    d = load()
    write_public(d)
    machines = d["machines"]
    n_all = len(machines)
    n_cap = sum(1 for m in machines if m.get("liters"))
    brands = sorted({m["brand"] for m in machines}, key=str.lower)
    blob = json.dumps(compact(d), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    def page(fr: bool) -> str:
        L = (lambda a, b: a if fr else b)
        lang = "fr" if fr else "en"
        path = FR_PATH if fr else EN_PATH
        mail_subj = L("Capacité de réservoir — correction", "Coolant tank capacity — correction")
        mail_body = L("Machine (marque, modèle, année) :%0D%0ACapacité du réservoir (L ou gal US) :%0D%0ASource (manuel, plaque, fiche) :%0D%0A",
                      "Machine (brand, model, year):%0D%0ATank capacity (L or US gal):%0D%0ASource (manual, plate, spec sheet):%0D%0A")
        mailto = f"mailto:info@coupefab.ca?subject={esc(mail_subj).replace(' ', '%20')}&amp;body={mail_body.replace(' ', '%20')}"
        # static machine table (works without JS, indexable)
        trs = []
        for m in machines:
            cap = (f'{nfr(m["liters"]) if fr else f"{m["liters"]:,}"} L · {nfr(m["us_gal"], 1) if fr else m["us_gal"]} gal'
                   if m.get("liters") else L("non publiée — entrez la vôtre", "not published — enter your own"))
            note = m.get("note_fr" if fr else "note_en") or ""
            src = f'<a href="{esc(m["source"])}" rel="nofollow noopener" target="_blank">{L("source", "source")}</a>' if m.get("source") else ""
            trs.append(f'<tr data-q="{esc((m["brand"] + " " + m["model"]).lower())}"><td><b>{esc(m["brand"])}</b> {esc(m["model"])}'
                       + (f'<div class="lq-sub">{esc(note)}</div>' if note else "")
                       + f'</td><td>{esc(TYPES[m["type"]][0 if fr else 1])}</td><td class="lq-r lq-num">{cap}</td><td>{src}</td></tr>')
        brand_list = ", ".join(brands)
        ld = json.dumps({"@context": "https://schema.org", "@type": "WebApplication",
                         "name": L("Calculateur de liquide de coupe (concentration, appoint, réfractomètre)", "Coolant calculator (mix, top-up, refractometer)"),
                         "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "inLanguage": "fr-CA" if fr else "en-CA",
                         "url": site + path, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CAD"},
                         "publisher": {"@type": "Organization", "name": "CoupeFab", "url": site + "/"}}, ensure_ascii=False)
        ex_ph = L("ex. VF-2, a55, VX-1500, Puma", "e.g. VF-2, a55, VX-1500, Puma")
        return f"""<link rel="stylesheet" href="/css/outillage.css?v={ver('css/outillage.css')}">
<link rel="stylesheet" href="/css/liquide.css?v={ver('css/liquide.css')}">
<script type="application/ld+json">{ld}</script>
<div class="tl lq" id="lq-app" data-lang="{lang}">
<section class="tl-hero">
  <div class="tl-hero-top">
    <div>
      <p class="tl-kicker">{L("Outil d’atelier · arrosage", "Shop tool · coolant")}</p>
      <h1>{L("Calculateur de liquide de coupe : mélange, appoint et réfractomètre", "Coolant calculator: mix, top-up and refractometer")}</h1>
      <p class="tl-lede">{L(f"Choisissez votre machine ({n_cap} réservoirs documentés, chacun avec sa source) ou entrez le volume du bassin. Le calculateur donne la quantité de concentré et d’eau pour un remplissage neuf, la correction d’un bassin trop riche ou trop pauvre, et convertit la lecture du réfractomètre (Brix) en vraie concentration.",
                             f"Pick your machine ({n_cap} documented tanks, each with its source) or enter the sump volume. The calculator gives the concentrate and water for a fresh fill, the correction for a sump that is too rich or too lean, and converts the refractometer reading (Brix) into true concentration.")}</p>
    </div>
    <p class="tl-stamp"><span><b>{n_all}</b> {L("machines", "machines")} · {len(brands)} {L("marques", "brands")}</span><span>{L("Calcul dans votre navigateur", "Runs in your browser")}</span><span>{L("Litres et gallons US", "Litres and US gallons")}</span></p>
  </div>
</section>

<noscript><p class="tl-note">{L("Le calculateur a besoin de JavaScript. Le tableau des capacités plus bas fonctionne sans.", "The calculator needs JavaScript. The capacity table below works without it.")}</p></noscript>

<form class="lq-setup" id="lq-setup" onsubmit="return false" aria-label="{L("Machine et réglages", "Machine and settings")}">
  <div class="lq-field lq-machine">
    <label for="lq-q">{L("Machine", "Machine")}</label>
    <input id="lq-q" type="search" list="lq-list" autocomplete="off" spellcheck="false" placeholder="{esc(ex_ph)}">
    <datalist id="lq-list"></datalist>
    <p class="lq-help" id="lq-machine-info" aria-live="polite">{L("Tapez une marque ou un modèle, ou entrez le volume vous-même.", "Type a brand or model, or enter the volume yourself.")}</p>
    <div class="lq-variants" id="lq-variants" hidden></div>
  </div>
  <div class="lq-field">
    <label for="lq-cap">{L("Capacité du réservoir", "Tank capacity")}</label>
    <div class="lq-unitrow"><input id="lq-cap" type="text" inputmode="decimal" autocomplete="off" placeholder="{L("ex. 208", "e.g. 208")}">
      <span class="lq-seg" role="group" aria-label="{L("Unité", "Unit")}"><button type="button" data-unit="L" aria-pressed="true">L</button><button type="button" data-unit="gal" aria-pressed="false">{L("gal US", "US gal")}</button></span></div>
  </div>
  <div class="lq-field">
    <label for="lq-target">{L("Concentration visée (%)", "Target concentration (%)")}</label>
    <input id="lq-target" type="text" inputmode="decimal" value="{L("6", "6")}" autocomplete="off">
    <div class="lq-chips" role="group" aria-label="{L("Valeurs courantes", "Common values")}"><button type="button" class="chip" data-target="4">4 %</button><button type="button" class="chip" data-target="6">6 %</button><button type="button" class="chip" data-target="8">8 %</button><button type="button" class="chip" data-target="10">10 %</button></div>
  </div>
  <div class="lq-field">
    <label for="lq-factor">{L("Facteur du réfractomètre", "Refractometer factor")}</label>
    <input id="lq-factor" type="text" inputmode="decimal" value="{L("1,0", "1.0")}" autocomplete="off">
    <p class="lq-help">{L("Indiqué sur la fiche technique du produit (souvent entre 1 et 2). 1,0 si inconnu.", "Printed on the product data sheet (often 1 to 2). 1.0 if unknown.")}</p>
  </div>
</form>

<div class="lq-grid">
  <section class="lq-card" aria-labelledby="lq-h-fresh">
    <h2 id="lq-h-fresh"><span class="lq-n">A</span> {L("Remplissage neuf", "Fresh fill")}</h2>
    <p class="lq-help">{L("Bassin vidé et nettoyé, rempli à la capacité ci-dessus.", "Sump drained and cleaned, filled to the capacity above.")}</p>
    <div class="lq-out" id="lq-fresh" aria-live="polite"><p class="lq-wait">{L("Entrez la capacité et la concentration.", "Enter the capacity and the concentration.")}</p></div>
  </section>

  <section class="lq-card" aria-labelledby="lq-h-fix">
    <h2 id="lq-h-fix"><span class="lq-n">B</span> {L("Appoint et correction", "Top-up and correction")}</h2>
    <div class="lq-fields">
      <div class="lq-field"><label for="lq-brix">{L("Lecture actuelle (°Brix)", "Current reading (°Brix)")}</label><input id="lq-brix" type="text" inputmode="decimal" autocomplete="off" placeholder="{L("ex. 4,2", "e.g. 4.2")}"></div>
      <div class="lq-field"><label for="lq-cur">{L("Niveau actuel", "Current level")} <span class="lq-u" data-u></span></label><input id="lq-cur" type="text" inputmode="decimal" autocomplete="off">
        <div class="lq-chips" role="group" aria-label="{L("Niveau en % du réservoir", "Level as % of tank")}"><button type="button" class="chip" data-lvl="50">50 %</button><button type="button" class="chip" data-lvl="70">70 %</button><button type="button" class="chip" data-lvl="85">85 %</button></div></div>
      <div class="lq-field"><label for="lq-final">{L("Niveau voulu après", "Level wanted after")} <span class="lq-u" data-u></span></label><input id="lq-final" type="text" inputmode="decimal" autocomplete="off" placeholder="{L("= capacité", "= capacity")}"></div>
    </div>
    <div class="lq-out" id="lq-fix" aria-live="polite"><p class="lq-wait">{L("Entrez la lecture et le niveau actuel.", "Enter the reading and the current level.")}</p></div>
  </section>

  <section class="lq-card" aria-labelledby="lq-h-refr">
    <h2 id="lq-h-refr"><span class="lq-n">C</span> {L("Réfractomètre", "Refractometer")}</h2>
    <div class="lq-fields"><div class="lq-field"><label for="lq-brix2">{L("Lecture (°Brix)", "Reading (°Brix)")}</label><input id="lq-brix2" type="text" inputmode="decimal" autocomplete="off" placeholder="{L("ex. 4,2", "e.g. 4.2")}"></div></div>
    <div class="lq-out" id="lq-refr" aria-live="polite"><p class="lq-wait">{L("Vraie concentration = lecture Brix × facteur du produit.", "True concentration = Brix reading × product factor.")}</p></div>
    <p class="lq-help">{L("Faites le zéro avec de l’eau du robinet, prélevez le liquide qui circule (pas le dessus du bassin) et lisez la ligne de partage bleu/blanc.", "Zero it with tap water, sample the circulating fluid (not the top of the sump) and read the blue/white boundary.")}</p>
  </section>
</div>

<div class="tl-caveat lq-safety" role="note"><p><b>{L("Suivez la fiche technique du fabricant.", "Follow the manufacturer’s data sheet.")}</b>
  {L("Ces calculs supposent un mélange homogène et la plage de concentration de votre produit. Versez toujours le concentré dans l’eau (jamais l’inverse), portez gants et lunettes (fiche de données de sécurité), et faites l’appoint avec un prémélange plutôt qu’avec de l’eau ou du concentré pur. L’eau s’évapore, pas le concentré : entre deux appoints, la concentration monte. Vérifiez au réfractomètre après chaque correction.",
     "These figures assume a well-mixed sump and your product’s concentration range. Always pour concentrate into water (never the reverse), wear gloves and eye protection (safety data sheet), and top up with premix rather than straight water or concentrate. Water evaporates, concentrate does not: between top-ups the concentration climbs. Check with the refractometer after each correction.")}</p></div>

<h2 class="tl-h2">{L("Plages de concentration typiques", "Typical concentration ranges")}</h2>
<div class="tl-scroll lq-ref"><table class="tl-table">
  <thead><tr><th>{L("Opération", "Operation")}</th><th class="lq-r">{L("Plage typique", "Typical range")}</th><th>{L("Remarque", "Note")}</th></tr></thead>
  <tbody>
    <tr><td>{L("Rectification (meulage)", "Grinding")}</td><td class="lq-r lq-num">3 – 5 %</td><td>{L("Mélange plus pauvre : moins de mousse, meule propre.", "Leaner mix: less foam, cleaner wheel.")}</td></tr>
    <tr><td>{L("Usinage léger à moyen (fraisage, tournage)", "Light to moderate machining (milling, turning)")}</td><td class="lq-r lq-num">4 – 6 %</td><td>{L("Point de départ courant : 5 à 7 %.", "Common starting point: 5 to 7%.")}</td></tr>
    <tr><td>{L("Usinage lourd (taraudage, perçage profond, inox, titane)", "Heavy machining (tapping, deep drilling, stainless, titanium)")}</td><td class="lq-r lq-num">7 – 12 %</td><td>{L("Plus de lubrification; surveillez la peau et la mousse.", "More lubricity; watch for skin irritation and foam.")}</td></tr>
  </tbody></table></div>
<p class="lq-src">{L("Sources : plages recommandées des huiles solubles", "Sources: recommended dilution ranges for soluble oils")} <a href="{QA_PRODUCTS}" rel="nofollow noopener" target="_blank">QA Lubricants</a> · <a href="{QA_BROCHURE}" rel="nofollow noopener" target="_blank">{L("« Coolant Basics » (lecture × facteur)", "“Coolant Basics” (reading × factor)")}</a>. {L("Votre produit peut différer : sa fiche technique a priorité.", "Your product may differ: its data sheet wins.")}
 {L("Pour le choix du fluide et l’arrosage :", "For choosing the fluid and aiming it:")} <a href="{GUIDE_FR if fr else GUIDE_EN}">{L("guide Arrosage et fluides de coupe", "Coolant and cutting fluids guide")}</a>.</p>

<h2 class="tl-h2" id="machines">{L("Capacité des réservoirs par machine", "Coolant tank capacity by machine")} <small class="lq-count">({n_all})</small></h2>
<p class="tl-lead">{L(f"Capacités publiées par le fabricant, un revendeur ou un manuel, avec la source sur chaque ligne. Marques : {brand_list}. Les options (réservoir agrandi, convoyeur, filtre papier) changent le volume : la plaque ou le manuel de votre machine a priorité.",
                      f"Capacities published by the maker, a dealer or a manual, with the source on every row. Brands: {brand_list}. Options (larger tank, chip conveyor, paper filter) change the volume: your machine’s plate or manual wins.")}</p>
<div class="lq-tablebar"><label class="lq-field lq-filter"><span>{L("Filtrer le tableau", "Filter the table")}</span><input type="search" id="lq-filter" autocomplete="off" placeholder="{esc(ex_ph)}"></label>
  <a class="tl-btn lq-suggest" href="{mailto}">{L("Proposer une capacité ou une correction", "Suggest a capacity or a correction")}</a></div>
<div class="tl-scroll"><table class="tl-table lq-table" id="lq-table">
  <thead><tr><th>{L("Machine", "Machine")}</th><th>{L("Type", "Type")}</th><th class="lq-r">{L("Réservoir", "Tank")}</th><th>{L("Source", "Source")}</th></tr></thead>
  <tbody>{''.join(trs)}</tbody></table></div>
<p class="lq-src">{L("Données compilées par CoupeFab, réutilisables sous", "Data compiled by CoupeFab, reusable under")} <a href="https://creativecommons.org/licenses/by/4.0/" rel="license noopener">CC BY 4.0</a> : <a href="/outils/machines-liquide-de-coupe.json">machines-liquide-de-coupe.json</a>. {L("Haas : fiches de Haas Automation UK (mêmes modèles qu’en Amérique du Nord). Une capacité manque ou semble fausse?", "Haas: Haas Automation UK spec sheets (same models as in North America). A capacity missing or wrong?")} <a href="{mailto}">info@coupefab.ca</a>.</p>
<script type="application/json" id="lq-data">{blob}</script>
</div>
<script src="/js/liquide-math.js?v={ver('js/liquide-math.js')}" defer></script>
<script src="/js/liquide.js?v={ver('js/liquide.js')}" defer></script>
"""

    meta = {"machines": n_all, "with_capacity": n_cap, "brands": len(brands)}
    return page(True), page(False), meta


def page_entries(site="https://coupefab.ca"):
    fr, en, meta = render(site)
    n = meta["with_capacity"]
    return [
        (FR_PATH, EN_PATH, "fr",
         "Calculateur de liquide de coupe : concentration, appoint et réfractomètre — CoupeFab",
         f"Calculez le concentré et l’eau pour remplir ou corriger le bassin de votre CNC (Haas, Makino, Okuma, Mazak, DN Solutions, Hurco, Fadal…) : {n} capacités de réservoir sourcées, lecture Brix × facteur, litres et gallons.",
         fr, False, False),
        (EN_PATH, FR_PATH, "en",
         "Coolant calculator: concentration, top-up and refractometer — CoupeFab",
         f"Work out the concentrate and water to fill or correct your CNC coolant sump (Haas, Makino, Okuma, Mazak, DN Solutions, Hurco, Fadal…): {n} sourced tank capacities, Brix × factor, litres and US gallons.",
         en, False, False),
    ]
