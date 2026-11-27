---
id: fiber-laser
hub: process
order: 2
nav: Laser fibre | Fiber laser
kicker: Procédé · découpe thermique | Process · thermal cutting
level: debutant
schema: Article
tags: fiber laser, laser cutting, assist gas, nitrogen, oxygen, lightburn, safety, class 4
related: plasma-cutting, lightburn, nesting, safety
prices: yes
fr_slug: laser-fibre
en_slug: fiber-laser-cutting
fr_title: Découpe laser fibre : gaz d’assistance, épaisseurs, sécurité et choix
en_title: Fiber laser cutting: assist gas, thicknesses, safety and choosing
fr_desc: Comment coupe un laser fibre, oxygène, azote ou air comprimé, ce qui fait la qualité du bord, la sécurité laser classe 4 et la différence avec le plasma — pour décider en connaissance de cause.
en_desc: How a fiber laser cuts, oxygen versus nitrogen versus compressed air, what makes edge quality, class 4 laser safety and how it differs from plasma — to decide with your eyes open.
---
=== fr
Un laser fibre concentre un faisceau infrarouge (autour de 1 µm de longueur d’onde) sur un point minuscule ; un **gaz d’assistance** chasse le métal fondu. Résultat : saignée fine, petits détails nets, peu de biseau, et des vitesses très élevées en tôle mince. Le prix d’entrée et l’exigence de sécurité sont plus élevés qu’en plasma.

## Le gaz d’assistance change tout

| Gaz | Effet | Usage typique |
|---|---|---|
| Oxygène | Réaction exothermique qui aide à couper ; bord oxydé | Acier au carbone, surtout en épaisseur |
| Azote | Gaz inerte, bord sans oxyde, brillant | Inox, aluminium, acier quand le bord doit être soudé ou peint sans préparation |
| Air comprimé | Compromis économique (contient azote et oxygène) | Tôle mince, quand le fabricant le permet |

L’azote à haute pression consomme beaucoup de gaz : c’est souvent le premier poste de coût d’exploitation après l’électricité. Les fabricants publient des tableaux de paramètres par puissance, gaz et épaisseur : utilisez ceux de votre machine.

## Qualité du bord : les facteurs

- **Position du foyer** et choix de buse.
- **Pression et pureté du gaz.**
- **Vitesse** : trop lente = bavure et brûlures ; trop rapide = coupe non traversante.
- **Propreté de la lentille de protection** : une lentille sale fait chuter la qualité d’un coup.
- **État de la tôle** : calamine, huile, film plastique (côté film selon la recommandation du fabricant).

## Laser ou plasma ?

| Critère | Laser fibre | Plasma |
|---|---|---|
| Petits trous, détails | Excellent | Limité (conicité) |
| Biseau | Très faible | Présent, selon la qualité de la source |
| Tôle épaisse | Possible selon la puissance, coût élevé | Fort, économique |
| Coût d’achat | Élevé | Bas à moyen |
| Sécurité | Classe 4 : enceinte ou zone contrôlée | Arc UV, fumées, bruit |

## Sécurité laser

Les lasers de découpe industriels sont de **classe 4** : le faisceau direct ou réfléchi peut causer des lésions oculaires et cutanées et allumer un feu. Une machine **enclose** et verrouillée peut être classée globalement en classe 1 en fonctionnement normal. Exigences de base : enceinte ou zone contrôlée, verrouillages qui fonctionnent, lunettes spécifiques à la longueur d’onde pour l’entretien faisceau ouvert, extraction des fumées, extincteur adapté. Références : IEC 60825-1 et ANSI Z136.1 ; au Québec, la CNESST publie de l’information sur les rayonnements. Voir [Sécurité](/guides/securite-cnc-cnesst/).

> [!WARN] Cuivre et laiton réfléchissent fortement : les lasers fibre les coupent mieux que les lasers CO₂, mais la réflexion arrière peut endommager la source si les paramètres et les protections ne sont pas ceux du fabricant.

## Petits lasers « hobby » et graveurs

Les graveurs à diode ou à fibre de faible puissance (galvo) gravent et marquent ; ils ne coupent pas de tôle d’acier. Leur logiciel courant est LightBurn (voir [LightBurn](/guides/lightburn-laser/)).

## Liste de vérification

- [ ] Tableau de paramètres du fabricant pour la puissance, le gaz et l’épaisseur
- [ ] Bon gaz d’assistance (oxygène, azote ou air) à la pression et à la pureté prévues
- [ ] Position du foyer et buse vérifiées
- [ ] Vitre (lentille) de protection propre
- [ ] Tôle propre ; film plastique placé du côté recommandé par le fabricant
- [ ] Cuivre et laiton : paramètres et protections du fabricant (réflexion arrière)
- [ ] Enceinte et verrouillages intacts (laser de classe 4)

## FAQ

### Combien d’épaisseur coupe un laser de X kW ?
Cela dépend de la matière, du gaz et de la qualité visée. Les fabricants publient des tableaux par puissance ; comparez la capacité **de qualité** et non la capacité maximale.

