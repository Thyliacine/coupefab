---
id: deburring
hub: process
order: 72
nav: Ébavurage et finition | Deburring and finishing
kicker: Procédé · après la coupe | Process · after cutting
level: debutant
schema: HowTo
tags: deburring, dross removal, slag, edge rounding, edge break, oxide removal, wide belt, brush, tumbling, vibratory, chamfer, burr, finishing, powder coating
related: laser-troubleshooting, plasma-troubleshooting, weld-prep, quoting
fr_slug: ebavurage-finition
en_slug: deburring-finishing
fr_title: Ébavurage et finition des pièces coupées : scories, bavures, arêtes et oxyde
en_title: Deburring and finishing cut parts: dross, burrs, edges and oxide
fr_desc: Quoi enlever (scories, bavure, arête vive, oxyde de coupe), dans quel ordre, avec quelle méthode (marteau, ponceuse à bande, brosses, tribofinition, machine à large bande), et comment le spécifier sur un dessin.
en_desc: What to remove (dross, burr, sharp edge, cutting oxide), in what order, with which method (hammer, belt sander, brushes, tumbling, wide-belt machine), and how to specify it on a drawing.
---
=== fr
La découpe laisse presque toujours quelque chose à reprendre : **scories** (métal resolidifié sous la pièce), **bavure** (petite lèvre), **arête vive** qui coupe les mains et accroche mal la peinture, et parfois **oxyde** de coupe sur le chant. L’ébavurage coûte du temps — il doit être prévu dans la soumission (voir [[quoting]]) et réduit à la source par un bon réglage de coupe.

## D’abord : réduire à la source

- Plasma : vitesse, hauteur et consommables selon la charte ; voir [[plasma-troubleshooting]].
- Laser : buse, centrage, focale, gaz ; voir [[laser-troubleshooting]].
- Une bonne coupe ne demande qu’un léger passage ; une mauvaise coupe peut coûter plus en ébavurage qu’en coupe.

## Quoi enlever et comment

| Défaut | Méthode courante | Remarques |
|---|---|---|
| Scories lourdes (plasma, oxycoupage) | Marteau à piquer, burin, poste de décrassage par impact | Les distributeurs d’équipements de finition recommandent d’enlever les scories **avant** le ponçage pour ne pas user les abrasifs |
| Bavure fine (laser, poinçonnage) | Ponceuse à bande, machine à large bande, brosses rotatives | Une ou deux passes selon la machine |
| Arête vive → arête cassée ou arrondie | Brosses, tribofinition (vibrateur), lime, chanfreineur | Préciser le rayon ou le chanfrein voulu |
| Oxyde sur le chant (coupe à l’O₂) | Brossage abrasif, meulage | Important avant peinture en poudre ou soudure selon la procédure |
| Coloration thermique sur inox | Décapage/passivation selon les règles de l’art, brossage dédié | Outils dédiés à l’inox |

## Choisir l’équipement selon le volume

| Volume | Équipement typique |
|---|---|
| Quelques pièces | Lime, meuleuse avec disque à lamelles, ponceuse à bande manuelle |
| Petites séries | Ponceuse à bande stationnaire, outil d’ébavurage de chant, tribofinition |
| Production | Machine à large bande avec brosses (ébavurage et arrondi des deux faces selon modèle) |

## Spécifier sur le dessin

- **« Casser les arêtes »** sans valeur laisse place à l’interprétation ; préférez un chanfrein ou rayon maximal (ex. « arêtes cassées 0,2–0,5 mm » si c’est votre exigence).
- Indiquer les faces où **aucune** bavure n’est acceptée (faces d’appui, faces visibles).
- Préciser si l’**oxyde** de coupe doit être retiré (peinture, soudure).

## Liste de vérification avant expédition

- [ ] Aucune scorie détachable au toucher
- [ ] Arêtes conformes au dessin (rayon/chanfrein)
- [ ] Faces visibles sans rayures d’ébavurage si exigé
- [ ] Oxyde retiré si la pièce va en peinture
- [ ] Pièces inox manipulées avec outils dédiés

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Poncer des scories lourdes | Abrasifs usés en minutes, pièces chauffées |
| Mêmes brosses pour acier et inox | Contamination, rouille sur l’inox |
| Ne pas chiffrer l’ébavurage | Marge perdue sur le travail |
| Arrondir trop les arêtes de pièces de précision | Cotes fonctionnelles hors tolérance |

## FAQ

### La tribofinition convient-elle aux grandes pièces ?
Elle convient surtout aux petites pièces en vrac ; les grandes tôles passent mieux sur machine à large bande ou à la main.

