---
id: autocad-dxf
hub: software
group: cad
order: 20
mono: AC
nav: AutoCAD (DXF) | AutoCAD (DXF)
kicker: Logiciel · CAO 2D | Software · 2D CAD
level: debutant
schema: HowTo
tags: autocad, dxf, dwg, overkill, join, pedit, purge, audit, splines, insunits, layers, cleanup
related: dxf-best-practices, bricscad, sheetcam, nesting
fr_slug: autocad-nettoyer-dxf
en_slug: autocad-dxf-cleanup
fr_title: AutoCAD : nettoyer un dessin et exporter un DXF prêt pour la découpe CNC
en_title: AutoCAD: clean up a drawing and export a DXF ready for CNC cutting
fr_desc: Unités, calques, doublons (OVERKILL), contours fermés (JOIN, PEDIT), splines, PURGE et AUDIT, puis enregistrement en DXF : la routine AutoCAD pour un fichier que la FAO accepte du premier coup.
en_desc: Units, layers, duplicates (OVERKILL), closed contours (JOIN, PEDIT), splines, PURGE and AUDIT, then saving as DXF: the AutoCAD routine for a file CAM accepts the first time.
---
=== fr
Un dessin d’architecte ou de bureau d’études n’est presque jamais prêt pour une table de découpe : cotes, cartouche, lignes en double, contours ouverts, blocs imbriqués. Voici la routine pour en tirer un DXF de découpe propre dans AutoCAD (les mêmes commandes existent dans [BricsCAD](/guides/bricscad-dxf/)).

## Routine de nettoyage

1. **Copier les pièces** à couper dans un nouveau dessin (ne pas nettoyer l’original).
2. **Unités** : `UNITS` et la variable `INSUNITS` (mm ou po) ; vérifier une cote connue avec `DIST`.
3. **Supprimer** cotes, textes, hachures, cartouche (ou les geler sur leurs calques puis les effacer).
4. **Décomposer** les blocs si nécessaire (`EXPLODE`), avec prudence : ne pas décomposer les polylignes déjà propres.
5. **Mettre à plat** : tout à Z = 0 (`FLATTEN` des Express Tools, ou vérifier l’élévation dans les propriétés).
6. **Doublons** : `OVERKILL` supprime les lignes superposées et les segments qui se chevauchent.
7. **Fermer les contours** : `JOIN` (ou `PEDIT` → Joindre) pour transformer lignes et arcs en polylignes fermées.
8. **Splines** : les convertir en polylignes ou arcs si la FAO les gère mal (`SPLINEDIT` → Convertir en polyligne, avec une précision adaptée).
9. **Calques** : COUPE, GRAVURE, PLI séparés, couleurs distinctes.
10. `PURGE` puis `AUDIT` pour enlever le superflu et corriger les erreurs.
11. **Enregistrer sous** DXF dans une version que votre FAO lit (en cas de doute, une version plus ancienne comme 2007 ou 2000).

> [!TIP] Une polyligne fermée se reconnaît dans la palette Propriétés (Fermé : Oui). Sélectionner tout et filtrer avec `QSELECT` permet de repérer les lignes qui ne sont pas des polylignes.

## Contrôle avant envoi

- [ ] Échelle 1:1, unités confirmées
- [ ] Aucun doublon (OVERKILL lancé)
- [ ] Contours fermés, aucun trou minuscule parasite
- [ ] Calques de découpe et de gravure séparés
- [ ] Rien d’autre que la géométrie à couper

Voir le détail dans [DXF : bonnes pratiques](/guides/dxf-bonnes-pratiques/).

## Erreurs fréquentes

| Erreur | Effet dans la FAO |
|---|---|
| Lignes en double | Double passage de torche, surchauffe |
| Petits jours entre segments | Contour ouvert, pas de compensation possible |
| Dessin en pieds-pouces architecturaux mal converti | Pièce à la mauvaise échelle |
| Splines très fines | Parcours saccadé, fichier lourd |

## FAQ

### AutoCAD LT suffit-il ?
Pour nettoyer et exporter un DXF 2D, oui. Les Express Tools (`FLATTEN`) ne sont pas offerts dans toutes les versions ; vérifiez alors l’élévation dans les propriétés.

## À valider en atelier (Michaël)

- La version de DXF que votre FAO préfère.

## Sources

- [Autodesk — Aide AutoCAD (commandes OVERKILL, JOIN, PEDIT, PURGE, AUDIT)](https://help.autodesk.com/view/ACD/2025/FRA/), consulté le 26 novembre 2026.
- [Autodesk — DXF reference](https://help.autodesk.com/view/OARX/2025/ENU/?guid=GUID-235B22E0-A567-4CF6-92D3-38A2306D73F3).
=== en
An architect’s or design office drawing is almost never ready for a cutting table: dimensions, title block, duplicate lines, open contours, nested blocks. Here is the routine to get a clean cut DXF out of AutoCAD (the same commands exist in [BricsCAD](/en/guides/bricscad-to-clean-dxf/)).

## Cleanup routine

1. **Copy the parts** to cut into a new drawing (never clean the original).
2. **Units**: `UNITS` and the `INSUNITS` variable (mm or in); check a known dimension with `DIST`.
3. **Delete** dimensions, text, hatches, title block (or freeze them on their layers and erase).
4. **Explode** blocks if needed (`EXPLODE`), carefully: do not explode polylines that are already clean.
5. **Flatten**: everything at Z = 0 (Express Tools `FLATTEN`, or check elevation in properties).
6. **Duplicates**: `OVERKILL` removes overlapping lines and segments.
7. **Close contours**: `JOIN` (or `PEDIT` → Join) to turn lines and arcs into closed polylines.
8. **Splines**: convert to polylines or arcs if your CAM handles them poorly (`SPLINEDIT` → Convert to polyline, with a suitable precision).
9. **Layers**: CUT, ETCH, BEND separate, distinct colours.
10. `PURGE` then `AUDIT` to remove clutter and fix errors.
11. **Save as** DXF in a version your CAM reads (when in doubt, an older version such as 2007 or 2000).

> [!TIP] A closed polyline shows in the Properties palette (Closed: Yes). Select all and filter with `QSELECT` to find lines that are not polylines.

## Check before sending

- [ ] 1:1 scale, units confirmed
- [ ] No duplicates (OVERKILL run)
- [ ] Closed contours, no tiny stray holes
- [ ] Cut and etch layers separate
- [ ] Nothing but geometry to cut

See details in [DXF best practices](/en/guides/dxf-best-practices/).

## Common mistakes

| Mistake | Effect in CAM |
|---|---|
| Duplicate lines | Double torch pass, overheating |
| Tiny gaps between segments | Open contour, no compensation possible |
| Architectural feet-inches drawing badly converted | Part at the wrong scale |
| Very fine splines | Jerky path, heavy file |

## FAQ

### Is AutoCAD LT enough?
For cleaning and exporting a 2D DXF, yes. Express Tools (`FLATTEN`) are not offered in every version; check elevation in properties instead.

## For Michaël to review

- The DXF version your CAM prefers.

## Sources

- [Autodesk — AutoCAD help (OVERKILL, JOIN, PEDIT, PURGE, AUDIT commands)](https://help.autodesk.com/view/ACD/2025/ENU/), consulted November 26, 2026.
- [Autodesk — DXF reference](https://help.autodesk.com/view/OARX/2025/ENU/?guid=GUID-235B22E0-A567-4CF6-92D3-38A2306D73F3).
