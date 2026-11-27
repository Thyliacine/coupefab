---
id: dxf-best-practices
hub: fundamentals
order: 10
nav: DXF : bonnes pratiques | DXF best practices
kicker: Fondamentaux · DAO/FAO | Fundamentals · CAD/CAM
level: debutant
schema: HowTo
tags: dxf, cad, cam, plasma, laser, waterjet, router, splines, layers, units
related: bricscad, autocad-dxf, solidworks-sheet-metal, sheetcam
fr_slug: dxf-bonnes-pratiques
en_slug: dxf-best-practices
fr_title: DXF pour la découpe : les règles qui évitent 90 % des problèmes
en_title: DXF for cutting: the rules that prevent 90% of problems
fr_desc: Unités, échelle 1:1, contours fermés, doublons, splines, calques, textes et petits détails : la liste de règles à suivre avant d’envoyer un DXF à un FAO ou à un sous-traitant de découpe.
en_desc: Units, 1:1 scale, closed contours, duplicates, splines, layers, text and tiny features: the rules to follow before sending a DXF to CAM or to a cutting job shop.
---
=== fr
Le DXF (Drawing Exchange Format, défini par Autodesk) reste le format d’échange universel pour la découpe 2D. Il est simple… et donc facile à mal remplir. Que vous l’envoyiez à votre propre FAO ou à un atelier de découpe, ces règles évitent l’essentiel des allers-retours.

## Les 10 règles

| # | Règle | Pourquoi |
|---|---|---|
| 1 | Échelle **1:1**, unités déclarées (mm ou po) | Le DXF ne garantit pas que l’unité sera bien lue |
| 2 | Une pièce par fichier (ou une par calque, si convenu) | Évite les confusions de quantités |
| 3 | **Contours fermés** | Sans contour fermé, pas de compensation de kerf ni d’intérieur/extérieur |
| 4 | **Aucun doublon** | Deux traits superposés = deux passes |
| 5 | Arcs et cercles natifs plutôt que splines ou polylignes segmentées | Mouvements fluides, fichiers légers |
| 6 | Géométrie à **Z = 0**, pas de 3D | Les FAO 2D ignorent ou rejettent le reste |
| 7 | Rien d’autre que la géométrie de coupe | Cotes, cartouche, hachures = coupes fantômes |
| 8 | Calques par fonction (coupe, marquage, pli) | Une opération FAO par calque |
| 9 | Textes convertis en géométrie si on doit les couper | Une police absente chez le découpeur change tout |
| 10 | Détails réalisables par le procédé | Un trou plus petit que l’épaisseur ne sort pas propre au plasma |

## Démarche de contrôle

1. **Rouvrir le DXF exporté** (pas le fichier source) dans un visualiseur ou le FAO.
2. **Mesurer** une cote connue : la pièce est-elle à la bonne taille ?
3. **Sélectionner tout** et compter les entités : un nombre anormal trahit des segments ou des doublons.
4. **Vérifier la fermeture** : la plupart des FAO signalent les contours ouverts à l’import (SheetCam les affiche différemment).
5. **Vérifier les calques** et leur nom.
6. **Contrôler les petits détails** par rapport au procédé et à l’épaisseur.

## Petits détails et procédé

Chaque procédé a ses limites : plasma (saignée plus large, biseau, petits trous coniques), laser fibre (saignée fine, détails fins possibles), jet d’eau (conicité selon la vitesse), routeur (rayon d’outil dans les coins intérieurs). Les fabricants publient des recommandations ; en l’absence de données, testez sur un coupon. Voir les guides [plasma](/guides/decoupe-plasma-cnc/), [laser fibre](/guides/laser-fibre/), [jet d’eau](/guides/jet-d-eau/) et [routeur](/guides/routeur-cnc/).

> [!TIP] Au routeur, un coin intérieur vif est impossible : il aura au minimum le rayon de la fraise. Dessinez les coins intérieurs avec ce rayon, ou prévoyez un dégagement en « os de chien » (dogbone) pour les assemblages.

## Exporter depuis votre logiciel

- **BricsCAD** : [De BricsCAD à un DXF propre](/guides/bricscad-dxf/)
- **AutoCAD** : [Nettoyer un DXF dans AutoCAD](/guides/autocad-nettoyer-dxf/)
- **SolidWorks** : [Tôlerie, déplié et DXF](/guides/solidworks-tolerie-dxf/)
- **Inventor** : [Tôlerie et Inventor CAM](/guides/inventor-tolerie-cam/)
- **Onshape** : [Tôlerie et CAM Studio](/guides/onshape-tolerie-cam/)
- **Fusion** : export DXF depuis une esquisse ou un déplié — voir [Fusion FAO](/guides/fusion-fao-debuter/)

## Envoyer à un atelier de découpe

- [ ] DXF 1:1 + PDF coté de la pièce (le PDF fait foi pour les cotes critiques)
- [ ] Matière, grade, épaisseur et quantité dans le nom du fichier ou le courriel
- [ ] Côté visible ou sens de brossage indiqué
- [ ] Tolérances réellement nécessaires (pas « ±0 » partout)
- [ ] Pliage éventuel : déplié **et** pièce pliée, rayon et K-factor utilisés

## Erreurs fréquentes

