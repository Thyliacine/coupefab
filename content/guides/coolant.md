---
id: coolant
hub: fundamentals
order: 42
nav: Arrosage et fluides de coupe | Coolant and cutting fluids
kicker: Fondamentaux · arrosage | Fundamentals · coolant
level: intermediaire
schema: HowTo
tags: coolant, arrosage, cutting fluid, fluide de coupe, emulsion, émulsion, mql, high pressure coolant, haute pression, through-tool, par le centre, precision coolant, chip control, dry machining, usinage à sec
related: feeds-speeds, tool-life, lathe-finish-chatter, stainless-steel
fr_slug: arrosage-fluides-de-coupe
en_slug: coolant-cutting-fluids
fr_title: Arrosage et fluides de coupe : émulsion, MQL, haute pression et où viser
en_title: Coolant and cutting fluids: emulsion, MQL, high pressure and where to aim
fr_desc: Les trois rôles du fluide de coupe, les types (émulsion, huile, air, MQL, cryogénie), arrosage dessus ou dessous en tournage, et les plages de pression utiles selon Sandvik Coromant.
en_desc: The three jobs of cutting fluid, the types (emulsion, oil, air, MQL, cryogenic), over versus under coolant in turning, and useful pressure ranges per Sandvik Coromant.
---
=== fr
Le fluide de coupe a trois rôles : **évacuer les copeaux**, **refroidir** et **lubrifier** entre l’outil et la pièce. Bien appliqué, il améliore la sécurité du procédé, la durée de vie des outils et la qualité des pièces. Mal dirigé, il coûte cher sans rien apporter.

## Les types de fluide

| Type | Description | Remarque |
|---|---|---|
| **Émulsion** | Eau + huile (environ 5 à 10 % d’huile) | Le plus courant |
| **Huile entière** | Huile pure | Certaines machines, taraudage, rectification |
| **Air comprimé** | Souffle | Évacue les copeaux, refroidit mal |
| **MQL** | Air + quantité minimale d’huile | Équipement spécial |
| **Cryogénie** | Gaz liquéfié | Refroidissement maximal, équipement spécial |

L’usinage **à sec** est parfois possible et avantageux (coût, environnement) avec le bon outil et le bon grade de carbure.

## Où viser (tournage)

- **Arrosage de précision dessus** (côté face de coupe) : refroidit et améliore le contrôle des copeaux ; avec de la pression, aide à les fractionner.
- **Arrosage dessous** (côté dépouille) : évacue la chaleur de la plaquette et prolonge la durée de vie.
- **Arrosage conventionnel** (buses orientables, gros débit) : inonde la zone ; pas conçu pour la haute pression.

Sandvik Coromant recommande : arrosage dessous pour la durée de vie ; dessus (et dessous) quand le contrôle des copeaux pose problème ; les deux pour les grades de carbure à revêtement PVD mince (superalliages, inox) afin d’éviter la déformation plastique.

## Plages de pression (arrosage de précision)

| Pression | Effet |
|---|---|
| 7–10 bar (100–150 psi) | Meilleur contrôle des copeaux dans l’acier et les matières courantes |
| 70–80 bar (1 000–1 200 psi) | Fractionnement des copeaux |
| 150–200 bar (2 200–2 900 psi) | Matières exigeantes : inox duplex, superalliages |

## Liste de vérification

- [ ] Concentration d’émulsion mesurée (réfractomètre) et dans la plage du fabricant
- [ ] Buses dirigées vers la zone de coupe, pas vers le porte-outil
- [ ] Arrosage par le centre utilisé quand l’outil le permet
- [ ] Pression adaptée à la matière
- [ ] Bac nettoyé et fluide entretenu (odeur, mousse, huiles étrangères)

## Erreurs fréquentes

- Arrosage intermittent sur des plaquettes carbure : chocs thermiques et fissures. Arrosez abondamment ou pas du tout.
- Buses mal orientées après un changement d’outil.
- Émulsion trop diluée : rouille et usure ; trop concentrée : mousse et irritation de la peau.

## FAQ

