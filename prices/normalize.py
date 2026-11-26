"""Normalisation helpers: grade/family/form detection, thickness parsing, weights.

Nothing here invents a price. These helpers only interpret text that a supplier
published (thickness, grade, size) and compute derived units ($/lb, $/sq ft)
from the published price and standard densities.
"""
import re
from fractions import Fraction

# --- Michaël's workplace catalogue (tracker material list) -------------------
CATALOGUE = {
    "inox": ["303", "304", "304L", "316", "316L", "410", "416", "17-4PH",
             "17-4PH H1150", "17-4PH H900", "Inconel", "Inconel 600"],
    "acier": ["1018", "1018 CR", "1018 HR", "1020", "1020 CR", "1020 HR", "1026",
              "1045", "1045 CR", "1045 HR", "4130", "4140", "4140 HT", "4340",
              "4340 HT", "12L14", "A36", "44W", "50W", "A106", "A500 gr.B",
              "A500 gr.C", "A513/A519", "A53", "O1"],
    "aluminium": ["3003", "5052", "6061", "6063"],
    "cuivre": ["C110"],
    "laiton": ["C360"],
    "bronze": ["C932"],
    "bronze_alu": ["C954"],
}
FAMILY_LABELS = {
    "inox": ("Inox", "Stainless"),
    "acier": ("Acier", "Steel"),
    "aluminium": ("Aluminium", "Aluminum"),
    "cuivre": ("Cuivre", "Copper"),
    "laiton": ("Laiton", "Brass"),
    "bronze": ("Bronze", "Bronze"),
    "bronze_alu": ("Bronze d’aluminium", "Aluminum bronze"),
}
# lb per cubic inch
DENSITY = {"acier": 0.2836, "inox": 0.289, "aluminium": 0.0975, "cuivre": 0.323,
           "laiton": 0.307, "bronze": 0.318, "bronze_alu": 0.269}

FORM_LABELS = {
    "tole": ("Tôle (< 3/16 po)", "Sheet (< 3/16 in)"),
    "plaque": ("Plaque (≥ 3/16 po)", "Plate (≥ 3/16 in)"),
    "barre_ronde": ("Barre ronde", "Round bar"),
    "barre_plate": ("Barre plate", "Flat bar"),
    "barre_carree": ("Barre carrée", "Square bar"),
    "barre_hex": ("Barre hexagonale", "Hex bar"),
    "tube_rond": ("Tube rond", "Round tube"),
    "tube_carre": ("Tube carré", "Square tube"),
    "tube_rect": ("Tube rectangulaire", "Rectangular tube"),
    "tuyau": ("Tuyau (pipe)", "Pipe"),
}

# Gauge tables (inches). Steel = Manufacturers' Standard Gauge.
GAUGE_STEEL = {3: .2391, 4: .2242, 5: .2092, 6: .1943, 7: .1793, 8: .1644, 9: .1495, 10: .1345,
               11: .1196, 12: .1046, 13: .0897, 14: .0747, 15: .0673, 16: .0598, 17: .0538,
               18: .0478, 19: .0418, 20: .0359, 21: .0329, 22: .0299, 23: .0269, 24: .0239,
               25: .0209, 26: .0179, 28: .0149, 30: .0120}
GAUGE_GALV = {8: .1681, 9: .1532, 10: .1382, 11: .1233, 12: .1084, 13: .0934, 14: .0785,
              15: .0710, 16: .0635, 17: .0575, 18: .0516, 19: .0456, 20: .0396, 21: .0366,
              22: .0336, 23: .0306, 24: .0276, 25: .0247, 26: .0217, 28: .0187, 30: .0157}
GAUGE_SS = {7: .1875, 8: .1719, 9: .1563, 10: .1406, 11: .1250, 12: .1094, 13: .0938,
            14: .0781, 15: .0703, 16: .0625, 17: .0563, 18: .0500, 19: .0438, 20: .0375,
            21: .0344, 22: .0313, 23: .0281, 24: .0250, 25: .0219, 26: .0188, 28: .0156}
GAUGE_AL = {6: .1620, 7: .1443, 8: .1285, 9: .1144, 10: .1019, 11: .0907, 12: .0808,
            13: .0720, 14: .0641, 15: .0571, 16: .0508, 17: .0453, 18: .0403, 19: .0359,
            20: .0320, 21: .0285, 22: .0253, 23: .0226, 24: .0201, 25: .0179, 26: .0159}

