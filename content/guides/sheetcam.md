---
id: sheetcam
hub: software
group: cam
order: 10
mono: SC
nav: SheetCam | SheetCam
kicker: Logiciel · FAO plasma | Software · plasma CAM
level: debutant
schema: HowTo
tags: sheetcam, plasma, cam, dxf, nesting, post-processor
related: bricscad, kerf, lead-ins-pierce, nesting
prices: no
fr_slug: debuter-sheetcam
en_slug: getting-started-sheetcam
fr_title: Débuter avec SheetCam : du DXF au G-code plasma
en_title: Getting started with SheetCam: from DXF to plasma G-code
fr_desc: Unités, job, import DXF, outil plasma, opération, imbrication et post-processeur : la démarche SheetCam pas à pas, avec les pièges que l’équipe SheetCam documente elle-même.
en_desc: Units, job, DXF import, plasma tool, operation, nesting and post processor: the SheetCam workflow step by step, with the pitfalls the SheetCam team documents itself.
---
=== fr
SheetCam est un logiciel de **FAO 2D** : il transforme un dessin (DXF, SVG…) en parcours de coupe pour plasma, oxycoupage, jet d’eau ou laser. Ce n’est pas un logiciel de dessin. Les manuels officiels sont en anglais ; ce guide en est un compagnon francophone, pas un substitut.

## En bref

| Question | Réponse courte |
|---|---|
| À quoi sert SheetCam ? | Générer le G-code de découpe 2D à partir d’un DXF |
| Version d’essai ? | Même exécutable que la version payante, sans limite de temps, mais limitée à environ 180 lignes de G-code (équipe SheetCam, forum officiel) |
| Où sont les manuels ? | Page *Support Manuals* de SheetCam LLC, et **Help → Tutorials** dans le logiciel |
| Le piège n° 1 ? | Deux réglages d’unités indépendants |

## Les deux réglages d’unités

L’équipe SheetCam le répète sur son forum : il y a **deux** endroits pour les unités, et ils sont indépendants.

- **Options → Application options** : unités d’affichage et de saisie (le canevas).
- **Options → Machine → Post Processor** : unités du G-code envoyé à la machine.

Ils n’ont pas à être identiques, mais un décalage mal compris donne des pièces 25,4 fois trop grandes ou trop petites. Vérifiez les deux avant la première coupe.

> [!WARN] Les tutoriels intégrés **modifient les Options et Job options** (matière, zone de travail, taille de table). Remettez les réglages de votre machine après un tutoriel.

## Démarche pas à pas

1. **Créer le job.** File → New job, puis Options → Job options : taille de la tôle, épaisseur, origine (souvent le coin avant gauche, X0 Y0) et hauteur de dégagement des rapides.
2. **Importer le dessin.** File → Import drawing. Dans la boîte de dialogue, faites correspondre l’échelle et les unités au fichier. Pièce minuscule ou énorme : c’est un conflit d’unités, réimportez.
3. **Vérifier la géométrie.** Contours ouverts, traits en double ou blocs non explosés se règlent idéalement dans le DAO (voir [BricsCAD → DXF propre](/guides/bricscad-dxf/) et [DXF : bonnes pratiques](/guides/dxf-bonnes-pratiques/)).
4. **Créer l’outil plasma.** Tools → New tool → Plasma. Saisissez le kerf, la vitesse, la hauteur de coupe, la hauteur et le délai de perçage **de la charte de votre source** — pas d’une valeur trouvée au hasard (voir [Kerf](/guides/kerf-qualite-coupe/)).
5. **Créer l’opération.** Operations → Plasma cut (ou Jet cut). Choisissez la couche, l’outil et le côté : **extérieur** pour le profil, **intérieur** pour les trous, **sur la ligne** pour un traçage.
6. **Régler entrées, sorties et ordre.** Lead-in, lead-out et sens de coupe dépendent de votre torche et de votre charte (voir [Entrées, sorties et perçage](/guides/entrees-sorties-percage-plasma/)). Les trous se coupent avant le contour extérieur.
7. **Imbriquer** si vous coupez plusieurs pièces (voir plus bas).
8. **Choisir le post-processeur.** Options → Machine → Post Processor : celui qui correspond à votre commande (Mach3, LinuxCNC, FireControl, etc.).
9. **Simuler, puis écrire le fichier.** Vérifiez la simulation (ordre, entrées, rapides), puis File → Post process.

