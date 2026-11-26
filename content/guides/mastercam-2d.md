---
id: mastercam-2d
hub: software
group: cam
order: 30
mono: Mc
nav: Mastercam 2D | Mastercam 2D
kicker: Logiciel · FAO | Software · CAM
level: intermediaire
schema: HowTo
tags: mastercam, dynamic motion, dynamic mill, peel mill, dynamic contour, 2d high speed, chaining, stock, verify, router
related: mastercam-posts-lathe, feeds-speeds, milling-troubleshooting, cnc-mill
fr_slug: mastercam-parcours-2d-dynamic
en_slug: mastercam-2d-toolpaths-dynamic-milling
fr_title: Mastercam : parcours 2D et fraisage dynamique (Dynamic Motion) sans se tromper
en_title: Mastercam: 2D toolpaths and dynamic milling (Dynamic Motion) done right
fr_desc: Définition machine, brut, chaînage, Dynamic Mill, Peel Mill, Dynamic Contour, Face et vérification : la démarche Mastercam en 2D, les niveaux de licence et les pièges de chaînage les plus courants.
en_desc: Machine definition, stock, chaining, Dynamic Mill, Peel Mill, Dynamic Contour, Face and verification: the Mastercam 2D workflow, licence levels and the most common chaining pitfalls.
---
=== fr
Mastercam est l’un des logiciels de FAO les plus répandus en atelier d’usinage. Sa force en 2D est la technologie **Dynamic Motion** : des parcours qui adaptent le mouvement à la matière restante pour garder une charge de copeau constante, ce qui permet d’utiliser toute la longueur de coupe de l’outil.

## Niveaux de licence (fraisage)

| Niveau | Ce qu’il couvre en bref |
|---|---|
| Mill Entry | Parcours 2D de base |
| Mill | 2D, dont les parcours **Dynamic Motion** 2D |
| Mill 3D | Parcours 3D avancés |
| Router | Équivalent orienté routeur (imbrication, panneaux) selon les options |

Vérifiez le détail exact auprès de votre revendeur : le contenu des niveaux change d’une version à l’autre.

## Démarche

1. **Définition machine** : choisir la machine (et donc le post) dans le gestionnaire de groupes de machines. Un mauvais choix ici produit un mauvais G-code plus loin. Voir [Post et tour Mastercam](/guides/mastercam-post-tour/).
2. **Brut** (Stock setup) : dimensions et origine ; l’origine du plan de travail doit correspondre à votre G54 — voir [Décalages d’origine](/guides/decalages-origine-g54/).
3. **Plans** : vérifier le plan d’outil et le plan de construction (WCS).
4. **Outils** : depuis une bibliothèque ou le catalogue d’un fabricant d’outils.
5. **Parcours** (menu 2D, groupe 2D High Speed pour les dynamiques) : choisir le parcours, **chaîner** la géométrie, régler les paramètres.
6. **Vérifier** : Backplot puis Verify (simulation matière).
7. **Post-traiter** (G1) et relire le programme.

## Quel parcours 2D dynamique choisir

| Parcours | Usage |
|---|---|
| **Dynamic Mill** | Poches, matière restante, bossages ; stratégie *Stay inside* (poche) ou *From outside* (surfaçage avec îlots) |
| **Peel Mill** | Fraiser entre des chaînes ouvertes (rainures, bandes) avec retours accélérés hors matière |
| **Dynamic Contour** | Contour avec mouvement dynamique ; évite d’enterrer l’outil dans les petits rayons |
| **Face** (style Dynamic) | Surfaçage du dessus du brut |
| Area Mill / Contour / Pocket classiques | Finition, géométrie simple, machines peu dynamiques |

## Chaînage : les régions de Dynamic Mill

Dynamic Mill accepte plusieurs types de chaînes dans une même opération :

- **Régions à usiner** : la zone à vider.
- **Régions d’évitement** : îlots à ne pas toucher.
- **Régions d’air** : zones sans matière où l’outil peut circuler et entrer.

> [!TIP] Une chaîne ouverte ou un doublon de géométrie est la cause numéro un des parcours qui « ne se calculent pas ». Nettoyez la géométrie importée (DXF) avant de chaîner — voir [DXF : bonnes pratiques](/guides/dxf-bonnes-pratiques/).

## Paramètres qui comptent en dynamique

- **Pas latéral** faible (souvent 5 à 15 % du diamètre selon matière et machine) et **profondeur** grande : suivez la fiche du fabricant d’outil.
- **Avance** recalculée pour l’amincissement du copeau — voir [Avances et vitesses](/guides/avances-vitesses/).
- **Entrée** : hélice ou entrée par l’extérieur (régions d’air).
- **Matière restante** activée pour reprendre derrière un gros outil.

## Erreurs fréquentes

| Erreur | Correctif |
|---|---|
| Mauvais groupe de machine | Recréer le groupe avec la bonne définition |
| Plan d’outil incorrect | Vérifier le WCS et le plan d’outil avant chaque opération |
| Parcours dynamique sur une machine qui ne suit pas | Lisser, réduire l’avance de raccordement, tester |
| Pas latéral trop grand | C’est un parcours HSM : petit pas, grande profondeur |

