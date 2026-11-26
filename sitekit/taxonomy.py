"""Guide hubs, mega-nav and labels (FR / EN)."""

HUBS = {
    # id: (fr_slug, en_slug, fr_title, en_title, fr_blurb, en_blurb)
    "software": ("logiciels", "software", "Logiciels CAO / FAO et commandes", "CAD/CAM software and controls",
                 "Mastercam, SolidWorks, Fusion, Inventor, BricsCAD, SheetCam, ProNest, LinuxCNC… Du modèle au G-code, logiciel par logiciel.",
                 "Mastercam, SolidWorks, Fusion, Inventor, BricsCAD, SheetCam, ProNest, LinuxCNC… From model to G-code, one program at a time."),
    "process": ("procedes", "processes", "Procédés de coupe et d’usinage", "Cutting and machining processes",
                "Plasma, laser fibre, jet d’eau, routeur, fraiseuse, tour, presse plieuse : comment ça marche, quoi surveiller.",
                "Plasma, fiber laser, waterjet, router, mill, lathe, press brake: how each works and what to watch."),
    "fundamentals": ("fondamentaux", "fundamentals", "Fondamentaux CNC", "CNC fundamentals",
                     "G-code, post-processeurs, décalages d’origine, avances et vitesses, kerf, entrées, imbrication, DXF, tolérances, pliage, nuances.",
                     "G-code, post processors, work offsets, feeds and speeds, kerf, lead-ins, nesting, DXF, tolerances, bending, grades."),
    "materials": ("materiaux", "materials", "Matériaux et nuances", "Materials and grades",
                  "Acier doux, inox, aluminium, cuivre, laiton, bronze, alliages de nickel : usinabilité, coupe, pliage, soudage et calibres, avec lien vers les prix publiés.",
                  "Mild steel, stainless, aluminum, copper, brass, bronze, nickel alloys: machinability, cutting, bending, welding and gauges, linked to published prices."),
    "troubleshooting": ("depannage", "troubleshooting", "Dépannage", "Troubleshooting",
                        "Scories plasma et laser, biseau, THC qui oscille, broutage, arrachement au routeur, erreurs de post : symptôme → cause → correctif.",
                        "Plasma and laser dross, bevel, THC hunting, chatter, router tear-out, post errors: symptom → cause → fix."),
    "shop": ("atelier", "shop", "Atelier : sécurité, soumissions, métrologie, formation", "Shop: safety, quoting, inspection, training",
             "EPI, fumées et CNESST, soumissions et taux horaires, montage et métrologie, formation au Québec, achats et consommables.",
             "PPE, fumes and CNESST, quoting and shop rates, fixturing and inspection, training in Quebec, buying and consumables."),
}
HUB_ORDER = ["software", "process", "fundamentals", "materials", "troubleshooting", "shop"]

SOFTWARE_GROUPS = [
    ("cad", "CAO / DAO", "CAD"),
    ("cam", "FAO / imbrication", "CAM / nesting"),
    ("control", "Commande machine", "Machine control"),
]

LEVELS = {"debutant": ("Débutant", "Beginner"), "intermediaire": ("Intermédiaire", "Intermediate"), "avance": ("Avancé", "Advanced")}

T = {
    "fr": {
        "home": "Accueil", "guides": "Guides", "prices": "Prix des tôles", "used": "Occasions", "news": "Infolettre",
        "about": "À propos", "search": "Rechercher", "search_ph": "Rechercher un guide (ex. SheetCam, K-factor, scories)…",
        "by_software": "Par logiciel", "by_process": "Par procédé", "by_topic": "Par sujet", "all_guides": "Tous les guides",
        "all_software": "Tous les logiciels", "menu": "Menu", "close": "Fermer", "on_page": "Sur cette page",
        "reviewed": "Révisé le", "read": "min de lecture", "draft": "Brouillon", "draft_tip": "Rédigé par CoupeFab à partir des documents officiels cités. Révision technique par Michaël Brassard en attente.",
        "related": "Guides connexes", "sources": "Sources", "next": "Poursuivre", "level": "Niveau",
        "report": "Une erreur, un ajout ? Écrivez-nous", "prices_cta_t": "Comparer le prix de la matière",
        "prices_cta_d": "Tôle, plaque, barre et tube : prix publiés chez les fournisseurs qui livrent au Québec, mis à jour chaque jour ouvrable.",
        "prices_cta_b": "Ouvrir le comparateur", "news_t": "Un guide par semaine, en français d’abord",
        "news_d": "Nouveaux guides, occasions au Québec et mouvements de prix. Pas de pub tierce.",
        "no_results": "Aucun guide trouvé. Essayez un autre mot (logiciel, procédé, matériau).",
        "skip": "Aller au contenu", "lang": "Langue", "explore": "Explorer", "legal": "Mentions",
    },
    "en": {
        "home": "Home", "guides": "Guides", "prices": "Sheet prices", "used": "Used equipment", "news": "Newsletter",
        "about": "About", "search": "Search", "search_ph": "Search guides (e.g. SheetCam, K-factor, dross)…",
        "by_software": "By software", "by_process": "By process", "by_topic": "By topic", "all_guides": "All guides",
        "all_software": "All software", "menu": "Menu", "close": "Close", "on_page": "On this page",
        "reviewed": "Reviewed", "read": "min read", "draft": "Draft", "draft_tip": "Written by CoupeFab from the official documents cited. Technical review by Michaël Brassard pending.",
        "related": "Related guides", "sources": "Sources", "next": "Keep going", "level": "Level",
        "report": "Spotted an error or want something added? Tell us", "prices_cta_t": "Compare material prices",
        "prices_cta_d": "Sheet, plate, bar and tube: published prices from suppliers serving Quebec, refreshed every business day.",
        "prices_cta_b": "Open the price tool", "news_t": "One guide a week, French-first",
        "news_d": "New guides, used equipment in Quebec and price moves. No third-party ads.",
        "no_results": "No guide found. Try another word (software, process, material).",
        "skip": "Skip to content", "lang": "Language", "explore": "Explore", "legal": "Legal",
    },
}

PATHS = {
    "fr": {"home": "/", "guides": "/guides/", "prices": "/prix/", "used": "/occasions/", "news": "/infolettre/",
           "about": "/a-propos/", "disc": "/divulgation/", "priv": "/confidentialite/"},
    "en": {"home": "/en/", "guides": "/en/guides/", "prices": "/en/sheet-prices/", "used": "/en/used-equipment/",
           "news": "/en/newsletter/", "about": "/en/about/", "disc": "/en/affiliate-disclosure/", "priv": "/en/privacy/"},
}


def hub_path(hub: str, lang: str) -> str:
    fr_slug, en_slug = HUBS[hub][0], HUBS[hub][1]
    return f"/guides/{fr_slug}/" if lang == "fr" else f"/en/guides/{en_slug}/"
