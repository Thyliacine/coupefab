"""Distance from Berthierville, QC (CoupeFab home) and a small city gazetteer."""
from __future__ import annotations

import math
import re
import unicodedata

BERTHIERVILLE = (46.0828, -73.1836)

CITIES: dict[str, tuple[float, float, str]] = {
    "berthierville": (46.0828, -73.1836, "QC"),
    "joliette": (46.0230, -73.4370, "QC"),
    "sorel-tracy": (46.0428, -73.1124, "QC"),
    "sorel": (46.0428, -73.1124, "QC"),
    "louiseville": (46.2550, -72.9410, "QC"),
    "trois-rivieres": (46.3432, -72.5477, "QC"),
    "trois-rivières": (46.3432, -72.5477, "QC"),
    "shawinigan": (46.5500, -72.7500, "QC"),
    "montreal": (45.5019, -73.5674, "QC"),
    "montréal": (45.5019, -73.5674, "QC"),
    "montreal-nord": (45.6000, -73.6333, "QC"),
    "montréal-nord": (45.6000, -73.6333, "QC"),
    "laval": (45.6066, -73.7123, "QC"),
    "longueuil": (45.5316, -73.5180, "QC"),
    "brossard": (45.4512, -73.4500, "QC"),
    "boucherville": (45.5910, -73.4360, "QC"),
    "repentigny": (45.7420, -73.4500, "QC"),
    "terrebonne": (45.7000, -73.6333, "QC"),
    "mascouche": (45.7500, -73.6000, "QC"),
    "saint-jerome": (45.7800, -74.0000, "QC"),
    "saint-jérôme": (45.7800, -74.0000, "QC"),
    "saint-jean-sur-richelieu": (45.3071, -73.2626, "QC"),
    "saint-hyacinthe": (45.6300, -72.9500, "QC"),
    "granby": (45.4000, -72.7300, "QC"),
    "farnham": (45.2833, -72.9833, "QC"),
    "bromont": (45.3167, -72.8500, "QC"),
    "sherbrooke": (45.4042, -71.8929, "QC"),
    "magog": (45.2667, -72.1500, "QC"),
    "drummondville": (45.8833, -72.4833, "QC"),
    "victoriaville": (46.0500, -71.9667, "QC"),
    "thetford mines": (46.0667, -71.3000, "QC"),
    "quebec": (46.8139, -71.2080, "QC"),
    "québec": (46.8139, -71.2080, "QC"),
    "quebec city": (46.8139, -71.2080, "QC"),
    "levis": (46.8030, -71.1770, "QC"),
    "lévis": (46.8030, -71.1770, "QC"),
    "saint-georges": (46.1167, -70.6667, "QC"),
    "riviere-du-loup": (47.8350, -69.5350, "QC"),
    "rimouski": (48.4500, -68.5300, "QC"),
    "saguenay": (48.4167, -71.0667, "QC"),
    "chicoutimi": (48.4167, -71.0667, "QC"),
    "alma": (48.5500, -71.6500, "QC"),
    "baie-comeau": (49.2167, -68.1500, "QC"),
    "sept-iles": (50.2167, -66.3833, "QC"),
    "rouyn-noranda": (48.2333, -79.0167, "QC"),
    "val-d'or": (48.1000, -77.7833, "QC"),
    "val-d’or": (48.1000, -77.7833, "QC"),
    "gatineau": (45.4765, -75.7013, "QC"),
    "hull": (45.4280, -75.7200, "QC"),
    "mont-saint-hilaire": (45.5667, -73.2000, "QC"),
    "beloeil": (45.5667, -73.2000, "QC"),
    "chambly": (45.4500, -73.2833, "QC"),
    "valleyfield": (45.2500, -74.1333, "QC"),
    "salaberry-de-valleyfield": (45.2500, -74.1333, "QC"),
    "lachute": (45.6500, -74.3333, "QC"),
    "saint-eustache": (45.5667, -73.9000, "QC"),
    "blainville": (45.6667, -73.8833, "QC"),
    "mirabel": (45.6500, -74.0833, "QC"),
    "lachine": (45.4411, -73.6758, "QC"),
    "anjou": (45.6167, -73.5500, "QC"),
    "saint-leonard": (45.5833, -73.5833, "QC"),
    "ottawa": (45.4215, -75.6972, "ON"),
    "cornwall": (45.0270, -74.7300, "ON"),
    "kingston": (44.2312, -76.4860, "ON"),
    "belleville": (44.1628, -77.3836, "ON"),
    "peterborough": (44.3000, -78.3167, "ON"),
    "oshawa": (43.8971, -78.8658, "ON"),
    "toronto": (43.6532, -79.3832, "ON"),
    "mississauga": (43.5890, -79.6441, "ON"),
    "brampton": (43.7315, -79.7624, "ON"),
    "vaughan": (43.8361, -79.4983, "ON"),
    "markham": (43.8561, -79.3370, "ON"),
    "richmond hill": (43.8828, -79.4403, "ON"),
    "oakville": (43.4675, -79.6877, "ON"),
    "burlington": (43.3255, -79.7990, "ON"),
    "hamilton": (43.2557, -79.8711, "ON"),
    "st. catharines": (43.1594, -79.2469, "ON"),
    "niagara falls": (43.0896, -79.0849, "ON"),
    "kitchener": (43.4516, -80.4925, "ON"),
    "waterloo": (43.4643, -80.5204, "ON"),
    "cambridge": (43.3616, -80.3144, "ON"),
    "guelph": (43.5448, -80.2482, "ON"),
    "london": (42.9849, -81.2453, "ON"),
    "windsor": (42.3149, -83.0364, "ON"),
    "sarnia": (42.9746, -82.4066, "ON"),
    "sudbury": (46.4917, -80.9930, "ON"),
    "north bay": (46.3091, -79.4608, "ON"),
    "thunder bay": (48.3809, -89.2477, "ON"),
    "barrie": (44.3894, -79.6903, "ON"),
    "concord": (43.8210, -79.5380, "ON"),
    "woodbridge": (43.7840, -79.5920, "ON"),
    "scarborough": (43.7764, -79.2318, "ON"),
    "etobicoke": (43.6205, -79.5132, "ON"),
    "vancouver": (49.2827, -123.1207, "BC"),
    "surrey": (49.1913, -122.8490, "BC"),
    "burnaby": (49.2488, -122.9805, "BC"),
    "victoria": (48.4284, -123.3656, "BC"),
    "kelowna": (49.8880, -119.4960, "BC"),
    "langley": (49.1044, -122.6604, "BC"),
    "calgary": (51.0447, -114.0719, "AB"),
    "edmonton": (53.5461, -113.4938, "AB"),
    "red deer": (52.2681, -113.8112, "AB"),
    "lethbridge": (49.6935, -112.8418, "AB"),
    "saskatoon": (52.1332, -106.6700, "SK"),
    "regina": (50.4452, -104.6189, "SK"),
    "winnipeg": (49.8954, -97.1385, "MB"),
    "halifax": (44.6488, -63.5752, "NS"),
    "dartmouth": (44.6650, -63.5670, "NS"),
    "moncton": (46.0878, -64.7782, "NB"),
    "saint john": (45.2731, -66.0633, "NB"),
    "fredericton": (45.9636, -66.6431, "NB"),
    "charlottetown": (46.2382, -63.1311, "PE"),
    "st. john's": (47.5615, -52.7126, "NL"),
    "whitehorse": (60.7212, -135.0568, "YT"),
    "yellowknife": (62.4540, -114.3718, "NT"),
}

