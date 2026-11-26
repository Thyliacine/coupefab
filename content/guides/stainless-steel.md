---
id: stainless-steel
hub: materials
order: 15
nav: Inox : 303, 304, 316 | Stainless: 303, 304, 316
kicker: Matériaux · inox | Materials · stainless
level: debutant
schema: Article
prices: yes
tags: stainless, inox, 303, 304, 304l, 316, 316l, 430, austenitic, work hardening, machinability, passivation, 2b, #4, nitrogen, laser, plasma
related: materials-grades, ph-17-4, feeds-speeds, laser-troubleshooting
fr_slug: inox-303-304-316
en_slug: stainless-steel-303-304-316
fr_title: Inox en atelier : 303, 304 et 316, écrouissage, usinage, coupe et finition
en_title: Stainless steel in the shop: 303, 304 and 316, work hardening, machining, cutting and finish
fr_desc: 303 pour l’usinage, 304 pour l’usage général, 316 pour la corrosion : différences, finis de tôle (2B, #4), écrouissage et comment l’éviter, coupe laser à l’azote et plasma, outils dédiés, avec lien vers les prix publiés.
en_desc: 303 for machining, 304 for general use, 316 for corrosion: differences, sheet finishes (2B, #4), work hardening and how to avoid it, nitrogen laser and plasma cutting, dedicated tools, linked to published prices.
---
=== fr
Les inox austénitiques **303, 304 et 316** couvrent la majorité des besoins d’atelier. Ils se ressemblent à l’œil, mais pas à l’usinage ni à la corrosion. Leur grand piège commun : l’**écrouissage** — l’inox durcit sous l’outil s’il frotte au lieu de couper.

## Les trois nuances

| Nuance | Particularité | Usage | En atelier |
|---|---|---|---|
| **303** | Soufre ajouté (inclusions qui fragmentent le copeau) | Pièces usinées en série (barres) | **La plus facile à usiner** des trois ; corrosion et soudabilité moindres ; rarement en tôle |
| **304 / 304L** | Inox « 18-8 » de base ; L = bas carbone pour le soudage | Tôle, tubes, équipements alimentaires, usage général | Usinage plus difficile (gommeux, écrouissable) |
| **316 / 316L** | Molybdène ajouté → meilleure résistance aux chlorures | Marin, chimique, pharmaceutique, salage des routes | Encore un peu plus difficile que le 304 à usiner |
| 430 (ferritique) | Magnétique, sans nickel | Électroménager, décoration | Moins cher, corrosion moindre |

Des fabricants de pièces citent des indices d’usinabilité de l’ordre de 75–80 % pour le 303, environ 45 % pour le 304 et 35–40 % pour le 316 (référence acier de décolletage) : retenez surtout l’**ordre** 303 > 304 > 316.

## Finis de tôle courants

| Fini | Aspect | Usage |
|---|---|---|
| 2B | Laminé à froid, mat-satiné | Usage industriel général |
| #4 (brossé) | Ligné, satiné | Visible : comptoirs, habillages |
| BA | Brillant recuit | Décoratif, réfléchissant |

Commandez le **film protecteur** si la face est visible, et précisez le **sens du brossage** pour les pièces #4.

## Usiner sans écrouir

- Outils **affûtés** à coupe positive, carbure revêtu ; changer avant l’usure avancée.
- **Avance franche et continue** : ne jamais laisser l’outil frotter ou s’arrêter en matière (pas de *dwell*).
- Couper **sous** la couche écrouie de la passe précédente (profondeur suffisante).
- Montage rigide, arrosage abondant ; vitesses modérées selon la fiche de l’outil (voir [[feeds-speeds]]).

## Couper l’inox

- **Laser fibre à l’azote** : bord propre et non oxydé ; un bord bleui signale souvent un gaz contaminé (voir [[laser-troubleshooting]]).
- **Plasma** : chartes inox (air, ou gaz spécifiques selon la source, ex. F5 ou H35 sur certains systèmes) ; voir [[cut-charts]].
- **Pas d’oxycoupage** standard (voir [[oxyfuel]]).

## Éviter la contamination

- Outils, brosses, disques et tables **dédiés à l’inox**, ou protection (film, bois) sur les tables en acier.
- Les particules de fer incrustées rouillent et donnent des taches : nettoyage et **passivation** selon les règles de l’art si nécessaire.

## Liste de vérification de commande

- [ ] Nuance exacte (304 vs 304L, 316 vs 316L)
- [ ] Fini (2B, #4, BA) et film protecteur
- [ ] Épaisseur en calibre **et** décimale (table inox, voir [[sheet-gauges]])
- [ ] Certificat d’usine si exigé
- [ ] Comparer les prix publiés dans le [[prix]]

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Choisir du 303 pour une pièce soudée ou en milieu salin | Soudabilité et corrosion insuffisantes |
| Laisser l’outil frotter | Surface écrouie, outil brûlé |
| Mêmes brosses que pour l’acier | Rouille de contamination |
| 304 en milieu chloré (sel, piscine) | Piqûres ; préférer 316 |

## FAQ

### L’inox 304 est-il magnétique ?
À l’état recuit, très peu ; il peut le devenir légèrement après écrouissage (pliage, usinage). Ce n’est pas un test fiable de nuance.

### 17-4PH, c’est aussi de l’inox ?
Oui, un inox martensitique à durcissement structural, traité thermiquement : voir [[ph-17-4]].

## À valider en atelier (Michaël)

- Vos paramètres d’usinage types pour le 304 et le 316.
- Les finis les plus demandés par vos clients.

## Sources

- [Carpenter Technology — Ideas for machining austenitic stainless steels](https://www.carpentertechnology.com/blog/ideas-for-machining-austenitic-stainless-steels), consulté le 26 novembre 2026.
- [Wexmar — Machining 303, 304 and 316 stainless: work hardening, tooling and cost](https://wexmar.com/blog/machining-303-304-316-stainless-work-hardening-tooling-cost/), consulté le 26 novembre 2026.
- [KGL Manufacturing — Stainless steel machinability: 303, 304, 316 and 17-4 PH compared](https://www.kglmfg.com/resources/blog/stainless-steel-machinability-grades/), consulté le 26 novembre 2026.
=== en
Austenitic stainless **303, 304 and 316** cover most shop needs. They look alike, but not when machining or in corrosion. Their big shared trap: **work hardening** — stainless hardens under the tool if it rubs instead of cutting.

## The three grades

| Grade | Distinctive feature | Use | In the shop |
|---|---|---|---|
| **303** | Added sulfur (inclusions that break the chip) | Production machined parts (bar) | **Easiest to machine** of the three; lower corrosion resistance and weldability; rare as sheet |
| **304 / 304L** | Basic “18-8” stainless; L = low carbon for welding | Sheet, tube, food equipment, general use | Harder to machine (gummy, work-hardens) |
| **316 / 316L** | Added molybdenum → better chloride resistance | Marine, chemical, pharma, road salt | A bit harder still than 304 to machine |
| 430 (ferritic) | Magnetic, no nickel | Appliances, decoration | Cheaper, lower corrosion resistance |

Parts makers quote machinability indexes of about 75–80% for 303, about 45% for 304 and 35–40% for 316 (free-machining steel reference): mostly remember the **order** 303 > 304 > 316.

## Common sheet finishes

| Finish | Look | Use |
|---|---|---|
| 2B | Cold-rolled, matte-satin | General industrial use |
| #4 (brushed) | Grained, satin | Visible: counters, cladding |
| BA | Bright annealed | Decorative, reflective |

Order **protective film** if the face is visible, and specify **grain direction** for #4 parts.

## Machining without work hardening

- **Sharp** positive-rake tools, coated carbide; change them before heavy wear.
- **Firm, continuous feed**: never let the tool rub or stop in the cut (no dwell).
- Cut **below** the work-hardened layer from the previous pass (enough depth).
- Rigid setup, generous coolant; moderate speeds per the tool’s data (see [[feeds-speeds]]).

## Cutting stainless

- **Fiber laser with nitrogen**: clean, oxide-free edge; a blued edge often means contaminated gas (see [[laser-troubleshooting]]).
- **Plasma**: stainless charts (air, or specific gases depending on the source, e.g. F5 or H35 on some systems); see [[cut-charts]].
- **No** standard oxyfuel (see [[oxyfuel]]).

## Avoiding contamination

- Tools, brushes, discs and tables **dedicated to stainless**, or protection (film, wood) on steel tables.
- Embedded iron particles rust and stain: cleaning and **passivation** per good practice if needed.

## Ordering checklist

- [ ] Exact grade (304 vs 304L, 316 vs 316L)
- [ ] Finish (2B, #4, BA) and protective film
- [ ] Thickness as gauge **and** decimal (stainless table, see [[sheet-gauges]])
- [ ] Mill certificate if required
- [ ] Compare published prices in the [[prix]]

## Common mistakes

| Mistake | Consequence |
|---|---|
| Choosing 303 for a welded part or salty environment | Inadequate weldability and corrosion resistance |
| Letting the tool rub | Work-hardened surface, burned tool |
| Same brushes as for steel | Contamination rust |
| 304 in chlorides (salt, pools) | Pitting; prefer 316 |

## FAQ

### Is 304 stainless magnetic?
Annealed, barely; it can become slightly magnetic after cold work (bending, machining). It isn’t a reliable grade test.

### Is 17-4PH stainless too?
Yes, a martensitic precipitation-hardening stainless, heat treated: see [[ph-17-4]].

## For Michaël to review

- Your typical machining parameters for 304 and 316.
- The finishes your customers ask for most.

## Sources

- [Carpenter Technology — Ideas for machining austenitic stainless steels](https://www.carpentertechnology.com/blog/ideas-for-machining-austenitic-stainless-steels), consulted November 26, 2026.
- [Wexmar — Machining 303, 304 and 316 stainless: work hardening, tooling and cost](https://wexmar.com/blog/machining-303-304-316-stainless-work-hardening-tooling-cost/), consulted November 26, 2026.
- [KGL Manufacturing — Stainless steel machinability: 303, 304, 316 and 17-4 PH compared](https://www.kglmfg.com/resources/blog/stainless-steel-machinability-grades/), consulted November 26, 2026.