## Le minimum pour qu’un parcours existe

D’après l’équipe SheetCam, il faut au moins : une **pièce** (Part — un import DXF en crée une), une **couche** (Layer), un **outil** et une **opération**. Sans opération, rien ne s’affiche et l’imbrication automatique ne fait rien.

## Imbrication automatique (version 8)

Selon la FAQ et le démarrage rapide v8, l’imbrication automatique part des **parcours déjà créés** (décalage de kerf, entrées et sorties compris), pas seulement du contour. Le logiciel calcule plusieurs variantes ; vous en choisissez une, puis Apply. L’imbrication manuelle reste possible. Voir aussi le guide [Imbrication](/guides/imbrication/).

## Erreurs fréquentes

| Symptôme | Cause probable | Correctif |
|---|---|---|
| Pièce 25,4× trop grande ou petite | Unités d’import ou du post | Vérifier les deux réglages d’unités, réimporter |
| Rien ne s’affiche après l’opération | Contours ouverts, mauvaise couche | Fermer les contours dans le DAO, vérifier la couche choisie |
| Trous trop grands, pièces trop petites | Kerf absent ou mal saisi | Mesurer un coupon, corriger le kerf de l’outil |
| G-code tronqué | Version d’essai (≈ 180 lignes) | Licence, ou tester avec une petite pièce |
| La machine ignore la hauteur de torche | Post qui n’est pas celui de la commande | Utiliser le post fourni par le fabricant de la table |

## Liste de vérification avant de couper

- [ ] Les deux réglages d’unités sont confirmés
- [ ] Tôle, épaisseur et origine du job correspondent à la table
- [ ] Outil créé avec les valeurs de la charte de *votre* source et consommables
- [ ] Trous en intérieur, profil en extérieur, trous coupés en premier
- [ ] Entrées hors des arêtes fonctionnelles de la pièce
- [ ] Post-processeur de votre commande, simulation vérifiée

## FAQ

### SheetCam peut-il dessiner des pièces ?
Il a des outils 2D simples, mais ce n’est pas un DAO. Dessinez dans BricsCAD, AutoCAD, SolidWorks, Fusion ou autre, puis exportez un DXF.

### Quel post-processeur choisir ?
Celui de votre commande. Les fabricants de tables fournissent souvent le leur (par exemple Langmuir pour FireControl). Si votre commande n’est pas dans la bibliothèque, SheetCam documente une API de post-processeur et peut réaliser un post sur mesure (sales@sheetcam.com, selon le forum officiel).

### La version d’essai suffit-elle pour apprendre ?
Oui pour apprendre l’interface : c’est le même logiciel. La limite d’environ 180 lignes empêche seulement de produire des programmes longs.

## À valider en atelier (Michaël)

- Les post-processeurs les plus courants dans les ateliers québécois (Machitech, FastCAM, contrôleurs courants).
- Un modèle de job type (taille de table, origine, unités) à proposer en exemple.
- Toute différence de menus entre la v8 et votre copie de travail.

## Sources

