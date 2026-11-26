---
id: router-tearout
hub: troubleshooting
order: 40
nav: Arrachements au routeur | Router tear-out
kicker: Dépannage · routeur | Troubleshooting · router
level: debutant
schema: HowTo
tags: router, routeur, tear-out, arrachement, éclats, plywood, contreplaqué, mélamine, laminate, upcut, downcut, compression bit, fraise à compression, ramp, rampe, chip load, mdf, fuzzing
related: cnc-router, feeds-speeds, vectric, milling-troubleshooting
fr_slug: routeur-arrachements-eclats
en_slug: router-tear-out-chipping
fr_title: Routeur CNC : éliminer les arrachements et les éclats dans le contreplaqué et la mélamine
en_title: CNC router: eliminating tear-out and chipping in plywood and melamine
fr_desc: Choisir entre fraise montante, descendante et à compression, régler la première passe d’une fraise à compression, entrer en rampe, et diagnostiquer les éclats en dessus ou en dessous du panneau.
en_desc: Choosing between upcut, downcut and compression bits, setting a compression bit’s first pass, ramping in, and diagnosing chipping on the top or bottom face of the sheet.
---
=== fr
Les **arrachements** (éclats de placage, fibres soulevées) au routeur viennent surtout du **sens de l’hélice** de la fraise par rapport à la face visible, puis de l’usure et des conditions de coupe. La bonne nouvelle : la plupart se règlent en choisissant la bonne géométrie et en l’utilisant correctement.

## Montante, descendante ou compression

| Géométrie | Effet | Bon pour | Attention |
|---|---|---|---|
| **Montante** (*upcut*) | Remonte les copeaux, bonne évacuation | Bois tendres et durs, plastiques, mousses ; rainures profondes | Peut arracher la face du dessus et soulever la pièce si le vacuum est faible |
| **Descendante** (*downcut*) | Pousse vers le bas, dessus net, pièce plaquée | Bois tendres, composites (MDF, contreplaqué plaqué, aggloméré) ; poches peu profondes | Copeaux recompactés dans la coupe, chaleur |
| **Compression** | Montante au bout, descendante au-dessus : les deux faces sont comprimées vers le centre | Panneaux plaqués ou mélaminés des deux côtés, découpe traversante | Inutile si la passe est moins profonde que la partie montante |

## La règle de la fraise à compression

La **première passe doit être plus profonde que la partie montante** de la fraise (souvent environ 6 mm, soit ¼ po, selon le modèle : vérifiez la fiche du fabricant). Sinon, seule la partie montante travaille sur le dessus, qui s’arrache comme avec une fraise montante. Idéalement, découpez en une seule passe pleine profondeur quand la machine et le serrage le permettent.

> [!TIP] Entrez **en rampe** plutôt qu’en plongée verticale avec une fraise descendante ou à compression : en plongée, les copeaux se tassent sous l’outil et la chaleur abîme l’arête et la pièce.

## Diagnostic rapide

| Symptôme | Cause probable | Correctif |
|---|---|---|
| Éclats sur le **dessus** | Fraise montante, ou compression trop peu profonde | Descendante ou compression, première passe plus profonde que la partie montante |
| Éclats sur le **dessous** | Fraise descendante en sortie de panneau | Compression ou montante ; martyr en bon état |
| Bords « poilus » partout | Arête usée, avance par dent trop faible (frottement) | Outil neuf ; augmenter l’avance ou réduire la vitesse (voir [[feeds-speeds]]) |
| Bords brûlés | Copeaux recompactés, avance trop lente | Rampe, meilleure aspiration, avance plus forte |
| Pièces qui bougent | Fraise montante + vacuum faible | Descendante/compression, onglets, ruban ou vis |

## Liste de vérification

- [ ] Géométrie adaptée au matériau et à la face visible
- [ ] Longueur de la partie montante connue (fiche du fabricant)
- [ ] Première passe plus profonde que cette longueur
- [ ] Entrées en rampe ; aspiration active
- [ ] Martyr plat et en bon état

## Erreurs fréquentes

- Faire des poches peu profondes à la fraise à compression : utilisez une descendante.
- Baisser l’avance « pour un meilleur fini » : la fraise frotte, chauffe et s’use plus vite.
- Garder une fraise usée sur de la mélamine, qui pardonne peu.

## FAQ

### Compression pour le MDF ?
Possible, mais le MDF est très abrasif : beaucoup d’ateliers gardent une fraise montante pour le MDF brut et réservent la compression aux panneaux plaqués ou mélaminés.

