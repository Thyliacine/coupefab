---
id: copper-brass
hub: materials
order: 30
nav: Cuivre, laiton, bronze | Copper, brass, bronze
kicker: Matériaux · alliages cuivreux | Materials · copper alloys
level: debutant
schema: Article
prices: yes
tags: copper, cuivre, brass, laiton, bronze, c110, c11000, c360, c36000, c932, c93200, c954, c95400, sae 660, aluminum bronze, machinability, bushing, busbar, laser, waterjet
related: materials-grades, feeds-speeds, waterjet, fiber-laser
fr_slug: cuivre-laiton-bronze-c110-c360-c932-c954
en_slug: copper-brass-bronze-c110-c360-c932-c954
fr_title: Cuivre, laiton et bronze : C110, C360, C932 et C954, usinabilité et coupe
en_title: Copper, brass and bronze: C110, C360, C932 and C954, machinability and cutting
fr_desc: Le cuivre C110 (conducteur, difficile à usiner), le laiton C360 (référence d’usinabilité 100), le bronze C932 (SAE 660, coussinets) et le bronze d’aluminium C954 : usages, usinage, coupe laser/jet d’eau/plasma, avec lien vers les prix publiés.
en_desc: C110 copper (conductive, hard to machine), C360 brass (machinability reference 100), C932 bronze (SAE 660, bushings) and C954 aluminum bronze: uses, machining, laser/waterjet/plasma cutting, linked to published prices.
---
=== fr
Les alliages cuivreux sont désignés par le système **UNS** (C + 5 chiffres, souvent abrégé à 3 : C11000 = C110). Leur usinabilité se mesure sur une échelle où le **laiton de décolletage C36000 = 100**, selon la Copper Development Association.

## Les quatre alliages du catalogue

| Alliage | Nom courant | Indice d’usinabilité (C360 = 100) | Usage typique |
|---|---|---|---|
| **C11000** (C110) | Cuivre électrolytique ETP | **20** | Barres omnibus, conducteurs, échangeurs, plaques de masse |
| **C36000** (C360) | Laiton de décolletage (au plomb) | **100** (référence) | Raccords, pièces décolletées, quincaillerie |
| **C93200** (C932) | Bronze au plomb et à l’étain, « SAE 660 » | **70** | Coussinets, bagues, plaques d’usure |
| **C95400** (C954) | Bronze d’aluminium | **60** | Bagues fortement chargées, engrenages, pièces d’usure |

Indices tirés de la CDA (Copper.org) et du fondeur Concast pour les alliages coulés. Ce sont des **indices relatifs**, pas des vitesses de coupe.

## Usiner

- **C360** : copeaux fragmentés, finition excellente, grandes vitesses ; outils à **angle de coupe nul ou faible** pour éviter que l’outil « tire » dans la matière (recommandation courante pour le laiton).
- **C110** : très ductile et collant ; copeaux longs, arête rapportée. Outils très affûtés à coupe positive, lubrification, évacuation des copeaux.
- **C932** : s’usine bien grâce au plomb ; c’est le choix classique des bagues usinées à partir de barres creuses coulées en continu.
- **C954** : plus dur et plus abrasif ; carbure recommandé, vitesses plus modérées.

> [!NOTE] C360 et C932 contiennent du **plomb**. Ventilation, hygiène (lavage des mains) et gestion des copeaux selon les règles applicables ; pour l’eau potable, des alliages sans plomb existent (règles NSF/ANSI 61/372).

## Couper la tôle et la plaque

- **Laser fibre** : le cuivre et le laiton sont très **réfléchissants** ; possible sur les machines prévues pour, avec les recettes du fabricant (souvent à l’azote ou à l’oxygène selon la machine). Ne pas improviser.
- **Jet d’eau** : la solution sans risque de réflexion ni zone thermique ; voir [[waterjet]].
- **Plasma** : possible sur le cuivre et le laiton avec les bons procédés, qualité de bord moindre ; vérifiez la charte de la source.
- **Routeur / fraiseuse** : très bien pour le laiton en plaque.

## Liste de vérification de commande

- [ ] Désignation UNS exacte (C11000, C36000, C93200, C95400)
- [ ] Forme : barre pleine, barre creuse (coussinets), plaque, tôle
- [ ] État (doux, demi-dur, dur pour le cuivre)
- [ ] Exigence « sans plomb » si eau potable
- [ ] Comparer les prix publiés dans le [[prix]] (le cuivre suit fortement le marché)

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Usiner du C110 comme du laiton | Copeaux qui collent, mauvais fini, outil brûlé |
| Outil à forte coupe positive dans le laiton | Prise brutale, vibrations |
| Couper du cuivre au laser sans recette ni protection anti-réflexion | Risque pour la source laser |
| Choisir du C932 pour l’eau potable | Plomb non conforme |

## FAQ