### Faut-il ébavurer les pièces destinées à la peinture en poudre ?
Oui en général : la poudre se retire des arêtes vives (effet de bord) et l’oxyde peut nuire à l’adhérence. Vérifiez avec votre peintre.

## À valider en atelier (Michaël)

- Votre équipement et vos temps d’ébavurage types par épaisseur.
- Les exigences d’arête de vos clients.

## Sources

- [Teqram — Sheet metal deburring: methods and process steps](https://teqram.com/en/insights/sheet-metal-deburring/), consulté le 26 novembre 2026.
- [Timesavers — Dross removal machine for sheet metal](https://www.timesaversint.com/knowledge-base/dross-removal-machine/), consulté le 26 novembre 2026.
- [Evotec — Heavy slag removal guide for plasma-cut parts](https://www.evotecgroup.com/newsroom/how-to-remove-heavy-slag-after-plasma-cutting-without-damaging-the-part), consulté le 26 novembre 2026.
=== en
Cutting nearly always leaves something to clean up: **dross** (resolidified metal under the part), a **burr** (small lip), a **sharp edge** that cuts hands and holds paint poorly, and sometimes cutting **oxide** on the edge. Deburring takes time — it must be priced in the quote (see [[quoting]]) and reduced at the source with good cut settings.

## First: reduce it at the source

- Plasma: speed, height and consumables per the chart; see [[plasma-troubleshooting]].
- Laser: nozzle, centering, focus, gas; see [[laser-troubleshooting]].
- A good cut needs only a light pass; a bad cut can cost more to deburr than to cut.

## What to remove and how

| Defect | Common method | Notes |
|---|---|---|
| Heavy dross (plasma, oxyfuel) | Chipping hammer, chisel, impact deslagging station | Finishing equipment makers recommend removing slag **before** grinding so abrasives don’t wear out |
| Fine burr (laser, punching) | Belt sander, wide-belt machine, rotary brushes | One or two passes depending on the machine |
| Sharp edge → broken or rounded edge | Brushes, vibratory finishing, file, edge deburring tool | Specify the radius or chamfer wanted |
| Oxide on the edge (O₂ cut) | Abrasive brushing, grinding | Important before powder coating or welding per the procedure |
| Heat tint on stainless | Pickling/passivation per good practice, dedicated brushing | Stainless-only tools |

## Equipment by volume

| Volume | Typical equipment |
|---|---|
| A few parts | File, grinder with flap disc, handheld belt sander |
| Small batches | Stationary belt sander, edge deburring tool, vibratory finishing |
| Production | Wide-belt machine with brushes (deburring and edge rounding, one or both sides depending on model) |

## Specify it on the drawing

- **“Break edges”** with no value invites interpretation; prefer a maximum chamfer or radius (e.g. “edges broken 0.2–0.5 mm” if that is your requirement).
- Call out faces where **no** burr is acceptable (bearing faces, visible faces).
- State whether cutting **oxide** must be removed (paint, welding).

## Pre-shipping checklist

- [ ] No dross that comes off by hand
- [ ] Edges per the drawing (radius/chamfer)
- [ ] Visible faces free of deburring scratches if required
- [ ] Oxide removed if the part goes to paint
- [ ] Stainless parts handled with dedicated tools

## Common mistakes

| Mistake | Consequence |
|---|---|
| Sanding heavy dross | Abrasives worn in minutes, parts heated |
| Same brushes for steel and stainless | Contamination, rust on stainless |
| Not pricing deburring | Margin lost on the job |
| Over-rounding edges on precision parts | Functional dimensions out of tolerance |

## FAQ

### Is vibratory finishing suitable for large parts?
It suits small parts in bulk; large sheets go better through a wide-belt machine or by hand.

### Should parts going to powder coat be deburred?
Generally yes: powder pulls back from sharp edges (edge effect) and oxide can hurt adhesion. Check with your coater.

## For Michaël to review

- Your equipment and typical deburring times by thickness.
- Your customers’ edge requirements.

## Sources

- [Teqram — Sheet metal deburring: methods and process steps](https://teqram.com/en/insights/sheet-metal-deburring/), consulted November 26, 2026.
- [Timesavers — Dross removal machine for sheet metal](https://www.timesaversint.com/knowledge-base/dross-removal-machine/), consulted November 26, 2026.
- [Evotec — Heavy slag removal guide for plasma-cut parts](https://www.evotecgroup.com/newsroom/how-to-remove-heavy-slag-after-plasma-cutting-without-damaging-the-part), consulted November 26, 2026.
