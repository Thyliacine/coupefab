---
id: plasma-bevel
hub: process
order: 22
nav: Plasma biseau (chanfrein) | Plasma bevel cutting
kicker: Procédé · plasma avancé | Process · advanced plasma
level: avance
schema: HowTo
tags: bevel, plasma bevel, v bevel, a bevel, y bevel, k bevel, land, true bevel, bevel head, xpr, compensation, weld prep, rotating head
related: weld-prep, plasma-cutting, cut-charts, hypertherm-edge-phoenix
fr_slug: plasma-biseau-chanfrein
en_slug: plasma-bevel-cutting
fr_title: Découpe plasma en biseau : types de chanfreins, compensation et réglage
en_title: Plasma bevel cutting: bevel types, compensation and setup
fr_desc: V, A, Y et K : vocabulaire des chanfreins plasma, ordre de coupe, compensation d’angle et de talon (True Bevel), et méthode de réglage sur pièce test pour obtenir des chanfreins prêts à souder.
en_desc: V, A, Y and K: plasma bevel vocabulary, cut order, angle and land compensation (True Bevel), and a test-part tuning method for weld-ready bevels.
---
=== fr
Une tête plasma **biseau** (rotative et inclinable) coupe les chanfreins de préparation de soudure en même temps que la pièce, au lieu de les meuler ou de les usiner après. Le gain est énorme sur la plaque, à condition de maîtriser la **compensation** : l’arc plasma ne coupe pas exactement à l’angle programmé, et le talon dépend de l’ordre des passes.

## Les types de biseaux

| Type | Description | Passes |
|---|---|---|
| **V** (biseau supérieur) | Chanfrein depuis le dessus, sans talon | 1 passe inclinée |
| **A** (biseau inférieur) | Chanfrein depuis le dessous | 1 passe inclinée |
| **Y** (V avec talon) | Talon droit en bas + chanfrein en haut | 2 passes : talon (droit) puis V |
| **K** (double avec talon) | Chanfrein bas + talon + chanfrein haut | 3 passes : A, talon, V |

Selon la documentation Hypertherm (*True Bevel*), pour un Y on coupe d’abord le talon droit, puis le chanfrein ; pour un K, le chanfrein inférieur, puis le talon, puis le chanfrein supérieur.

## Pourquoi compenser

- L’angle réellement obtenu diffère de l’angle commandé (le jet a son propre angle de coupe et le kerf varie avec l’inclinaison).
- La vitesse doit baisser quand l’épaisseur traversée augmente (épaisseur sur la diagonale).
- Le talon dépend de la position de la passe précédente : une petite erreur de compensation se lit directement sur la hauteur ou la largeur du talon.

Les chartes **True Bevel** de Hypertherm (systèmes XPR, HPR selon les cas) donnent des compensations d’angle et de position par épaisseur et angle ; on les ajuste ensuite à partir de mesures. La relation utilisée pour corriger le talon : **correction = erreur de talon × tan(angle réel)**, appliquée à la passe concernée.

## Méthode de réglage

1. Choisir le procédé et la charte biseau correspondant à la matière, l’épaisseur et l’angle.
2. Couper une **pièce test** (carré) avec le chanfrein voulu sur chaque côté.
3. **Mesurer** l’angle (rapporteur d’angle ou gabarit) et le talon (pied à coulisse) sur plusieurs côtés.
4. Corriger d’abord l’**angle**, puis la **position** (talon), une variable à la fois.
5. Enregistrer la compensation dans la charte personnalisée de la commande.
6. Valider sur une deuxième pièce test et documenter.

## Liste de vérification

- [ ] Tête biseau calibrée (procédure du fabricant) et sans jeu
- [ ] Consommables biseau conformes
- [ ] Hauteur et palpage adaptés à la torche inclinée
- [ ] Ordre des passes correct pour Y et K
- [ ] Mesures notées dans la fiche de procédé

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Programmer l’angle du dessin sans compensation | Angle et talon hors tolérance de la procédure de soudage |
| Garder la vitesse de la coupe droite | Coupe incomplète ou scories en biseau |
| Corriger angle et position en même temps | Réglage qui tourne en rond |
| Oublier les règles de soudure | Chanfrein « beau » mais non conforme à la WPS ; voir [[weld-prep]] |

## FAQ

