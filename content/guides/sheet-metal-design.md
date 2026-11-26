---
id: sheet-metal-design
hub: fundamentals
order: 43
nav: Concevoir pour la tôle | Sheet metal design rules
kicker: Fondamentaux · conception | Fundamentals · design
level: debutant
schema: HowTo
tags: sheet metal design, conception tôlerie, dfm, flange length, longueur de rebord, hole to bend, trou près du pli, bend relief, dégagement de pli, hole size, laser, plasma, press brake, plieuse
related: press-brake, bend-allowance, dxf-best-practices, fiber-laser
fr_slug: conception-tolerie-regles-dfm
en_slug: sheet-metal-design-rules-dfm
fr_title: Concevoir une pièce de tôlerie fabricable : rebords, trous près des plis et dégagements
en_title: Designing manufacturable sheet metal: flanges, holes near bends and reliefs
fr_desc: Les règles de base pour des pièces découpées puis pliées sans surprise : longueur minimale de rebord, distance trou–pli, taille et position des trous, dégagements de pli, d’après les guides de Protolabs.
en_desc: The basic rules for parts that are cut then bent without surprises: minimum flange length, hole-to-bend distance, hole size and placement, bend reliefs, based on Protolabs’ guides.
---
=== fr
Beaucoup de problèmes de pliage se règlent **au dessin**. Une pièce bien conçue se découpe, se plie et se monte du premier coup ; une pièce mal conçue force l’atelier à des reprises coûteuses. Les règles ci-dessous viennent des guides publics de Protolabs ; les valeurs exactes dépendent de l’outillage de chaque atelier.

## Règles de base

| Règle | Valeur indicative | Pourquoi |
|---|---|---|
| **Longueur minimale de rebord** | 4 × l’épaisseur | La plieuse doit tenir la pièce (trois points de contact) ; sinon le rebord se déforme ou doit être usiné |
| **Distance trou ou découpe → pli** | 4 × l’épaisseur depuis l’extérieur du pli | La matière s’étire près du pli : un trou rond devient ovale |
| **Diamètre minimal de trou** | ≥ épaisseur | Découpe et poinçonnage propres |
| **Trou → bord** | 1,6 mm (≤ 0,9 mm d’épaisseur), 3,2 mm (plus épais) | Éviter la déformation |

> [!NOTE] Les valeurs détaillées varient selon la matière, l’épaisseur et le rayon de pli (par exemple 2,5 à 4 × l’épaisseur + le rayon chez Protolabs). Demandez les règles de l’atelier qui fabriquera la pièce.

## Quand un trou doit être près d’un pli

1. **Accepter la déformation** si le trou n’est pas critique.
2. **Déplacer le trou** hors de la zone de 4 × l’épaisseur (solution la plus courante).
3. **Réduire le rayon de pli** intérieur pour limiter l’étirement.
4. **Prolonger la découpe à travers le pli** ou ajouter un **dégagement** pour que la matière s’étire sans toucher l’élément critique.

## Liste de vérification

- [ ] Épaisseur et matière définies dans le modèle (voir [[sheet-gauges]])
- [ ] Rebords d’au moins 4 × l’épaisseur (ou selon l’atelier)
- [ ] Trous et découpes hors de la zone de 4 × l’épaisseur autour des plis
- [ ] Dégagements de pli aux coins
- [ ] Développé calculé avec le facteur K de l’atelier (voir [[bend-allowance]])
- [ ] DXF propre pour la découpe (voir [[dxf-best-practices]])

## Erreurs fréquentes

- Dessiner un rebord trop court pour la matrice de la plieuse.
- Placer un trou de vis juste au bord d’un pli : il sort ovale.
- Oublier les dégagements aux coins : déchirures.
- Utiliser un facteur K générique au lieu de celui de l’atelier.

## FAQ

### Ces règles valent-elles pour le laser et le plasma ?
Oui pour le pliage. La découpe a ses propres limites (taille minimale des trous, qualité de bord) qui dépendent du procédé : voir [[plasma-cutting]] et [[fiber-laser]].