- Exporter un fichier en pouces lu en millimètres (pièce 25,4 fois trop petite).
- Laisser la cote d’ensemble ou le cadre : le découpeur coupe un rectangle de plus.
- Splines exportées en centaines de segments : mouvement saccadé, temps de coupe allongé.
- Texte en police TrueType non convertie.

## FAQ

### Quelle version de DXF ?
La plus récente que le destinataire lit sans erreur. Une version ancienne (R12, par exemple) reste parfois demandée par de vieux logiciels, mais peut convertir ou perdre certaines entités.

### DXF ou DWG ?
Pour la découpe, DXF. Le DWG est natif à AutoCAD et moins universel en FAO.

## Sources

- [Autodesk — DXF Reference](https://help.autodesk.com/view/OARX/2025/ENU/?guid=GUID-235B22E0-A567-4CF6-92D3-38A2306D73F3), consulté le 26 novembre 2026.
- [Aide BricsCAD — DXFOUT](https://help.bricsys.com/en-us/document/command-reference/d/dxfout-command?version=V26).
- [SheetCam LLC — Support Manuals](https://sheetcamshop.myshopify.com/pages/support).
=== en
DXF (Drawing Exchange Format, defined by Autodesk) is still the universal exchange format for 2D cutting. It is simple… and therefore easy to fill badly. Whether it goes to your own CAM or to a cutting job shop, these rules prevent most back-and-forth.

## The 10 rules

| # | Rule | Why |
|---|---|---|
| 1 | **1:1** scale, units declared (mm or in) | DXF does not guarantee units are read correctly |
| 2 | One part per file (or one per layer, if agreed) | Avoids quantity mix-ups |
| 3 | **Closed contours** | No closed contour, no kerf compensation or inside/outside |
| 4 | **No duplicates** | Two overlapping lines = two passes |
| 5 | Native arcs and circles rather than splines or segmented polylines | Smooth motion, light files |
| 6 | Geometry at **Z = 0**, no 3D | 2D CAM ignores or rejects the rest |
| 7 | Nothing but cut geometry | Dimensions, title block, hatches = ghost cuts |
| 8 | Layers by function (cut, mark, bend) | One CAM operation per layer |
| 9 | Text exploded to geometry if it must be cut | A missing font at the job shop changes everything |
| 10 | Features the process can make | A hole smaller than the thickness will not come out clean on plasma |

## Check procedure

1. **Reopen the exported DXF** (not the source file) in a viewer or CAM.
2. **Measure** a known dimension: is the part the right size?
3. **Select all** and count entities: an odd count reveals segments or duplicates.
4. **Check closure**: most CAM flags open contours on import (SheetCam displays them differently).
5. **Check layers** and their names.
6. **Check small features** against the process and thickness.

## Small features and process

Every process has limits: plasma (wider kerf, bevel, tapered small holes), fiber laser (narrow kerf, fine detail possible), waterjet (taper depending on speed), router (tool radius in inside corners). Manufacturers publish guidance; without data, test on a coupon. See the [plasma](/en/guides/cnc-plasma-cutting/), [fiber laser](/en/guides/fiber-laser-cutting/), [waterjet](/en/guides/waterjet-cutting/) and [router](/en/guides/cnc-router/) guides.

> [!TIP] On a router a sharp inside corner is impossible: it will have at least the cutter radius. Draw inside corners with that radius, or add “dogbone” reliefs for joinery.

## Exporting from your software

- **BricsCAD**: [From BricsCAD to a clean DXF](/en/guides/bricscad-to-clean-dxf/)
- **AutoCAD**: [Cleaning up a DXF in AutoCAD](/en/guides/autocad-dxf-cleanup/)
- **SolidWorks**: [Sheet metal, flat pattern and DXF](/en/guides/solidworks-sheet-metal-flat-pattern-dxf/)
- **Inventor**: [Sheet metal and Inventor CAM](/en/guides/inventor-sheet-metal-and-cam/)
- **Onshape**: [Sheet metal and CAM Studio](/en/guides/onshape-sheet-metal-cam/)
- **Fusion**: DXF export from a sketch or flat pattern — see [Fusion CAM](/en/guides/fusion-cam-getting-started/)

## Sending to a cutting job shop

- [ ] 1:1 DXF + dimensioned PDF (the PDF governs critical dimensions)
- [ ] Material, grade, thickness and quantity in the file name or email
- [ ] Visible side or brushing direction stated
- [ ] Tolerances you really need (not “±0” everywhere)
- [ ] If bent: flat pattern **and** formed part, radius and K-factor used

## Common mistakes

- Exporting in inches and reading in millimetres (part 25.4 times too small).
- Leaving the overall border: the shop cuts one more rectangle.
- Splines exported as hundreds of segments: jerky motion, longer cut time.
- TrueType text not exploded.

## FAQ

### Which DXF version?
The newest one the recipient reads without errors. An old version (R12, for example) is sometimes still requested by legacy software, but may convert or drop some entities.

### DXF or DWG?
For cutting, DXF. DWG is native to AutoCAD and less universal in CAM.

## Sources

- [Autodesk — DXF Reference](https://help.autodesk.com/view/OARX/2025/ENU/?guid=GUID-235B22E0-A567-4CF6-92D3-38A2306D73F3), consulted November 26, 2026.
- [BricsCAD Help — DXFOUT](https://help.bricsys.com/en-us/document/command-reference/d/dxfout-command?version=V26).
- [SheetCam LLC — Support Manuals](https://sheetcamshop.myshopify.com/pages/support).
