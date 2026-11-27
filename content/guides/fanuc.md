---
id: fanuc
hub: software
group: control
order: 50
mono: Fa
nav: Commande Fanuc | Fanuc control
kicker: Commande machine · Fanuc | Machine control · Fanuc
level: intermediaire
schema: HowTo
tags: fanuc, 0i-f, 0i-f plus, 30i-b, 31i, 32i, g54, g54.1, g10, macro b, custom macro, work offsets, tool offsets, program number, cnc control
related: haas, siemens-sinumerik, work-offsets, gcode
fr_slug: commande-fanuc-cnc
en_slug: fanuc-cnc-control
fr_title: Commande Fanuc : origines, correcteurs, format de programme et post sans surprise
en_title: Fanuc CNC control: work offsets, tool offsets, program format and a surprise-free post
fr_desc: Les séries Fanuc (0i-F Plus, 30i-B Plus), le format de programme, les origines G54–G59 et additionnelles, G10, les correcteurs d’outil et les points à vérifier avant de lancer un programme venu d’une autre machine.
en_desc: Fanuc series (0i-F Plus, 30i-B Plus), program format, G54–G59 and additional work offsets, G10, tool offsets and what to check before running a program written for another machine.
codes: fanuc
---
=== fr
**Fanuc** équipe une grande partie des fraiseuses et des tours CNC industriels. Le dialecte Fanuc sert de référence à beaucoup d’autres commandes (Haas, LinuxCNC et plusieurs commandes asiatiques en reprennent l’essentiel), mais **chaque constructeur de machine active ses propres options et paramètres**. Ce guide donne la démarche ; le manuel de *votre* machine a toujours le dernier mot.

## Les séries courantes

| Série | Positionnement (selon Fanuc America) |
|---|---|
| **0i-F Plus** | Commande « applications générales », fonctions personnalisables, fraisage et tournage courants |
| **30i / 31i / 32i-B Plus** | Usinage avancé : grande vitesse, multi-axes et multi-canaux, machines 5 axes |

> [!NOTE] Deux machines « Fanuc » peuvent se comporter différemment : options achetées (nombre d’origines additionnelles, macros, cycles), paramètres et cycles du constructeur. Notez la série exacte et la liste d’options avant d’écrire ou d’adapter un post.

## Format de programme

| Élément | Rôle |
|---|---|
| `%` | Début et fin de bande (transfert) |
| `O1234` | Numéro de programme |
| `(COMMENTAIRE)` | Commentaires entre parenthèses |
| `N10` | Numéro de bloc (facultatif) |
| `M30` | Fin de programme et retour au début |

Un en-tête prudent remet la commande dans un état connu : plan, unités, annulation de compensation et de cycle, mode absolu.

```gcode
%
O1001 (SUPPORT - OP10)
G17 G21 G40 G49 G80 G90
T1 M06
G54 G00 X0. Y0. S2500 M03
G43 H01 Z50. M08
...
M30
%
```

## Origines pièce (décalages)

1. **G54 à G59** : six origines standard, réglées à l’écran des décalages ou par programme.
2. **Origines additionnelles** : `G54.1 P1`… avec l’option « 48 origines additionnelles » de FANUC, on a `G54.1 P1` à `P48` en plus de G54–G59 ; une autre option porte le total à 300 jeux (`P1`–`P300`) sur certaines séries. Vérifiez quelles options sont actives sur votre machine (écran des paramètres ou fiche du fabricant de la machine).
3. **Écriture par programme** : `G10 L2 P1` écrit G54 ; `G10 L20 P1` écrit l’origine additionnelle P1. En `G90`, la valeur remplace ; en `G91`, elle s’ajoute.
4. **Vérifier** : afficher la position absolue sur un point connu de la pièce avant le premier cycle.

> [!WARN] Un `G10` en `G91` laissé dans un programme décale l’origine **à chaque exécution**. Relisez toujours le mode actif avant un `G10`.

## Correcteurs d’outil

- **Longueur** : `G43 H..` applique la longueur ; `G49` l’annule. Habitude d’atelier : `H` = numéro d’outil.
- **Rayon** : `G41/G42 D..` ; le registre `D` contient le rayon (ou l’usure seulement si le post sort la trajectoire compensée — choisissez une convention et tenez-vous-y).
- **Usure** : ajustez l’usure, pas la géométrie, pour corriger une cote en production.

## Macros

