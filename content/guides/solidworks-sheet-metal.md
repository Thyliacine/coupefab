---
id: solidworks-sheet-metal
hub: software
group: cad
order: 10
mono: SW
nav: SOLIDWORKS tôlerie | SOLIDWORKS sheet metal
kicker: Logiciel · CAO | Software · CAD
level: intermediaire
schema: HowTo
tags: solidworks, sheet metal, flat pattern, dxf, dwg, k-factor, bend table, bend deduction, base flange, bend lines, mapping
related: bend-allowance, dxf-best-practices, press-brake, solidworks-drawings-cam
fr_slug: solidworks-tolerie-dxf
en_slug: solidworks-sheet-metal-flat-pattern-dxf
fr_title: SOLIDWORKS tôlerie : paramètres de pliage, déplié et export DXF propre pour la découpe
en_title: SOLIDWORKS sheet metal: bend parameters, flat pattern and a clean DXF for cutting
fr_desc: Tôle de base, facteur K, tableau de pliage ou déduction, déplié, puis export DXF/DWG du déplié avec lignes de pliage sur leur propre calque : la démarche pour envoyer un fichier qui se coupe du premier coup.
en_desc: Base flange, K-factor, bend table or deduction, flat pattern, then DXF/DWG export of the flat pattern with bend lines on their own layer: the workflow to send a file that cuts right the first time.
---
=== fr
Un déplié SOLIDWORKS n’est juste que si les paramètres de pliage correspondent à l’atelier qui va plier. Le DXF n’est utile que s’il contient la bonne géométrie, sur les bons calques, à l’échelle 1:1.

## 1. Paramètres de tôlerie

Dans la fonction **Tôle de base / languette** (Base Flange/Tab), ou dans les paramètres de la fonction Tôlerie :

| Paramètre | Ce qu’il faut y mettre |
|---|---|
| Épaisseur | L’épaisseur réelle (calibre converti en mm ou po) |
| Rayon de pliage | Le rayon intérieur que **l’outillage de l’atelier** produit |
| Tolérance de pliage | Facteur K, tableau de pliage, valeur de tolérance ou de déduction |
| Dégagement de pliage | Rectangulaire, oblong ou déchirure selon la pièce |

> [!TIP] Demandez à votre plieur son **facteur K ou son tableau de déduction** pour la matière, l’épaisseur et l’ouverture de vé utilisées. Un facteur K générique donne un déplié approximatif. Voir [Pliage et facteur K](/guides/pliage-k-factor/).

Les **gabarits de tôlerie** (sheet metal gauge tables) permettent de lier épaisseur, rayon et facteur K par matière, pour que tout le bureau utilise les mêmes valeurs.

## 2. Modéliser pour la fabrication

- Plis de rayon constant, pas de trous trop près d’une ligne de pliage (règles dans [Pliage](/guides/pliage-k-factor/) et [Presse plieuse](/guides/presse-plieuse/)).
- Fonctions de tôlerie natives (Bord, Ourlet, Pli esquissé) plutôt que des volumes convertis.
- Vérifier que la pièce se **déplie** sans erreur (fonction Déplier/Mise à plat).

## 3. Exporter le déplié en DXF/DWG

1. Dans l’arbre de création, clic droit sur **État déplié** (Flat Pattern) → **Exporter en DXF/DWG**, ou Fichier → Enregistrer sous → DXF.
2. Dans le gestionnaire *Sortie DXF/DWG*, choisir **Tôlerie**.
3. Entités à exporter : **Géométrie**, et **Lignes de pliage** si le plieur les veut. Décocher Lignes de pliage pour un fichier de découpe seule.
4. Pour séparer les plis vers le haut et vers le bas : Options → *Mappage personnalisé SOLIDWORKS vers DXF/DWG* → Activer, puis assigner les entités « lignes de pliage – haut » et « – bas » à des calques distincts.
5. Vérifier l’aperçu, enregistrer.

> [!WARN] Depuis SOLIDWORKS 2022, les lignes de pliage ne vont plus automatiquement dans un calque BEND : sans mappage, elles peuvent arriver mélangées à la géométrie. Un logiciel de découpe risque alors de les couper. Créez un fichier de mappage et réutilisez-le.

## 4. Vérifier le DXF avant de l’envoyer

- [ ] Unités et échelle 1:1 (mesurer une cote connue)
- [ ] Contours fermés, sans doublons
- [ ] Lignes de pliage sur leur propre calque (ou absentes)
- [ ] Pas de cotes, cartouche ni texte dans le fichier de découpe
- [ ] Gravures sur un calque séparé

Voir [DXF : bonnes pratiques](/guides/dxf-bonnes-pratiques/).

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Facteur K par défaut | Pièce pliée hors cote |
| Rayon modélisé ≠ rayon d’atelier | Longueurs de bord fausses |
| Lignes de pliage non mappées | Coupées par erreur |
| Export d’une vue de mise en plan à l’échelle | DXF pas à 1:1 |

