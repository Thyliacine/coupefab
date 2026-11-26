---
id: weld-prep
hub: process
order: 70
nav: Préparation de soudure | Weld preparation
kicker: Procédé · avant soudage | Process · before welding
level: intermediaire
schema: HowTo
tags: weld prep, bevel, chamfer, groove weld, root face, land, root opening, included angle, fit-up, cwb, csa w47.1, csa w59, aws d1.1, wps, mill scale, oxide, plasma bevel
related: plasma-bevel, deburring, oxyfuel, tolerances
fr_slug: preparation-soudure-chanfrein
en_slug: weld-preparation-bevels
fr_title: Préparer une pièce pour la soudure : chanfreins, talon, écartement et propreté
en_title: Preparing parts for welding: bevels, root face, root opening and cleanliness
fr_desc: Vocabulaire d’un joint à chanfrein (angle, talon, écartement), d’où viennent les dimensions (procédure de soudage, CSA W59, AWS D1.1), comment couper et nettoyer le chanfrein au plasma, à l’oxycoupage ou à la meule, et liste de vérification d’assemblage.
en_desc: Groove joint vocabulary (angle, root face, root opening), where dimensions come from (welding procedure, CSA W59, AWS D1.1), how to cut and clean the bevel with plasma, oxyfuel or grinding, and a fit-up checklist.
---
=== fr
Une bonne soudure commence à la découpe. Un chanfrein mal coupé, un talon irrégulier ou une surface oxydée coûtent plus cher en meulage, en reprise et en rejet qu’un réglage de machine soigné.

> [!NOTE] Les dimensions d’un joint (angle, talon, écartement) ne se choisissent pas « au feeling » : elles viennent de la **procédure de soudage** (WPS) de l’entreprise, qualifiée selon la norme applicable. Au Canada, la certification des entreprises de soudage relève de **CSA W47.1** (acier) via le **Bureau canadien de soudage (CWB)**, et la conception des assemblages en acier de **CSA W59**. Aux États-Unis, l’équivalent courant est **AWS D1.1**.

## Le vocabulaire d’un joint à chanfrein

| Terme | Anglais | Définition |
|---|---|---|
| Angle de chanfrein | Bevel angle | Angle coupé sur une pièce |
| Angle d’ouverture | Included angle / groove angle | Angle total entre les deux pièces (deux chanfreins de 30° → 60°) |
| Talon | Root face / land | Méplat non chanfreiné au fond du joint |
| Écartement | Root opening / gap | Distance entre les pièces à la racine |
| Préparation en V, X, U, J | V, double-V, U, J groove | Forme du joint selon l’épaisseur et l’accès |

Exemple tiré d’un guide Lincoln Electric pour le soudage de tuyaux : angle d’ouverture de 60° (30° par côté), talon et écartement d’environ 1/16 po. C’est un **exemple de procédure pour un cas donné**, pas une règle universelle.

## Couper le chanfrein

| Méthode | Avantages | Limites |
|---|---|---|
| Plasma avec tête biseau (CNC) | Rapide, répétable, chanfreins intégrés aux pièces | Investissement, réglages de compensation d’angle ; voir [[plasma-bevel]] |
| Plasma ou oxycoupage manuel avec guide | Peu coûteux | Régularité dépendante de l’opérateur |
| Chanfreineuse (outil rotatif, portable ou stationnaire) | Surface usinée propre, sans zone thermique | Vitesse, formes droites surtout |
| Meulage | Disponible partout | Lent, irrégulier, poussières |
| Usinage (fraiseuse, tour) | Précision maximale, talon exact | Pièces de taille limitée |

## Nettoyer avant de souder

- **Calamine, oxyde de coupe, rouille, peinture, huile** : à retirer sur la zone de soudure selon la WPS (souvent quelques centimètres de chaque côté).
- Bord coupé à l’**oxygène** (laser ou oxycoupage) : couche d’oxyde à considérer selon la procédure.
- **Aluminium** : brossage à la brosse inox dédiée et dégraissage juste avant de souder.
- **Inox** : outils dédiés (brosses, disques) pour éviter la contamination au fer.
- Retirer les **scories** et bavures (voir [[deburring]]).

## Liste de vérification d’assemblage (*fit-up*)

- [ ] Dimensions du joint conformes au dessin et à la WPS (angle, talon, écartement)
- [ ] Désalignement (*hi-lo*) dans la tolérance de la procédure
- [ ] Surfaces propres et sèches sur la largeur prescrite
- [ ] Pointage correct, pièces bridées pour limiter la déformation
- [ ] Préchauffage si exigé par la procédure (épaisseur, nuance)
- [ ] Identification des pièces et traçabilité matière si demandées

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Talon trop épais | Manque de pénétration à la racine |
| Talon nul ou écartement trop grand | Effondrement, perçage de la racine |
| Angle trop fermé | Mauvais accès, manque de fusion sur les flancs |
| Souder sur l’oxyde ou la calamine | Porosités, inclusions |
| Chanfrein coupé sans compenser le kerf | Pièce trop courte, écartement faux |

## FAQ

### Qui fixe l’angle et le talon ?
Le dessin et la procédure de soudage qualifiée de l’entreprise ; les normes contiennent des joints préqualifiés avec leurs tolérances.

### Faut-il meuler un bord coupé au plasma avant de souder ?
Ça dépend de la procédure, de la nuance et de l’état du bord (scories, nitruration, oxyde) ; beaucoup de procédures exigent au moins un nettoyage mécanique.

