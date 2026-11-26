---
id: inventor
hub: software
group: cad
order: 30
mono: Iv
nav: Inventor | Inventor
kicker: Logiciel · CAO | Software · CAD
level: intermediaire
schema: HowTo
tags: inventor, sheet metal, unfold rule, k-factor, flat pattern, dxf, inventor cam, autodesk
related: solidworks-sheet-metal, bend-allowance, dxf-best-practices, fusion-cam
fr_slug: inventor-tolerie-cam
en_slug: inventor-sheet-metal-and-cam
fr_title: Autodesk Inventor : règles de tôlerie, déplié, DXF et Inventor CAM
en_title: Autodesk Inventor: sheet metal rules, flat pattern, DXF and Inventor CAM
fr_desc: Styles et règles de dépliage (facteur K, tableau de pliage), création du déplié, export de la face dépliée en DXF avec calques, et où se situe Inventor CAM par rapport à Fusion.
en_desc: Sheet metal styles and unfold rules (K-factor, bend table), creating the flat pattern, exporting the flat face to DXF with layers, and where Inventor CAM sits compared to Fusion.
---
=== fr
Inventor gère la tôlerie par des **règles** centralisées : une fois la règle de l’atelier définie, tous les dépliés l’utilisent. C’est l’étape qui décide si les pièces pliées tombent à la cote.

## 1. Règles de tôlerie et de dépliage

Dans **Valeurs par défaut de la tôlerie** (Sheet Metal Defaults), on choisit :

| Élément | Contenu |
|---|---|
| Règle de tôlerie | Matière, épaisseur, rayon de pliage, dégagements |
| Règle de dépliage | Facteur K linéaire, **tableau de pliage** ou équation personnalisée |

> [!TIP] Créez une règle par combinaison matière / épaisseur / outillage, avec les valeurs mesurées par votre plieur. Voir [Pliage et facteur K](/guides/pliage-k-factor/).

## 2. Modéliser et déplier

1. Créer la pièce avec le gabarit **Tôlerie**.
2. Fonctions natives : Face, Contour de face, Bord, Ourlet, Pli.
3. **Créer le déplié** (Create Flat Pattern) ; corriger les erreurs signalées.
4. Vérifier l’orientation et les dimensions du déplié.

## 3. Exporter en DXF

1. Dans le déplié, clic droit sur la face (ou sur « Déplié » dans le navigateur) → **Enregistrer une copie sous / Exporter la face en DXF**.
2. Choisir la version de DXF.
3. Onglet **Calques** : activer ou désactiver le contour extérieur, les contours intérieurs, les lignes de pliage haut et bas, les gravures, et leur donner un nom de calque.
4. Désactiver les calques inutiles pour la découpe (lignes tangentes, axes de pliage si non voulus).

> [!WARN] Exporter les lignes de pliage sur le même calque que la coupe risque de les faire couper. Gardez-les sur des calques dédiés, ou désactivez-les.

## 4. Inventor CAM

Inventor CAM (issu d’Inventor HSM) intègre la FAO dans Inventor, avec une logique proche de celle de [Fusion](/guides/fusion-fao-debuter/) : configuration, opérations 2D / 3D, simulation, post-traitement avec la même bibliothèque de posts Autodesk. Il est offert avec la **Product Design & Manufacturing Collection** ; vérifiez le niveau inclus dans votre abonnement.

## Liste de vérification

- [ ] Règle de dépliage de l’atelier appliquée
- [ ] Déplié sans erreur
- [ ] DXF : calques de coupe, de pliage et de gravure séparés
- [ ] Échelle 1:1 vérifiée dans un visualiseur

## FAQ

### Inventor ou Fusion pour un petit atelier ?
Inventor est fort en grosses assemblées et en tôlerie de production ; Fusion est plus abordable et intègre la FAO dans le même environnement. Le choix dépend surtout de vos clients et de leurs formats de fichiers.

## À valider en atelier (Michaël)

- Votre règle de dépliage et les calques DXF attendus par votre FAO.

## Sources

- [Autodesk — Aide Inventor : règles de tôlerie et de dépliage](https://help.autodesk.com/view/INVNTOR/2025/ENU/), consulté le 26 novembre 2026.
- [Autodesk — Inventor CAM](https://www.autodesk.com/products/inventor-cam/overview).
- [Autodesk — Product Design & Manufacturing Collection](https://www.autodesk.com/collections/product-design-manufacturing/overview).
=== en
Inventor handles sheet metal with centralized **rules**: once the shop’s rule is defined, every flat pattern uses it. That step decides whether bent parts come out to size.

## 1. Sheet metal and unfold rules

In **Sheet Metal Defaults**, you choose:

| Item | Contents |
|---|---|
| Sheet metal rule | Material, thickness, bend radius, reliefs |
| Unfold rule | Linear K-factor, **bend table** or custom equation |

> [!TIP] Create one rule per material / thickness / tooling combination, with values measured by your bender. See [Bend allowance and K-factor](/en/guides/bend-allowance-k-factor/).

## 2. Model and unfold

1. Create the part from the **Sheet Metal** template.
2. Native features: Face, Contour Flange, Flange, Hem, Bend.
3. **Create Flat Pattern**; fix any reported errors.
4. Check the flat pattern orientation and size.

## 3. Export to DXF

1. In the flat pattern, right-click the face (or “Flat Pattern” in the browser) → **Save Copy As / Export Face As DXF**.
2. Choose the DXF version.
3. **Layer** tab: turn the outer profile, inner profiles, bend up and down lines, and etching on or off, and name their layers.
4. Turn off layers not needed for cutting (tangent lines, bend centrelines if not wanted).

> [!WARN] Exporting bend lines on the same layer as the cut may get them cut. Keep them on dedicated layers or turn them off.

## 4. Inventor CAM

Inventor CAM (from Inventor HSM) builds CAM into Inventor, with logic close to [Fusion](/en/guides/fusion-cam-getting-started/): setup, 2D / 3D operations, simulation, posting with the same Autodesk post library. It is offered with the **Product Design & Manufacturing Collection**; check which level your subscription includes.

## Checklist

- [ ] Shop unfold rule applied
- [ ] Flat pattern without errors
- [ ] DXF: cut, bend and etch layers separate
- [ ] 1:1 scale checked in a viewer

## FAQ

### Inventor or Fusion for a small shop?
Inventor is strong in large assemblies and production sheet metal; Fusion is more affordable and builds CAM into the same environment. The choice depends mostly on your customers and their file formats.

## For Michaël to review

- Your unfold rule and the DXF layers your CAM expects.

## Sources

- [Autodesk — Inventor help: sheet metal and unfold rules](https://help.autodesk.com/view/INVNTOR/2025/ENU/), consulted November 26, 2026.
- [Autodesk — Inventor CAM](https://www.autodesk.com/products/inventor-cam/overview).
- [Autodesk — Product Design & Manufacturing Collection](https://www.autodesk.com/collections/product-design-manufacturing/overview).
