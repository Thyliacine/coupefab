"""Turn a raw storefront item into a CoupeFab tooling row (category, spec, pack size, CAD price)."""
from __future__ import annotations

import hashlib
import re
import unicodedata

CATEGORIES = [
    # id, group, fr, en
    ("plasma", "plasma", "Consommables plasma (électrode, buse, bouclier)", "Plasma consumables (electrode, nozzle, shield)"),
    ("laser", "laser", "Consommables laser (buse, hublot, lentille)", "Laser consumables (nozzle, window, lens)"),
    ("router-bit", "routeur", "Fraises pour routeur CNC", "CNC router bits"),
    ("end-mill", "usinage", "Fraises en bout", "End mills"),
    ("drill", "usinage", "Forets et mèches", "Drills"),
    ("tap", "usinage", "Tarauds et filières", "Taps and dies"),
    ("insert", "usinage", "Plaquettes carbure (outils indexables)", "Carbide inserts"),
    ("insert-holder", "usinage", "Porte-plaquettes, barres d’alésage, fraises à surfacer", "Insert holders, boring bars, face mills"),
    ("collet", "usinage", "Pinces de serrage et porte-outils (ER, CAT, R8)", "Collets and toolholders (ER, CAT, R8)"),
    ("saw", "coupe", "Lames de scie (ruban, circulaire, cloche)", "Saw blades (band, circular, hole)"),
    ("abrasive", "coupe", "Abrasifs (disques à lamelles, à tronçonner, meules)", "Abrasives (flap discs, cut-off wheels, grinding)"),
    ("brake", "plieuse", "Outillage de plieuse (poinçons, matrices)", "Press-brake tooling (punches, dies)"),
    ("measure", "mesure", "Instruments de mesure", "Measuring tools"),
]
GROUPS = [
    ("plasma", "Plasma", "Plasma"), ("laser", "Laser", "Laser"), ("routeur", "Routeur CNC", "CNC router"),
    ("usinage", "Usinage (fraiseuse, tour, perçage)", "Machining (mill, lathe, drilling)"),
    ("coupe", "Sciage et meulage", "Sawing and grinding"), ("plieuse", "Presse plieuse", "Press brake"),
    ("mesure", "Mesure", "Measuring"),
]
CAT_GROUP = {c[0]: c[1] for c in CATEGORIES}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.lower().replace("’", "'").replace("″", '"').replace("”", '"')


def rx(p):
    return re.compile(p, re.I)


