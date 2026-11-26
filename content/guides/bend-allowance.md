---
id: bend-allowance
hub: fundamentals
order: 30
nav: Pliage : K-factor et déduction | Bending: K-factor and deduction
kicker: Fondamentaux · tôlerie | Fundamentals · sheet metal
level: intermediaire
schema: HowTo
tags: bend allowance, bend deduction, k-factor, sheet metal, press brake, solidworks, inventor, flat pattern
related: press-brake, solidworks-sheet-metal, inventor, tolerances
prices: yes
fr_slug: pliage-k-factor
en_slug: bend-allowance-k-factor
fr_title: Pliage : longueur développée, K-factor et déduction de pli, avec les formules
en_title: Bending: bend allowance, K-factor and bend deduction, with the formulas
fr_desc: Calculer un déplié juste : formules de la longueur de pli (BA), du retrait extérieur (OSSB) et de la déduction (BD), retrouver le K-factor réel à partir d’un pli d’essai, et le saisir dans la CAO.
en_desc: Get the flat pattern right: formulas for bend allowance (BA), outside setback (OSSB) and bend deduction (BD), back-calculate the real K-factor from a test bend, and enter it in CAD.
---
=== fr
Quand on plie une tôle, l’extérieur s’allonge et l’intérieur se comprime. Quelque part entre les deux, la **fibre neutre** garde sa longueur. Toute la question du déplié est de savoir où elle se trouve : c’est le **K-factor**. Avec lui, la CAO (SolidWorks, Inventor, Onshape, Fusion) calcule une longueur développée qui sort juste après pliage.

## Les définitions

| Symbole | Grandeur |
|---|---|
| T | Épaisseur de la tôle |
| R | Rayon intérieur de pli |
| A | Angle de pli (angle **plié**, en degrés : 90° pour une équerre) |
| K | K-factor = position de la fibre neutre ÷ T (entre 0 et 1) |
| BA | Longueur de pli (bend allowance) : longueur de la fibre neutre dans le pli |
| OSSB | Retrait extérieur (outside setback) |
| BD | Déduction de pli (bend deduction) |

## Les formules

- **BA** = A × (π / 180) × (R + K × T)
- **OSSB** = tan(A / 2) × (R + T)
- **BD** = 2 × OSSB − BA
- **Longueur développée** = somme des longueurs de ailes mesurées à l’extérieur (jusqu’aux lignes de moule) − BD pour chaque pli ; ou somme des parties droites + BA pour chaque pli.

L’aide SolidWorks décrit ces mêmes relations (longueur de pli, déduction, K-factor) et laisse choisir la méthode par pièce ou par tableau.

## D’où vient le rayon intérieur ?

En pliage **en l’air** sur presse plieuse, le rayon intérieur n’est pas celui du poinçon : il se forme selon l’ouverture du V. Steve Benson (The Fabricator) donne la « règle des 20 % » : le rayon intérieur vaut environ **15 à 17 %** de l’ouverture du V pour l’acier laminé à froid, **20 à 22 %** pour l’inox 304 et **9 à 11 %** pour l’aluminium 5052-H32 (commencer à la valeur médiane, puis ajuster). Voir [Presse plieuse](/guides/presse-plieuse/).

> [!WARN] Saisir dans la CAO un rayon de pli qui n’est pas celui que la presse produira donne un déplié faux, même avec le bon K-factor.

## Retrouver votre K-factor réel (pli d’essai)

1. **Couper une bande** de longueur développée connue L (mesurez-la précisément), dans la nuance et l’épaisseur visées.
2. **Plier à 90°** avec l’outillage de production.
3. **Mesurer** les deux ailes à l’extérieur (jusqu’à l’intersection des faces extérieures prolongées) : a et b. Mesurez aussi le rayon intérieur réel R (jauge de rayon).
4. **Calculer** BD = a + b − L.
5. **Calculer** BA = 2 × OSSB − BD, avec OSSB = tan(45°) × (R + T) = R + T.
6. **Calculer** K = ( BA / (A × π / 180) − R ) / T.
7. **Saisir** K (ou directement BD) dans la CAO pour cette combinaison matière + épaisseur + outillage, et noter la source.

### Exemple (chiffres d’essai fictifs)
T = 3,0 mm, L = 100,0 mm, ailes mesurées a = 51,9 mm et b = 53,0 mm, R mesuré = 3,8 mm, A = 90°.
BD = 51,9 + 53,0 − 100,0 = 4,9 mm. OSSB = 3,8 + 3,0 = 6,8 mm. BA = 2 × 6,8 − 4,9 = 8,7 mm.
K = (8,7 / 1,5708 − 3,8) / 3,0 ≈ (5,54 − 3,8) / 3,0 ≈ 0,58. Résultat plausible ; avec vos vraies mesures, le chiffre sera le vôtre.

## Tableaux de pliage

Plutôt qu’un K-factor unique, la plupart des CAO acceptent un **tableau** (épaisseur × rayon × angle → BD ou BA). C’est la méthode la plus fiable en production : chaque ligne vient d’un pli d’essai réel.

## Erreurs fréquentes

- Confondre angle plié et angle inclus (180° − angle plié).
- Mesurer les ailes à l’intérieur au lieu de l’extérieur.
- Utiliser un K-factor « générique » pour toutes les épaisseurs.
- Oublier que le sens de laminage influence le rayon minimal et la fissuration.

