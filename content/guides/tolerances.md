---
id: tolerances
hub: fundamentals
order: 31
nav: Tolérances | Tolerances
kicker: Fondamentaux · dessin | Fundamentals · drawings
level: intermediaire
schema: Article
tags: tolerances, iso 2768, fits, drawings, gd&t, plasma, laser, machining
related: solidworks-drawings-cam, bend-allowance, dxf-best-practices, cnc-mill
fr_slug: tolerances-cnc
en_slug: cnc-tolerances
fr_title: Tolérances en fabrication : ISO 2768, ajustements et ce que chaque procédé tient
en_title: Tolerances in fabrication: ISO 2768, fits and what each process can hold
fr_desc: Tolérances générales ISO 2768-1, ajustements ISO 286, cotation fonctionnelle et tolérances réalistes selon le procédé (plasma, laser, pliage, usinage) — pour des dessins qui coûtent le juste prix.
en_desc: ISO 2768-1 general tolerances, ISO 286 fits, functional dimensioning and realistic tolerances by process (plasma, laser, bending, machining) — for drawings that cost the right price.
---
=== fr
Une tolérance trop large donne une pièce qui ne s’assemble pas ; une tolérance trop serrée multiplie le prix (procédé plus lent, contrôle, rebuts). Le bon dessin ne serre que ce qui est **fonctionnel** et renvoie le reste à une tolérance générale.

## Tolérances générales ISO 2768-1

La norme ISO 2768-1 définit des tolérances par défaut pour les cotes linéaires sans tolérance indiquée, en quatre classes : **f** (fine), **m** (moyenne), **c** (grossière), **v** (très grossière). Elle s’appelle dans le cartouche, par exemple « ISO 2768-m ». Valeurs pour les cotes linéaires (mm) :

| Plage de cote (mm) | f | m | c | v |
|---|--:|--:|--:|--:|
| 0,5 à 3 | ±0,05 | ±0,1 | ±0,2 | — |
| > 3 à 6 | ±0,05 | ±0,1 | ±0,3 | ±0,5 |
| > 6 à 30 | ±0,1 | ±0,2 | ±0,5 | ±1 |
| > 30 à 120 | ±0,15 | ±0,3 | ±0,8 | ±1,5 |
| > 120 à 400 | ±0,2 | ±0,5 | ±1,2 | ±2,5 |
| > 400 à 1000 | ±0,3 | ±0,8 | ±2 | ±4 |
| > 1000 à 2000 | ±0,5 | ±1,2 | ±3 | ±6 |
| > 2000 à 4000 | — | ±2 | ±4 | ±8 |

> [!NOTE] Ce tableau reprend les valeurs de la norme telles qu’elles sont largement reproduites ; la norme officielle (achetée auprès de l’ISO ou du CCN) fait foi. ISO 2768-2 couvre les tolérances géométriques générales (classes H, K, L).

## Ajustements ISO 286 (arbres et alésages)

Pour un roulement, une goupille ou un arbre, on utilise un **ajustement** : une lettre (position) et un chiffre (qualité IT). Exemples courants : **H7/g6** (glissant), **H7/h6** (glissant juste), **H7/p6** (serré). Les écarts exacts dépendent du diamètre : consultez le tableau ISO 286-2 ou celui de votre fournisseur de roulements. Ces tolérances relèvent de l’usinage (alésage, rectification), pas de la découpe.

## Ce que chaque procédé tient (ordres de grandeur)

Les capacités réelles dépendent de la machine, de l’épaisseur et de l’état de l’atelier. Demandez toujours au fabricant ou au sous-traitant sa capacité publiée ; à défaut, voici comment raisonner :

| Procédé | Ce qui limite la précision | Conseil de dessin |
|---|---|---|
| Plasma | Largeur et biseau de saignée, chaleur, état de la torche | Tolérances larges ; percer ou aléser les trous critiques |
| Laser fibre | Dilatation, épaisseur, réglages | Plus serré que le plasma ; vérifier avec l’atelier |
| Jet d’eau | Conicité (taper), vitesse | Indiquer la face de référence ; tête à compensation de conicité si critique |
| Pliage | Angle, rayon, variation de l’épaisseur | Coter depuis une seule référence ; éviter les chaînes de cotes à travers plusieurs plis |
| Fraisage / tournage | Machine, outil, montage, température | Serrer seulement les surfaces fonctionnelles |

## Cotation fonctionnelle : les règles de base

1. **Choisir les références** (datums) qui correspondent à l’assemblage réel.
2. **Coter depuis ces références**, pas en chaîne : les erreurs s’additionnent en chaîne.
3. **Ne tolérancer serré que ce qui touche** une autre pièce.
4. **Renvoyer le reste** à une tolérance générale dans le cartouche.
5. **Indiquer l’état de surface** seulement où il compte.
6. **En tôlerie pliée**, coter les ailes à l’extérieur ou à l’intérieur de façon cohérente avec la méthode de l’atelier.

## Erreurs fréquentes

- « ±0,01 » partout par habitude : le prix explose, la pièce n’est pas meilleure.
- Chaînes de cotes à travers trois plis : impossible à tenir.
- Aucune tolérance générale au cartouche : chaque cote devient une discussion.
- Demander un ajustement H7 sur un trou plasma.

## FAQ

