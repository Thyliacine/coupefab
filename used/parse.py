"""Normalize titles into category, make, model, year, hours and a relevance flag."""
from __future__ import annotations

import hashlib
import re
import unicodedata

# Display labels (fr, en)
CATEGORIES = {
    "plasma_table": ("Table plasma", "Plasma table"),
    "laser": ("Laser", "Laser"),
    "waterjet": ("Jet d’eau", "Waterjet"),
    "router": ("Routeur CNC", "CNC router"),
    "mill": ("Fraiseuse / centre d’usinage", "Mill / machining centre"),
    "lathe": ("Tour", "Lathe"),
    "press_brake": ("Presse plieuse", "Press brake"),
    "shear": ("Cisaille", "Shear"),
    "roll": ("Rouleau à plaques", "Plate roll"),
    "punch": ("Poinçonneuse", "Punch / ironworker"),
    "welder": ("Soudeuse", "Welder"),
    "compressor": ("Compresseur", "Compressor"),
    "edm": ("Électroérosion", "EDM"),
    "saw": ("Scie à métaux", "Metal saw"),
    "other": ("Autre", "Other"),
}

# Official-ish make aliases, longest first when matching.
MAKES = [
    "hypertherm", "machitech", "thermal dynamics", "lincoln electric", "miller electric",
    "bystronic", "trumpf", "truma", "amada", "lvd", "prima power", "salvagnini", "mitsubishi",
    "mazak", "okuma", "dmg mori", "deckel maho", "doosan", "dn solutions", "haas", "hurco",
    "fadal", "bridgeport", "hardinge", "cincinnati", "makino", "kitamura", "brother", "tormach",
    "takumi", "awea", "enshu", "tos varnsdorf", "innocenti", "pegard", "alesa monti",
    "esab", "koike", "messer", "kaliburn", "avid cnc", "torchmate", "plasmacam", "langmuir",
    "boss laser", "primeweld", "yeswelder", "forney", "lotos", "everlast", "hobart", "miller",
    "lincoln", "baykal", "durma", "accurpress", "accurshear", "haco", "ermak", "gasparini",
    "davi", "cidan", "roper whitney", "baileigh", "piranha", "metfab", "wysong", "niagara",
    "pacific", "allsteel", "flow", "omax", "wardjet", "jet edge", "calypso", "chukar",
    "hyd-mech", "hydmech", "marvel", "doall", "kalamazoo", "king canada", "jet",
    "sullair", "atlas copco", "ingersoll rand", "kaeser", "quincy", "chicago pneumatic", "ozen",
    "e.b.f", "ebf", "hd ebf", "alpha lazer", "alpha laser", "xintian", "ajan",
    "scm", "biesse", "homag", "thermwood", "multicam", "axyz", "c.r. onsrud", "cr onsrud",
    "shopsabre", "laguna", "first", "berico", "mcdougall", "milltronics", "romi", "takisawa",
    "ycm", "sodick", "fanuc", "siemens", "centroid", "masso", "pronovost", "hydro précision",
    "hydro precision", "fusion arc", "otc-daihen",
]