PLASMA_CTX = rx(r"plasma|hypertherm|powermax|duramax|cutmaster|thermal dynamics|\bsl60\b|\bsl100\b|\bxpr\b|\bhpr\d|maxpro|razorweld|\bpt-?\d{2}|\bt45\b|\bt60\b|\bt80\b|\bt100\b|\bfinecut\b")
PLASMA_PART = rx(r"electrode|nozzle|\bbuse|\btip\b|tips\b|shield|bouclier|swirl|turbulence|retaining cap|\bcap\b|cartridge|cartouche|consumable|consommable|deflector|deflecteur|diffuser|gouging")
LASER_CTX = rx(r"laser|raytools|precitec|wsx|bodor|\bbm1\d\d|bt240|ipg")
LASER_PART = rx(r"nozzle|\bbuse|window|hublot|lens|lentille|ceramic|ceramique|protective|protection lens|collimat|focus(ing)? lens|lentille de focalisation|cover slide|sensor ring")
LASER_NOT = rx(r"auto ?focus head|cutting head|tete de coupe|level|niveau|pointer|thermometer|tachometer|distance meter|measure|guide|sight|engraver machine|cutting machine|engraving machine|module|goggles|glasses|lunettes|safety")
BRAKE = rx(r"joggle|press ?brake|presse plieuse|plieuse|brake punch|brake die|v-?die|gooseneck punch|promecam|amada style|amada/|wila|trumpf style|euro style punch|segmented punch|\bpunch\b.*\b\d{2,3} ?mm\b.*(t/m|ton)|matrice")
ROUTER = rx(r"router|routeur|upcut|up-cut|up cut|downcut|down-cut|down cut|compression|v-?bit|v-?groove|spoilboard|surfacing|o-?flute|single flute|engraving bit|onsrud|whiteside|\bcnc bits?\b|mortise")
BIT_WORD = rx(r"\bbits?\b|spiral|fraise|meche|cutter|flute|\bshank|queue")
ENDMILL = rx(r"end ?-?mills?|endmills?|fraise en bout|fraises? (carbure|a bout|a rayon)|ball ?nose|bull ?nose|corner radius|drill ?mill|chamfer mill|roughing|\b\d flutes?\b|\b\d fl\b|flutes? regulier|square end")
TAP = rx(r"\btaps?\b|taraud|tap (and|&) die|\bdies? (hex|round|thread)|thread(ing)? die|filiere|threadmill|thread mill|tap set|\bunc\b.*\btap|\bnpt\b.*tap|tap handle|tourne-a-gauche")
DRILL = rx(r"\bdrills?\b|drill bits?|\bforets?\b|\bmeches?\b|annular cutter|step drill|spot drill|center drill|centre drill|jobber|screw machine length|taper length|silver ?& ?deming|reduced shank|cobalt drill|countersink|fraise a chambrer|counterbore")
INSERT = rx(r"\binserts?\b|plaquettes?|\b(cnmg|tnmg|apmt|apkt|dcmt|dcgt|ccmt|ccgt|wnmg|vbmt|vcgt|vcmt|snmg|tcmt|tcgt|dnmg|vnmg|sekt|semt|rpmt|rdmt|mgmn|tpgt|tpmr|lnmu|r390|wcmx|spgt|spmg|xomx)\s?-?\d")
INSERT_HOLDER = rx(r"boring bar|barre d'alesage|turning (tool ?)?holder|tool holder.*insert|porte-plaquette|indexable|face mill|fraise a surfacer|shell mill|parting (tool|blade)|grooving holder|threading holder|quick change tool post|tool post|\bmclnr|\bsclcr|\bsdjcr|\bmwlnr")
COLLET = rx(r"\bcollets?\b|pinces? de serrage|\ber ?(8|11|16|20|25|32|40|50)\b|\b5c\b|\br8\b|\bcat ?40\b|\bcat ?50\b|\bbt ?30\b|\bbt ?40\b|\bhsk|\bnt30|\bnt40|\biso ?30\b|tool ?holder|porte-outil|collet chuck|drill chuck|mandrin|pull stud|retention knob|end mill holder|shrink fit|side lock|weldon|morse taper|\bmt[1-5]\b|arbor")
SAW = rx(r"band ?saw blades?|bandsaw|lames? de scie|lame a ruban|saw blades?|hacksaw blade|hole ?saws?|scies?-cloches?|cold saw blade|reciprocating (saw )?blade|jig ?saw blade|sawzall|metal cutting blade|tct blade|cermet blade|portaband|portable band")
SAW_ITEM = rx(r"blade|lame|hole ?saw|scie-cloche|scies-cloches|\btpi\b")
ABRASIVE = rx(r"flap ?discs?|disques? a lamelles|cut-?off (wheel|disc)s?|cutoff wheels?|cutting (disc|wheel)s?|disques? a tronconner|disque a couper|grinding (wheel|disc)|meules?|fib(er|re) discs?|disques? de fibre|sanding (disc|belt)|bandes? de poncage|abrasi(f|fs|ve|ves)\b|wire (wheel|brush|cup)|buffing|polishing (wheel|compound)|brosses? metallique|surface conditioning|non-?woven|quick change disc|roloc|bench grinder wheel|\bgrit\b|\bgrain \d{2,3}|zirconia (flap|disc|belt)|ceramic (flap|disc|belt)|depressed center|scotch-brite|strip disc|polishing wheel")
MEASURE = rx(r"calipers?|pied a coulisse|micromet|dial indicator|test indicator|indicateur|comparateur|height ga(u)?ge|bore ga(u)?ge|pin ga(u)?ge|gage blocks?|gauge blocks?|feeler ga|edge finder|machinist'?s? square|combination square|protractor|rapporteur|thread (pitch )?ga(u)?ge|radius ga(u)?ge|depth ga(u)?ge|machinist level|precision level|surface plate|v-?blocks?|1-2-3 block|parallels set|telescoping ga(u)?ge|small hole ga|sine bar|dial depth|vernier|\bdro\b|digital readout|linear scale")
EXCLUDE = rx(r"balance amount|gant|glove|cordon|rallonge|extension cord|film etirable|templistik|crayon|\bvis\b|screws?\b|autotaraud|gift ?card|carte[- ]cadeau|t-shirt|hoodie|\bhat\b|casquette|sticker|shipping|livraison|warranty|garantie|sample|echantillon|\brental\b|location|service|repair|reparation|financing|deposit|depot|bundle deal|\bcatalog")
MACHINE = rx(r"\b(woodturner|tool grinder|sharpening system|sharpener|grinder|cnc press brake|press brake machine|lathe|tour a metaux|milling machine|mill/drill|drill press|band ?saw machine|cnc router machine|cnc plasma table|plasma cutter|plasma cutting system|welder|soudeuse|compressor|dust collector|table saw|jointer|planer|drill press|metal cutting band saw|horizontal band ?saw|vertical band ?saw|bench grinder|angle grinder|meuleuse|machine)\b")