### Bronze ou laiton pour une bague ?
Pour un coussinet, on choisit un **bronze** (C932 pour usage général, C954 pour charges élevées) ; le laiton C360 sert surtout aux pièces décolletées.

### Pourquoi le prix du cuivre varie-t-il autant ?
Il suit le cours du métal sur les marchés (LME/COMEX) ; vérifiez les prix courants avant de soumissionner (voir [[quoting]]).

## À valider en atelier (Michaël)

- Vos fournisseurs habituels de barres creuses C932 et vos usages du C954.

## Sources

- [Copper Development Association — C11000](https://alloys.copper.org/alloy/C11000), consulté le 26 novembre 2026.
- [Copper Development Association — C95400](https://alloys.copper.org/alloy/C95400), consulté le 26 novembre 2026.
- [Concast — Continuous-cast machinability ratings (PDF)](https://www.concast.com/files/cast_machinability_ratings.pdf), consulté le 26 novembre 2026.
- [Copper Development Association — Comparative machinability of brasses (PDF)](https://archive.copper.org/applications/rodbar/pdf/a7009.pdf), consulté le 26 novembre 2026.
=== en
Copper alloys use the **UNS** system (C + 5 digits, often shortened to 3: C11000 = C110). Their machinability is rated on a scale where **free-cutting brass C36000 = 100**, per the Copper Development Association.

## The four catalogue alloys

| Alloy | Common name | Machinability rating (C360 = 100) | Typical use |
|---|---|---|---|
| **C11000** (C110) | ETP copper | **20** | Busbars, conductors, heat exchangers, ground plates |
| **C36000** (C360) | Free-cutting (leaded) brass | **100** (reference) | Fittings, screw-machine parts, hardware |
| **C93200** (C932) | Leaded tin bronze, “SAE 660” | **70** | Bushings, sleeves, wear plates |
| **C95400** (C954) | Aluminum bronze | **60** | Heavily loaded bushings, gears, wear parts |

Ratings from the CDA (Copper.org) and the Concast foundry for cast alloys. They are **relative indexes**, not cutting speeds.

## Machining

- **C360**: broken chips, excellent finish, high speeds; **zero or low rake** tools to avoid the tool “pulling” into the material (common advice for brass).
- **C110**: very ductile and sticky; long chips, built-up edge. Very sharp positive-rake tools, lubrication, chip evacuation.
- **C932**: machines well thanks to lead; the classic choice for bushings machined from continuous-cast hollow bar.
- **C954**: harder and more abrasive; carbide recommended, more moderate speeds.

> [!NOTE] C360 and C932 contain **lead**. Ventilation, hygiene (hand washing) and chip handling per applicable rules; for drinking water, lead-free alloys exist (NSF/ANSI 61/372 rules).

## Cutting sheet and plate

- **Fiber laser**: copper and brass are highly **reflective**; possible on machines designed for it, with the manufacturer’s recipes (often nitrogen or oxygen depending on the machine). Don’t improvise.
- **Waterjet**: no reflection risk, no heat zone; see [[waterjet]].
- **Plasma**: possible on copper and brass with the right processes, lower edge quality; check the source’s chart.
- **Router / mill**: very good for brass plate.

## Ordering checklist

- [ ] Exact UNS designation (C11000, C36000, C93200, C95400)
- [ ] Form: solid bar, hollow bar (bushings), plate, sheet
- [ ] Temper (soft, half-hard, hard for copper)
- [ ] “Lead-free” requirement if potable water
- [ ] Compare published prices in the [[prix]] (copper tracks the market closely)

## Common mistakes

| Mistake | Consequence |
|---|---|
| Machining C110 like brass | Sticky chips, poor finish, burned tool |
| High positive-rake tool in brass | Grabbing, vibration |
| Laser-cutting copper without a recipe or back-reflection protection | Risk to the laser source |
| Choosing C932 for potable water | Non-compliant lead |

## FAQ

### Bronze or brass for a bushing?
For a bearing, choose a **bronze** (C932 for general use, C954 for high loads); C360 brass is mainly for screw-machine parts.

### Why does copper’s price swing so much?
It tracks the metal market (LME/COMEX); check current prices before quoting (see [[quoting]]).

## For Michaël to review

- Your usual C932 hollow bar suppliers and your uses of C954.

## Sources

- [Copper Development Association — C11000](https://alloys.copper.org/alloy/C11000), consulted November 26, 2026.
- [Copper Development Association — C95400](https://alloys.copper.org/alloy/C95400), consulted November 26, 2026.
- [Concast — Continuous-cast machinability ratings (PDF)](https://www.concast.com/files/cast_machinability_ratings.pdf), consulted November 26, 2026.
- [Copper Development Association — Comparative machinability of brasses (PDF)](https://archive.copper.org/applications/rodbar/pdf/a7009.pdf), consulted November 26, 2026.