# Category detectors: (category, regex) first match wins, so order matters.
_CAT_RULES = [
    ("plasma_table", r"\b(table\s+(de\s+)?d[eé]coupe\s+plasma|cnc\s+plasma|plasma\s+(cutting\s+)?table|d[eé]coupe\s+plasma|plasma[- ]cutter|powermax|xpr[\s-]?\d|hpr[\s-]?\d|avenger|sabre exe|crossfire)\b"),
    ("laser", r"\b((cnc\s+)?(fiber|fibre)\s+laser|d[eé]coupeuse\s+laser|laser\s+(fibre|fiber|cnc|cutting|d[eé]coupe)|bystronic|byspeed|trumpf\s+3\d|amada\s+fo|apollo\s+cnc\s+fiber)\b"),
    ("waterjet", r"\b(jet\s*d['’]?eau|water\s*jet|waterjet|omax|wardjet|flow\s+water|calypso|chukar)\b"),
    ("press_brake", r"\b(presse?\s+plieuse|press[- ]brake|trumabend|titan\s+25t|aphs|hg[\s-]?\d{3,4})\b"),
    ("shear", r"\b(cisaille|shear(?!\s*baler)|accur shear|accurshear)\b"),
    ("roll", r"\b(rouleau\s+[àa]\s+plaques|plate[- ]roll|plate\s+bending|4[- ]roll|4\s+rouleaux)\b"),
    ("punch", r"\b(poinçonneuse|punch\s+press|ironworker|embosseuse|d[eé]fonceuse embosseuse|punch and laser)\b"),
    ("edm", r"\b(electro[- ]?erosion|[eé]lectro[eé]rosion|\bedm\b|wire\s+edm|sinker)\b"),
    ("router", r"\b(routeur\s+cnc|cnc\s+router|table\s+pleine|nesting|thermwood|pratix|rover\s+s|axyz|onsrud|shopsabre)\b"),
    ("lathe", r"\b(tour\s+(cnc|[àa]\s+fer|hybride)|cnc\s+lathe|turning\s+center|turning\s+centre|\bst[-]?\d{1,2}\b|multiplex|toolroom\s+lathe)\b"),
    ("mill", r"\b(fraiseuse|centre\s+d['’]?usinage|machining\s+center|machining\s+centre|vertical\s+mill|\bvf[-]?\d|\btm[-]?\d|boring\s+mill|al[eé]sage|surfaceuse|grinder|milling\s+machine|toolroom\s+mill)\b"),
    ("welder", r"\b(soudeuse|weld(er|ing)\s+(machine|cell|power)?|weld\s+cell|mig\s+|tig\s+|multiprocess)\b"),
    ("compressor", r"\b(compresseur|air\s+compressor|screw\s+compressor|rotary\s+screw)\b"),
    ("saw", r"\b(scie\s+[àa]\s+(ruban|m[eé]tal|metaux)|band\s*saw|cold\s+saw|hyd[- ]?mech)\b"),
]

RELEVANT = re.compile(
    r"\b(cnc|plasma|laser|waterjet|jet\s*d['’]?eau|fraiseuse|machining\s+cent|tour\s+(cnc|[àa]\s+fer)|"
    r"lathe|press[- ]brake|presse?\s+plieuse|cisaille|shear|poinçonn|punch|rouleau\s+[àa]\s+plaques|"
    r"plate[- ]roll|soudeuse|weld(er|ing)|compresseur|compressor|edm|[eé]lectro[eé]rosion|"
    r"routeur|router|hypertherm|haas|mazak|trumpf|bystronic|amada|esab|okuma|bridgeport|"
    r"band\s*saw|scie\s+[àa]\s+(ruban|m[eé]tal)|perceuse\s+radiale|radial\s+drill|"
    r"surface\s*grinder|boring\s+mill|ironworker|powermax|langmuir|crossfire|tormach|avid|torchmate)\b",
    re.I,
)

IRRELEVANT = re.compile(
    r"\b(souffleur\s+[àa]\s+neige|snow\s*blower|botteuse|pellet\s+mill|baler|shear\s+baler|shredder|scanner|"
    r"granulator|centrifugal\s+pump|curtain[- ]side\s+trailer|vibrating\s+screen|"
    r"cardboard|plastic\s+film|spoon\s+filling|bag[- ]making|pallet\s+line|"
    r"ligne\s+de\s+jointage|ensacheuse|mouluri[eè]re|plaqueuse\s+de\s+chants|"
    r"sableuse\s+[àa]\s+(panneaux|ballon|marches)|corroyeur|planeur\s+1\s+face|"
    r"chambre\s+[àa]\s+peinture|air\s+make[- ]up)\b",
    re.I,
)

