"""Error-code / alarm reference: content/error-codes.json -> /codes-erreur/ (FR) and /en/error-codes/ (EN),
plus per-brand tables reused inside guides ("Codes d'erreur" tab).

Rule: only codes read in a public manual or official document; every table cites its source."""
import json
import re
from functools import lru_cache
from pathlib import Path

from .layout import esc, SITE
from .taxonomy import T, PATHS

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "content" / "error-codes.json"
URL = {"fr": "/codes-erreur/", "en": "/en/error-codes/"}
KIND = {"cnc": ("Commandes CNC (fraiseuse, tour)", "CNC controls (mill, lathe)"),
        "plasma": ("Plasma", "Plasma"),
        "laser": ("Laser fibre", "Fiber laser"),
        "router": ("Routeurs et contrôleurs PC", "Routers and PC controllers")}
KIND_ORDER = ["cnc", "plasma", "laser", "router"]


@lru_cache(maxsize=1)
def data():
    if not DATA.exists():
        return {"sources": {}, "brands": [], "codes": [], "missing": [], "accessed": ""}
    return json.loads(DATA.read_text(encoding="utf-8"))


def _guide_link(gid, lang):
    if not gid:
        return ""
    from .guides import by_id
    g = by_id().get(gid)
    if not g:
        return ""
    return f'<a href="{g.url(lang)}">{esc(g.nav(lang))}</a>'


def _src_line(keys, lang):
    d = data()
    fr = lang == "fr"
    items = []
    for k in keys:
        s = d["sources"].get(k)
        if s:
            items.append(f'<a href="{esc(s["u"])}" class="ext" rel="noopener">{esc(s["t"])}</a>')
    lab = "Source" if len(items) == 1 else "Sources"
    when = f' · {"consulté le 26 novembre 2026" if fr else "consulted November 26, 2026"}'
    return f'<p class="ec-src"><strong>{lab} :</strong> {" ; ".join(items)}{when}</p>' if fr else \
           f'<p class="ec-src"><strong>{lab}:</strong> {"; ".join(items)}{when}</p>'


def _rows(codes, lang, with_brand=False):
    fr = lang == "fr"
    out = []
    for c in codes:
        meaning = c["fr"] if fr else c["en"]
        act = c["afr"] if fr else c["aen"]
        msg = f'<span class="ec-msg">{esc(c["m"])}</span>' if c.get("m") and c["m"] not in ("Fault",) else ""
        pri = f'<span class="ec-pri ec-pri-{esc(_slug(c["p"]))}">{esc(_pri(c["p"], lang))}</span>' if c.get("p") else ""
        hay = " ".join([c["c"], c.get("m", ""), c["fr"], c["en"], c["b"]]).lower()
        out.append(f'<tr data-b="{c["b"]}" data-q="{esc(hay)}"><th scope="row" class="ec-code"><code>{esc(c["c"])}</code>{pri}</th>'
                   f'<td>{msg}{esc(meaning)}</td><td>{esc(act)}</td></tr>')
    return "".join(out)


def _slug(s):
    return re.sub(r"[^a-z]+", "-", s.lower().replace("é", "e").replace("ê", "e")).strip("-")


_PRI_EN = {"Défaillance": "Failure", "Erreur": "Error", "Alerte": "Alert", "Info": "Info", "Arrêt": "Stops"}


def _pri(p, lang):
    return p if lang == "fr" else _PRI_EN.get(p, p)


def brand_block(bkey, lang, heading_level=3, limit=None):
    """One brand: heading, note, table, source line."""
    d = data()
    fr = lang == "fr"
    b = next((x for x in d["brands"] if x["k"] == bkey), None)
    if not b:
        return ""
    codes = [c for c in d["codes"] if c["b"] == bkey]
    shown = codes if not limit else codes[:limit]
    srcs = []
    for c in codes:
        if c["s"] not in srcs:
            srcs.append(c["s"])
    note = b["nfr"] if fr else b["nen"]
    hid = f"ec-{bkey}"
    h = f'<h{heading_level} id="{hid}">{esc(b["n"])} — {esc(b["fr"] if fr else b["en"])} <span class="ec-count">{len(codes)}</span></h{heading_level}>'
    cols = ("Code", "Signification", "Quoi vérifier") if fr else ("Code", "Meaning", "What to check")
    more = ""
    if limit and len(codes) > limit:
        more = (f'<p class="ec-more"><a href="{URL[lang]}#{hid}">{"Voir les" if fr else "See all"} {len(codes)} codes {esc(b["n"])} →</a></p>')
    return (f'<section class="ec-brand" data-brand="{bkey}" data-kind="{b["kind"]}">{h}'
            + (f'<p class="ec-note">{esc(note)}</p>' if note else "")
            + f'<div class="table-wrap" tabindex="0"><table class="ec-table"><caption class="vh">{esc(b["n"])} — {esc(b["fr"] if fr else b["en"])}</caption>'
            f'<thead><tr><th scope="col">{cols[0]}</th><th scope="col">{cols[1]}</th><th scope="col">{cols[2]}</th></tr></thead>'
            f'<tbody>{_rows(shown, lang)}</tbody></table></div>{more}{_src_line(srcs, lang)}</section>')


