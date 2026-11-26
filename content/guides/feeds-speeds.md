---
id: feeds-speeds
hub: fundamentals
order: 4
nav: Avances et vitesses | Feeds and speeds
kicker: Fondamentaux · usinage | Fundamentals · machining
level: intermediaire
schema: HowTo
tags: feeds, speeds, rpm, chip load, sfm, chip thinning, mill, router, lathe, aluminum, steel, stainless
related: cnc-mill, cnc-router, milling-troubleshooting, materials-grades
prices: yes
fr_slug: avances-vitesses
en_slug: feeds-and-speeds
fr_title: Avances et vitesses : les formules, la méthode, et d’où viennent les chiffres
en_title: Feeds and speeds: the formulas, the method, and where the numbers come from
fr_desc: Vitesse de coupe, tr/min, avance par dent, amincissement des copeaux, débit de copeaux : les formules exactes en métrique et en impérial, et comment partir des données du fabricant d’outils.
en_desc: Cutting speed, RPM, chip load, chip thinning, removal rate: the exact formulas in metric and imperial, and how to start from the tool maker’s data.
---
=== fr
Les « bonnes » avances et vitesses ne sont pas dans un tableau universel : elles dépendent de l’outil (diamètre, nombre de dents, revêtement, matière), de la matière usinée, de la rigidité de la machine et de l’engagement. Ce guide donne les **formules exactes** et une **méthode** ; les valeurs de départ viennent toujours de la fiche du **fabricant de l’outil**.

## Les grandeurs

| Symbole | Grandeur | Unités |
|---|---|---|
| Vc (ou SFM) | Vitesse de coupe à la périphérie de l’outil | m/min (ou pi/min) |
| n | Vitesse de broche | tr/min |
| D | Diamètre de l’outil (fraisage) ou de la pièce (tournage) | mm (ou po) |
| z | Nombre de dents (goujures) | — |
| fz | Avance par dent (charge de copeau) | mm/dent (ou po/dent) |
| vf | Avance de table | mm/min (ou po/min) |
| ap / ae | Profondeur axiale / engagement radial | mm |

## Les formules

| Calcul | Métrique | Impérial |
|---|---|---|
| Vitesse de broche | n = (Vc × 1000) / (π × D) | n = (SFM × 12) / (π × D) ≈ 3,82 × SFM / D |
| Avance de table (fraisage) | vf = n × z × fz | vf = n × z × fz |
| Avance (tournage) | vf = n × fn (fn en mm/tr) | vf = n × fn (po/tr) |
| Débit de copeaux (fraisage) | Q = ap × ae × vf / 1000 (cm³/min) | Q = ap × ae × vf (po³/min) |

## L’amincissement des copeaux

Quand l’engagement radial ae est **inférieur à la moitié du diamètre**, le copeau réel est plus mince que fz. Pour une fraise à épaulement droit :

épaisseur max ≈ fz × 2 × √( (ae/D) × (1 − ae/D) )

Pour garder l’épaisseur de copeau visée, on **augmente fz** en conséquence. C’est le principe des parcours à engagement constant (Dynamic Motion dans Mastercam, Adaptive dans Fusion) : faible ae, grande ap, fz augmentée.

> [!TIP] Un copeau trop mince frotte au lieu de couper : chaleur, usure rapide, écrouissage de l’inox. Si l’outil chauffe sans raison, vérifiez d’abord que l’épaisseur réelle de copeau n’est pas trop faible.

## La méthode, pas à pas

1. **Trouver la fiche** du fabricant de l’outil pour la matière (groupe ISO P acier, M inox, K fonte, N aluminium…) : elle donne Vc et fz de départ selon le diamètre.
2. **Calculer n** avec la formule ; plafonner au maximum de la broche. Si n est plafonné, recalculer Vc réelle.
3. **Calculer vf** = n × z × fz, corrigé pour l’amincissement si ae < D/2.
4. **Vérifier la machine** : puissance et couple de broche à ce régime, avance maximale, rigidité (petite machine = engagement réduit, pas avance réduite à l’aveugle).
5. **Commencer prudemment** : par exemple à une fraction des valeurs du catalogue sur une machine légère, puis monter en écoutant et en regardant les copeaux.
6. **Lire les copeaux** : couleur, forme, son. Noter les valeurs qui marchent dans votre bibliothèque d’outils FAO.

