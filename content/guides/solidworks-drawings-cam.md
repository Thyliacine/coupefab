---
id: solidworks-drawings-cam
hub: software
group: cam
order: 40
mono: SW
nav: SOLIDWORKS CAM et mises en plan | SOLIDWORKS CAM and drawings
kicker: Logiciel · FAO | Software · CAM
level: intermediaire
schema: Article
tags: solidworks, solidworks cam, camworks, drawings, mbd, technology database, tolerance based machining, setup sheet
related: solidworks-sheet-metal, tolerances, post-processors, mastercam-2d
fr_slug: solidworks-mises-en-plan-cam
en_slug: solidworks-drawings-and-cam
fr_title: SOLIDWORKS : mises en plan pour l’atelier et SOLIDWORKS CAM (Standard ou Professional)
en_title: SOLIDWORKS: shop-ready drawings and SOLIDWORKS CAM (Standard or Professional)
fr_desc: Ce qu’une mise en plan doit contenir pour l’usinage et le pliage, la différence entre SOLIDWORKS CAM Standard et Professional, l’usinage basé sur les fonctions et la base de données technologique.
en_desc: What a drawing must contain for machining and bending, the difference between SOLIDWORKS CAM Standard and Professional, feature-based machining and the technology database.
---
=== fr
SOLIDWORKS sert à deux choses en atelier : produire des **mises en plan** que l’atelier peut lire sans appeler le dessinateur, et, avec **SOLIDWORKS CAM**, programmer l’usinage directement depuis le modèle.

## Une mise en plan prête pour l’atelier

| Élément | Pourquoi |
|---|---|
| Matière, nuance, épaisseur, fini | Achat et choix des paramètres — voir [Nuances](/guides/nuances-metaux/) |
| Tolérance générale (ex. ISO 2768-m) | Évite de coter chaque tolérance — voir [Tolérances](/guides/tolerances-cnc/) |
| Cotes fonctionnelles seulement tolérancées serré | Le serré coûte cher |
| Vue dépliée et tableau de pliage (tôlerie) | Angle, sens, rayon, ordre |
| Révision et date | L’atelier doit savoir quelle version il fabrique |
| Ébavurage, arêtes vives | Une note évite des retours |

> [!TIP] Une cote sans tolérance n’est pas « exacte » : elle relève de la tolérance générale indiquée dans le cartouche. Sans tolérance générale, l’atelier devine.

## SOLIDWORKS CAM : Standard ou Professional

| | Standard | Professional |
|---|---|---|
| Disponibilité | Inclus avec un abonnement SOLIDWORKS actif | Achat séparé |
| Fraisage 2,5 axes | Oui | Oui |
| Fraisage 3 axes, usinage haute vitesse (VoluMill) | — | Oui |
| Tournage | — | Oui |
| Usinage d’assemblages, 3+2 | — | Oui |

SOLIDWORKS CAM est propulsé par la technologie **CAMWorks** ; HCL commercialise aussi CAMWorks comme produit distinct, avec davantage d’options.

## Comment SOLIDWORKS CAM raisonne

1. **Reconnaissance des fonctions** : le logiciel identifie poches, trous, bossages, contours dans le modèle.
2. **Base de données technologique (TechDB)** : des règles associent chaque type de fonction à des opérations, des outils et des paramètres.
3. **Usinage basé sur les tolérances** (TBM) : les tolérances et états de surface du modèle orientent le choix des opérations (par exemple alésage plutôt que perçage).
4. Génération des parcours, simulation, post-traitement.

> [!NOTE] La qualité du résultat dépend surtout de la TechDB. Investir quelques jours à y entrer vos outils, matières et stratégies est ce qui rend le logiciel rapide ensuite.

## Erreurs fréquentes

| Erreur | Correctif |
|---|---|
| TechDB par défaut jamais adaptée | Entrer vos outils et vos avances |
| Mauvaise machine ou post | Choisir la machine avant de générer |
| Plan sans tolérance générale | Ajouter la norme dans le cartouche |

## FAQ

### SOLIDWORKS CAM remplace-t-il Mastercam ?
Pour des pièces prismatiques simples en 2,5 axes, il peut suffire. Pour du 3 axes avancé, du tournage poussé ou du multiaxe, comparez avec [Mastercam](/guides/mastercam-parcours-2d-dynamic/).

## À valider en atelier (Michaël)

- Modèle de cartouche et notes générales que vous recommandez.

## Sources

- [SOLIDWORKS — SOLIDWORKS CAM](https://www.solidworks.com/product/solidworks-cam), consulté le 26 novembre 2026.
- [HCL CAMWorks](https://camworks.com/).
- [ISO 2768-1 — Tolérances générales](https://www.iso.org/standard/7748.html).
=== en
SOLIDWORKS does two jobs in a shop: produce **drawings** the shop can read without calling the designer, and, with **SOLIDWORKS CAM**, program machining straight from the model.

## A shop-ready drawing

| Item | Why |
|---|---|
| Material, grade, thickness, finish | Purchasing and parameter choice — see [Metal grades](/en/guides/metal-grades/) |
| General tolerance (e.g., ISO 2768-m) | Avoids tolerancing every dimension — see [Tolerances](/en/guides/cnc-tolerances/) |
| Tight tolerances on functional dimensions only | Tight is expensive |
| Flat view and bend table (sheet metal) | Angle, direction, radius, order |
| Revision and date | The shop must know which version it is making |
| Deburr, sharp edges | A note avoids returns |

> [!TIP] A dimension without a tolerance is not “exact”: it falls under the general tolerance in the title block. Without a general tolerance, the shop guesses.

## SOLIDWORKS CAM: Standard or Professional

| | Standard | Professional |
|---|---|---|
| Availability | Included with an active SOLIDWORKS subscription | Separate purchase |
| 2.5-axis milling | Yes | Yes |
| 3-axis milling, high-speed machining (VoluMill) | — | Yes |
| Turning | — | Yes |
| Assembly machining, 3+2 | — | Yes |

SOLIDWORKS CAM is powered by **CAMWorks** technology; HCL also sells CAMWorks as a separate product with more options.

## How SOLIDWORKS CAM thinks

1. **Feature recognition**: the software identifies pockets, holes, bosses and contours in the model.
2. **Technology database (TechDB)**: rules map each feature type to operations, tools and parameters.
3. **Tolerance-based machining** (TBM): model tolerances and surface finishes drive operation choice (for example boring instead of drilling).
4. Toolpath generation, simulation, posting.

> [!NOTE] Result quality depends mostly on the TechDB. Spending a few days entering your tools, materials and strategies is what makes the software fast afterwards.

## Common mistakes

| Mistake | Fix |
|---|---|
| Default TechDB never adapted | Enter your tools and feeds |
| Wrong machine or post | Pick the machine before generating |
| Drawing without a general tolerance | Add the standard in the title block |

## FAQ

### Does SOLIDWORKS CAM replace Mastercam?
For simple 2.5-axis prismatic parts, it can be enough. For advanced 3-axis, heavy turning or multi-axis, compare with [Mastercam](/en/guides/mastercam-2d-toolpaths-dynamic-milling/).

## For Michaël to review

- The title block template and general notes you recommend.

## Sources

- [SOLIDWORKS — SOLIDWORKS CAM](https://www.solidworks.com/product/solidworks-cam), consulted November 26, 2026.
- [HCL CAMWorks](https://camworks.com/).
- [ISO 2768-1 — General tolerances](https://www.iso.org/standard/7748.html).