### ISO 2768 ou ASME Y14.5 ?
ISO 2768 donne des tolérances générales par défaut ; ASME Y14.5 (et ISO 1101 / GPS) définissent la cotation géométrique (GD&T). En Amérique du Nord, beaucoup de dessins suivent ASME pour la géométrie et indiquent une tolérance de bloc au cartouche.

### Quelle classe ISO 2768 pour de la tôlerie découpée ?
Souvent « m » ou « c » selon le procédé et l’épaisseur. Confirmez avec la capacité de l’atelier qui fabrique.

## À valider en atelier (Michaël)

- Les tolérances réellement tenues sur vos tables plasma et en pliage.
- Le bloc de tolérances utilisé dans vos dessins.

## Sources

- [ISO 2768-1:1989 — Tolérances générales (fiche ISO)](https://www.iso.org/standard/7748.html), consulté le 26 novembre 2026.
- [ISO 286-2 — Système de codification ISO des tolérances (fiche ISO)](https://www.iso.org/standard/54915.html).
- [ASME Y14.5 — Dimensioning and Tolerancing](https://www.asme.org/codes-standards/find-codes-standards/y14-5-dimensioning-tolerancing).
=== en
Too loose a tolerance gives a part that does not assemble; too tight multiplies the price (slower process, inspection, scrap). A good drawing tightens only what is **functional** and sends the rest to a general tolerance.

## ISO 2768-1 general tolerances

ISO 2768-1 defines default tolerances for linear dimensions without an indicated tolerance, in four classes: **f** (fine), **m** (medium), **c** (coarse), **v** (very coarse). It is called up in the title block, for example “ISO 2768-m”. Values for linear dimensions (mm):

| Size range (mm) | f | m | c | v |
|---|--:|--:|--:|--:|
| 0.5 to 3 | ±0.05 | ±0.1 | ±0.2 | — |
| > 3 to 6 | ±0.05 | ±0.1 | ±0.3 | ±0.5 |
| > 6 to 30 | ±0.1 | ±0.2 | ±0.5 | ±1 |
| > 30 to 120 | ±0.15 | ±0.3 | ±0.8 | ±1.5 |
| > 120 to 400 | ±0.2 | ±0.5 | ±1.2 | ±2.5 |
| > 400 to 1000 | ±0.3 | ±0.8 | ±2 | ±4 |
| > 1000 to 2000 | ±0.5 | ±1.2 | ±3 | ±6 |
| > 2000 to 4000 | — | ±2 | ±4 | ±8 |

> [!NOTE] This table reproduces the standard’s values as widely published; the official standard (bought from ISO or the Standards Council of Canada) governs. ISO 2768-2 covers general geometric tolerances (classes H, K, L).

## ISO 286 fits (shafts and holes)

For a bearing, pin or shaft you use a **fit**: a letter (position) and a number (IT grade). Common examples: **H7/g6** (sliding), **H7/h6** (locational clearance), **H7/p6** (interference). Exact deviations depend on diameter: use the ISO 286-2 table or your bearing supplier’s. These are machining tolerances (boring, grinding), not cutting tolerances.

## What each process holds (orders of magnitude)

Real capability depends on the machine, thickness and shop condition. Always ask the maker or job shop for its published capability; failing that, reason like this:

| Process | What limits precision | Drawing advice |
|---|---|---|
| Plasma | Kerf width and bevel, heat, torch condition | Loose tolerances; drill or ream critical holes |
| Fiber laser | Thermal growth, thickness, settings | Tighter than plasma; confirm with the shop |
| Waterjet | Taper, speed | State the datum face; taper-compensating head if critical |
| Bending | Angle, radius, thickness variation | Dimension from one datum; avoid chains across several bends |
| Milling / turning | Machine, tool, fixturing, temperature | Tighten functional surfaces only |

## Functional dimensioning: the basics

1. **Choose datums** that match the real assembly.
2. **Dimension from those datums**, not in a chain: errors add up in a chain.
3. **Tighten only what touches** another part.
4. **Send the rest** to a general tolerance in the title block.
5. **Specify surface finish** only where it matters.
6. **On bent parts**, dimension flanges outside or inside consistently with the shop’s method.

## Common mistakes

- “±0.01” everywhere out of habit: the price explodes, the part is no better.
- Dimension chains across three bends: impossible to hold.
- No general tolerance in the title block: every dimension becomes an argument.
- Asking for an H7 fit on a plasma hole.

## FAQ

### ISO 2768 or ASME Y14.5?
ISO 2768 gives default general tolerances; ASME Y14.5 (and ISO 1101 / GPS) define geometric dimensioning (GD&T). In North America many drawings follow ASME for geometry and state a block tolerance in the title block.

### Which ISO 2768 class for cut sheet metal?
Often “m” or “c” depending on process and thickness. Confirm against the capability of the shop making it.

## For Michaël to review

- The tolerances actually held on your plasma tables and in bending.
- The tolerance block used on your drawings.

## Sources

- [ISO 2768-1:1989 — General tolerances (ISO page)](https://www.iso.org/standard/7748.html), consulted November 26, 2026.
- [ISO 286-2 — ISO code system for tolerances (ISO page)](https://www.iso.org/standard/54915.html).
- [ASME Y14.5 — Dimensioning and Tolerancing](https://www.asme.org/codes-standards/find-codes-standards/y14-5-dimensioning-tolerancing).