## À valider en atelier (Michaël)

- Les WPS et joints types de vos clients (W47.1).
- Votre méthode de chanfrein préférée selon l’épaisseur.

## Sources

- [Bureau canadien de soudage (CWB Group) — Certification CSA W47.1](https://www.cwbgroup.org/services/certification/company-certification/csa-w471-fusion-welding-of-steel), consulté le 26 novembre 2026.
- [CSA Group — CSA W59, Construction soudée en acier](https://www.csagroup.org/store/product/W59-18/), consulté le 26 novembre 2026.
- [Lincoln Electric — Guide to welding pipe (PDF)](https://ch-delivery.lincolnelectric.com/api/public/content/a8186a0774ae4156af05bc3714e83070?v=e0ed76e7), consulté le 26 novembre 2026.
- [Lincoln Electric — Weld fusion vs weld penetration](https://www.lincolnelectric.com/en/welding-and-cutting-resource-center/process-and-theory/weld-fusion-vs-weld-penetration), consulté le 26 novembre 2026.
=== en
A good weld starts at the cut. A poorly cut bevel, an uneven root face or an oxidized surface costs more in grinding, rework and rejects than careful machine setup.

> [!NOTE] Joint dimensions (angle, root face, root opening) aren’t chosen by feel: they come from the company’s **welding procedure** (WPS), qualified to the applicable standard. In Canada, welding company certification falls under **CSA W47.1** (steel) through the **Canadian Welding Bureau (CWB)**, and steel welded construction design under **CSA W59**. In the US, the common equivalent is **AWS D1.1**.

## Groove joint vocabulary

| Term | French | Definition |
|---|---|---|
| Bevel angle | Angle de chanfrein | Angle cut on one piece |
| Included angle / groove angle | Angle d’ouverture | Total angle between both pieces (two 30° bevels → 60°) |
| Root face / land | Talon | Unbevelled flat at the bottom of the joint |
| Root opening / gap | Écartement | Distance between the pieces at the root |
| V, double-V, U, J groove | Préparation en V, X, U, J | Joint shape based on thickness and access |

Example from a Lincoln Electric pipe welding guide: 60° included angle (30° per side), root face and root opening of about 1/16 in. That is a **procedure example for one case**, not a universal rule.

## Cutting the bevel

| Method | Advantages | Limits |
|---|---|---|
| Plasma with bevel head (CNC) | Fast, repeatable, bevels built into the parts | Investment, angle compensation setup; see [[plasma-bevel]] |
| Manual plasma or oxyfuel with a guide | Inexpensive | Consistency depends on the operator |
| Beveling machine (rotary, portable or stationary) | Clean machined surface, no heat zone | Speed, mostly straight edges |
| Grinding | Available everywhere | Slow, uneven, dust |
| Machining (mill, lathe) | Highest precision, exact land | Limited part size |

## Clean before welding

- **Mill scale, cutting oxide, rust, paint, oil**: remove from the weld zone per the WPS (often a few centimetres each side).
- Edge cut with **oxygen** (laser or oxyfuel): oxide layer to consider per the procedure.
- **Aluminum**: dedicated stainless brush and degrease right before welding.
- **Stainless**: dedicated tools (brushes, discs) to avoid iron contamination.
- Remove **dross** and burrs (see [[deburring]]).

## Fit-up checklist

- [ ] Joint dimensions per the drawing and WPS (angle, root face, root opening)
- [ ] Misalignment (hi-lo) within the procedure tolerance
- [ ] Surfaces clean and dry over the prescribed width
- [ ] Proper tacking, parts clamped to limit distortion
- [ ] Preheat if the procedure requires it (thickness, grade)
- [ ] Part identification and material traceability if required

## Common mistakes

| Mistake | Consequence |
|---|---|
| Root face too thick | Lack of root penetration |
| No root face or gap too wide | Burn-through, sagging root |
| Angle too narrow | Poor access, lack of sidewall fusion |
| Welding over oxide or scale | Porosity, inclusions |
| Bevel cut without kerf compensation | Part too short, wrong gap |

## FAQ

### Who sets the angle and root face?
The drawing and the company’s qualified welding procedure; standards contain prequalified joints with their tolerances.

### Should a plasma-cut edge be ground before welding?
It depends on the procedure, grade and edge condition (dross, nitriding, oxide); many procedures require at least mechanical cleaning.

## For Michaël to review

- Your customers’ WPSs and typical joints (W47.1).
- Your preferred beveling method by thickness.

## Sources

- [Canadian Welding Bureau (CWB Group) — CSA W47.1 certification](https://www.cwbgroup.org/services/certification/company-certification/csa-w471-fusion-welding-of-steel), consulted November 26, 2026.
- [CSA Group — CSA W59, Welded steel construction](https://www.csagroup.org/store/product/W59-18/), consulted November 26, 2026.
- [Lincoln Electric — Guide to welding pipe (PDF)](https://ch-delivery.lincolnelectric.com/api/public/content/a8186a0774ae4156af05bc3714e83070?v=e0ed76e7), consulted November 26, 2026.
- [Lincoln Electric — Weld fusion vs weld penetration](https://www.lincolnelectric.com/en/welding-and-cutting-resource-center/process-and-theory/weld-fusion-vs-weld-penetration), consulted November 26, 2026.
