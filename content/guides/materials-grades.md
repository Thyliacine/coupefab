---
id: materials-grades
hub: materials
order: 40
nav: Grades de métaux | Metal grades
kicker: Fondamentaux · matériaux | Fundamentals · materials
level: debutant
schema: Article
tags: materials, grades, a36, 44w, 1018, 4140, 304, 316, 5052, 6061, c110, c360, c932, stainless, aluminum, steel
related: feeds-speeds, plasma-cutting, bend-allowance, nesting
prices: yes
fr_slug: nuances-metaux
en_slug: metal-grades
fr_title: Grades et alliages de métaux en atelier : acier, inox, aluminium, cuivre, laiton, bronze
en_title: Metal grades in the shop: steel, stainless, aluminum, copper, brass, bronze
fr_desc: A36, 44W, 1018, 4140, A500, 304, 316, 17-4PH, 5052, 6061, C110, C360, C932 : à quoi sert chaque grade, comment il se coupe, se plie, se soude et s’usine, avec lien vers les prix publiés.
en_desc: A36, 44W, 1018, 4140, A500, 304, 316, 17-4PH, 5052, 6061, C110, C360, C932: what each grade is for, how it cuts, bends, welds and machines, linked to published prices.
---
=== fr
Ce guide suit le catalogue d’un atelier québécois réel (celui que suit notre [comparateur de prix](/prix/)) : aciers au carbone et alliés, aciers de construction, inox, aluminium et alliages cuivreux. Les propriétés mécaniques exactes viennent des normes (ASTM, CSA, AA) et des certificats d’usine (*mill certs*) ; ici, on parle d’usage et de comportement en atelier.

> [!NOTE]
> **« Grade », c’est quoi ?** C’est le nom précis du métal commandé : A36 ou 44W pour l’acier de construction, 304 ou 316 pour l’inox, 5052 ou 6061 pour l’aluminium. Pour l’aluminium et le cuivre, on dit aussi **alliage**. Les normes françaises écrivent « nuance » ; en atelier au Québec, on dit « grade ». C’est la même chose.

## Aciers de construction (profilés, plaques, tubes)

| Grade | Norme | Où on le voit | En atelier |
|---|---|---|---|
| A36 | ASTM A36 | Plaque, profilés, barres plates | Le « acier doux » de référence : soudable, se coupe bien au plasma et à l’oxycoupage |
| 44W / 50W | CSA G40.21 | Plaque et profilés au Canada | Le chiffre est la limite élastique minimale en ksi (44 ou 50) ; grade canadien courant en charpente |
| A500 gr. B / C | ASTM A500 | Tubes structuraux (HSS) carrés, rectangulaires, ronds | Formé à froid, soudé ; gr. C plus résistant |
| A53 / A106 | ASTM A53, A106 | Tuyau | A106 pour service haute température ; souvent vendu au tuyau, pas à la tôle |
| A513 / A519 | ASTM A513, A519 | Tube mécanique (DOM, sans soudure) | Tolérances plus serrées que le structural |

## Aciers au carbone et alliés (barres, usinage)

| Grade | Caractère | Usage typique |
|---|---|---|
| 1018 / 1020 | Bas carbone, usinable, soudable | Pièces usinées générales, gabarits ; « CR » = laminé à froid (fini et tolérance meilleurs), « HR » = laminé à chaud |
| 1045 | Carbone moyen | Arbres, pièces plus résistantes ; trempe possible |
| 12L14 | Au plomb, décolletage | Usinabilité élevée, mauvaise soudabilité |
| 4130 / 4140 / 4340 | Chrome-molybdène (et nickel pour 4340) | Pièces fortement sollicitées ; « HT » = prétraité (traité thermiquement) |
| O1 | Acier à outils trempant à l’huile | Outillage, poinçons, lames |

> [!WARN] Souder du 4140 ou du 1045 demande en général préchauffage et procédure adaptée ; le 12L14 se soude mal. Suivez une procédure qualifiée (CSA W47.1 / W59 au Canada pour les structures).

## Inox

| Grade | Famille | En atelier |
|---|---|---|
| 304 / 304L | Austénitique 18-8 | La plus courante ; « L » = bas carbone, meilleure après soudage ; s’écrouit à l’usinage |
| 316 / 316L | Austénitique au molybdène | Meilleure résistance aux chlorures (milieu marin, alimentaire, chimique) |
| 303 | Austénitique au soufre | Version « décolletage » du 304 ; soudabilité réduite |
| 410 / 416 | Martensitique | Trempable, magnétique ; 416 = version usinable |
| 17-4PH | À durcissement structural | Haute résistance ; l’état (H900, H1150…) change dureté et ténacité |
| Inconel 600 | Alliage de nickel | Haute température ; coûteux et difficile à usiner |