## Exemple de calcul (valeurs hypothétiques)

Supposons qu’une fiche d’outil donne, pour une fraise carbure 3 dents de 10 mm dans un alliage d’aluminium, Vc = 300 m/min et fz = 0,05 mm/dent (ce sont des chiffres d’exemple, **pas** une recommandation) :

- n = 300 × 1000 / (π × 10) ≈ 9 549 tr/min
- vf = 9 549 × 3 × 0,05 ≈ 1 432 mm/min
- À ae = 1 mm (10 % du diamètre) : facteur d’amincissement = 2 × √(0,1 × 0,9) = 0,6 → pour garder 0,05 mm d’épaisseur réelle, fz ≈ 0,05 / 0,6 ≈ 0,083 mm/dent, soit vf ≈ 2 387 mm/min.

## Routeur CNC

Sur un routeur, la broche tourne vite et la machine est moins rigide : on raisonne surtout en **charge de copeau** (fz), à partir des tableaux du fabricant de la fraise (Onsrud, Amana, Harvey…). Trop lent pour le régime donne de la poussière et de la chaleur, pas une coupe « plus douce ».

## Erreurs fréquentes

- Réduire l’avance sans réduire le régime : copeau trop mince, frottement, usure.
- Oublier l’amincissement en parcours adaptatif : outil qui « danse » sous sa charge réelle de conception.
- Confondre avance par dent et avance par tour.
- Appliquer une Vc d’outil carbure à un outil HSS (ou l’inverse).

## FAQ

### Où trouver des données fiables gratuitement ?
Les catalogues et calculateurs des fabricants d’outils (Sandvik Coromant, Kennametal, Harvey Tool, Iscar…). Ce sont des points de départ pour des machines rigides : adaptez à la vôtre.

### Et pour le plasma ou le laser ?
Ce ne sont pas des « avances et vitesses » d’outil coupant : la vitesse de coupe vient de la charte du fabricant de la source. Voir [Kerf et qualité de coupe](/guides/kerf-qualite-coupe/).

## À valider en atelier (Michaël)

- Une ou deux combinaisons outil-matière éprouvées à donner en exemple, avec la machine.
- Les marques d’outils réellement achetées au Québec.

## Sources

