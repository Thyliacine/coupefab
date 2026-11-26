---
id: gcode
hub: fundamentals
order: 1
nav: G-code et M-code | G-code & M-code
kicker: Fondamentaux · référence | Fundamentals · reference
level: debutant
schema: Article
tags: g-code, m-code, cnc, mill, router, plasma, lathe, linuxcnc, fanuc
related: work-offsets, post-processors, feeds-speeds, linuxcnc
fr_slug: reference-g-code-m-code
en_slug: g-code-m-code-reference
fr_title: Référence G-code et M-code : les codes à connaître par cœur
en_title: G-code and M-code reference: the codes to know by heart
fr_desc: Les codes G et M courants (mouvements, plans, unités, compensation, cycles, broche, arrosage) avec leur sens, un exemple commenté et les pièges entre commandes.
en_desc: Common G and M codes (motion, planes, units, compensation, canned cycles, spindle, coolant) with their meaning, an annotated example and the traps between controls.
---
=== fr
Le G-code (normalisé à l’origine par l’EIA RS-274 et l’ISO 6983) est la langue des machines CNC. Les **codes G** décrivent la géométrie et les modes ; les **codes M** pilotent les fonctions machine (broche, arrosage, fin de programme). Chaque commande a son dialecte : ce tableau suit la documentation **LinuxCNC**, très proche des conventions de type Fanuc, et signale les écarts courants. Votre manuel de commande a toujours le dernier mot.

## Codes modaux : la notion clé

La plupart des codes sont **modaux** : ils restent actifs jusqu’à ce qu’un autre code du même groupe les remplace. Un `G1` reste actif ligne après ligne ; un `G91` oublié rend tout le reste du programme incrémental. C’est la source n° 1 des collisions « inexplicables ».

## Mouvements

| Code | Sens | Notes |
|---|---|---|
| `G0` | Déplacement rapide | Vitesse max de la machine ; trajectoire pas forcément en ligne droite sur toutes les commandes |
| `G1` | Interpolation linéaire à l’avance `F` | Le mouvement de coupe de base |
| `G2` / `G3` | Arc horaire / antihoraire | Centre en `I J K` (ou rayon `R`) |
| `G4` | Temporisation | `P` en secondes sur LinuxCNC ; en millisecondes sur certaines commandes de type Fanuc selon le réglage — vérifiez |

## Plans, unités, distances

| Code | Sens |
|---|---|
| `G17` / `G18` / `G19` | Plan XY / XZ / YZ (G18 est le plan habituel du tour) |
| `G20` / `G21` | Pouces / millimètres |
| `G90` / `G91` | Coordonnées absolues / incrémentales |
| `G90.1` / `G91.1` | Centres d’arc `I J K` absolus / incrémentaux (LinuxCNC, Mach) |
| `G93` / `G94` / `G95` | Avance en temps inverse / par minute / par tour |

## Origines et positions machine

| Code | Sens |
|---|---|
| `G53` | Déplacement en coordonnées machine (non modal) |
| `G54` à `G59` | Systèmes de coordonnées pièce 1 à 6 — voir [Décalages d’origine](/guides/decalages-origine-g54/) |
| `G28` / `G30` | Retour à une position de référence (souvent via un point intermédiaire : attention à l’ordre des axes) |
| `G92` | Décalage de coordonnées « temporaire » — puissant et piégeux, à éviter si vous ne maîtrisez pas son annulation |

## Compensation d’outil

| Code | Sens |
|---|---|
| `G40` | Annule la compensation de rayon |
| `G41` / `G42` | Compensation à gauche / à droite de la trajectoire |
| `G43 H…` | Compensation de longueur d’outil |
| `G49` | Annule la compensation de longueur |

## Cycles fixes (perçage)

| Code | Sens |
|---|---|
| `G81` | Perçage simple |
| `G82` | Perçage avec temporisation au fond |
| `G83` | Perçage par débourrage (peck) |
| `G73` | Débourrage court / brise-copeaux (selon commande) |
| `G84` | Taraudage (rigide ou flottant selon la machine) |
| `G80` | Annule le cycle fixe |
| `G98` / `G99` | Retour au plan initial / au plan R |

## Tour

| Code | Sens |
|---|---|
| `G96` | Vitesse de coupe constante (CSS) |
| `G97` | Vitesse de broche constante en tr/min |
| `G7` / `G8` | Mode diamètre / rayon (LinuxCNC) |
| `G76` | Cycle de filetage (paramètres très différents selon la commande) |

## Codes M courants

| Code | Sens |
|---|---|
| `M0` / `M1` | Arrêt programme / arrêt optionnel |
| `M2` / `M30` | Fin de programme (`M30` rembobine sur la plupart des commandes) |
| `M3` / `M4` / `M5` | Broche horaire / antihoraire / arrêt — en plasma, souvent torche ON / OFF |
| `M6` | Changement d’outil (avec `T…`) |
| `M7` / `M8` / `M9` | Brouillard / arrosage / arrêt arrosage |
| `M62`–`M65` | Sorties numériques synchronisées ou immédiates (LinuxCNC), utilisées notamment pour le THC plasma |

