---
id: aluminum
hub: materials
order: 20
nav: Aluminium : 5052, 6061, 6063 | Aluminum: 5052, 6061, 6063
kicker: Matériaux · aluminium | Materials · aluminum
level: debutant
schema: Article
prices: yes
tags: aluminum, aluminium, 5052, 6061, 6063, 3003, 7075, t6, t5, h32, temper, extrusion, bending, welding, machining, plasma, laser
related: materials-grades, sheet-gauges, bend-allowance, feeds-speeds
fr_slug: aluminium-5052-6061-6063
en_slug: aluminum-5052-6061-6063
fr_title: Aluminium en atelier : 5052, 6061 et 6063, états (T6, H32) et comment les couper, plier, souder et usiner
en_title: Aluminum in the shop: 5052, 6061 and 6063, tempers (T6, H32) and how to cut, bend, weld and machine them
fr_desc: Quel alliage pour quelle pièce : 5052-H32 pour la tôle pliée, 6061-T6 pour l’usinage et la structure, 6063 pour les profilés. Désignation des états, pliage, soudage, coupe plasma/laser et usinage, avec lien vers les prix publiés.
en_desc: Which grade for which part: 5052-H32 for bent sheet, 6061-T6 for machining and structure, 6063 for extrusions. Temper designations, bending, welding, plasma/laser cutting and machining, linked to published prices.
---
=== fr
L’aluminium d’atelier se résume souvent à trois alliages : **5052** (tôle à plier), **6061** (plaque, barres, usinage, structure) et **6063** (profilés extrudés, architecture). Les choisir correctement évite les fissures au pliage, les pièces trop molles et les surcoûts.

## Lire une désignation : alliage + état

| Partie | Exemple | Signification |
|---|---|---|
| Série | 5xxx | Alliage au magnésium, **non traitable thermiquement** (durci par écrouissage) |
| Série | 6xxx | Alliage magnésium-silicium, **traitable thermiquement** |
| État H | H32 | Écroui puis stabilisé (5052-H32 est l’état de tôle le plus courant) |
| État T | T6 | Mis en solution et vieilli artificiellement (résistance maximale du 6061) |
| État T | T5, T52 | Refroidi à la sortie de la presse puis vieilli (courant pour 6063 extrudé) |
| État O | O | Recuit, le plus mou et le plus formable |

## Comparatif des trois alliages

| Critère | 5052-H32 | 6061-T6 | 6063-T5/T6 |
|---|---|---|---|
| Usage typique | Tôle pliée, boîtiers, réservoirs, marine | Plaque et barre usinées, pièces structurales | Profilés, cadres, architecture, pièces anodisées décoratives |
| Pliage | **Excellent**, rayons serrés possibles | Médiocre en T6 : risque de fissure, rayons généreux ou état O/T4 | Bon pour les profilés selon l’état |
| Soudage | Très bon | Bon, mais **perte de résistance** dans la zone soudée | Bon, même remarque |
| Usinage | Plus « gommeux » | **Très bon** (copeaux nets) | Correct |
| Anodisation | Bonne | Bonne | **Excellente** (aspect décoratif) |
| Résistance | Moyenne | La plus élevée des trois | Moyenne |

Pour les propriétés exactes (limite élastique, allongement), utilisez les fiches techniques des producteurs (Hydro, etc.) et les certificats d’usine.

## Couper l’aluminium

- **Plasma** : fonctionne, avec les chartes aluminium (air ou gaz spécifiques selon la source). Bord moins net que sur l’acier ; voir [[cut-charts]].
- **Laser fibre** : coupe propre à l’**azote** ; matière réfléchissante, suivez les recettes du fabricant. Voir [[laser-troubleshooting]].
- **Jet d’eau** : aucune zone affectée thermiquement ; idéal pour les plaques épaisses ou les pièces sensibles. Voir [[waterjet]].
- **Routeur** : très efficace en tôle et plaque avec des fraises à une ou deux dents pour l’alu ; voir [[cnc-router]].

## Plier l’aluminium

- Le sens du laminage compte : plier **perpendiculairement** au laminage quand c’est possible.
- Le 6061-T6 se plie mal à rayon serré ; demandez du 5052-H32 pour la tôle pliée, ou du 6061 en état plus doux.
- Le K-factor et le retour élastique diffèrent de l’acier ; voir [[bend-allowance]] et [[press-brake]].

## Usiner l’aluminium

- Fraises à 2 ou 3 dents, goujures polies, grandes vitesses : suivez les fiches des fabricants d’outils (voir [[feeds-speeds]]).
- L’ennemi est l’**arête rapportée** (copeau collé) : lubrification ou air comprimé, évacuation des copeaux.
- Le 6061-T6 et le 7075 s’usinent mieux que le 5052 ou les états mous.

## Commander

- [ ] Alliage **et** état (ex. 5052-H32, 6061-T6511 pour barre détendue par étirage)
- [ ] Épaisseur en décimale (les calibres aluminium suivent Brown & Sharpe, voir [[sheet-gauges]])
- [ ] Film protecteur si la face est visible
- [ ] Certificat d’usine si la pièce est structurale
- [ ] Comparer les prix publiés dans le [[prix]]

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Plier du 6061-T6 à rayon serré | Fissures à l’extérieur du pli |
| Utiliser la table de calibres acier | Épaisseur fausse |
| Souder une pièce 6061-T6 « structurale » sans en tenir compte au calcul | Zone soudée moins résistante |
| Mêmes brosses que pour l’acier | Contamination, porosités au soudage |