### Faut-il un DXF différent ?
Non, mais le laser permet des détails plus fins : vérifiez que les petits éléments sont voulus. Voir [DXF : bonnes pratiques](/guides/dxf-bonnes-pratiques/).

## À valider en atelier (Michaël)

- Les ateliers laser du Québec qui acceptent la sous-traitance (à nommer seulement avec leur accord).
- Votre expérience de comparaison laser / plasma sur des pièces réelles.

## Sources

- [IEC 60825-1 — Safety of laser products](https://webstore.iec.ch/en/publication/3587), consulté le 26 novembre 2026.
- [ANSI Z136.1 — Safe Use of Lasers (Laser Institute of America)](https://www.lia.org/resources/laser-safety-information/laser-safety-standards/ansi-z136-standards/z136-1).
- [CNESST — Ventilation des lieux de travail](https://www.cnesst.gouv.qc.ca/fr/prevention-securite/identifier-corriger-risques/liste-informations-prevention/ventilation-lieux-travail).
=== en
A fiber laser focuses an infrared beam (around 1 µm wavelength) onto a tiny spot; an **assist gas** blows out the molten metal. The result: narrow kerf, crisp small features, little bevel, and very high speeds on thin sheet. Entry price and safety requirements are higher than plasma.

## Assist gas changes everything

| Gas | Effect | Typical use |
|---|---|---|
| Oxygen | Exothermic reaction helps cutting; oxidized edge | Carbon steel, especially thicker |
| Nitrogen | Inert gas, oxide-free bright edge | Stainless, aluminum, steel when the edge must be welded or painted without prep |
| Compressed air | Economic compromise (contains nitrogen and oxygen) | Thin sheet, when the maker allows it |

High-pressure nitrogen uses a lot of gas: it is often the top running cost after electricity. Makers publish parameter tables by power, gas and thickness: use your machine’s.

## Edge quality: the factors

- **Focus position** and nozzle choice.
- **Gas pressure and purity.**
- **Speed**: too slow = burr and burning; too fast = no break-through.
- **Protective window cleanliness**: a dirty window drops quality instantly.
- **Sheet condition**: mill scale, oil, plastic film (film side per the maker’s advice).

## Laser or plasma?

| Criterion | Fiber laser | Plasma |
|---|---|---|
| Small holes, detail | Excellent | Limited (taper) |
| Bevel | Very low | Present, depends on source quality |
| Thick plate | Possible with power, high cost | Strong, economical |
| Purchase cost | High | Low to medium |
| Safety | Class 4: enclosure or controlled area | UV arc, fumes, noise |

## Laser safety

Industrial cutting lasers are **class 4**: the direct or reflected beam can injure eyes and skin and start fires. An **enclosed**, interlocked machine can be classified class 1 overall in normal operation. Basics: enclosure or controlled area, working interlocks, wavelength-specific eyewear for open-beam service, fume extraction, a suitable extinguisher. References: IEC 60825-1 and ANSI Z136.1; in Quebec, CNESST publishes radiation guidance. See [Safety](/en/guides/cnc-shop-safety/).

> [!WARN] Copper and brass are highly reflective: fiber lasers cut them better than CO₂ lasers, but back-reflection can damage the source if parameters and protections are not the maker’s.

## Small “hobby” lasers and engravers

Low-power diode or fiber (galvo) engravers engrave and mark; they do not cut steel sheet. Their common software is LightBurn (see [LightBurn](/en/guides/lightburn-laser/)).

## Checklist

- [ ] Maker’s parameter table for the power, gas and thickness
- [ ] Right assist gas (oxygen, nitrogen or air) at the specified pressure and purity
- [ ] Focus position and nozzle checked
- [ ] Protective window (cover glass) clean
- [ ] Clean sheet; plastic film on the side the maker recommends
- [ ] Copper and brass: maker’s parameters and protections (back reflection)
- [ ] Enclosure and interlocks intact (class 4 laser)

## FAQ

### How thick does an X kW laser cut?
It depends on material, gas and target quality. Makers publish tables by power; compare the **quality** capacity, not the maximum.

### Do I need a different DXF?
No, but laser allows finer detail: make sure small features are intended. See [DXF best practices](/en/guides/dxf-best-practices/).

## For Michaël to review

- Quebec laser job shops that accept subcontracting (named only with their agreement).
- Your experience comparing laser and plasma on real parts.

## Sources

- [IEC 60825-1 — Safety of laser products](https://webstore.iec.ch/en/publication/3587), consulted November 26, 2026.
- [ANSI Z136.1 — Safe Use of Lasers (Laser Institute of America)](https://www.lia.org/resources/laser-safety-information/laser-safety-standards/ansi-z136-standards/z136-1).
- [CNESST — Workplace ventilation (French)](https://www.cnesst.gouv.qc.ca/fr/prevention-securite/identifier-corriger-risques/liste-informations-prevention/ventilation-lieux-travail).