### Et si mon rebord doit être plus court ?
Parlez-en à l’atelier : usinage après pliage, outillage spécial ou autre méthode.

## À valider en atelier (Michaël)

- Longueurs minimales de rebord selon nos matrices.
- Facteur K et rayons utilisés par matière.

## Sources

- [Protolabs — Sheet Metal Fabrication Design Guidelines](https://www.protolabs.com/services/sheet-metal-fabrication/design-guidelines/) : éléments près des plis (4 × l’épaisseur), solutions, rebords et trois points de contact. Consulté le 26 novembre 2026.
- [Protolabs — Design for Sheet Metal Fabrication Toolkit](https://www.protolabs.com/resources/design-for-sheet-metal-fabrication-toolkit/) : tableaux par matière et épaisseur.
- [Protolabs — Sheet metal tolerances (PDF)](https://www.protolabs.com/media/roognect/sheet-metal-tolerances-one-pager-2.pdf) : diamètre minimal de trou, distances trou–bord.

=== en
Many bending problems are solved **on the drawing**. A well-designed part is cut, bent and assembled right the first time; a poorly designed one forces costly rework. The rules below come from Protolabs’ public guides; exact values depend on each shop’s tooling.

## Basic rules

| Rule | Typical value | Why |
|---|---|---|
| **Minimum flange length** | 4 × thickness | The press brake must hold the part (three points of contact); otherwise the flange deforms or needs machining |
| **Hole or cut-out → bend** | 4 × thickness from the outside of the bend | Material stretches near the bend: a round hole turns oval |
| **Minimum hole diameter** | ≥ thickness | Clean cutting and punching |
| **Hole → edge** | 1.6 mm (≤ 0.9 mm thick), 3.2 mm (thicker) | Avoid distortion |

> [!NOTE] Detailed values vary with material, thickness and bend radius (for example 2.5 to 4 × thickness + radius at Protolabs). Ask the shop making the part for its rules.

## When a hole must sit near a bend

1. **Accept the distortion** if the hole isn’t critical.
2. **Move the hole** out of the 4 × thickness zone (most common fix).
3. **Use a smaller inside bend radius** to limit stretching.
4. **Extend the cut-out through the bend** or add a **relief** so the material stretches without touching the critical feature.

## Checklist

- [ ] Thickness and material defined in the model (see [[sheet-gauges]])
- [ ] Flanges at least 4 × thickness (or per the shop)
- [ ] Holes and cut-outs outside the 4 × thickness zone around bends
- [ ] Bend reliefs at corners
- [ ] Flat pattern computed with the shop’s K-factor (see [[bend-allowance]])
- [ ] Clean DXF for cutting (see [[dxf-best-practices]])

## Common mistakes

- Drawing a flange too short for the press-brake die.
- Putting a screw hole right at a bend: it comes out oval.
- Forgetting corner reliefs: tearing.
- Using a generic K-factor instead of the shop’s.

## FAQ

### Do these rules apply to laser and plasma?
Yes for bending. Cutting has its own limits (minimum hole size, edge quality) that depend on the process: see [[plasma-cutting]] and [[fiber-laser]].

### What if my flange must be shorter?
Talk to the shop: machining after bending, special tooling or another method.

## For Michaël to review

- Minimum flange lengths for our dies.
- K-factor and radii used per material.

## Sources

- [Protolabs — Sheet Metal Fabrication Design Guidelines](https://www.protolabs.com/services/sheet-metal-fabrication/design-guidelines/): features near bends (4 × thickness), fixes, flanges and three points of contact. Consulted November 26, 2026.
- [Protolabs — Design for Sheet Metal Fabrication Toolkit](https://www.protolabs.com/resources/design-for-sheet-metal-fabrication-toolkit/): tables by material and thickness.
- [Protolabs — Sheet metal tolerances (PDF)](https://www.protolabs.com/media/roognect/sheet-metal-tolerances-one-pager-2.pdf): minimum hole diameter, hole-to-edge distances.