- [SheetCam LLC — Support Manuals](https://sheetcamshop.myshopify.com/pages/support) (guides 8.0, manuels A4 et US Letter), consulté le 26 novembre 2026.
- [Forum SheetCam — « Where to learn Sheetcam »](https://forum.sheetcam.com/t/where-to-learn-sheetcam/8102), réponse de l’équipe (sheetcamCS2), 10 septembre 2024.
- FAQ et démarrage rapide SheetCam v8 (l’opération doit exister avant l’imbrication automatique).
=== en
SheetCam is **2D CAM** software: it turns a drawing (DXF, SVG…) into cut paths for plasma, oxy-fuel, waterjet or laser. It is not a drawing program. The official manuals are in English; this guide is a companion, not a substitute.

## At a glance

| Question | Short answer |
|---|---|
| What is SheetCam for? | Generating 2D cutting G-code from a DXF |
| Trial version? | Same executable as the paid version, no time limit, but capped at about 180 lines of G-code (SheetCam team, official forum) |
| Where are the manuals? | SheetCam LLC *Support Manuals* page, and **Help → Tutorials** in the software |
| Pitfall no. 1? | Two independent unit settings |

## The two unit settings

The SheetCam team repeats it on its forum: there are **two** places for units, and they are independent.

- **Options → Application options**: display and input units (the canvas).
- **Options → Machine → Post Processor**: units of the G-code sent to the machine.

They do not have to match, but a misunderstood mismatch gives parts 25.4 times too large or too small. Check both before your first cut.

> [!WARN] The built-in tutorials **change Options and Job options** (material, work area, table size). Restore your machine settings after a tutorial.

## Step by step

1. **Create the job.** File → New job, then Options → Job options: sheet size, thickness, origin (often the front-left corner, X0 Y0) and rapid clearance height.
2. **Import the drawing.** File → Import drawing. In the dialog, match scale and units to the file. Tiny or huge part: that is a units conflict, re-import.
3. **Check the geometry.** Open contours, duplicate lines or unexploded blocks are best fixed in CAD (see [BricsCAD → clean DXF](/en/guides/bricscad-to-clean-dxf/) and [DXF best practices](/en/guides/dxf-best-practices/)).
4. **Create the plasma tool.** Tools → New tool → Plasma. Enter kerf, speed, cut height, pierce height and pierce delay **from your power source’s cut chart** — not a number found at random (see [Kerf](/en/guides/kerf-and-cut-quality/)).
5. **Create the operation.** Operations → Plasma cut (or Jet cut). Pick the layer, tool and side: **outside** for the profile, **inside** for holes, **on the line** for marking.
6. **Set lead-ins, lead-outs and order.** Lead-in, lead-out and cut direction depend on your torch and chart (see [Lead-ins, lead-outs and pierce](/en/guides/lead-ins-pierce-height/)). Holes are cut before the outside profile.
7. **Nest** if you cut several parts (see below).
8. **Choose the post processor.** Options → Machine → Post Processor: the one matching your control (Mach3, LinuxCNC, FireControl, etc.).
9. **Simulate, then write the file.** Check the simulation (order, leads, rapids), then File → Post process.

## The minimum for a toolpath to exist

According to the SheetCam team you need at least: a **part** (a DXF import creates one), a **layer**, a **tool** and an **operation**. Without an operation nothing shows and auto-nesting does nothing.

## Auto-nesting (version 8)

Per the v8 FAQ and quick start, auto-nesting works from the **toolpaths already created** (kerf offset, leads included), not just the outline. The software computes several variants; you pick one, then Apply. Manual nesting is still available. See also [Nesting](/en/guides/nesting/).

## Common mistakes

| Symptom | Likely cause | Fix |
|---|---|---|
| Part 25.4× too big or small | Import or post units | Check both unit settings, re-import |
| Nothing shows after the operation | Open contours, wrong layer | Close contours in CAD, check the selected layer |
| Holes oversize, parts undersize | Kerf missing or wrong | Measure a coupon, correct the tool kerf |
| Truncated G-code | Trial version (≈ 180 lines) | License it, or test with a small part |
| Machine ignores torch height | Post does not match the control | Use the post supplied by the table maker |

## Pre-cut checklist

- [ ] Both unit settings confirmed
- [ ] Job sheet, thickness and origin match the table
- [ ] Tool built from *your* source and consumables chart
- [ ] Holes inside, profile outside, holes cut first
- [ ] Lead-ins kept off functional edges
- [ ] Post processor for your control, simulation checked

## FAQ

### Can SheetCam draw parts?
It has simple 2D tools, but it is not CAD. Draw in BricsCAD, AutoCAD, SolidWorks, Fusion or similar, then export a DXF.

### Which post processor should I use?
The one for your control. Table makers often supply their own (for example Langmuir for FireControl). If your control is missing, SheetCam documents a post-processor API and can quote a custom post (sales@sheetcam.com, per the official forum).

### Is the trial enough to learn?
Yes, for learning the interface: it is the same software. The roughly 180-line cap only stops you from producing long programs.

## For Michaël to review

- The post processors most used in Quebec shops (Machitech, FastCAM, common controls).
- A typical job template (table size, origin, units) to offer as an example.
- Any menu differences between v8 and your working copy.

## Sources

- [SheetCam LLC — Support Manuals](https://sheetcamshop.myshopify.com/pages/support) (8.0 guides, A4 and US Letter manuals), consulted November 26, 2026.
- [SheetCam forum — “Where to learn Sheetcam”](https://forum.sheetcam.com/t/where-to-learn-sheetcam/8102), team reply (sheetcamCS2), September 10, 2024.
- SheetCam v8 FAQ and quick start (the operation must exist before auto-nesting).