Au plasma, l’inox se coupe idéalement avec les gaz et consommables prévus par le fabricant de la source ; à l’air, la face coupée s’oxyde. Les fumées de découpe et de soudage d’inox contiennent du chrome : voir [Sécurité](/guides/securite-cnc-cnesst/).

## Aluminium

| Grade | Caractère | Usage typique |
|---|---|---|
| 3003 | Non traitable, très formable | Tôlerie légère, carters, réservoirs simples |
| 5052 (souvent H32) | Non traitable, bonne résistance à la corrosion | **Le** grade de tôle pliée : se plie bien, se soude bien |
| 6061 (souvent T6) | Traitable thermiquement | Plaques et barres usinées, structure ; se plie mal à rayon serré à l’état T6 |
| 6063 | Traitable, extrusion | Profilés architecturaux |

> [!TIP] Pour une pièce pliée, 5052-H32 est le choix par défaut ; pour une pièce usinée, 6061-T6. Plier du 6061-T6 à petit rayon finit souvent par une fissure sur l’extérieur du pli.

## Cuivre, laiton, bronze

| Grade | Nom courant | En atelier |
|---|---|---|
| C110 | Cuivre ETP | Conducteur électrique (barres omnibus) ; gommeux à l’usinage ; réfléchit fortement le laser |
| C360 | Laiton de décolletage | Référence d’usinabilité ; raccords, pièces tournées |
| C932 | Bronze SAE 660 | Coussinets et bagues |
| C954 | Bronze d’aluminium | Coussinets fortement chargés, résistance à l’usure |

## Comment choisir

1. **Fonction** : charge, corrosion, température, conductivité.
2. **Procédé** : pliage (5052 plutôt que 6061-T6), soudage (304L plutôt que 303), usinage (12L14, C360).
3. **Disponibilité et prix** : comparez dans le [comparateur](/prix/) — tôle, plaque, barre et tube.
4. **Certificat** : demandez le certificat d’usine si la pièce est structurale ou réglementée.

## FAQ

### A36 ou 44W ?
Les deux sont des aciers de construction courants ; 44W est le grade CSA canadien, A36 le grade ASTM. Beaucoup de produits sont certifiés aux deux (double certification) : vérifiez le certificat.

### Pourquoi l’inox « colle » à l’usinage ?
Les austénitiques (304, 316) s’écrouissent : un outil qui frotte durcit la surface. Copeau suffisant, outil affûté, pas d’arrêt en pleine coupe. Voir [Avances et vitesses](/guides/avances-vitesses/).

## À valider en atelier (Michaël)

- Les grades les plus demandés dans votre atelier et vos remarques d’usage.
- Les doubles certifications courantes chez vos fournisseurs.

## Sources