PROVINCE_CENTROID = {
    "QC": (46.8, -71.2), "ON": (44.5, -79.0), "BC": (49.3, -123.1), "AB": (53.5, -113.5),
    "SK": (52.1, -106.7), "MB": (49.9, -97.1), "NS": (44.6, -63.6), "NB": (45.9, -66.6),
    "PE": (46.2, -63.1), "NL": (47.6, -52.7), "YT": (60.7, -135.1), "NT": (62.5, -114.4),
    "NU": (63.7, -68.5),
}

US_CITIES = {
    "tampa": (27.9506, -82.4572, "FL"),
    "clearwater": (27.9659, -82.8001, "FL"),
    "miami": (25.7617, -80.1918, "FL"),
    "atlanta": (33.7490, -84.3880, "GA"),
    "houston": (29.7604, -95.3698, "TX"),
    "dallas": (32.7767, -96.7970, "TX"),
    "chicago": (41.8781, -87.6298, "IL"),
    "detroit": (42.3314, -83.0458, "MI"),
    "cleveland": (41.4993, -81.6944, "OH"),
    "los angeles": (34.0522, -118.2437, "CA"),
    "oxnard": (34.1975, -119.1771, "CA"),
    "new york": (40.7128, -74.0060, "NY"),
    "buffalo": (42.8864, -78.8784, "NY"),
    "boston": (42.3601, -71.0589, "MA"),
    "seattle": (47.6062, -122.3321, "WA"),
    "denver": (39.7392, -104.9903, "CO"),
}


def _fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace("\u2019", "'").replace("saint ", "st ").replace("st-", "st ").replace("ste-", "ste ")
    return re.sub(r"\s+", " ", s).strip()


def haversine_km(a: tuple[float, float], b: tuple[float, float] = BERTHIERVILLE) -> float:
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(h))


def geocode(city: str | None, province: str | None) -> tuple[float, float] | None:
    if city:
        key = _fold(city)
        if key in CITIES:
            return CITIES[key][0], CITIES[key][1]
        if key in US_CITIES:
            return US_CITIES[key][0], US_CITIES[key][1]
        for name, (lat, lon, _pr) in {**CITIES, **US_CITIES}.items():
            if name in key or key in name:
                return lat, lon
    pr = (province or "").upper()
    if pr in PROVINCE_CENTROID:
        return PROVINCE_CENTROID[pr]
    return None


def distance_from_berthierville(city: str | None, province: str | None) -> float | None:
    pt = geocode(city, province)
    if not pt:
        return None
    return round(haversine_km(pt), 1)


def parse_province(text: str) -> str | None:
    tl = " " + _fold(text or "") + " "
    mapping = [
        (r"\b(qc|quebec|p\.?q\.?)\b", "QC"),
        (r"\b(on|ontario)\b", "ON"),
        (r"\b(bc|british columbia|colombie[- ]britannique)\b", "BC"),
        (r"\b(ab|alberta)\b", "AB"),
        (r"\b(sk|saskatchewan)\b", "SK"),
        (r"\b(mb|manitoba)\b", "MB"),
        (r"\b(ns|nouvelle[- ]ecosse|nova scotia)\b", "NS"),
        (r"\b(nb|nouveau[- ]brunswick|new brunswick)\b", "NB"),
        (r"\b(pe|pei|prince edward)\b", "PE"),
        (r"\b(nl|terre[- ]neuve|newfoundland)\b", "NL"),
        (r"\b(yt|yukon)\b", "YT"),
        (r"\b(nt|nwt|northwest territor)\b", "NT"),
        (r"\b(nu|nunavut)\b", "NU"),
        (r"\b(usa|u\.s\.a\.|united states|\bfl\b|\bca\b california|texas|ohio|michigan|new york|illinois|florida)\b", "US"),
    ]
    for pat, code in mapping:
        if re.search(pat, tl, re.I):
            return code
    return None
