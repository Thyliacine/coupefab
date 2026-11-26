---
id: camworks
hub: software
group: cam
order: 34
mono: CW
nav: CAMWorks | CAMWorks
kicker: Logiciel · FAO intégrée | Software · integrated CAM
level: intermediaire
schema: HowTo
tags: camworks, solidworks cam, afr, automatic feature recognition, techdb, technology database, knowledge-based machining, 2.5 axis, tolerance based machining
related: solidworks-drawings-cam, mastercam-2d, feeds-speeds, post-processors
fr_slug: camworks-fao-solidworks
en_slug: camworks-cam-solidworks
fr_title: CAMWorks (et SOLIDWORKS CAM) : reconnaissance d’entités et base technologique
en_title: CAMWorks (and SOLIDWORKS CAM): feature recognition and the technology database
fr_desc: Démarche CAMWorks en 2,5 axes : machine, brut, extraction des entités usinables (AFR), règles de la TechDB, génération des opérations, simulation et post. Comment bâtir sa base technologique sans tout casser.
en_desc: The CAMWorks 2.5-axis workflow: machine, stock, extracting machinable features (AFR), TechDB rules, generating operations, simulation and posting. How to build your technology database without breaking things.
---
=== fr
CAMWorks (HCL) est une FAO intégrée à SOLIDWORKS (et à Solid Edge). **SOLIDWORKS CAM** en est une version dérivée, livrée par Dassault avec certaines licences SOLIDWORKS. L’idée centrale : on n’usine que des **entités usinables** (poches, trous, rainures, bossages…) reconnues sur le modèle, et une **base technologique** (TechDB) décide des opérations, outils et paramètres.

## Les deux piliers

| Pilier | Ce que ça fait | À retenir |
|---|---|---|
| **AFR** (*Automatic Feature Recognition*) | Analyse le modèle et crée les entités 2,5 axes courantes | Ce qu’AFR ne trouve pas se crée à la main (*New 2.5 Axis Feature*) |
| **TechDB** (*Technology Database*) | Usinage basé sur la connaissance : règles « telle entité, telle matière → telles opérations dans tel ordre » | Faites une **copie de sauvegarde** de la base par défaut avant toute modification |

La TechDB est organisée en quatre couches selon HCL : **machines**, **magasin d’outils** (*tool crib*), **paramètres d’opération** (avances, vitesses, profondeurs, pas) et **règles d’usinage** (stratégies).

## Démarche type (fraisage 2,5 axes)

1. **Machine** : choisir la définition de machine (et son post) dans l’onglet CAMWorks.
2. **Magasin d’outils** : associer le bon magasin à la machine.
3. **Brut** (*Stock Manager*) : boîte englobante, esquisse extrudée ou pièce brute.
4. **Setups / plans de travail** : origine et orientation cohérentes avec votre G54 (voir [[work-offsets]]).
5. **Extraire les entités** (*Extract Machinable Features*) : AFR crée poches, trous, rainures, etc.
6. **Compléter** les entités manquantes à la main ; vérifier les attributs (borgne/débouchant, filetage).
7. **Générer le plan d’opérations** : la TechDB propose ébauche, finition, pointage, perçage…
8. **Générer les parcours**, puis **simuler** (matière et collisions).
9. **Post-traiter** et relire le G-code (voir [[post-processors]]).

## Bâtir sa TechDB sans se perdre

- Commencer par **une machine** réelle (nom descriptif, course de broche, avance max, nombre d’outils).
- Entrer les outils qui couvrent la majorité des travaux, avec leur vraie géométrie ; compléter au fil des jobs.
- Définir les paramètres pour **vos** matières courantes à partir des fiches des fabricants d’outils (voir [[feeds-speeds]]).
- Écrire des règles simples pour les entités les plus fréquentes (trou taraudé, poche rectangulaire), puis raffiner.

> [!TIP] Un magasin d’outils incomplet mais exact vaut mieux qu’un magasin complet mais faux : CAMWorks choisira des outils que vous n’avez pas.

## Usinage basé sur les tolérances (TBM)

Les éditions qui l’incluent lisent les tolérances et le fini de surface du modèle (annotations 3D, MBD) pour choisir la stratégie : par exemple un trou à tolérance serrée reçoit un alésage plutôt qu’un simple perçage. Utile si le bureau d’études annote correctement ; voir [[tolerances]].

## Erreurs fréquentes

| Erreur | Correctif |
|---|---|
| Modifier la TechDB par défaut sans sauvegarde | Copier le fichier de base avant de commencer ; travailler sur une copie active |
| Entités mal reconnues sur une pièce importée (STEP) | Réparer le modèle ; créer les entités à la main |
| Origine du setup différente du G54 réel | Aligner le plan de travail sur l’origine de montage |
| Faire confiance aux avances par défaut | Les remplacer par les données de vos outils |

## Liste de vérification avant post

- [ ] Bonne machine et bon post sélectionnés
- [ ] Brut et origine vérifiés
- [ ] Toutes les entités présentes (rien d’oublié par AFR)
- [ ] Simulation sans collision ni matière restante non voulue
- [ ] G-code relu : unités, G54, changements d’outil, arrosage

## FAQ

### SOLIDWORKS CAM ou CAMWorks ?
SOLIDWORKS CAM est construit sur la technologie CAMWorks avec un périmètre adapté aux licences SOLIDWORKS ; CAMWorks ajoute des modules (tournage avancé, multi-axes, etc.) selon l’édition. Comparez les éditions auprès d’un revendeur.