## FAQ

### Faut-il une mise en plan pour exporter le déplié ?
Non. L’export direct depuis la pièce suffit pour la découpe. La mise en plan reste utile pour le pliage (angles, sens, cotes) — voir [SOLIDWORKS mises en plan et FAO](/guides/solidworks-mises-en-plan-cam/).

## À valider en atelier (Michaël)

- Votre facteur K ou tableau de pliage réel par matière et épaisseur.

## Sources

- [SOLIDWORKS Help — Exporting sheet metal parts to DXF or DWG files](https://help.solidworks.com/2024/english/SolidWorks/sldworks/c_exporting_to_dxf_or_dwg_files.htm), consulté le 26 novembre 2026.
- [SOLIDWORKS Help — Bend allowance](https://help.solidworks.com/2024/english/SolidWorks/sldworks/c_Bend_Allowance.htm).
- [SendCutSend — Mapping bend lines in SOLIDWORKS (changement 2022)](https://sendcutsend.com/blog/how-to-map-bend-lines-into-layers-and-linetypes-in-solidworks/).
=== en
A SOLIDWORKS flat pattern is only right if the bend parameters match the shop that will bend it. A DXF is only useful if it holds the right geometry, on the right layers, at 1:1 scale.

## 1. Sheet metal parameters

In the **Base Flange/Tab** feature, or in the Sheet-Metal feature parameters:

| Parameter | What to enter |
|---|---|
| Thickness | The real thickness (gauge converted to mm or in) |
| Bend radius | The inside radius **the shop’s tooling** produces |
| Bend allowance | K-factor, bend table, allowance or deduction value |
| Auto relief | Rectangular, obround or tear depending on the part |

> [!TIP] Ask your bender for their **K-factor or deduction table** for the material, thickness and V-opening used. A generic K-factor gives an approximate flat. See [Bend allowance and K-factor](/en/guides/bend-allowance-k-factor/).

**Sheet metal gauge tables** link thickness, radius and K-factor per material so the whole office uses the same values.

## 2. Model for manufacturing

- Constant-radius bends, no holes too close to a bend line (rules in [Bend allowance](/en/guides/bend-allowance-k-factor/) and [Press brake](/en/guides/press-brake-bending/)).
- Native sheet metal features (Edge Flange, Hem, Sketched Bend) rather than converted solids.
- Check the part **flattens** without error (Flatten).

## 3. Export the flat pattern to DXF/DWG

1. In the FeatureManager tree, right-click **Flat-Pattern** → **Export to DXF/DWG**, or File → Save As → DXF.
2. In the *DXF/DWG Output* PropertyManager, pick **Sheet metal**.
3. Entities to export: **Geometry**, and **Bend lines** if the bender wants them. Clear Bend lines for a cut-only file.
4. To separate up and down bends: Options → *Custom Map SOLIDWORKS to DXF/DWG* → Enable, then assign “Bend lines – up direction” and “– down direction” to separate layers.
5. Check the preview, save.

> [!WARN] Since SOLIDWORKS 2022, bend lines no longer go to a BEND layer by default: without mapping, they may land mixed with geometry. Cutting software may then cut them. Create a map file and reuse it.

## 4. Check the DXF before sending

- [ ] Units and 1:1 scale (measure a known dimension)
- [ ] Closed contours, no duplicates
- [ ] Bend lines on their own layer (or absent)
- [ ] No dimensions, title block or text in the cut file
- [ ] Etching on a separate layer

See [DXF best practices](/en/guides/dxf-best-practices/).

## Common mistakes

| Mistake | Consequence |
|---|---|
| Default K-factor | Bent part out of tolerance |
| Modelled radius ≠ shop radius | Wrong flange lengths |
| Unmapped bend lines | Cut by mistake |
| Exporting a scaled drawing view | DXF not 1:1 |

## FAQ

### Do I need a drawing to export the flat?
No. Direct export from the part is enough for cutting. A drawing remains useful for bending (angles, direction, dimensions) — see [SOLIDWORKS drawings and CAM](/en/guides/solidworks-drawings-and-cam/).

## For Michaël to review

- Your real K-factor or bend table per material and thickness.

## Sources

- [SOLIDWORKS Help — Exporting sheet metal parts to DXF or DWG files](https://help.solidworks.com/2024/english/SolidWorks/sldworks/c_exporting_to_dxf_or_dwg_files.htm), consulted November 26, 2026.
- [SOLIDWORKS Help — Bend allowance](https://help.solidworks.com/2024/english/SolidWorks/sldworks/c_Bend_Allowance.htm).
- [SendCutSend — Mapping bend lines in SOLIDWORKS (2022 change)](https://sendcutsend.com/blog/how-to-map-bend-lines-into-layers-and-linetypes-in-solidworks/).