INSERT_NOT = rx(r"insert bits?|s[/\\\\]d bit|screwdriver|tournevis|thread insert|helicoil|planer|jointer|spiral cutterhead|foam|table insert|zero.?clearance|dado|throat|packout|toughsystem|nylon|polyurethane|urethane|socket insert|sock\b|hex socket|phillips|frearson|torx|square recess|knife")
COLLET_NOT = rx(r"grinder|rectifieuse|meuleuse|rotary saw|impact|torque wrench|brush|\btig\b|buffing|allsaw|arbortech|trim router|palm router|spindle motor|\bvfd\b|separateur")

BRANDS = ["Hypertherm", "Thermal Dynamics", "ESAB", "Lincoln", "Miller", "Amana", "Onsrud", "Whiteside", "CMT",
          "Freud", "Sandvik", "Kennametal", "Iscar", "Mitsubishi", "Kyocera", "Seco", "Walter", "Dormer", "Guhring",
          "OSG", "Harvey", "Kodiak", "YG-1", "Morse", "Starrett", "Mitutoyo", "Fowler", "Insize", "Accusize",
          "Norton", "3M", "Pferd", "Rhodius", "Lenox", "Bahco", "Wikus", "Milwaukee", "DeWalt", "Makita", "Bosch",
          "Raytools", "Precitec", "WSX", "Bodor", "Wila", "Amada", "Trumpf", "Lyndex", "Techniks", "Bison",
          "Jacobs", "Albrecht", "Rohm", "Greenfield", "Irwin", "Hanson", "Viking", "Chicago-Latrobe", "Cle-Line",
          "Precision Twist", "Triumph", "Union Butterfield", "Nachi", "Emuge", "Yamawa", "Garr", "SGS", "Dimar",
          "Belin", "Spetool", "Sharpex", "Busy Bee", "Craftex", "King Canada", "Tuff Tooth", "Simonds", "Timberwolf"]
BRAND_RX = [(b, rx(r"\b" + re.escape(b) + r"\b")) for b in BRANDS]

PACK = [
    rx(r"(?:pack of|paquet de|pqt de|boite de|box of|bo[iî]te de|pkg of|pk of|lot de|set of|jeu de|caisse de|case of|qty\.?|quantity:?)\s*(\d{1,4})\b"),
    rx(r"\b(\d{1,4})\s*(?:/|-)?\s*(?:pk|pack|pcs?|pieces|pieces|ct|count|per box|/box|/bx|/pkg|pkg|units?|unites)\b"),
    rx(r"\b(\d{1,4})\s*(?:pc|pce|pcs)\.?\s*(?:set|jeu|kit)\b"),
    rx(r"\((\d{1,4})\)\s*$"),
]

SPEC = [
    rx(r"(?:o|ø|dia\.?|diam(?:etre|eter)?\.?)\s*\d+(?:[./]\d+)?\s*(?:mm|\"|in|po)?"),
    rx(r"\b\d+(?:-\d+)?/\d+\s*(?:\"|in\b|po\b|inch)"),
    rx(r"\b\d+(?:\.\d+)?\s*mm\b"),
    rx(r"\b\d+\s*(?:flutes?|fl|dents?|teeth|t)\b"),
    rx(r"\b(?:grit|grain)\s*\d{2,4}|\b\d{2,4}\s*(?:grit|grain)\b"),
    rx(r"\b\d+(?:/\d+)?\s*tpi\b"),
    rx(r"\b\d{2,3}\s*a(?:mp)?s?\b"),
    rx(r"\b(?:er|cat|bt)\s?\d{2}\b"),
    rx(r"\b(?:m\d+(?:\.\d+)?\s*x\s*\d+(?:\.\d+)?|\d+/\d+-\d+|#\d+-\d+)\b"),
    rx(r"\b\d{2,3}\s*°"),
]