### CAMWorks fait-il du plasma ?
Il existe des options de découpe selon les versions, mais pour un atelier de découpe de tôle, un logiciel dédié reste souvent plus direct ; voir [[sheetcam]] et [[pronest]].

## À valider en atelier (Michaël)

- Les règles TechDB qui vous font gagner le plus de temps.
- Votre expérience SOLIDWORKS CAM vs CAMWorks.

## Sources

- [HCL CAMWorks — Mill Tutorial (PDF)](https://camworks.s3.amazonaws.com/Website/Docs/Manuals/Mill_Tutorial.pdf), consulté le 26 novembre 2026.
- [HCL CAMWorks — Building your first Technology Database from scratch](https://camworks.com/blog/building-your-first-technology-database-from-scratch-in-camworks/), consulté le 26 novembre 2026.
- [HCL CAMWorks — 2.5 Axis Milling](https://camworks.com/modules/25axis-milling/), consulté le 26 novembre 2026.
- [SOLIDWORKS — SOLIDWORKS CAM](https://www.solidworks.com/product/solidworks-cam), consulté le 26 novembre 2026.
=== en
CAMWorks (HCL) is CAM integrated into SOLIDWORKS (and Solid Edge). **SOLIDWORKS CAM** is a derived version that Dassault ships with some SOLIDWORKS licences. The core idea: you only machine **machinable features** (pockets, holes, slots, bosses…) recognized on the model, and a **technology database** (TechDB) decides operations, tools and parameters.

## The two pillars

| Pillar | What it does | Remember |
|---|---|---|
| **AFR** (Automatic Feature Recognition) | Analyzes the model and creates common 2.5-axis features | Anything AFR misses is created by hand (*New 2.5 Axis Feature*) |
| **TechDB** (Technology Database) | Knowledge-based machining: rules “this feature, this material → these operations in this order” | Make a **backup copy** of the default database before changing anything |

HCL describes the TechDB as four layers: **machines**, **tool crib**, **operation parameters** (feeds, speeds, depths, stepovers) and **machining rules** (strategies).

## Typical workflow (2.5-axis milling)

1. **Machine**: pick the machine definition (and its post) in the CAMWorks tab.
2. **Tool crib**: assign the right crib to the machine.
3. **Stock** (Stock Manager): bounding box, extruded sketch or stock part.
4. **Setups / work planes**: origin and orientation consistent with your G54 (see [[work-offsets]]).
5. **Extract Machinable Features**: AFR creates pockets, holes, slots, etc.
6. **Complete** missing features by hand; check attributes (blind/through, threads).
7. **Generate the operation plan**: the TechDB proposes roughing, finishing, spot drilling, drilling…
8. **Generate toolpaths**, then **simulate** (stock and collisions).
9. **Post** and read the G-code (see [[post-processors]]).

## Building your TechDB without getting lost

- Start with **one** real machine (descriptive name, spindle range, max feed, tool capacity).
- Enter the tools that cover most jobs, with real geometry; add more as jobs require.
- Set parameters for **your** usual materials from tool makers’ data (see [[feeds-speeds]]).
- Write simple rules for the most frequent features (tapped hole, rectangular pocket), then refine.

> [!TIP] An incomplete but accurate tool crib beats a complete but wrong one: CAMWorks will pick tools you don’t own.

## Tolerance-based machining (TBM)

Editions that include it read model tolerances and surface finish (3D annotations, MBD) to choose the strategy: for example a tight-tolerance hole gets reamed rather than just drilled. Useful when engineering annotates properly; see [[tolerances]].

## Common mistakes

| Mistake | Fix |
|---|---|
| Editing the default TechDB without a backup | Copy the database file first; work on an active copy |
| Features poorly recognized on an imported part (STEP) | Repair the model; create features by hand |
| Setup origin different from the real G54 | Align the work plane to the fixture origin |
| Trusting default feeds | Replace them with your tools’ data |

## Pre-post checklist

- [ ] Right machine and post selected
- [ ] Stock and origin checked
- [ ] All features present (nothing missed by AFR)
- [ ] Simulation with no collision or unintended leftover stock
- [ ] G-code read: units, G54, tool changes, coolant

## FAQ

### SOLIDWORKS CAM or CAMWorks?
SOLIDWORKS CAM is built on CAMWorks technology with a scope matched to SOLIDWORKS licences; CAMWorks adds modules (advanced turning, multi-axis, etc.) depending on edition. Compare editions with a reseller.

### Does CAMWorks do plasma?
Some versions offer cutting options, but for a sheet-cutting shop dedicated software is usually more direct; see [[sheetcam]] and [[pronest]].

## For Michaël to review

- The TechDB rules that save you the most time.
- Your experience with SOLIDWORKS CAM vs CAMWorks.

## Sources

- [HCL CAMWorks — Mill Tutorial (PDF)](https://camworks.s3.amazonaws.com/Website/Docs/Manuals/Mill_Tutorial.pdf), consulted November 26, 2026.
- [HCL CAMWorks — Building your first Technology Database from scratch](https://camworks.com/blog/building-your-first-technology-database-from-scratch-in-camworks/), consulted November 26, 2026.
- [HCL CAMWorks — 2.5 Axis Milling](https://camworks.com/modules/25axis-milling/), consulted November 26, 2026.
- [SOLIDWORKS — SOLIDWORKS CAM](https://www.solidworks.com/product/solidworks-cam), consulted November 26, 2026.
