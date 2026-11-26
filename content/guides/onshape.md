---
id: onshape
hub: software
group: cad
order: 40
mono: On
nav: Onshape | Onshape
kicker: Logiciel · CAO en ligne | Software · cloud CAD
level: debutant
schema: HowTo
tags: onshape, sheet metal, flat pattern, dxf, k-factor, cam studio, cloud cad, ptc
related: solidworks-sheet-metal, bend-allowance, dxf-best-practices, fusion-cam
fr_slug: onshape-tolerie-cam
en_slug: onshape-sheet-metal-cam
fr_title: Onshape : tôlerie, export DXF du déplié et CAM Studio
en_title: Onshape: sheet metal, flat pattern DXF export and CAM Studio
fr_desc: Modèle de tôlerie avec facteur K, vue dépliée et tableau de pliage, export DXF/DWG du déplié, puis ce que couvre CAM Studio selon le forfait Onshape.
en_desc: Sheet metal model with K-factor, flat view and bend table, DXF/DWG export of the flat pattern, then what CAM Studio covers depending on the Onshape plan.
---
=== fr
Onshape est une CAO entièrement dans le navigateur : pas d’installation, historique de versions intégré, partage par lien. Sa tôlerie est simple et son déplié est **toujours à jour**, affiché à côté du modèle 3D.

## 1. Créer un modèle de tôlerie

1. Fonction **Modèle de tôlerie** (Sheet metal model) à partir d’une esquisse ou en convertissant un solide.
2. Régler **épaisseur**, **rayon de pliage**, **facteur K**, type de dégagement.
3. Ajouter des **brides** (Flange), **ourlets** (Hem), **plis** (Bend), **onglets** (Tab).

> [!TIP] Le facteur K par défaut est une estimation. Entrez la valeur de votre plieur — voir [Pliage et facteur K](/guides/pliage-k-factor/).

## 2. Vue dépliée et tableau

Le panneau **Sheet metal** affiche le **déplié** et un **tableau** des plis (angle, rayon, sens). Une modification du modèle met le déplié à jour immédiatement.

## 3. Exporter le DXF

1. Dans la vue dépliée, clic droit sur le déplié → **Exporter en DXF/DWG** (ou via le tableau de tôlerie).
2. Choisir unités et version.
3. Vérifier dans un visualiseur que les lignes de pliage sont sur un calque séparé ou absentes pour la découpe.

Pour un ensemble de pièces, une **mise en plan** de la vue dépliée peut aussi être exportée en DXF, à l’échelle 1:1.

## 4. CAM Studio

| | Ce qu’il faut savoir |
|---|---|
| Lancement | Janvier 2025 |
| Inclus avec | Forfaits **Professional** et **Enterprise** (pas Standard ni Free) |
| Capacités | Usinage 2,5 et 3 axes |
| 4 et 5 axes | **CAM Studio Advanced**, offre séparée |

Comme dans [Fusion](/guides/fusion-fao-debuter/), la FAO est associative : le parcours suit les modifications du modèle.

## Liste de vérification

- [ ] Facteur K et rayon de l’atelier
- [ ] Déplié vérifié (cotes globales)
- [ ] DXF sans lignes de pliage sur le calque de coupe
- [ ] Unités du DXF confirmées

## FAQ

### La version gratuite d’Onshape convient-elle à un atelier ?
Le forfait Free rend les documents **publics** et est destiné à un usage non commercial. Pour des pièces de clients, prenez un forfait payant.

## À valider en atelier (Michaël)

- Retour sur l’export DXF Onshape avec votre FAO.

## Sources

- [Onshape — Sheet metal (aide)](https://cad.onshape.com/help/Content/sheetmetal.htm), consulté le 26 novembre 2026.
- [Onshape — CAM Studio](https://www.onshape.com/en/features/cam-studio).
- [Onshape — Forfaits et tarifs](https://www.onshape.com/en/pricing).
=== en
Onshape is CAD entirely in the browser: no install, built-in version history, link sharing. Its sheet metal is simple and its flat pattern is **always up to date**, shown next to the 3D model.

## 1. Create a sheet metal model

1. **Sheet metal model** feature from a sketch or by converting a solid.
2. Set **thickness**, **bend radius**, **K-factor**, relief type.
3. Add **Flanges**, **Hems**, **Bends**, **Tabs**.

> [!TIP] The default K-factor is an estimate. Enter your bender’s value — see [Bend allowance and K-factor](/en/guides/bend-allowance-k-factor/).

## 2. Flat view and table

The **Sheet metal** panel shows the **flat pattern** and a **table** of bends (angle, radius, direction). A model change updates the flat immediately.

## 3. Export the DXF

1. In the flat view, right-click the flat pattern → **Export as DXF/DWG** (or through the sheet metal table).
2. Choose units and version.
3. Check in a viewer that bend lines are on a separate layer, or absent for cutting.

For a set of parts, a **drawing** of the flat view can also be exported to DXF at 1:1.

## 4. CAM Studio

| | What to know |
|---|---|
| Launch | January 2025 |
| Included with | **Professional** and **Enterprise** plans (not Standard or Free) |
| Capabilities | 2.5- and 3-axis machining |
| 4- and 5-axis | **CAM Studio Advanced**, separate offer |

As in [Fusion](/en/guides/fusion-cam-getting-started/), CAM is associative: the toolpath follows model changes.

## Checklist

- [ ] Shop K-factor and radius
- [ ] Flat pattern checked (overall dimensions)
- [ ] DXF without bend lines on the cut layer
- [ ] DXF units confirmed

## FAQ

### Is Onshape’s free plan fine for a shop?
The Free plan makes documents **public** and is meant for non-commercial use. For customer parts, take a paid plan.

## For Michaël to review

- Feedback on Onshape DXF export with your CAM.

## Sources

- [Onshape — Sheet metal (help)](https://cad.onshape.com/help/Content/sheetmetal.htm), consulted November 26, 2026.
- [Onshape — CAM Studio](https://www.onshape.com/en/features/cam-studio).
- [Onshape — Plans and pricing](https://www.onshape.com/en/pricing).