- [ASTM A36 — Carbon structural steel](https://www.astm.org/a0036_a0036m-19.html), consulté le 26 novembre 2026.
- [ASTM A500 — Cold-formed structural tubing](https://www.astm.org/a0500_a0500m-23.html).
- [CSA G40.20/G40.21 — Structural quality steel](https://www.csagroup.org/store/product/G40.20-13-G40.21-13/).
- [The Aluminum Association — Alloy and temper system](https://www.aluminum.org/).
- [Copper Development Association — Alloy data](https://www.copper.org/resources/properties/).
=== en
This guide follows the catalogue of a real Quebec shop (the one our [price tool](/en/sheet-prices/) tracks): carbon and alloy steels, structural steels, stainless, aluminum and copper alloys. Exact mechanical properties come from the standards (ASTM, CSA, AA) and mill certs; here we talk about use and shop behaviour.

## Structural steels (shapes, plate, tube)

| Grade | Standard | Where you see it | In the shop |
|---|---|---|---|
| A36 | ASTM A36 | Plate, shapes, flat bar | The reference “mild steel”: weldable, cuts well with plasma and oxy-fuel |
| 44W / 50W | CSA G40.21 | Plate and shapes in Canada | The number is the minimum yield in ksi (44 or 50); a common Canadian structural grade |
| A500 gr. B / C | ASTM A500 | Structural tube (HSS), square, rectangular, round | Cold-formed, welded; gr. C is stronger |
| A53 / A106 | ASTM A53, A106 | Pipe | A106 for high-temperature service; sold as pipe, not sheet |
| A513 / A519 | ASTM A513, A519 | Mechanical tube (DOM, seamless) | Tighter tolerances than structural |

## Carbon and alloy steels (bar, machining)

| Grade | Character | Typical use |
|---|---|---|
| 1018 / 1020 | Low carbon, machinable, weldable | General machined parts, fixtures; “CR” = cold rolled (better finish and tolerance), “HR” = hot rolled |
| 1045 | Medium carbon | Shafts, stronger parts; can be hardened |
| 12L14 | Leaded, free-machining | Very machinable, poor weldability |
| 4130 / 4140 / 4340 | Chrome-moly (plus nickel for 4340) | Highly stressed parts; “HT” = pre-hardened (heat treated) |
| O1 | Oil-hardening tool steel | Tooling, punches, blades |

> [!WARN] Welding 4140 or 1045 generally requires preheat and a suitable procedure; 12L14 welds poorly. Follow a qualified procedure (CSA W47.1 / W59 in Canada for structures).

## Stainless

| Grade | Family | In the shop |
|---|---|---|
| 304 / 304L | Austenitic 18-8 | The most common; “L” = low carbon, better after welding; work-hardens when machined |
| 316 / 316L | Austenitic with molybdenum | Better chloride resistance (marine, food, chemical) |
| 303 | Austenitic with sulphur | Free-machining 304; reduced weldability |
| 410 / 416 | Martensitic | Hardenable, magnetic; 416 = free-machining |
| 17-4PH | Precipitation hardening | High strength; condition (H900, H1150…) changes hardness and toughness |
| Inconel 600 | Nickel alloy | High temperature; costly and hard to machine |

On plasma, stainless is best cut with the gases and consumables the power source maker specifies; on air, the cut face oxidizes. Stainless cutting and welding fumes contain chromium: see [Safety](/en/guides/cnc-shop-safety/).

## Aluminum

| Grade | Character | Typical use |
|---|---|---|
| 3003 | Non-heat-treatable, very formable | Light sheet work, covers, simple tanks |
| 5052 (often H32) | Non-heat-treatable, good corrosion resistance | **The** bent-sheet grade: bends well, welds well |
| 6061 (often T6) | Heat-treatable | Machined plate and bar, structure; bends poorly at tight radii in T6 |
| 6063 | Heat-treatable, extrusion | Architectural extrusions |

> [!TIP] For a bent part, 5052-H32 is the default; for a machined part, 6061-T6. Bending 6061-T6 at a tight radius often ends with a crack on the outside of the bend.

## Copper, brass, bronze

| Grade | Common name | In the shop |
|---|---|---|
| C110 | ETP copper | Electrical conductor (bus bar); gummy to machine; strongly reflects laser |
| C360 | Free-cutting brass | The machinability benchmark; fittings, turned parts |
| C932 | SAE 660 bearing bronze | Bushings and bearings |
| C954 | Aluminum bronze | Heavily loaded bushings, wear resistance |

## How to choose

1. **Function**: load, corrosion, temperature, conductivity.
2. **Process**: bending (5052 over 6061-T6), welding (304L over 303), machining (12L14, C360).
3. **Availability and price**: compare in the [price tool](/en/sheet-prices/) — sheet, plate, bar and tube.
4. **Certification**: ask for the mill cert if the part is structural or regulated.

## FAQ

### A36 or 44W?
Both are common structural steels; 44W is the Canadian CSA grade, A36 the ASTM grade. Many products are dual-certified: check the cert.

### Why does stainless “stick” when machining?
Austenitics (304, 316) work-harden: a rubbing tool hardens the surface. Enough chip, a sharp tool, no dwelling mid-cut. See [Feeds and speeds](/en/guides/feeds-and-speeds/).

## For Michaël to review

- The grades most requested in your shop and your usage notes.
- Common dual certifications at your suppliers.

## Sources

- [ASTM A36 — Carbon structural steel](https://www.astm.org/a0036_a0036m-19.html), consulted November 26, 2026.
- [ASTM A500 — Cold-formed structural tubing](https://www.astm.org/a0500_a0500m-23.html).
- [CSA G40.20/G40.21 — Structural quality steel](https://www.csagroup.org/store/product/G40.20-13-G40.21-13/).
- [The Aluminum Association — Alloy and temper system](https://www.aluminum.org/).
- [Copper Development Association — Alloy data](https://www.copper.org/resources/properties/).