# ALX category slugs that are in scope even if the title is terse.
ALX_OK_SLUGS = {
    "transformation-metaux-usagees", "cnc-decoupe-au-laser", "presse-plieuse-press-brake",
    "cisaille-metal", "punch-press", "rouleaux-formateur", "tours", "fraiseuse",
    "centre-dusinage-cnc", "surfaceuse-grinder", "compresseur-a-vis", "compresseur-a-piston",
    "cnc-table-pleine", "cnc-table-pleine-cnc-a-bois", "presse-metal", "presse-a-die",
}

YEAR_RE = re.compile(r"\b((?:19|20)\d{2})\b")
HOURS_RE = re.compile(r"\b(\d[\d\s,]{0,6})\s*(?:h|hrs?|heures?|spindle hours?|hours?)\b", re.I)
PRICE_RE = re.compile(
    r"(?:USD|CAD|C\$|US\$|\$)\s*([\d]{1,3}(?:[\s,\u00a0]\d{3})+(?:\.\d{2})?|[\d]+(?:\.\d{2})?)"
    r"|([\d]{1,3}(?:[\s,\u00a0]\d{3})+(?:\.\d{2})?)\s*(?:\$|CAD|USD)",
    re.I,
)


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", (s or ""))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("\xa0", " ")).strip()


def unescape_basic(s: str) -> str:
    return (s or "").replace("&amp;", "&").replace("&prime;", "′").replace("&#x27;", "'").replace("&apos;", "'").replace("&#39;", "'").replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">")


def slug_id(source: str, url: str, title: str = "") -> str:
    raw = (url or title or "").encode("utf-8")
    h = hashlib.sha1(raw).hexdigest()[:10]
    return f"{source}-{h}"


def is_relevant(title: str, category_blob: str = "") -> bool:
    blob = f"{title} {category_blob}"
    if IRRELEVANT.search(blob):
        return False
    if RELEVANT.search(blob):
        return True
    # category slug fallback
    slugs = re.findall(r"[a-z0-9-]{4,}", (category_blob or "").lower())
    if any(s in ALX_OK_SLUGS or "metaux" in s or "metal" in s for s in slugs):
        return True
    return False


def category_of(title: str, category_blob: str = "") -> str:
    blob = f"{title} {category_blob}"
    for cat, pat in _CAT_RULES:
        if re.search(pat, blob, re.I):
            return cat
    # ALX slug hints
    low = (category_blob or "").lower()
    if "presse-plieuse" in low or "press-brake" in low:
        return "press_brake"
    if "cisaille" in low:
        return "shear"
    if "tours" in low:
        return "lathe"
    if "fraiseuse" in low or "centre-dusinage" in low:
        return "mill"
    if "compresseur" in low:
        return "compressor"
    if "cnc-table" in low or "nesting" in low:
        return "router"
    if "decoupe-au-laser" in low or "laser" in low:
        return "laser"
    if "punch" in low:
        return "punch"
    if "rouleaux" in low:
        return "roll"
    return "other"


def extract_year(text: str) -> int | None:
    years = [int(y) for y in YEAR_RE.findall(text or "")]
    years = [y for y in years if 1970 <= y <= 2026]
    return years[0] if years else None


def extract_hours(text: str) -> int | None:
    m = HOURS_RE.search(text or "")
    if not m:
        return None
    try:
        return int(re.sub(r"[^\d]", "", m.group(1)))
    except ValueError:
        return None


def extract_price(text: str) -> tuple[float | None, str | None]:
    """Return (amount, currency) if a price is clearly published in the text."""
    if not text:
        return None, None
    low = text.lower()
    if any(k in low for k in ("demander le prix", "ask for price", "request a quote", "prix sur demande", "call for price", "call for pricing")):
        # A page that only invites a quote is not a published asking price,
        # even if an amount appears in a nearby script or API.
        if not re.search(r"\$\s*\d", text):
            return None, None
    m = PRICE_RE.search(text.replace("\u202f", " ").replace(",", ","))
    if not m:
        return None, None
    raw = m.group(1) or m.group(2)
    if not raw:
        return None, None
    n = raw.replace("\xa0", "").replace(" ", "").replace(",", "")
    try:
        amt = float(n)
    except ValueError:
        return None, None
    if amt < 20 or amt > 5_000_000:
        return None, None
    cur = "CAD"
    around = text[max(0, m.start() - 12): m.end() + 8].upper()
    if "USD" in around or "US$" in around:
        cur = "USD"
    return amt, cur