### Pourquoi ma fraise à compression arrache-t-elle quand même ?
Presque toujours parce que la passe est moins profonde que la partie montante, ou que l’outil est usé.

## À valider en atelier (Michaël)

- Fraises et avances utilisées chez nous pour la mélamine et le contreplaqué de bouleau.
- Profondeur de première passe retenue selon le modèle de fraise.

## Sources

- [C.R. Onsrud — Finding the Right Tool for the Job on Your CNC Router](https://cronsrud.com/finding-the-right-tool-for-the-job-on-your-cnc-router/) : effets des géométries montante, descendante et compression. Consulté le 26 novembre 2026.
- [AXYZ — How to Use a Compression Bit](https://www.axyz.com/us/en/blog/using-a-compression-bit/) : principe de la compression, entrée en rampe.
- [Popular Woodworking — Compression Bits (CNC Tooling Basics, part 3)](https://www.popularwoodworking.com/techniques/cnc-tooling-basics-for-woodworkers-part-three/) : première passe plus profonde que la partie montante.

=== en
Router **tear-out** (chipped veneer, lifted fibers) comes mostly from the bit’s **helix direction** relative to the visible face, then from wear and cutting conditions. The good news: most of it is fixed by picking the right geometry and using it correctly.

## Upcut, downcut or compression

| Geometry | Effect | Good for | Watch out |
|---|---|---|---|
| **Upcut** | Lifts chips, good evacuation | Soft and hard woods, plastics, foam; deep slots | Can tear the top face and lift the part if vacuum is weak |
| **Downcut** | Pushes down, clean top, part held down | Softwood, composites (MDF, veneered plywood, particleboard); shallow pockets | Chips repacked in the cut, heat |
| **Compression** | Upcut at the tip, downcut above: both faces squeezed toward the middle | Sheets veneered or laminated on both sides, through cuts | Pointless if the pass is shallower than the upcut section |

## The compression-bit rule

The **first pass must be deeper than the bit’s upcut section** (often about 6 mm, or ¼ in, depending on the model: check the maker’s data). Otherwise only the upcut part works on the top face, which tears as with an upcut bit. Ideally cut in one full-depth pass when the machine and hold-down allow.

> [!TIP] **Ramp in** rather than plunging straight down with a downcut or compression bit: when plunging, chips pack under the tool and the heat damages the edge and the part.

## Quick diagnosis

| Symptom | Likely cause | Fix |
|---|---|---|
| Chipping on the **top** | Upcut bit, or compression too shallow | Downcut or compression, first pass deeper than the upcut section |
| Chipping on the **bottom** | Downcut bit breaking through | Compression or upcut; spoilboard in good shape |
| Fuzzy edges everywhere | Worn edge, chip load too low (rubbing) | New tool; raise feed or lower RPM (see [[feeds-speeds]]) |
| Burnt edges | Repacked chips, feed too slow | Ramp, better dust collection, higher feed |
| Parts moving | Upcut + weak vacuum | Downcut/compression, tabs, tape or screws |

## Checklist

- [ ] Geometry suits the material and the visible face
- [ ] Upcut section length known (maker’s data)
- [ ] First pass deeper than that length
- [ ] Ramped entries; dust collection on
- [ ] Spoilboard flat and in good shape

## Common mistakes

- Shallow pocketing with a compression bit: use a downcut.
- Lowering feed “for a better finish”: the bit rubs, heats and wears faster.
- Keeping a worn bit on melamine, which is unforgiving.

## FAQ

### Compression for MDF?
Possible, but MDF is very abrasive: many shops keep an upcut for raw MDF and save compression bits for veneered or melamine sheets.

### Why does my compression bit still tear out?
Almost always because the pass is shallower than the upcut section, or the tool is worn.

## For Michaël to review

- Bits and feeds we use for melamine and birch plywood.
- First-pass depth used per bit model.

## Sources

- [C.R. Onsrud — Finding the Right Tool for the Job on Your CNC Router](https://cronsrud.com/finding-the-right-tool-for-the-job-on-your-cnc-router/): upcut, downcut and compression effects. Consulted November 26, 2026.
- [AXYZ — How to Use a Compression Bit](https://www.axyz.com/us/en/blog/using-a-compression-bit/): compression principle, ramping in.
- [Popular Woodworking — Compression Bits (CNC Tooling Basics, part 3)](https://www.popularwoodworking.com/techniques/cnc-tooling-basics-for-woodworkers-part-three/): first pass deeper than the upcut section.