EXCLUDE = re.compile(
    r"perforat|expanded|mesh|grat|grecian|windsor|checker|diamond|tread|larm|uhmw|ptfe|"
    r"nylon|acrylic|polycarb|plastic|caoutchouc|rubber|usag|used|gift card|painted|prepaint|"
    r"pr[ée]peint|wire|grillage|offcut|chute|remnant|drop|thread|filet", re.I)


def detect_family(text: str):
    t = text.lower()
    if re.search(r"alum\w* bronze|bronze d.?alu|c954", t):
        return "bronze_alu"
    if re.search(r"stainless|inox|\bss\b|inconel|17-4|\b30[34]l?\b|\b316l?\b", t):
        return "inox"
    if re.search(r"alumin", t):
        return "aluminium"
    if re.search(r"copper|cuivre|\bc110\b", t):
        return "cuivre"
    if re.search(r"brass|laiton|\bc3[46]0\b|\bc260\b", t):
        return "laiton"
    if re.search(r"bronze|c932|sae ?660", t):
        return "bronze"
    if re.search(r"steel|acier|carbon|galv|\ba36\b|44w|hot rolled|cold rolled|\bhr\b|\bcr\b|1018|1020|1045|4140|4130|12l14|a500|a513|a53|drill rod|\bo1\b", t):
        return "acier"
    return None


def _hr_cr(t):
    if re.search(r"cold[ -]?(rolled|drawn|finish)|\bcr\b|\bcf\b|\bcd\b|laminé à froid", t, re.I):
        return " CR"
    if re.search(r"hot[ -]?rolled|\bhr\b|laminé à chaud", t, re.I):
        return " HR"
    return ""


def detect_grade(text: str, family: str):
    """Return (grade, in_catalogue). grade is None when the text does not name one."""
    t = text
    if family == "inox":
        for pat, g in [(r"17-?4\s*-?PH.*H\s*1150|H1150.*17-?4", "17-4PH H1150"),
                       (r"17-?4\s*-?PH.*H\s*900|H900.*17-?4", "17-4PH H900"),
                       (r"17-?4", "17-4PH"), (r"inconel\s*600", "Inconel 600"),
                       (r"inconel", "Inconel"), (r"304L", "304L"), (r"316L", "316L"),
                       (r"\b303\b", "303"), (r"\b304\b", "304"), (r"\b316\b", "316"),
                       (r"\b410\b", "410"), (r"\b416\b", "416"), (r"\b430\b", "430")]:
            if re.search(pat, t, re.I):
                return g, g in CATALOGUE["inox"]
        return None, False
    if family == "acier":
        for pat, g in [(r"12L14", "12L14"), (r"4140.*(HT|heat[- ]treat|pre-?hard|\bPH\b)", "4140 HT"),
                       (r"4140", "4140"), (r"4340.*(HT|heat[- ]treat|pre-?hard)", "4340 HT"),
                       (r"4340", "4340"), (r"4130", "4130"), (r"\b1045\b", "1045"),
                       (r"\b1026\b", "1026"), (r"\b1020\b", "1020"), (r"\b1018\b", "1018"),
                       (r"A500\D{0,12}(gr(ade)?\.?\s*C)\b", "A500 gr.C"), (r"A500", "A500 gr.B"),
                       (r"A51[39]", "A513/A519"), (r"A106", "A106"), (r"\bA53\b", "A53"),
                       (r"\bA36\b", "A36"), (r"44W", "44W"), (r"50W", "50W"),
                       (r"\bO-?1\b|drill rod|\b01 precision ground", "O1"),
                       (r"hard plate|\bAR\s?[45]00\b|\bT[14]00\b", "Plaque dure (AR/T400)"),
                       (r"\b1144\b", "1144"), (r"\b1215\b", "1215"),
                       (r"A653|galvani[sz]", "Galvanisé A653"), (r"galvanneal", "Galvannealed A653"),
                       (r"A1011", "HR A1011"), (r"A1008", "CR A1008")]:
            if re.search(pat, t, re.I):
                if g in ("1018", "1020", "1045"):
                    g = g + _hr_cr(t)
                if g == "A500 gr.B" and not re.search(r"gr(ade)?\.?\s*B", t, re.I):
                    g = "A500"  # grade letter not stated
                if g == "A500":
                    return g, True
                return g, g in CATALOGUE["acier"]
        hc = _hr_cr(t).strip()
        if hc:
            return f"{hc} (nuance non précisée)", False
        return None, False
    if family == "aluminium":
        for g in ["3003", "5052", "6061", "6063", "5005", "3105", "5086", "2024", "7075", "1100"]:
            if re.search(r"\b" + g + r"\b", t):
                return g, g in CATALOGUE["aluminium"]
        return None, False
    if family == "cuivre":
        return ("C110", True) if re.search(r"C?110\b", t) else (None, False)
    if family == "laiton":
        if re.search(r"C?360\b", t):
            return "C360", True
        if re.search(r"C?260\b", t):
            return "C260", False
        return None, False
    if family == "bronze":
        if re.search(r"C?932|660", t):
            return "C932", True
        return None, False
    if family == "bronze_alu":
        return ("C954", True) if re.search(r"954", t) else (None, False)
    return None, False