def clean_name(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def classify(text: str, src_id: str) -> str | None:
    t = norm(text)
    if EXCLUDE.search(t):
        return None
    if src_id == "fabtooling" or BRAKE.search(t):
        if not rx(r"hand punch|punch set|center punch|pin punch|transfer punch|hole punch|leather").search(t):
            return "brake"
    if LASER_CTX.search(t) and LASER_PART.search(t) and not LASER_NOT.search(t):
        return "laser"
    if PLASMA_CTX.search(t) and PLASMA_PART.search(t) and not rx(r"mig|tig torch|welding tip|contact tip|tweco|collet body").search(t):
        return "plasma"
    if MEASURE.search(t) and not rx(r"bit|blade|disc|wheel|insert").search(t):
        return "measure"
    if ABRASIVE.search(t) and not rx(r"router|end ?mill|drill bit|panel tool|carbide burr|\btaps?\b|insert").search(t):
        return "abrasive"
    if SAW.search(t) and SAW_ITEM.search(t):
        return "saw"
    if INSERT.search(t) and not INSERT_NOT.search(t):
        if (INSERT_HOLDER.search(t) or rx(r"holders?|boring bar|end ?mill|face mill|shell mill|indexable").search(t)) and not rx(r"^\s*\w{4}\s?\d").search(t) and not rx(r"^[^|]*\binserts?\b[^|]*(pack|pcs|/pack)").search(t):
            return "insert-holder"
        return "insert"
    if INSERT_HOLDER.search(t):
        return "insert-holder"
    if TAP.search(t) and not rx(r"tap water|robinet|faucet|tapping screw").search(t):
        if rx(r"chuck|holder|collet|adapter|mandrin").search(t):
            return "collet"
        return "tap"
    if ROUTER.search(t) and BIT_WORD.search(t):
        return "router-bit"
    if rx(r"countersink|fraise a chambrer|counterbore|centre drill|center drill").search(t) and not rx(r"router|routeur").search(t):
        return "drill"
    if ENDMILL.search(t) and not rx(r"socket|burr|fraise rotative|chisel|gouge|ciseau").search(t):
        if rx(r"holders?|adapter|arbor|sleeve|porte").search(t):
            return "collet"
        return "end-mill"
    if COLLET.search(t) and not COLLET_NOT.search(t):
        return "collet"
    if DRILL.search(t) and not rx(r"drill press|perceuse|cordless|impact driver|drill driver|hammer drill|drill guide|tile|stone|glass|masonry|maconnerie|\bsds\b|concrete|beton|mortis|auger|forstner|brad ?point|dowel|wood").search(t):
        return "drill"
    return None


def pack_qty(text: str):
    t = norm(text)
    for p in PACK:
        m = p.search(t)
        if m:
            n = int(m.group(1))
            if 1 < n <= 1000:
                return n
    return None


def spec_of(raw) -> str:
    if raw.get("variant"):
        return raw["variant"][:120]
    t = raw["title"]
    found = []
    for p in SPEC:
        for m in p.finditer(t):
            s = m.group(0).strip()
            if s and s not in found:
                found.append(s)
    return " · ".join(found[:5])


def brand_of(raw, src) -> str:
    v = (raw.get("vendor") or "").strip()
    bad = {"", "default", "vendor", "unknown", src["name"].lower(), src["host"].split(".")[0].lower(), "my store"}
    text = raw["title"] + " " + raw.get("variant", "")
    for b, r in BRAND_RX:
        if r.search(text):
            return b
    if v.lower() not in bad and len(v) < 40:
        return v
    return ""


def to_row(raw, src, fx, date):
    price = raw.get("price") or 0
    if price <= 0 or price > 25000:
        return None
    text = " ".join([raw["title"], raw.get("variant", ""), raw.get("ptype", "")])
    t = norm(text)
    if MACHINE.search(norm(raw["title"])) and price > 400 and not rx(r"blade|lame|bit|insert|collet|nozzle|electrode|disc|disque|consumable").search(t):
        return None
    cat = classify(text, src["id"])
    if not cat:
        # tags are noisy; only use them as a last resort for stores that sell tooling only
        cat = classify(raw["title"] + " " + " ".join(raw.get("tags") or []), src["id"]) if src["id"] in ("cncrouterstore", "sharpex", "fabtooling") else None
    if not cat:
        return None
    cur = src["currency"]
    rate = fx["rate"] if cur == "USD" else None
    cad = round(price * rate, 2) if rate else round(price, 2)
    pq = pack_qty(raw["title"] + " " + raw.get("variant", ""))
    unit = round(cad / pq, 2) if pq else cad
    name = raw["title"][:160]
    return {
        "cat": cat, "name": name, "spec": spec_of(raw), "sku": raw.get("sku", "")[:40],
        "brand": brand_of(raw, src), "pack": pq, "price_cad": cad, "unit_cad": unit,
        "price_orig": round(price, 2), "currency": cur, "source": src["id"], "url": raw.get("url"),
        "fetched": date, "in_stock": bool(raw.get("available", True)),
    }


def dedupe(rows):
    seen, out = set(), []
    for r in rows:
        k = (r["source"], r["name"], r["spec"], r["price_cad"])
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


CAP_PER_CAT = 350


def cap(rows):
    """Keep at most CAP_PER_CAT rows per (source, category): in-stock first, then cheapest per unit."""
    by = {}
    for r in rows:
        by.setdefault(r["cat"], []).append(r)
    out = []
    for cat, rs in by.items():
        rs.sort(key=lambda r: (not r["in_stock"], r["unit_cad"]))
        out += rs[:CAP_PER_CAT]
    return out
