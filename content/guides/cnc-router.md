---
id: cnc-router
hub: process
order: 4
nav: Routeur CNC | CNC router
kicker: Procédé · usinage | Process · machining
level: debutant
schema: Article
tags: router, cnc router, wood, aluminum, plastics, spoilboard, vacuum table, vectric, ugs, grbl, chip load
related: feeds-speeds, vectric, ugs-grbl, work-offsets
fr_slug: routeur-cnc
en_slug: cnc-router
fr_title: Routeur CNC : bois, plastiques et aluminium, de la fixation au premier fichier
en_title: CNC router: wood, plastics and aluminum, from workholding to the first file
fr_desc: Comment fonctionne un routeur CNC, choisir les fraises, fixer la pièce (table à vide, martyr, brides), régler l’origine, calculer la charge de copeau et éviter les brûlures et les pièces qui bougent.
en_desc: How a CNC router works, choosing bits, holding the work (vacuum table, spoilboard, clamps), setting zero, computing chip load and avoiding burns and moving parts.
---
=== fr
Le routeur CNC est une machine à portique, à broche rapide, conçue pour les grands panneaux : bois, MDF, contreplaqué, plastiques, composites et — avec prudence — aluminium. Il est moins rigide qu’une fraiseuse : on compense par des passes moins engagées et une bonne gestion des copeaux.

## La chaîne type

| Étape | Outils courants |
|---|---|
| Dessin et parcours | Vectric VCarve/Aspire, Fusion, Carbide Create, FreeCAD CAM |
| Envoi du G-code | Commande de la machine, UGS (grbl), Mach4, LinuxCNC |
| Origine et outils | Plaque de touche, palpeur, présetteur |

Voir [Vectric](/guides/vectric-vcarve-aspire/), [UGS et grbl](/guides/ugs-grbl/), [Fusion](/guides/fusion-fao-debuter/).

## Choisir la fraise

| Type | Effet | Quand |
|---|---|---|
| Hélice montante (up-cut) | Évacue les copeaux vers le haut ; arrache un peu le dessus | Rainures profondes, aluminium |
| Hélice descendante (down-cut) | Dessus net ; pousse les copeaux vers le bas | Contreplaqué, mélamine, faibles profondeurs |
| Compression | Dessus et dessous nets | Panneaux plaqués, découpe traversante |
| Simple goujure « O-flute » | Grande évacuation | Plastiques, aluminium |
| Fraise en V | Gravure, V-carving | Lettrage, chanfreins |

## Fixer la pièce

1. **Table martyre (spoilboard)** surfacée pour être parallèle aux axes.
2. **Table à vide** pour les panneaux : efficace sur les grandes pièces, moins sur les petites qui se détachent en fin de coupe.
3. **Brides, vis, ruban double face** pour les pièces isolées — loin de la trajectoire.
4. **Attaches (tabs)** dans le FAO pour retenir les pièces jusqu’à la fin.

> [!WARN] Une pièce qui se libère en fin de coupe peut être projetée. Attaches, ordre de coupe et lunettes, toujours.

## Charge de copeau et brûlures

Les fabricants de fraises (Onsrud, Amana, Harvey…) donnent une **charge de copeau** par diamètre et matière. Avance = tr/min × nombre de goujures × charge de copeau ([formules](/guides/avances-vitesses/)). Des brûlures sur le bois signalent presque toujours une avance trop **lente** pour le régime, ou une fraise émoussée — pas une avance trop rapide.

## Aluminium au routeur

Possible avec : fraise 1 ou 2 goujures pour l’aluminium, faible profondeur ou engagement réduit (parcours adaptatif), lubrification par brouillard ou air, et une machine rigide. Commencez prudemment et écoutez.

## Erreurs fréquentes

- Origine Z prise sur le dessus d’une pièce d’épaisseur variable, pour une coupe traversante (préférer le dessus du martyr, `G55` par exemple).
- Coins intérieurs vifs dessinés alors que la fraise laisse son rayon — voir [DXF](/guides/dxf-bonnes-pratiques/).
- Pas d’attaches : pièces qui bougent et se font entamer.
- Poussière fine sans captation : santé et risque d’incendie.

## Liste de vérification