def detect_form(text: str, hint: str = ""):
    t = (hint + " " + text).lower()
    if re.search(r"\bpipe\b|tuyau|sch(edule)?\s*\d", t):
        return "tuyau"
    if re.search(r"square tube|tube carr|sq\.? tube|hss square", t):
        return "tube_carre"
    if re.search(r"rect\w* tube|tube rect|hss rect", t):
        return "tube_rect"
    if re.search(r"\btube|tubing|\bdom\b|hss round", t):
        return "tube_rond"
    if re.search(r"flat bar|barre plate|\bflat\b", t):
        return "barre_plate"
    if re.search(r"square bar|barre carr|\bsquare\b", t):
        return "barre_carree"
    if re.search(r"hex", t):
        return "barre_hex"
    if re.search(r"round bar|barre ronde|\bround\b|drill rod|rod\b|chrome", t):
        return "barre_ronde"
    if re.search(r"sheet|plate|plaque|t[ôo]le|feuille", t):
        return "feuille"  # resolved to tole/plaque by thickness
    return None


def _num(s: str) -> float:
    s = s.strip().replace(",", ".")
    m = re.fullmatch(r"(\d+)[- ](\d+)/(\d+)", s)
    if m:
        return int(m.group(1)) + int(m.group(2)) / int(m.group(3))
    if "/" in s:
        return float(Fraction(s))
    return float(s)


def gauge_table(family, grade):
    if family == "inox":
        return GAUGE_SS
    if family == "aluminium" or family in ("cuivre", "laiton"):
        return GAUGE_AL
    if grade and grade.lower().startswith("galv"):
        return GAUGE_GALV
    return GAUGE_STEEL


def parse_thickness(text: str, family: str, grade=None):
    """Return (thickness_in, gauge, how). Prefers an explicit decimal next to a gauge."""
    t = text.replace("″", '"').replace("”", '"').replace("&#8243;", '"')
    gauge = None
    m = re.search(r"(\d{1,2})\s*(?:ga\b|ga\.|g\b|gauge|jauges?|calibre)", t, re.I)
    if m:
        gauge = int(m.group(1))
    # explicit decimal like .075, 0.075", 0,075PO, (.060" thick)
    m = re.search(r"(?<![\d/])(0?[.,]\d{2,4})\s*(?:\"|po\b|in\b|”|thick|$|\s|\)|x)", t, re.I)
    if m:
        try:
            v = _num(m.group(1))
            if 0.005 < v < 1.0:
                return round(v, 4), gauge, "decimal"
        except Exception:
            pass
    if gauge is not None:
        tab = gauge_table(family, grade)
        if gauge in tab:
            return tab[gauge], gauge, "gauge"
    m = re.search(r"(?<![\d.])(\d+[- ]\d+/\d+|\d+/\d+|\d+(?:\.\d+)?)\s*(?:\"|inch|in\b|po\b|”)", t, re.I)
    if m:
        try:
            v = _num(m.group(1))
            if 0 < v <= 12:
                return round(v, 4), None, "fraction"
        except Exception:
            pass
    return None, gauge, None


def sheet_or_plate(thk_in):
    if thk_in is None:
        return "tole"
    return "plaque" if thk_in >= 0.1875 - 1e-4 else "tole"


def sheet_weight_lb(family, thk_in, w_in, l_in):
    if not (thk_in and w_in and l_in):
        return None
    return DENSITY[family] * thk_in * w_in * l_in


def fmt_frac(x):
    if x is None:
        return ""
    for den in (2, 4, 8, 16, 32):
        n = round(x * den)
        if abs(n / den - x) < 0.0006 and n:
            whole, rem = divmod(n, den)
            f = Fraction(rem, den)
            if whole and rem:
                return f"{whole}-{f.numerator}/{f.denominator}"
            if whole:
                return str(whole)
            return f"{f.numerator}/{f.denominator}"
    return ""