def guide_section(brand_keys, lang):
    """Markdown-free HTML section for a guide's 'Codes d'erreur' tab. Returns (html, toc_entry)."""
    fr = lang == "fr"
    hid = "codes-d-erreur" if fr else "error-codes"
    title = "Codes d’erreur et alarmes" if fr else "Error codes and alarms"
    intro = ("Codes tirés uniquement des manuels et documents officiels publics, avec la source sous chaque tableau. "
             "Le numéro exact et sa signification peuvent varier selon la version du logiciel et le fabricant de la machine : en cas de doute, le manuel de <em>votre</em> machine fait foi."
             if fr else
             "Codes taken only from public manuals and official documents, with the source under each table. "
             "Exact numbers and meanings can vary with software version and machine builder: when in doubt, <em>your</em> machine’s manual wins.")
    blocks = "".join(brand_block(k, lang, 3, limit=40) for k in brand_keys)
    look = (f'<p class="ec-cta"><a class="btn-ghost" href="{URL[lang]}">{"Chercher un code dans toutes les marques" if fr else "Search a code across all brands"} →</a></p>')
    return f'<section class="ec-guide"><h2 id="{hid}">{title}</h2><p>{intro}</p>{blocks}{look}</section>', (2, hid, title)


def _first_response(lang):
    if lang == "fr":
        return """<ol class="steps ec-steps">
<li><strong>Sécurisez.</strong> Arrêt d’urgence si quelqu’un ou quelque chose est en danger. Ne mettez jamais la main dans la zone de travail d’une machine en alarme sans cadenassage.</li>
<li><strong>Notez tout</strong> avant d’appuyer sur RESET : numéro, texte exact, axe, bloc ou ligne du programme, ce que la machine faisait. Une photo de l’écran suffit.</li>
<li><strong>Lisez l’historique</strong> des alarmes : la première alarme de la série est souvent la vraie cause (ex. surcharge suivie de surintensité = collision).</li>
<li><strong>Cherchez le code ici</strong>, puis dans le manuel de votre machine : le fabricant de la machine ajoute souvent ses propres alarmes (API).</li>
<li><strong>Corrigez une cause à la fois</strong> et refaites un essai à vitesse réduite (bloc par bloc, avance réduite, marche à vide).</li>
<li><strong>Appelez le service</strong> pour tout ce qui touche l’armoire électrique, les variateurs ou une alarme qui revient. Donnez-leur vos notes.</li>
</ol>"""
    return """<ol class="steps ec-steps">
<li><strong>Make it safe.</strong> E-stop if anyone or anything is at risk. Never reach into the work zone of a machine in alarm without lockout.</li>
<li><strong>Write it all down</strong> before pressing RESET: number, exact text, axis, program block or line, what the machine was doing. A photo of the screen is enough.</li>
<li><strong>Read the alarm history</strong>: the first alarm in the chain is often the real cause (e.g. overload followed by overcurrent = crash).</li>
<li><strong>Look the code up here</strong>, then in your machine’s manual: builders often add their own (PLC) alarms.</li>
<li><strong>Fix one cause at a time</strong> and test at reduced speed (single block, reduced feed, dry run).</li>
<li><strong>Call service</strong> for anything inside the electrical cabinet, drives, or an alarm that keeps coming back. Give them your notes.</li>
</ol>"""