### À sec ou arrosé en fraisage ?
Ça dépend de la matière et du grade de carbure ; en fraisage interrompu, l’arrosage peut causer des fissures thermiques. Suivez la recommandation du fabricant d’outils.

### La haute pression vaut-elle l’investissement ?
Pour l’inox, les superalliages et le perçage profond, souvent oui ; elle consomme plus d’énergie, à prendre en compte.

## À valider en atelier (Michaël)

- Fluides et concentrations utilisés chez nous.
- Pression disponible sur nos machines.

## Sources

- [Sandvik Coromant — How to apply coolant and cutting fluid in turning](https://www.sandvik.coromant.com/en-us/knowledge/general-turning/how-to-apply-coolant-and-cutting-fluid-in-turning) : rôles, types de fluides, arrosage dessus/dessous, plages de pression. Consulté le 26 novembre 2026.
- [Sandvik Coromant — Troubleshooting in turning](https://www.sandvik.coromant.com/en-us/knowledge/general-turning/troubleshooting-turning) : fissures thermiques et arrosage intermittent.

=== en
Cutting fluid has three jobs: **chip evacuation**, **cooling** and **lubrication** between tool and part. Applied correctly, it improves process security, tool life and part quality. Aimed badly, it costs money and does nothing.

## Fluid types

| Type | Description | Note |
|---|---|---|
| **Emulsion** | Water + oil (about 5–10% oil) | Most common |
| **Straight oil** | Neat oil | Some machines, tapping, grinding |
| **Compressed air** | Blast | Clears chips, poor cooling |
| **MQL** | Air + minimum quantity of oil | Special equipment |
| **Cryogenic** | Liquefied gas | Maximum cooling, special equipment |

**Dry** machining is sometimes possible and worthwhile (cost, environment) with the right tool and grade.

## Where to aim (turning)

- **Precision over coolant** (rake side): cools and improves chip control; with pressure, helps break chips.
- **Under coolant** (flank side): pulls heat out of the insert and extends tool life.
- **Conventional coolant** (adjustable nozzles, high flow): floods the zone; not meant for high pressure.

Sandvik Coromant recommends: under coolant for tool life; over (and under) when chip control is an issue; both for thin PVD grades (superalloys, stainless) to avoid plastic deformation.

## Pressure ranges (precision coolant)

| Pressure | Effect |
|---|---|
| 7–10 bar (100–150 psi) | Better chip control in steel and common materials |
| 70–80 bar (1,000–1,200 psi) | Chip breaking |
| 150–200 bar (2,200–2,900 psi) | Demanding materials: duplex stainless, superalloys |

## Checklist

- [ ] Emulsion concentration measured (refractometer) and within the maker’s range
- [ ] Nozzles aimed at the cutting zone, not the holder
- [ ] Through-tool coolant used when the tool allows
- [ ] Pressure suited to the material
- [ ] Sump cleaned and fluid maintained (smell, foam, tramp oil)

## Common mistakes

- Intermittent coolant on carbide inserts: thermal shock and cracks. Flood it or keep it dry.
- Nozzles misaimed after a tool change.
- Emulsion too lean: rust and wear; too rich: foam and skin irritation.

## FAQ

### Dry or wet when milling?
Depends on material and grade; in interrupted milling, coolant can cause thermal cracks. Follow the tool maker’s recommendation.

### Is high pressure worth it?
For stainless, superalloys and deep drilling, often yes; it uses more energy, which needs to be considered.

## For Michaël to review

- Fluids and concentrations we use.
- Pressure available on our machines.

## Sources

- [Sandvik Coromant — How to apply coolant and cutting fluid in turning](https://www.sandvik.coromant.com/en-us/knowledge/general-turning/how-to-apply-coolant-and-cutting-fluid-in-turning): jobs, fluid types, over/under coolant, pressure ranges. Consulted November 26, 2026.
- [Sandvik Coromant — Troubleshooting in turning](https://www.sandvik.coromant.com/en-us/knowledge/general-turning/troubleshooting-turning): thermal cracks and intermittent coolant.