## FAQ

### 6061 ou 6063 pour un cadre ?
6063 pour les profilés d’apparence (anodisation, formes complexes) ; 6061 si la résistance prime. Les deux existent en tubes et profilés.

### Peut-on tremper le 5052 ?
Non : il ne durcit pas par traitement thermique, seulement par écrouissage (états H).

## À valider en atelier (Michaël)

- Les alliages et états que vous tenez en stock et leurs rayons de pliage minimaux pratiques.

## Sources

- [The Aluminum Association — Alloy and temper designation](https://www.aluminum.org/), consulté le 26 novembre 2026.
- [Hydro — Alloy 6063 data sheet (PDF)](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2026_data_sheet_6063-rev-062026.pdf), consulté le 26 novembre 2026.
- [AES — Aluminum grades for extrusions](https://alum-ext.com/learn/aluminum-grades-for-extrusions/), consulté le 26 novembre 2026.
- [Winston Materials — Aluminum alloy & temper guide](https://www.winstonmaterials.com/resources/aluminum-alloy-temper-guide/), consulté le 26 novembre 2026.
=== en
Shop aluminum often comes down to three grades: **5052** (sheet to bend), **6061** (plate, bar, machining, structure) and **6063** (extrusions, architectural). Choosing correctly avoids cracked bends, parts that are too soft and extra cost.

## Reading a designation: alloy + temper

| Part | Example | Meaning |
|---|---|---|
| Series | 5xxx | Magnesium alloy, **not heat-treatable** (strain-hardened) |
| Series | 6xxx | Magnesium-silicon alloy, **heat-treatable** |
| H temper | H32 | Strain-hardened then stabilized (5052-H32 is the most common sheet temper) |
| T temper | T6 | Solution heat-treated and artificially aged (6061’s strongest temper) |
| T temper | T5, T52 | Cooled from the press then aged (common for extruded 6063) |
| O temper | O | Annealed, softest and most formable |

## The three grades compared

| Criterion | 5052-H32 | 6061-T6 | 6063-T5/T6 |
|---|---|---|---|
| Typical use | Bent sheet, enclosures, tanks, marine | Machined plate and bar, structural parts | Extrusions, frames, architecture, decorative anodized parts |
| Bending | **Excellent**, tight radii possible | Poor in T6: risk of cracking, generous radii or O/T4 temper | Good for extrusions depending on temper |
| Welding | Very good | Good, but **strength loss** in the weld zone | Good, same remark |
| Machining | Gummier | **Very good** (clean chips) | Fair |
| Anodizing | Good | Good | **Excellent** (decorative finish) |
| Strength | Medium | Highest of the three | Medium |

For exact properties (yield, elongation), use producer data sheets (Hydro, etc.) and mill certificates.

## Cutting aluminum

- **Plasma**: works, with aluminum charts (air or specific gases depending on the source). Edge less clean than on steel; see [[cut-charts]].
- **Fiber laser**: clean cut with **nitrogen**; reflective material, follow the manufacturer’s recipes. See [[laser-troubleshooting]].
- **Waterjet**: no heat-affected zone; ideal for thick plate or sensitive parts. See [[waterjet]].
- **Router**: very effective on sheet and plate with single- or two-flute aluminum cutters; see [[cnc-router]].

## Bending aluminum

- Grain direction matters: bend **across** the rolling direction when possible.
- 6061-T6 bends poorly at tight radii; ask for 5052-H32 for bent sheet, or 6061 in a softer temper.
- K-factor and springback differ from steel; see [[bend-allowance]] and [[press-brake]].

## Machining aluminum

- 2- or 3-flute end mills, polished flutes, high speeds: follow tool makers’ data (see [[feeds-speeds]]).
- The enemy is **built-up edge** (welded chip): lubrication or air blast, chip evacuation.
- 6061-T6 and 7075 machine better than 5052 or soft tempers.

## Ordering

- [ ] Grade **and** temper (e.g. 5052-H32, 6061-T6511 for stress-relieved stretched bar)
- [ ] Thickness in decimals (aluminum gauges follow Brown & Sharpe, see [[sheet-gauges]])
- [ ] Protective film if the face is visible
- [ ] Mill certificate if the part is structural
- [ ] Compare published prices in the [[prix]]

## Common mistakes

| Mistake | Consequence |
|---|---|
| Bending 6061-T6 at a tight radius | Cracks on the outside of the bend |
| Using the steel gauge table | Wrong thickness |
| Welding a “structural” 6061-T6 part without accounting for it in design | Weaker weld zone |
| Same brushes as for steel | Contamination, weld porosity |

## FAQ

### 6061 or 6063 for a frame?
6063 for appearance extrusions (anodizing, complex shapes); 6061 if strength comes first. Both come as tube and profiles.

### Can 5052 be heat-treated?
No: it doesn’t harden by heat treatment, only by strain hardening (H tempers).

## For Michaël to review

- The grades and tempers you stock and their practical minimum bend radii.

## Sources

- [The Aluminum Association — Alloy and temper designation](https://www.aluminum.org/), consulted November 26, 2026.
- [Hydro — Alloy 6063 data sheet (PDF)](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2026_data_sheet_6063-rev-062026.pdf), consulted November 26, 2026.
- [AES — Aluminum grades for extrusions](https://alum-ext.com/learn/aluminum-grades-for-extrusions/), consulted November 26, 2026.
- [Winston Materials — Aluminum alloy & temper guide](https://www.winstonmaterials.com/resources/aluminum-alloy-temper-guide/), consulted November 26, 2026.