## FAQ

### Mastercam convient-il à la découpe plasma ?
Mastercam a des solutions pour le profilage, mais pour un atelier plasma, un logiciel dédié (SheetCam, ProNest) est souvent plus simple — voir [SheetCam](/guides/debuter-sheetcam/) et [ProNest](/guides/pronest-imbrication/).

## À valider en atelier (Michaël)

- Vos parcours et paramètres types pour l’acier doux et l’aluminium.

## Sources

- [Mastercam — Dynamic Motion](https://www.mastercam.com/solutions/products/dynamic-motion/), consulté le 26 novembre 2026.
- [Mastercam Canada — Mill 2D (niveaux de licence)](https://www.mastercam.ca/products/mastercam/mill-2d/).
- [Mastercam — Getting Started Series, Basic 2D Machining (PDF)](https://www.mastercam.dk/download/mastercam/tutorials/Basic_2D_Machining_Tutorial.pdf).
=== en
Mastercam is one of the most widely used CAM packages in machine shops. Its 2D strength is **Dynamic Motion** technology: toolpaths that adapt motion to the remaining stock to keep a constant chip load, which lets you use the tool’s full flute length.

## Licence levels (milling)

| Level | What it covers, briefly |
|---|---|
| Mill Entry | Basic 2D toolpaths |
| Mill | 2D, including 2D **Dynamic Motion** toolpaths |
| Mill 3D | Advanced 3D toolpaths |
| Router | Router-oriented equivalent (nesting, panels) depending on options |

Check the exact contents with your reseller: level contents change between versions.

## Workflow

1. **Machine definition**: pick the machine (and therefore the post) in the machine group manager. A wrong choice here produces wrong G-code later. See [Mastercam posts and lathe](/en/guides/mastercam-posts-and-lathe/).
2. **Stock setup**: dimensions and origin; the work plane origin must match your G54 — see [Work offsets](/en/guides/work-offsets-g54/).
3. **Planes**: check tool plane and construction plane (WCS).
4. **Tools**: from a library or a tool maker’s catalogue.
5. **Toolpaths** (2D menu, 2D High Speed group for dynamics): pick the toolpath, **chain** the geometry, set parameters.
6. **Verify**: Backplot then Verify (stock simulation).
7. **Post** (G1) and read the program.

## Which 2D dynamic toolpath to use

| Toolpath | Use |
|---|---|
| **Dynamic Mill** | Pockets, rest material, bosses; *Stay inside* (pocket) or *From outside* (facing with islands) |
| **Peel Mill** | Milling between open chains (slots, strips) with accelerated back-feed out of material |
| **Dynamic Contour** | Contour with dynamic motion; avoids burying the tool in small radii |
| **Face** (Dynamic style) | Facing the top of the stock |
| Classic Area Mill / Contour / Pocket | Finishing, simple geometry, less dynamic machines |

## Chaining: Dynamic Mill regions

Dynamic Mill accepts several chain types in one operation:

- **Machining regions**: the area to clear.
- **Avoidance regions**: islands not to touch.
- **Air regions**: areas with no material where the tool can travel and enter.

> [!TIP] An open chain or duplicate geometry is the number one cause of toolpaths that “won’t calculate”. Clean imported geometry (DXF) before chaining — see [DXF best practices](/en/guides/dxf-best-practices/).

## Parameters that matter in dynamic milling

- Small **stepover** (often 5–15% of diameter depending on material and machine) and large **depth**: follow the tool maker’s sheet.
- **Feed** recalculated for chip thinning — see [Feeds and speeds](/en/guides/feeds-and-speeds/).
- **Entry**: helix or entry from outside (air regions).
- **Rest material** on to clean up behind a big tool.

## Common mistakes

| Mistake | Fix |
|---|---|
| Wrong machine group | Recreate the group with the right definition |
| Wrong tool plane | Check WCS and tool plane before each operation |
| Dynamic path on a machine that can’t keep up | Smooth, reduce link feed, test |
| Stepover too large | It is an HSM path: small stepover, large depth |

## FAQ

### Is Mastercam suited to plasma cutting?
Mastercam has profiling solutions, but for a plasma shop dedicated software (SheetCam, ProNest) is often simpler — see [SheetCam](/en/guides/getting-started-sheetcam/) and [ProNest](/en/guides/pronest-nesting/).

## For Michaël to review

- Your typical toolpaths and parameters for mild steel and aluminum.

## Sources

- [Mastercam — Dynamic Motion](https://www.mastercam.com/solutions/products/dynamic-motion/), consulted November 26, 2026.
- [Mastercam Canada — Mill 2D (licence levels)](https://www.mastercam.ca/products/mastercam/mill-2d/).
- [Mastercam — Getting Started Series, Basic 2D Machining (PDF)](https://www.mastercam.dk/download/mastercam/tutorials/Basic_2D_Machining_Tutorial.pdf).