Les **macros personnalisées** (souvent appelées *Macro B*) ajoutent variables (`#1`…, `#100`…, `#500`…), calculs et sauts conditionnels. Elles servent au palpage, aux familles de pièces et aux compteurs. Les variables `#500` et plus sont généralement conservées à la mise hors tension : documentez celles que vous utilisez.

## Liste de vérification avant de lancer un programme externe

- [ ] Série et options de la commande connues (origines additionnelles, macros, cycles)
- [ ] Post configuré pour **cette** machine (changement d’outil, M-codes d’arrosage, cycles de perçage)
- [ ] Unités `G20/G21` cohérentes avec les décalages réglés
- [ ] Origine appelée = origine réglée ; longueurs d’outil à jour
- [ ] Premier passage en marche bloc à bloc, avance réduite, Z de sécurité vérifié

## Erreurs fréquentes

- Supposer qu’un programme d’une autre machine Fanuc tournera tel quel : M-codes et cycles du constructeur diffèrent.
- Oublier le point décimal dans les coordonnées : selon un paramètre, `X10` peut être lu comme 10 mm **ou** 0,010 mm. Un post Fanuc doit toujours écrire `X10.`.
- Laisser `G41/G42` actif à la fin d’un contour.
- Corriger la géométrie d’outil au lieu de l’usure, puis perdre la référence.

## FAQ

### Mon programme Haas tournera-t-il sur une Fanuc ?
Les bases (G0/G1/G2/G3, G54, G43, cycles G81–G83) sont proches, mais les M-codes, les cycles spéciaux et les origines étendues diffèrent (Haas `G154`, Fanuc `G54.1`). Repostez avec le bon post au lieu d’éditer à la main.

### Où trouver le manuel ?
Auprès du constructeur ou du revendeur de la machine : le manuel Fanuc d’origine plus les documents propres au constructeur (M-codes, cycles, options).

### Faut-il utiliser G10 en production ?
Oui pour des familles de pièces ou des montages multiples, à condition de l’encadrer : mode absolu, commentaire clair et simulation.

## À valider en atelier (Michaël)

- Série, options et plage d’origines additionnelles des machines Fanuc de l’atelier.
- Convention `D` (rayon complet ou usure) utilisée avec nos posts.
- Comportement du point décimal (paramètre) sur nos machines.

## Sources