> [!WARN] En plasma, chaque commande a ses propres codes pour la torche, le palpage de hauteur (IHS) et le THC : FireControl utilise par exemple `H0`/`H1` selon la documentation Langmuir. Utilisez le post-processeur du fabricant — voir [Post-processeurs](/guides/post-processeurs/).

## Exemple commenté (fraisage, mm)

```gcode
%
O1001 (PLAQUE 100x60 - CONTOUR)
G21 G17 G40 G49 G80 G90     (mm, plan XY, annulations, absolu)
G54                         (origine piece 1)
T1 M6                       (outil 1 : fraise 10 mm)
S8000 M3                    (broche 8000 tr/min, sens horaire)
G43 H1 Z25.                 (compensation de longueur, Z securite)
M8                          (arrosage)
G0 X-8. Y-8.
Z2.
G1 Z-3. F300.               (plongee)
G41 D1 X0. F800.            (entree avec compensation de rayon)
Y60.
X100.
Y0.
X-2.
G40 X-8. Y-8.               (sortie, annulation)
G0 Z25. M9
M5
G28 G91 Z0.                 (retour Z reference)
G90
M30
%
```

Les vitesses et avances de cet exemple ne sont **pas** des recommandations : elles viennent du calcul de [Avances et vitesses](/guides/avances-vitesses/) et des données de votre fabricant d’outils.

## Ligne de sécurité

Commencez chaque programme par une ligne qui remet les modes dans un état connu, par exemple `G21 G17 G40 G49 G80 G90` (adaptez `G20`/`G21`). Elle protège contre les modes laissés actifs par le programme précédent ou par une saisie manuelle (MDI).

## Erreurs fréquentes

- `G91` resté actif après un retour `G28 G91 Z0` : remettez `G90` tout de suite.
- Arc refusé (« arc radius error ») : centres `I J` incrémentaux alors que la commande attend de l’absolu (`G90.1`), ou l’inverse.
- `G4 P1` qui attend 1 ms au lieu de 1 s (ou l’inverse) selon le dialecte.
- Compensation `G41` activée sur un mouvement trop court pour la rampe d’entrée.

## FAQ

### G-code Fanuc, Haas, LinuxCNC, grbl : est-ce la même chose ?
Le cœur (G0–G3, G17–G21, G90/G91, M3/M5…) est commun. Les cycles, les macros, les sous-programmes et les codes machine diffèrent. grbl implémente un sous-ensemble ; vérifiez sa liste de codes supportés.

### Faut-il écrire le G-code à la main ?
Pour comprendre, corriger et faire de petites opérations en MDI, oui. Pour les pièces, le FAO et un bon post-processeur font le travail.

## À valider en atelier (Michaël)

- Le dialecte des commandes les plus courantes dans vos ateliers (plasma et usinage).
- Une ligne de sécurité type pour vos machines.

## Sources