def extract_make_model(title: str) -> tuple[str | None, str | None]:
    t = unescape_basic(norm_ws(title))
    low = fold(t).lower()
    make = None
    make_raw = None
    for m in sorted(MAKES, key=len, reverse=True):
        if re.search(r"\b" + re.escape(m) + r"\b", low):
            make = m
            # recover original casing span
            idx = low.find(m)
            make_raw = t[idx: idx + len(m)] if idx >= 0 else m
            break
    if not make:
        # first Capitalized token often is the make
        m = re.search(r"\b([A-Z][A-Za-z0-9.&-]{1,24})\b", t)
        if m and m.group(1).lower() not in {"cnc", "table", "used", "machine", "press", "laser", "tour", "scie"}:
            make = m.group(1).lower()
            make_raw = m.group(1)
    model = None
    if make:
        # tokens after the make that look like a model (letters+digits, or known pattern)
        pat = re.compile(re.escape(make) + r"\s+([A-Z0-9][A-Z0-9./-]{1,24}(?:\s+[A-Z0-9][A-Z0-9./-]{1,16}){0,2})", re.I)
        mm = pat.search(fold(t))
        if mm:
            model = norm_ws(mm.group(1))
            # strip trailing year
            model = re.sub(r"\s+(?:19|20)\d{2}$", "", model).strip()
    # common compact patterns
    if not model:
        mm = re.search(r"\b(VF-?\d\S*|ST-?\d\S*|EC-?\d+|PL\d+|HPR\d+\w*|XPR\s?\d+|Powermax\s?\d+\w*|APHS\s?\S+|BySpeed\S*|FO\s?\d+\S*|V\s?200|HG\s?\d+)\b", t, re.I)
        if mm:
            model = mm.group(1)
    return (make_raw or make), model


def size_class(title: str, category: str, tonnage: float | None = None) -> str | None:
    """A coarse class so a hobby table is not compared to a 10x26 production table."""
    t = fold(title or "").lower()
    if tonnage and category in {"press_brake", "punch", "shear", "other"}:
        if tonnage <= 80:
            return "small"
        if tonnage <= 200:
            return "medium"
        return "large"
    # table size in feet: "5 x 5", "10 × 26", "5x10"
    m = re.search(r"(\d{1,2})\s*[x×]\s*(\d{1,2})\s*(?:pi|ft|pieds|')?", t)
    if m and category in {"plasma_table", "laser", "waterjet", "router"}:
        a, b = int(m.group(1)), int(m.group(2))
        area = a * b
        if area <= 40:
            return "small"
        if area <= 90:
            return "medium"
        return "large"
    m = re.search(r"(\d{2,4})\s*(?:t|tonnes?|ton)\b", t)
    if m and category in {"press_brake", "punch", "other"}:
        ton = int(m.group(1))
        if ton <= 80:
            return "small"
        if ton <= 200:
            return "medium"
        return "large"
    if category == "mill":
        if re.search(r"\bvf-?[1-3]\b|\btm-\d\b", t):
            return "small"
        if re.search(r"\bvf-?[4-6]\b", t):
            return "medium"
        if re.search(r"\bvf-?[7-9]\b|boring\s+mill", t):
            return "large"
    return None


def looks_sold(text: str) -> bool:
    return bool(re.search(r"\b(vendu|sold!?|sold\s+out|n['’]est plus disponible)\b", text or "", re.I))


def looks_new_machine(text: str) -> bool:
    """True when the listing is clearly a new (not used) machine. Still shown, tagged."""
    return bool(re.search(r"\b(neuf|unused|new in crate|brand new|machineries neuves|new in stock)\b|^new\s+[A-Z]", text or "", re.I))