### Une table d’entrée de gamme peut-elle faire du biseau ?
Le biseau demande une tête motorisée, une commande et un logiciel qui la gèrent (imbrication avec chanfreins, comme ProNest) ; c’est un équipement industriel. Le biseau manuel au guide reste possible pour de petites quantités.

### Quel logiciel pour programmer des biseaux ?
Les logiciels d’imbrication industriels (ProNest et équivalents) gèrent les attributs de biseau par arête ; voir [[pronest]].

## À valider en atelier (Michaël)

- Les équipements biseau rencontrés et leurs tolérances obtenues.

## Sources

- [Hypertherm — True Bevel technology: bevel compensation cut charts (livre blanc, PDF)](https://www.hypertherm.com/globalassets/learn-about-cutting/articles/wp_807830r1.pdf), consulté le 26 novembre 2026.
- [The Fabricator — Better bevels with plasma arc cutting](https://www.thefabricator.com/thefabricator/article/plasmacutting/better-bevels-with-plasma-arc-cutting), consulté le 26 novembre 2026.
=== en
A **bevel** plasma head (rotating and tilting) cuts weld-prep bevels at the same time as the part, instead of grinding or machining them later. The gain on plate is huge, provided you master **compensation**: the plasma arc doesn’t cut exactly at the programmed angle, and the land depends on the order of passes.

## Bevel types

| Type | Description | Passes |
|---|---|---|
| **V** (top bevel) | Bevel from the top, no land | 1 tilted pass |
| **A** (bottom bevel) | Bevel from the bottom | 1 tilted pass |
| **Y** (V with land) | Straight land at the bottom + top bevel | 2 passes: land (straight) then V |
| **K** (double with land) | Bottom bevel + land + top bevel | 3 passes: A, land, V |

Per Hypertherm’s *True Bevel* documentation, for a Y you cut the straight land first, then the bevel; for a K, the bottom bevel, then the land, then the top bevel.

## Why compensate

- The actual angle differs from the commanded angle (the jet has its own cut angle and kerf varies with tilt).
- Speed must drop as the thickness crossed increases (thickness along the diagonal).
- The land depends on where the previous pass landed: a small compensation error shows directly in land height or width.

Hypertherm’s **True Bevel** charts (XPR, HPR depending on the case) give angle and position compensations by thickness and angle; you then fine-tune from measurements. The relation used to correct the land: **correction = land error × tan(actual angle)**, applied to the relevant pass.

## Tuning method

1. Pick the process and bevel chart for the material, thickness and angle.
2. Cut a **test part** (square) with the desired bevel on each side.
3. **Measure** the angle (protractor or gauge) and land (caliper) on several sides.
4. Correct the **angle** first, then **position** (land), one variable at a time.
5. Save the compensation in the control’s custom chart.
6. Validate on a second test part and document it.

## Checklist

- [ ] Bevel head calibrated (manufacturer’s procedure) with no play
- [ ] Bevel consumables as specified
- [ ] Height and sensing suited to the tilted torch
- [ ] Correct pass order for Y and K
- [ ] Measurements recorded in the process sheet

## Common mistakes

| Mistake | Consequence |
|---|---|
| Programming the drawing angle without compensation | Angle and land outside the welding procedure tolerance |
| Keeping straight-cut speed | Incomplete cut or dross on the bevel |
| Correcting angle and position together | Tuning goes in circles |
| Forgetting welding rules | “Nice” bevel that doesn’t meet the WPS; see [[weld-prep]] |

## FAQ

### Can an entry-level table cut bevels?
Bevel cutting needs a motorized head, plus a control and software that drive it (nesting with bevels, like ProNest); it’s industrial equipment. Manual guided beveling is still possible for small quantities.

### What software programs bevels?
Industrial nesting software (ProNest and similar) handles bevel attributes per edge; see [[pronest]].

## For Michaël to review

- Bevel equipment you’ve met and the tolerances achieved.

## Sources

- [Hypertherm — True Bevel technology: bevel compensation cut charts (white paper, PDF)](https://www.hypertherm.com/globalassets/learn-about-cutting/articles/wp_807830r1.pdf), consulted November 26, 2026.
- [The Fabricator — Better bevels with plasma arc cutting](https://www.thefabricator.com/thefabricator/article/plasmacutting/better-bevels-with-plasma-arc-cutting), consulted November 26, 2026.