- [Sandvik Coromant — Milling formulas and definitions](https://www.sandvik.coromant.com/en-us/knowledge/machining-formulas-definitions/milling-formulas-definitions), consulté le 26 novembre 2026.
- [Sandvik Coromant — Turning formulas and definitions](https://www.sandvik.coromant.com/en-us/knowledge/machining-formulas-definitions/turning-formulas-definitions).
- [Harvey Performance — Chip thinning](https://www.harveyperformance.com/in-the-loupe/combat-chip-thinning/).
=== en
The “right” feeds and speeds are not in a universal table: they depend on the tool (diameter, flutes, coating, substrate), the workpiece material, machine rigidity and engagement. This guide gives the **exact formulas** and a **method**; starting values always come from the **tool maker’s** data.

## The quantities

| Symbol | Quantity | Units |
|---|---|---|
| Vc (or SFM) | Cutting speed at the tool periphery | m/min (or ft/min) |
| n | Spindle speed | rpm |
| D | Tool diameter (milling) or part diameter (turning) | mm (or in) |
| z | Number of flutes | — |
| fz | Feed per tooth (chip load) | mm/tooth (or in/tooth) |
| vf | Table feed | mm/min (or in/min) |
| ap / ae | Axial depth / radial engagement | mm |

## The formulas

| Calculation | Metric | Imperial |
|---|---|---|
| Spindle speed | n = (Vc × 1000) / (π × D) | n = (SFM × 12) / (π × D) ≈ 3.82 × SFM / D |
| Table feed (milling) | vf = n × z × fz | vf = n × z × fz |
| Feed (turning) | vf = n × fn (fn in mm/rev) | vf = n × fn (in/rev) |
| Removal rate (milling) | Q = ap × ae × vf / 1000 (cm³/min) | Q = ap × ae × vf (in³/min) |

## Chip thinning

When radial engagement ae is **less than half the diameter**, the real chip is thinner than fz. For a square-shoulder end mill:

max chip thickness ≈ fz × 2 × √( (ae/D) × (1 − ae/D) )

To keep the target chip thickness, **increase fz** accordingly. That is the principle behind constant-engagement toolpaths (Dynamic Motion in Mastercam, Adaptive in Fusion): low ae, deep ap, higher fz.

> [!TIP] A chip that is too thin rubs instead of cutting: heat, fast wear, work-hardened stainless. If a tool runs hot for no reason, first check the real chip thickness is not too low.

## The method, step by step

1. **Find the tool maker’s data** for the material (ISO group P steel, M stainless, K cast iron, N aluminum…): it gives starting Vc and fz by diameter.
2. **Compute n** with the formula; cap at spindle max. If n is capped, recompute the real Vc.
3. **Compute vf** = n × z × fz, corrected for chip thinning when ae < D/2.
4. **Check the machine**: spindle power and torque at that speed, max feed, rigidity (small machine = less engagement, not blindly less feed).
5. **Start conservatively**: for example a fraction of catalogue values on a light machine, then step up while listening and watching chips.
6. **Read the chips**: colour, shape, sound. Save what works in your CAM tool library.

## Worked example (hypothetical values)

Suppose a tool sheet gives, for a 10 mm 3-flute carbide end mill in an aluminum alloy, Vc = 300 m/min and fz = 0.05 mm/tooth (example numbers, **not** a recommendation):

- n = 300 × 1000 / (π × 10) ≈ 9,549 rpm
- vf = 9,549 × 3 × 0.05 ≈ 1,432 mm/min
- At ae = 1 mm (10% of diameter): thinning factor = 2 × √(0.1 × 0.9) = 0.6 → to keep a real 0.05 mm chip, fz ≈ 0.05 / 0.6 ≈ 0.083 mm/tooth, so vf ≈ 2,387 mm/min.

## CNC router

On a router the spindle is fast and the machine less rigid: think mainly in **chip load** (fz), from the bit maker’s charts (Onsrud, Amana, Harvey…). Too slow a feed for the rpm makes dust and heat, not a “gentler” cut.

## Common mistakes

- Lowering feed without lowering rpm: chip too thin, rubbing, wear.
- Ignoring chip thinning in adaptive paths: the tool runs well below its design load.
- Confusing feed per tooth with feed per revolution.
- Applying a carbide Vc to an HSS tool (or vice versa).

## FAQ

### Where can I find reliable data for free?
Tool makers’ catalogues and calculators (Sandvik Coromant, Kennametal, Harvey Tool, Iscar…). They are starting points for rigid machines: adapt to yours.

### What about plasma or laser?
Those are not cutting-tool feeds and speeds: cut speed comes from the power source maker’s chart. See [Kerf and cut quality](/en/guides/kerf-and-cut-quality/).

## For Michaël to review

- One or two proven tool–material combinations to give as examples, with the machine.
- Tool brands actually bought in Quebec.

## Sources

- [Sandvik Coromant — Milling formulas and definitions](https://www.sandvik.coromant.com/en-us/knowledge/machining-formulas-definitions/milling-formulas-definitions), consulted November 26, 2026.
- [Sandvik Coromant — Turning formulas and definitions](https://www.sandvik.coromant.com/en-us/knowledge/machining-formulas-definitions/turning-formulas-definitions).
- [Harvey Performance — Chip thinning](https://www.harveyperformance.com/in-the-loupe/combat-chip-thinning/).