## FAQ

### Quelle valeur de K par défaut ?
Le K-factor par défaut de SolidWorks est 0,5 ; c’est un point de départ logiciel, pas une mesure. Faites un pli d’essai.

### K-factor ou déduction de pli ?
Les deux décrivent la même réalité. La déduction est plus intuitive à l’atelier ; le K-factor se transpose mieux à d’autres angles.

## À valider en atelier (Michaël)

- Vos tableaux de pliage réels (matière, épaisseur, V, BD).
- Un exemple chiffré issu d’un vrai pli d’essai pour remplacer l’exemple fictif.

## Sources

- [SolidWorks Help — Bend Allowance](https://help.solidworks.com/2025/english/SolidWorks/sldworks/c_Bend_Allowance.htm), consulté le 26 novembre 2026.
- [SolidWorks Help — K-Factor](https://help.solidworks.com/2025/english/SolidWorks/sldworks/c_K-Factor.htm).
- [The Fabricator — Six steps for selecting the right die for press brakes (S. Benson)](https://www.thefabricator.com/thefabricator/article/bending/six-steps-for-selecting-the-right-die-for-press-brakes).
=== en
When sheet is bent, the outside stretches and the inside compresses. Somewhere between, the **neutral axis** keeps its length. Getting the flat pattern right means knowing where it sits: that is the **K-factor**. With it, CAD (SolidWorks, Inventor, Onshape, Fusion) computes a developed length that comes out right after bending.

## Definitions

| Symbol | Quantity |
|---|---|
| T | Sheet thickness |
| R | Inside bend radius |
| A | Bend angle (the angle **bent**, in degrees: 90° for a square bend) |
| K | K-factor = neutral axis position ÷ T (between 0 and 1) |
| BA | Bend allowance: length of the neutral axis in the bend |
| OSSB | Outside setback |
| BD | Bend deduction |

## The formulas

- **BA** = A × (π / 180) × (R + K × T)
- **OSSB** = tan(A / 2) × (R + T)
- **BD** = 2 × OSSB − BA
- **Developed length** = sum of flange lengths measured outside (to the mold lines) − BD for each bend; or sum of straight portions + BA for each bend.

The SolidWorks help describes the same relationships (bend allowance, deduction, K-factor) and lets you pick the method per part or by table.

## Where does the inside radius come from?

In **air bending** on a press brake, the inside radius is not the punch radius: it forms according to the V opening. Steve Benson (The Fabricator) gives the “20 percent rule”: the inside radius is about **15–17%** of the V opening for cold-rolled steel, **20–22%** for 304 stainless and **9–11%** for 5052-H32 aluminum (start at the median, then adjust). See [Press brake](/en/guides/press-brake-bending/).

> [!WARN] Entering a bend radius in CAD that is not what the press will produce gives a wrong flat, even with the right K-factor.

## Finding your real K-factor (test bend)

1. **Cut a strip** of known developed length L (measure it precisely), in the target grade and thickness.
2. **Bend to 90°** with production tooling.
3. **Measure** both flanges outside (to the intersection of the extended outside faces): a and b. Also measure the real inside radius R (radius gauge).
4. **Compute** BD = a + b − L.
5. **Compute** BA = 2 × OSSB − BD, with OSSB = tan(45°) × (R + T) = R + T.
6. **Compute** K = ( BA / (A × π / 180) − R ) / T.
7. **Enter** K (or BD directly) in CAD for that material + thickness + tooling combination, and note the source.

### Example (made-up test numbers)
T = 3.0 mm, L = 100.0 mm, measured flanges a = 51.9 mm and b = 53.0 mm, measured R = 3.8 mm, A = 90°.
BD = 51.9 + 53.0 − 100.0 = 4.9 mm. OSSB = 3.8 + 3.0 = 6.8 mm. BA = 2 × 6.8 − 4.9 = 8.7 mm.
K = (8.7 / 1.5708 − 3.8) / 3.0 ≈ (5.54 − 3.8) / 3.0 ≈ 0.58. A plausible result; with your real measurements the number will be yours.

## Bend tables

Rather than a single K-factor, most CAD accepts a **table** (thickness × radius × angle → BD or BA). It is the most reliable method in production: every row comes from a real test bend.

## Common mistakes

- Confusing bend angle with included angle (180° − bend angle).
- Measuring flanges inside instead of outside.
- Using one “generic” K-factor for every thickness.
- Forgetting that rolling direction affects minimum radius and cracking.

## FAQ

### What default K should I use?
The SolidWorks default K-factor is 0.5; it is a software starting point, not a measurement. Do a test bend.

### K-factor or bend deduction?
Both describe the same reality. Deduction is more intuitive on the shop floor; K-factor transfers better to other angles.

## For Michaël to review

- Your real bend tables (material, thickness, V, BD).
- A worked example from a real test bend to replace the made-up one.

## Sources

- [SolidWorks Help — Bend Allowance](https://help.solidworks.com/2025/english/SolidWorks/sldworks/c_Bend_Allowance.htm), consulted November 26, 2026.
- [SolidWorks Help — K-Factor](https://help.solidworks.com/2025/english/SolidWorks/sldworks/c_K-Factor.htm).
- [The Fabricator — Six steps for selecting the right die for press brakes (S. Benson)](https://www.thefabricator.com/thefabricator/article/bending/six-steps-for-selecting-the-right-die-for-press-brakes).