- [ ] Table martyre surfacée et parallèle aux axes
- [ ] Fraise adaptée (montante, descendante, compression, O-flute, V) à la matière et à la coupe
- [ ] Avance calculée à partir de la charge de copeau du fabricant de fraise
- [ ] Pièce tenue (vide, brides, vis, ruban) loin de la trajectoire ; attaches dans le FAO
- [ ] Origine Z prise au bon endroit (dessus du martyr pour une coupe traversante)
- [ ] Captation de poussière en marche
- [ ] Lunettes de protection

## FAQ

### Un routeur peut-il couper de l’acier ?
Pas comme mode de travail normal. Pour l’acier, voyez plasma, laser, jet d’eau ou fraiseuse.

### Table à vide ou brides ?
Table à vide pour les panneaux répétitifs ; brides pour les pièces uniques et épaisses. Beaucoup d’ateliers combinent les deux.

## Sources

- [Vectric — VCarve](https://www.vectric.com/products/vcarve/), consulté le 26 novembre 2026.
- [Harvey Performance — Chip thinning](https://www.harveyperformance.com/in-the-loupe/combat-chip-thinning/).
- [grbl — Wiki](https://github.com/gnea/grbl/wiki).
=== en
A CNC router is a gantry machine with a fast spindle, built for large panels: wood, MDF, plywood, plastics, composites and — carefully — aluminum. It is less rigid than a mill: you compensate with lighter engagement and good chip control.

## The typical chain

| Step | Common tools |
|---|---|
| Drawing and toolpaths | Vectric VCarve/Aspire, Fusion, Carbide Create, FreeCAD CAM |
| Sending G-code | The machine’s control, UGS (grbl), Mach4, LinuxCNC |
| Zero and tools | Touch plate, probe, tool setter |

See [Vectric](/en/guides/vectric-vcarve-aspire/), [UGS and grbl](/en/guides/ugs-grbl/), [Fusion](/en/guides/fusion-cam-getting-started/).

## Choosing the bit

| Type | Effect | When |
|---|---|---|
| Up-cut spiral | Lifts chips out; slightly tears the top | Deep slots, aluminum |
| Down-cut spiral | Clean top; pushes chips down | Plywood, melamine, shallow cuts |
| Compression | Clean top and bottom | Veneered panels, through cuts |
| Single “O-flute” | Big chip evacuation | Plastics, aluminum |
| V-bit | Engraving, V-carving | Lettering, chamfers |

## Holding the work

1. **Spoilboard** surfaced parallel to the axes.
2. **Vacuum table** for panels: effective on large parts, less on small parts that break free at the end.
3. **Clamps, screws, double-sided tape** for single parts — away from the path.
4. **Tabs** in CAM to hold parts until the end.

> [!WARN] A part that breaks free at the end of a cut can be thrown. Tabs, cut order and safety glasses, always.

## Chip load and burning

Bit makers (Onsrud, Amana, Harvey…) give a **chip load** by diameter and material. Feed = rpm × flutes × chip load ([formulas](/en/guides/feeds-and-speeds/)). Burn marks on wood almost always mean a feed too **slow** for the rpm, or a dull bit — not too fast a feed.

## Aluminum on a router

Possible with: a 1- or 2-flute aluminum bit, shallow depth or reduced engagement (adaptive path), mist or air, and a rigid machine. Start conservatively and listen.

## Common mistakes

- Z zero on top of a part of varying thickness for a through cut (prefer the spoilboard top, `G55` for example).
- Sharp inside corners drawn while the bit leaves its radius — see [DXF](/en/guides/dxf-best-practices/).
- No tabs: parts move and get gouged.
- Fine dust without collection: health and fire risk.

## Checklist

- [ ] Spoilboard surfaced and parallel to the axes
- [ ] Bit suited (up-cut, down-cut, compression, O-flute, V) to the material and cut
- [ ] Feed calculated from the bit maker’s chip load
- [ ] Part held (vacuum, clamps, screws, tape) away from the toolpath; tabs in CAM
- [ ] Z zero set in the right place (top of spoilboard for through cuts)
- [ ] Dust collection running
- [ ] Safety glasses

## FAQ

### Can a router cut steel?
Not as a normal mode of work. For steel, look at plasma, laser, waterjet or a mill.

### Vacuum table or clamps?
Vacuum for repetitive panels; clamps for one-off thick parts. Many shops combine both.

## Sources

- [Vectric — VCarve](https://www.vectric.com/products/vcarve/), consulted November 26, 2026.
- [Harvey Performance — Chip thinning](https://www.harveyperformance.com/in-the-loupe/combat-chip-thinning/).
- [grbl — Wiki](https://github.com/gnea/grbl/wiki).