def page(lang):
    from .guides import breadcrumbs
    from .layout import ASSET_V
    d = data()
    fr = lang == "fr"
    t, p = T[lang], PATHS[lang]
    total = len(d["codes"])
    crumbs = breadcrumbs(lang, [(t["home"], p["home"]), (t["guides"], p["guides"]), ("Codes d’erreur" if fr else "Error codes", None)])
    opts = "".join(f'<option value="{b["k"]}">{esc(b["n"])} — {esc(b["fr"] if fr else b["en"])} ({b["count"]})</option>'
                   for k in KIND_ORDER for b in d["brands"] if b["kind"] == k)
    kinds = (f'<button type="button" class="chip" aria-pressed="true" data-kind="all">{"Tout" if fr else "All"}</button>'
             + "".join(f'<button type="button" class="chip" aria-pressed="false" data-kind="{k}">{esc(KIND[k][0 if fr else 1])}</button>' for k in KIND_ORDER))
    sections = []
    for k in KIND_ORDER:
        bs = [b for b in d["brands"] if b["kind"] == k]
        if not bs:
            continue
        sections.append(f'<div class="ec-kind" data-kind-sec="{k}"><h2 class="sec-h" id="{k}">{esc(KIND[k][0 if fr else 1])}</h2>'
                        + "".join(brand_block(b["k"], lang, 3) for b in bs) + "</div>")
    missing = "".join(f'<li><strong>{esc(m["n"])}</strong> — {esc(m["fr"] if fr else m["en"])}</li>' for m in d["missing"])
    counts = " · ".join(f'{esc(b["n"])} {esc(b["fr"] if fr else b["en"]).split(" (")[0]} : {b["count"]}' if fr else f'{esc(b["n"])} {esc(b["en"]).split(" (")[0]}: {b["count"]}' for b in d["brands"])
    title = "Codes d’erreur et alarmes CNC, plasma et laser" if fr else "CNC, plasma and laser error codes and alarms"
    lede = (f"{total} codes et messages tirés des manuels officiels (Haas, Siemens, FANUC, Hypertherm, ESAB, Lincoln, Grbl…), en français et en anglais, avec la source sous chaque tableau. Tapez le code tel qu’il s’affiche."
            if fr else
            f"{total} codes and messages from official manuals (Haas, Siemens, FANUC, Hypertherm, ESAB, Lincoln, Grbl…), in English and French, with the source under each table. Type the code as it appears.")
    ld = json.dumps({"@context": "https://schema.org", "@type": "TechArticle", "headline": title, "inLanguage": "fr-CA" if fr else "en-CA",
                     "url": SITE + URL[lang], "dateModified": d.get("accessed", "2026-11-26"),
                     "publisher": {"@type": "Organization", "name": "CoupeFab", "url": SITE + "/"}}, ensure_ascii=False)
    return f"""
<link rel="stylesheet" href="/css/guides2.css?v={ASSET_V}">
<div class="page ec-page">
{crumbs}
<header class="page-head">
  <p class="kicker">{"Dépannage · référence" if fr else "Troubleshooting · reference"}</p>
  <h1>{title}</h1>
  <p class="lede">{lede}</p>
</header>
<form class="ec-tools" role="search" action="{URL[lang]}">
  <div class="ec-field ec-field-q">
    <label for="ec-q">{"Code ou mot-clé" if fr else "Code or keyword"}</label>
    <input type="search" id="ec-q" name="q" inputmode="search" autocomplete="off" placeholder="{'ex. 0-50, 108, 25050, ALARM:9, pression' if fr else 'e.g. 0-50, 108, 25050, ALARM:9, pressure'}" aria-describedby="ec-status">
  </div>
  <div class="ec-field">
    <label for="ec-brand">{"Marque et commande" if fr else "Brand and control"}</label>
    <select id="ec-brand" name="b"><option value="">{"Toutes les marques" if fr else "All brands"} ({total})</option>{opts}</select>
  </div>
  <div class="chips ec-kinds" role="group" aria-label="{'Type de machine' if fr else 'Machine type'}">{kinds}</div>
  <p id="ec-status" class="ec-status" role="status" aria-live="polite"></p>
</form>
<p class="ec-empty" hidden>{"Aucun code trouvé. Vérifiez la marque, essayez sans tirets ou avec un mot du message." if fr else "No code found. Check the brand, try without dashes or with a word from the message."}</p>
<details class="ec-first">
  <summary>{"Première réaction devant une alarme (à lire une fois)" if fr else "First response to an alarm (read once)"}</summary>
  {_first_response(lang)}
</details>
{''.join(sections)}
<section class="ec-missing">
  <h2 id="{'marques-absentes' if fr else 'missing-brands'}">{"Marques sans liste publique vérifiable" if fr else "Brands without a verifiable public list"}</h2>
  <p>{"Nous ne publions aucun code que nous n’avons pas lu dans un document officiel. Pour ces marques, consultez le manuel fourni avec la machine ou le service du fabricant :" if fr else "We publish no code we have not read in an official document. For these brands, use the manual shipped with the machine or the builder’s service:"}</p>
  <ul>{missing}</ul>
  <p class="ec-src">{"Un code manque ou est mal traduit ? " if fr else "Missing or mistranslated code? "}<a href="{p['about']}#contact">{"Écrivez-nous avec la page du manuel" if fr else "Send us the manual page"}</a>.</p>
</section>
</div>
<script src="/js/codes.js?v={ASSET_V}" defer></script>
<script type="application/ld+json">{ld}</script>
"""


def search_entries(lang):
    fr = lang == "fr"
    d = data()
    brands = " ".join(b["n"] + " " + (b["fr"] if fr else b["en"]) for b in d["brands"])
    return [{"t": "Codes d’erreur et alarmes" if fr else "Error codes and alarms",
             "d": ("Chercher un code d’alarme Haas, Siemens, FANUC, Hypertherm Powermax et XPR, ESAB, Lincoln, Grbl…" if fr
                   else "Look up Haas, Siemens, FANUC, Hypertherm Powermax and XPR, ESAB, Lincoln, Grbl alarm codes…"),
             "u": URL[lang], "h": "", "c": "Outil" if fr else "Tool", "k": ("alarme code erreur défaut " if fr else "alarm error fault code ") + brands}]
