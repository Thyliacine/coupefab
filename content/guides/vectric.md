---
id: vectric
hub: software
group: cam
order: 60
mono: Vc
nav: Vectric VCarve / Aspire | Vectric VCarve / Aspire
kicker: Logiciel · FAO routeur | Software · router CAM
level: debutant
schema: HowTo
tags: vectric, vcarve, aspire, cut2d, router, v-carving, signs, tiling, toolpaths, post processor
related: cnc-router, feeds-speeds, ugs-grbl, post-processors
fr_slug: vectric-vcarve-aspire
en_slug: vectric-vcarve-aspire
fr_title: Vectric VCarve et Aspire : choisir l’édition et réussir ses parcours au routeur
en_title: Vectric VCarve and Aspire: picking the edition and getting router toolpaths right
fr_desc: VCarve Desktop, VCarve Pro ou Aspire : ce qui les distingue (taille de travail, 3D), la configuration du travail, les parcours profil, poche et V-carving, et le choix du post pour votre routeur.
en_desc: VCarve Desktop, VCarve Pro or Aspire: what sets them apart (job size, 3D), job setup, profile, pocket and V-carving toolpaths, and choosing the post for your router.
---
=== fr
Les logiciels **Vectric** sont la référence chez les utilisateurs de routeurs CNC pour l’enseigne, l’ébénisterie et la décoration : dessin 2D, parcours et post-traitement dans un seul programme.

## Quelle édition

| Édition | Taille de travail | Ce qu’elle ajoute |
|---|---|---|
| VCarve Desktop | Limitée à **24 × 24 po** (pavage possible pour plus grand) | Dessin 2D, parcours 2D et V-carving, import de modèles 3D |
| VCarve Pro | **Illimitée** | Pavage avancé, imbrication, usage production |
| Aspire | Illimitée | **Modélisation 3D** (reliefs) en plus de VCarve Pro |

Les licences sont perpétuelles ; vérifiez sur le site de Vectric les conditions de mise à jour actuelles.

## Démarche

1. **Configuration du travail** : simple ou double face, dimensions et épaisseur du matériau, origine XY (coin ou centre) et **zéro Z** (dessus du matériau ou table).
2. Dessiner ou importer (DXF, SVG, PDF, images).
3. **Parcours** :
   - **Profil** (contour) : intérieur, extérieur ou sur la ligne ; passes ; **ponts** (tabs) pour tenir les pièces.
   - **Poche** : évidement plat.
   - **V-carving** : gravure en V à profondeur variable selon la largeur du trait.
   - **Perçage**, **Texture**, **Usinage 3D** (Aspire, ou modèles importés).
4. **Prévisualiser** le résultat en 3D.
5. **Enregistrer le parcours** avec le **post** de votre machine.

> [!TIP] Les ponts (tabs) empêchent la pièce de bouger au dernier passage. Prévoyez-en au moins deux ou trois par pièce, plus grands sur les matériaux légers.

## Choisir le post

Vectric fournit une longue liste de posts par marque de machine et de commande (grbl, Mach, contrôleurs de fabricants). Choisissez celui de votre machine et de vos unités (mm ou po), avec ou sans changement d’outil. Voir [Post-processeurs](/guides/post-processeurs/).

## Erreurs fréquentes

| Erreur | Correctif |
|---|---|
| Zéro Z au dessus du matériau dans le logiciel, sur la table dans la machine | Utiliser la même référence partout |
| Épaisseur du matériau mal mesurée | Mesurer au pied à coulisse à plusieurs endroits |
| Pas de ponts | Pièce arrachée en fin de coupe |
| Mauvais post (unités) | Pièce à l’échelle 25,4 |

## FAQ

### Puis-je passer de VCarve Desktop à Pro plus tard ?
Vectric propose des mises à niveau entre éditions ; consultez leur page de prix pour les conditions.

## À valider en atelier (Michaël)

- Vos réglages types de ponts et de passes pour le contreplaqué et le MDF.

## Sources

- [Vectric — Comparaison des produits](https://www.vectric.com/compare/), consulté le 26 novembre 2026.
- [Vectric — VCarve Desktop](https://www.vectric.com/products/vcarve-desktop).
- [Vectric — Aspire](https://www.vectric.com/products/aspire/).
=== en
**Vectric** software is the go-to for CNC router users in signmaking, cabinetry and decor: 2D drawing, toolpaths and posting in one program.

## Which edition

| Edition | Job size | What it adds |
|---|---|---|
| VCarve Desktop | Limited to **24 × 24 in** (tiling for larger) | 2D drawing, 2D and V-carving toolpaths, 3D model import |
| VCarve Pro | **Unlimited** | Advanced tiling, nesting, production use |
| Aspire | Unlimited | **3D modelling** (reliefs) on top of VCarve Pro |

Licences are perpetual; check Vectric’s site for current update terms.

## Workflow

1. **Job setup**: single or double sided, material size and thickness, XY origin (corner or centre) and **Z zero** (material top or table).
2. Draw or import (DXF, SVG, PDF, images).
3. **Toolpaths**:
   - **Profile**: inside, outside or on the line; passes; **tabs** to hold parts.
   - **Pocket**: flat clearing.
   - **V-carving**: V engraving with depth varying with stroke width.
   - **Drilling**, **Texture**, **3D machining** (Aspire, or imported models).
4. **Preview** the result in 3D.
5. **Save toolpath** with your machine’s **post**.

> [!TIP] Tabs stop the part from moving on the final pass. Plan at least two or three per part, larger on light materials.

## Choosing the post

Vectric ships a long list of posts by machine brand and control (grbl, Mach, maker controllers). Pick the one for your machine and units (mm or in), with or without tool change. See [Post processors](/en/guides/post-processors/).

## Common mistakes

| Mistake | Fix |
|---|---|
| Z zero on material top in software, on the table at the machine | Use the same reference everywhere |
| Material thickness mismeasured | Measure with calipers in several places |
| No tabs | Part ripped loose at the end of the cut |
| Wrong post (units) | Part scaled by 25.4 |

## FAQ

### Can I move from VCarve Desktop to Pro later?
Vectric offers upgrades between editions; see their pricing page for terms.

## For Michaël to review

- Your typical tab and pass settings for plywood and MDF.

## Sources

- [Vectric — Product comparison](https://www.vectric.com/compare/), consulted November 26, 2026.
- [Vectric — VCarve Desktop](https://www.vectric.com/products/vcarve-desktop).
- [Vectric — Aspire](https://www.vectric.com/products/aspire/).