- [LinuxCNC — G-codes](https://linuxcnc.org/docs/stable/html/gcode/g-code.html), consulté le 26 novembre 2026.
- [LinuxCNC — M-codes](https://linuxcnc.org/docs/stable/html/gcode/m-code.html).
- [LinuxCNC — Coordinate systems](https://linuxcnc.org/docs/stable/html/gcode/coordinates.html).
- [grbl — Wiki (codes supportés)](https://github.com/gnea/grbl/wiki).
- [Langmuir Systems — Post Processing for FireControl (PDF)](https://assets.langmuirsystems.com/doc/Post+Processing+for+FireControl.pdf).
=== en
G-code (originally standardized as EIA RS-274 and ISO 6983) is the language of CNC machines. **G codes** describe geometry and modes; **M codes** drive machine functions (spindle, coolant, program end). Every control has its dialect: this table follows the **LinuxCNC** documentation, close to Fanuc-style conventions, and flags common differences. Your control manual always has the last word.

## Modal codes: the key idea

Most codes are **modal**: they stay active until another code from the same group replaces them. A `G1` stays active line after line; a forgotten `G91` makes the rest of the program incremental. That is the no. 1 source of “unexplainable” crashes.

## Motion

| Code | Meaning | Notes |
|---|---|---|
| `G0` | Rapid move | Machine max speed; path is not necessarily straight on every control |
| `G1` | Linear interpolation at feed `F` | The basic cutting move |
| `G2` / `G3` | Clockwise / counter-clockwise arc | Centre in `I J K` (or radius `R`) |
| `G4` | Dwell | `P` in seconds on LinuxCNC; milliseconds on some Fanuc-style controls depending on settings — check |

## Planes, units, distances

| Code | Meaning |
|---|---|
| `G17` / `G18` / `G19` | XY / XZ / YZ plane (G18 is the usual lathe plane) |
| `G20` / `G21` | Inches / millimetres |
| `G90` / `G91` | Absolute / incremental coordinates |
| `G90.1` / `G91.1` | Absolute / incremental arc centres `I J K` (LinuxCNC, Mach) |
| `G93` / `G94` / `G95` | Inverse-time / per-minute / per-revolution feed |

## Origins and machine positions

| Code | Meaning |
|---|---|
| `G53` | Move in machine coordinates (non-modal) |
| `G54` to `G59` | Work coordinate systems 1 to 6 — see [Work offsets](/en/guides/work-offsets-g54/) |
| `G28` / `G30` | Return to a reference position (often via an intermediate point: watch axis order) |
| `G92` | “Temporary” coordinate offset — powerful and tricky, avoid unless you master cancelling it |

## Tool compensation

| Code | Meaning |
|---|---|
| `G40` | Cancel cutter radius compensation |
| `G41` / `G42` | Compensation left / right of the path |
| `G43 H…` | Tool length compensation |
| `G49` | Cancel length compensation |

## Canned cycles (drilling)

| Code | Meaning |
|---|---|
| `G81` | Simple drilling |
| `G82` | Drilling with dwell at bottom |
| `G83` | Peck drilling |
| `G73` | Chip-break peck (control-dependent) |
| `G84` | Tapping (rigid or floating depending on machine) |
| `G80` | Cancel canned cycle |
| `G98` / `G99` | Retract to initial plane / R plane |

## Lathe

| Code | Meaning |
|---|---|
| `G96` | Constant surface speed (CSS) |
| `G97` | Constant spindle RPM |
| `G7` / `G8` | Diameter / radius mode (LinuxCNC) |
| `G76` | Threading cycle (parameters differ a lot between controls) |

## Common M codes

| Code | Meaning |
|---|---|
| `M0` / `M1` | Program stop / optional stop |
| `M2` / `M30` | Program end (`M30` rewinds on most controls) |
| `M3` / `M4` / `M5` | Spindle CW / CCW / stop — in plasma, often torch ON / OFF |
| `M6` | Tool change (with `T…`) |
| `M7` / `M8` / `M9` | Mist / flood / coolant off |
| `M62`–`M65` | Synchronized or immediate digital outputs (LinuxCNC), used for plasma THC among others |

> [!WARN] In plasma, each control has its own codes for torch, initial height sensing (IHS) and THC: FireControl, for example, uses `H0`/`H1` per Langmuir’s documentation. Use the manufacturer’s post processor — see [Post processors](/en/guides/post-processors/).

## Annotated example (milling, mm)

```gcode
%
O1001 (PLATE 100x60 - PROFILE)
G21 G17 G40 G49 G80 G90     (mm, XY plane, cancels, absolute)
G54                         (work offset 1)
T1 M6                       (tool 1: 10 mm end mill)
S8000 M3                    (spindle 8000 rpm, clockwise)
G43 H1 Z25.                 (length comp, safe Z)
M8                          (flood coolant)
G0 X-8. Y-8.
Z2.
G1 Z-3. F300.               (plunge)
G41 D1 X0. F800.            (lead-in with radius comp)
Y60.
X100.
Y0.
X-2.
G40 X-8. Y-8.               (lead-out, cancel)
G0 Z25. M9
M5
G28 G91 Z0.                 (Z reference return)
G90
M30
%
```

The speeds and feeds in this example are **not** recommendations: they come from the [Feeds and speeds](/en/guides/feeds-and-speeds/) math and your tool maker’s data.

## Safety line

Start every program with a line that resets modes to a known state, for example `G21 G17 G40 G49 G80 G90` (adapt `G20`/`G21`). It protects against modes left active by the previous program or a manual (MDI) entry.

## Common mistakes

- `G91` left active after a `G28 G91 Z0` return: restore `G90` immediately.
- Arc rejected (“arc radius error”): incremental `I J` centres while the control expects absolute (`G90.1`), or vice versa.
- `G4 P1` waiting 1 ms instead of 1 s (or the reverse) depending on dialect.
- `G41` activated on a move too short for the lead-in ramp.

## FAQ

### Fanuc, Haas, LinuxCNC, grbl G-code: is it the same?
The core (G0–G3, G17–G21, G90/G91, M3/M5…) is shared. Cycles, macros, subprograms and machine codes differ. grbl implements a subset; check its supported-code list.

### Should I write G-code by hand?
To understand, fix, and run small MDI jobs, yes. For parts, CAM and a good post processor do the work.

## For Michaël to review

- The dialect of the most common controls in your shops (plasma and machining).
- A standard safety line for your machines.

## Sources

- [LinuxCNC — G-codes](https://linuxcnc.org/docs/stable/html/gcode/g-code.html), consulted November 26, 2026.
- [LinuxCNC — M-codes](https://linuxcnc.org/docs/stable/html/gcode/m-code.html).
- [LinuxCNC — Coordinate systems](https://linuxcnc.org/docs/stable/html/gcode/coordinates.html).
- [grbl — Wiki (supported codes)](https://github.com/gnea/grbl/wiki).
- [Langmuir Systems — Post Processing for FireControl (PDF)](https://assets.langmuirsystems.com/doc/Post+Processing+for+FireControl.pdf).
