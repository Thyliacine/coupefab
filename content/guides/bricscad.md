---
id: bricscad
hub: software
group: cad
order: 22
mono: Bc
nav: BricsCAD → DXF | BricsCAD → DXF
kicker: Logiciel · DAO | Software · CAD
level: debutant
schema: HowTo
tags: bricscad, dxf, cad, sheetcam, plasma
related: dxf-best-practices, autocad-dxf, sheetcam, kerf
fr_slug: bricscad-dxf
en_slug: bricscad-to-clean-dxf
fr_title: De BricsCAD à un DXF propre pour la découpe
en_title: From BricsCAD to a clean DXF for cutting
fr_desc: DXFOUT, précision décimale, version DXF, objets mandataires et nettoyage : exporter depuis BricsCAD un DXF que SheetCam, ProNest ou n’importe quel FAO lit du premier coup.
en_desc: DXFOUT, decimal precision, DXF version, proxy objects and cleanup: export a DXF from BricsCAD that SheetCam, ProNest or any CAM reads the first time.
---
=== fr
Un DXF « propre » pour la découpe, c’est un fichier dont les **unités**, la **version** et la **géométrie** correspondent à ce que le FAO sait lire : contours fermés, aucun objet mandataire, précision utile à la machine. BricsCAD (Lite, Pro et plus) a tout ce qu’il faut ; voici la démarche.

## La commande officielle : DXFOUT

Selon l’aide BricsCAD, **DXFOUT** enregistre le dessin courant en DXF. Options documentées :

| Option | Ce qu’elle fait | Conseil découpe |
|---|---|---|
| Decimal places | 0 à 16 décimales | L’aide note que certaines machines CNC exigent **4 décimales** |
| Entities | N’exporte que la sélection (sinon tout) | Sélectionnez la géométrie de coupe seulement |
| Binary | Format binaire (sinon ASCII) | Restez en ASCII, plus tolérant en FAO |
| Version | Version DXF (par défaut la plus récente) | Une version plus ancienne peut aider un vieux FAO, mais peut perdre des entités |

La commande **EXPORT** existe aussi pour d’autres formats ; pour la découpe, DXFOUT est le point de départ officiel.

## Démarche pas à pas

1. **Confirmer les unités.** Tapez `UNITS` (ou vérifiez `INSUNITS`) : millimètres ou pouces, et notez-le pour l’import dans le FAO.
2. **Isoler la pièce.** Copiez la géométrie de coupe dans un dessin neuf ou sur un calque dédié ; laissez cartouche, cotes, hachures et textes de présentation.
3. **Ramener à plat.** Toute la géométrie doit être à Z = 0. Les objets 3D ou les blocs dynamiques posent problème à la plupart des FAO 2D.
4. **Fermer les contours.** Joignez lignes et arcs en polylignes fermées (`JOIN` ou `PEDIT` → Join). Un contour ouvert ne reçoit pas de compensation de kerf.
5. **Supprimer les doublons.** Les traits superposés donnent deux passes au même endroit. Nettoyez avec `OVERKILL` si disponible dans votre édition, sinon à la main.
6. **Convertir les objets mandataires.** S’il y a des objets AEC ou personnalisés, l’aide BricsCAD documente `EXPORTTOAUTOCAD` pour les convertir en blocs natifs ; `WBLOCK` peut aussi extraire une géométrie utilisable. Puis explosez les blocs (`EXPLODE`).
7. **Purger.** `PURGE` des définitions inutilisées, y compris imbriquées ; fusionnez ou supprimez les calques résiduels.
8. **Organiser les calques.** Un calque par fonction (COUPE, MARQUAGE, PLI, GRAVURE) selon la convention de l’atelier ; le FAO peut alors associer une opération par calque.
9. **Exporter.** `DXFOUT` → ASCII, 4 décimales si votre machine l’exige, option Entities pour ne prendre que la pièce.
10. **Vérifier à la réouverture.** Rouvrez le DXF (ou importez-le dans le FAO) et mesurez une cote connue.

## Liste de vérification avant le FAO

- [ ] Unités confirmées (mm ou po) et notées pour l’import
- [ ] Géométrie 2D à Z = 0, contours fermés
- [ ] Aucun trait en double, aucun objet mandataire, blocs explosés
- [ ] Calques séparés : coupe, marquage, pli, gravure
- [ ] Cartouche, cotes et hachures exclus de l’export
- [ ] ASCII, version et décimales choisies

## Erreurs fréquentes

| Symptôme dans le FAO | Cause | Correctif dans BricsCAD |
|---|---|---|
| Pièce à la mauvaise échelle | Unités du dessin | `UNITS` / `INSUNITS`, réexporter |
| Pas de compensation de kerf | Contour ouvert | `JOIN` / `PEDIT`, vérifier les extrémités |
| Double passe, trait plus large | Doublons | `OVERKILL` ou suppression manuelle |
| Objets invisibles ou ignorés | Mandataires, blocs | `EXPORTTOAUTOCAD`, `EXPLODE` |
| Cercles en segments | Courbe approximée à l’export | Garder arcs et cercles natifs ; éviter les splines si le FAO les segmente mal |

## FAQ

### Faut-il exporter en R12 ?
Pas par défaut. Utilisez la version la plus récente que votre FAO lit correctement ; descendez seulement si l’import échoue, en vérifiant ce qui est perdu.

### Splines ou arcs ?
Les FAO 2D gèrent toujours lignes, arcs et cercles. Les splines sont souvent converties en petits segments, ce qui peut ralentir la machine. Préférez des arcs pour la géométrie fonctionnelle.