- [FANUC America — Série 0i-F Plus](https://www.fanucamerica.com/products/series/0i-f-plus), consulté le 26 novembre 2026.
- [FANUC America — 30i-B Plus](https://www.fanucamerica.com/products/cnc/30i-b-plus), consulté le 26 novembre 2026.
- [FANUC America — CNC Options](https://www.fanucamerica.com/support/cnc/options) : option « 48 additional work offsets » (G54.1 P1–P48), consulté le 26 novembre 2026.
- [FANUC America — CNC Function Catalog (PDF)](https://www.fanucamerica.com/uploads/files/cnc-function-catalog.pdf) : « Addition of workpiece coordinate system » 48 et 300 jeux, consulté le 26 novembre 2026.
- [LinuxCNC — G-codes (G10 L2/L20, G43, G54–G59)](https://linuxcnc.org/docs/stable/html/gcode/g-code.html) : référence publique du dialecte de type Fanuc.
- [LinuxCNC — Coordinate systems](https://linuxcnc.org/docs/stable/html/gcode/coordinates.html).
- [Haas — Mill Programming Workbook (PDF)](https://haascnc.com/content/dam/haascnc/en/service/reference/programming-workbooks/mill---programming-workbook.pdf) : commande de type Fanuc, utile pour comparer.

=== en
**Fanuc** controls a large share of industrial CNC mills and lathes. The Fanuc dialect is the reference many other controls follow (Haas, LinuxCNC and several Asian controls share most of it), but **every machine builder enables its own options and parameters**. This guide gives the method; *your* machine’s manual always has the final word.

## Common series

| Series | Positioning (per FANUC America) |
|---|---|
| **0i-F Plus** | “General applications” control, customizable functions, everyday milling and turning |
| **30i / 31i / 32i-B Plus** | Advanced machining: high speed, multi-axis and multi-path, 5-axis machines |

> [!NOTE] Two “Fanuc” machines can behave differently: purchased options (number of additional offsets, macros, cycles), parameters and builder cycles. Write down the exact series and option list before writing or adapting a post.

## Program format

| Element | Role |
|---|---|
| `%` | Tape start and end (transfer) |
| `O1234` | Program number |
| `(COMMENT)` | Comments in parentheses |
| `N10` | Block number (optional) |
| `M30` | Program end and rewind |

A careful header puts the control in a known state: plane, units, compensation and canned cycle cancelled, absolute mode.

```gcode
%
O1001 (BRACKET - OP10)
G17 G21 G40 G49 G80 G90
T1 M06
G54 G00 X0. Y0. S2500 M03
G43 H01 Z50. M08
...
M30
%
```

## Work offsets

1. **G54 to G59**: six standard offsets, set on the offset page or by program.
2. **Additional offsets**: `G54.1 P1`… with FANUC’s “48 additional work offsets” option you get `G54.1 P1` to `P48` on top of G54–G59; a separate option raises the total to 300 sets (`P1`–`P300`) on some series. Check which options your machine actually has (parameter screen or the machine builder’s spec sheet).
3. **Writing by program**: `G10 L2 P1` writes G54; `G10 L20 P1` writes additional offset P1. In `G90` the value replaces; in `G91` it adds.
4. **Check**: display the absolute position on a known point of the part before the first cycle.

> [!WARN] A `G10` in `G91` left in a program shifts the offset **every time it runs**. Always check the active mode before a `G10`.

## Tool offsets

- **Length**: `G43 H..` applies the length; `G49` cancels it. Shop habit: `H` = tool number.
- **Radius**: `G41/G42 D..`; the `D` register holds the radius (or wear only if the post outputs the compensated path — pick one convention and stick to it).
- **Wear**: adjust wear, not geometry, to correct a size in production.

## Macros

**Custom macros** (often called *Macro B*) add variables (`#1`…, `#100`…, `#500`…), math and conditional jumps. They are used for probing, part families and counters. Variables `#500` and up are usually retained at power-off: document the ones you use.

## Checklist before running an outside program

- [ ] Control series and options known (additional offsets, macros, cycles)
- [ ] Post configured for **this** machine (tool change, coolant M-codes, drilling cycles)
- [ ] `G20/G21` units consistent with the offsets that were set
- [ ] Offset called = offset set; tool lengths current
- [ ] First run in single block, reduced feed, safe Z checked

## Common mistakes

- Assuming a program from another Fanuc machine will run as is: builder M-codes and cycles differ.
- Dropping the decimal point: depending on a parameter, `X10` may be read as 10 mm **or** 0.010 mm. A Fanuc post should always write `X10.`.
- Leaving `G41/G42` active at the end of a contour.
- Editing tool geometry instead of wear, then losing the reference.

## FAQ

### Will my Haas program run on a Fanuc?
The basics (G0/G1/G2/G3, G54, G43, G81–G83 cycles) are close, but M-codes, special cycles and extended offsets differ (Haas `G154`, Fanuc `G54.1`). Re-post with the right post instead of hand-editing.

### Where do I get the manual?
From the machine builder or dealer: the original Fanuc manual plus the builder’s own documents (M-codes, cycles, options).

### Should I use G10 in production?
Yes for part families or multiple fixtures, as long as it is controlled: absolute mode, a clear comment and simulation.

## For Michaël to review

- Series, options and additional-offset range of the shop’s Fanuc machines.
- `D` convention (full radius or wear) used with our posts.
- Decimal-point behaviour (parameter) on our machines.

## Sources

- [FANUC America — 0i-F Plus series](https://www.fanucamerica.com/products/series/0i-f-plus), consulted November 26, 2026.
- [FANUC America — 30i-B Plus](https://www.fanucamerica.com/products/cnc/30i-b-plus), consulted November 26, 2026.
- [FANUC America — CNC Options](https://www.fanucamerica.com/support/cnc/options): “48 additional work offsets” option (G54.1 P1–P48), consulted November 26, 2026.
- [FANUC America — CNC Function Catalog (PDF)](https://www.fanucamerica.com/uploads/files/cnc-function-catalog.pdf): “Addition of workpiece coordinate system” 48 and 300 pairs, consulted November 26, 2026.
- [LinuxCNC — G-codes (G10 L2/L20, G43, G54–G59)](https://linuxcnc.org/docs/stable/html/gcode/g-code.html): public reference for the Fanuc-style dialect.
- [LinuxCNC — Coordinate systems](https://linuxcnc.org/docs/stable/html/gcode/coordinates.html).
- [Haas — Mill Programming Workbook (PDF)](https://haascnc.com/content/dam/haascnc/en/service/reference/programming-workbooks/mill---programming-workbook.pdf): a Fanuc-style control, useful for comparison.