### Combien de décimales ?
L’aide BricsCAD signale que certaines machines CNC exigent 4 décimales. Au-delà, vous n’ajoutez que du poids au fichier.

## À valider en atelier (Michaël)

- Votre convention de calques réelle entre BricsCAD et SheetCam.
- La version DXF et le réglage de décimales qui marchent sur vos tables.
- Les commandes vraiment utilisées (DXFOUT, EXPORT, WBLOCK, EXPORTTOAUTOCAD) pour une pièce simple ou un assemblage.

## Sources

- [Aide BricsCAD — DXFOUT (V26)](https://help.bricsys.com/en-us/document/command-reference/d/dxfout-command?version=V26), consultée le 26 novembre 2026.
- [Aide BricsCAD — EXPORTTOAUTOCAD (V26)](https://help.bricsys.com/en-us/document/command-reference/e/exporttoautocad-command?version=V26).
- [Aide BricsCAD — EXPORT](https://helpcenter.bricsys.com/en-us/document/command-reference/e/export-command?version=V27).
=== en
A “clean” DXF for cutting is a file whose **units**, **version** and **geometry** match what the CAM can read: closed contours, no proxy objects, precision the machine can use. BricsCAD (Lite, Pro and up) has everything you need; here is the workflow.

## The official command: DXFOUT

According to the BricsCAD help, **DXFOUT** saves the current drawing as DXF. Documented options:

| Option | What it does | Cutting advice |
|---|---|---|
| Decimal places | 0 to 16 decimals | The help notes some CNC machines require **4 decimals** |
| Entities | Exports the selection only (otherwise everything) | Select the cut geometry only |
| Binary | Binary format (otherwise ASCII) | Stay in ASCII, more tolerant in CAM |
| Version | DXF version (default: most recent) | An older version may help an old CAM but can drop entities |

The **EXPORT** command covers other formats; for cutting, DXFOUT is the official starting point.

## Step by step

1. **Confirm units.** Type `UNITS` (or check `INSUNITS`): millimetres or inches, and note it for the CAM import.
2. **Isolate the part.** Copy the cut geometry to a new drawing or a dedicated layer; leave title block, dimensions, hatches and presentation text behind.
3. **Flatten.** All geometry at Z = 0. 3D objects or dynamic blocks trouble most 2D CAM.
4. **Close contours.** Join lines and arcs into closed polylines (`JOIN` or `PEDIT` → Join). An open contour gets no kerf compensation.
5. **Remove duplicates.** Overlapping lines give two passes in the same place. Clean with `OVERKILL` if your edition has it, otherwise by hand.
6. **Convert proxy objects.** For AEC or custom objects, the BricsCAD help documents `EXPORTTOAUTOCAD` to convert them to native blocks; `WBLOCK` can also extract usable geometry. Then explode blocks (`EXPLODE`).
7. **Purge.** `PURGE` unused definitions, nested ones included; merge or delete leftover layers.
8. **Organize layers.** One layer per function (CUT, MARK, BEND, ETCH) following shop convention; the CAM can then map one operation per layer.
9. **Export.** `DXFOUT` → ASCII, 4 decimals if your machine needs it, Entities option to take the part only.
10. **Check on reopen.** Reopen the DXF (or import it in CAM) and measure a known dimension.

## Pre-CAM checklist

- [ ] Units confirmed (mm or in) and noted for import
- [ ] 2D geometry at Z = 0, closed contours
- [ ] No duplicate lines, no proxy objects, blocks exploded
- [ ] Separate layers: cut, mark, bend, etch
- [ ] Title block, dimensions and hatches excluded
- [ ] ASCII, version and decimals chosen

## Common mistakes

| Symptom in CAM | Cause | Fix in BricsCAD |
|---|---|---|
| Part at the wrong scale | Drawing units | `UNITS` / `INSUNITS`, re-export |
| No kerf compensation | Open contour | `JOIN` / `PEDIT`, check endpoints |
| Double pass, wide line | Duplicates | `OVERKILL` or manual delete |
| Invisible or ignored objects | Proxies, blocks | `EXPORTTOAUTOCAD`, `EXPLODE` |
| Circles come in as segments | Curve approximated on export | Keep native arcs and circles; avoid splines if your CAM segments them badly |

## FAQ

### Should I export R12?
Not by default. Use the newest version your CAM reads correctly; step down only if import fails, and check what gets lost.

### Splines or arcs?
2D CAM always handles lines, arcs and circles. Splines are often converted to many tiny segments, which can slow the machine. Prefer arcs for functional geometry.

### How many decimals?
The BricsCAD help notes some CNC machines require 4 decimals. More only adds file weight.

## For Michaël to review

- Your actual BricsCAD → SheetCam layer convention.
- The DXF version and decimal setting that work on your tables.
- Which commands you really use (DXFOUT, EXPORT, WBLOCK, EXPORTTOAUTOCAD) for a simple part versus an assembly.

## Sources

- [BricsCAD Help — DXFOUT (V26)](https://help.bricsys.com/en-us/document/command-reference/d/dxfout-command?version=V26), consulted November 26, 2026.
- [BricsCAD Help — EXPORTTOAUTOCAD (V26)](https://help.bricsys.com/en-us/document/command-reference/e/exporttoautocad-command?version=V26).
- [BricsCAD Help — EXPORT](https://helpcenter.bricsys.com/en-us/document/command-reference/e/export-command?version=V27).
