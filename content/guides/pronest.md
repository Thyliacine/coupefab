---
id: pronest
hub: software
group: cam
order: 80
mono: PN
nav: ProNest | ProNest
kicker: Logiciel · imbrication | Software · nesting
level: avance
schema: Article
tags: pronest, hypertherm, nesting, true hole, cut charts, plasma, laser, oxyfuel, waterjet, production
related: nesting, sheetcam, plasma-cutting, consumables
fr_slug: pronest-imbrication
en_slug: pronest-nesting
fr_title: ProNest : imbrication de production pour plasma, laser, oxycoupage et jet d’eau
en_title: ProNest: production nesting for plasma, laser, oxyfuel and waterjet
fr_desc: Ce que fait un logiciel d’imbrication de production comme ProNest d’Hypertherm, la différence entre ProNest et ProNest LT, et quand il vaut mieux qu’un logiciel plus simple comme SheetCam.
en_desc: What a production nesting package such as Hypertherm’s ProNest does, the difference between ProNest and ProNest LT, and when it beats a simpler package such as SheetCam.
---
=== fr
**ProNest** est le logiciel de FAO et d’imbrication d’Hypertherm pour la découpe de tôle en production. Là où un logiciel comme [SheetCam](/guides/debuter-sheetcam/) prépare surtout des parcours, ProNest gère aussi l’**utilisation des tôles**, les **chutes**, les **commandes** et l’**estimation des coûts**.

## Ce qu’apporte un logiciel d’imbrication de production

| Fonction | Gain |
|---|---|
| Imbrication automatique avancée | Meilleure utilisation de la tôle — voir [Imbrication](/guides/imbrication/) |
| Paramètres de procédé intégrés (tableaux de coupe du fabricant) | Vitesse, hauteur, entrées selon matière et épaisseur |
| Technologies de qualité de trou propres aux sources Hypertherm | Trous plus cylindriques en plasma |
| Coupe en ligne commune, pontage, chaînage | Moins de perçages, moins de temps |
| Gestion des chutes et de l’inventaire de tôles | Réutilisation, traçabilité |
| Estimation de temps et de coût | Soumissions plus justes |

## ProNest ou ProNest LT

| | ProNest | ProNest LT |
|---|---|---|
| Public | Production industrielle | Usage industriel léger |
| Procédés | Dont plasma haute définition (XPR, HyPerformance), jet d’eau en biseau | Plasma conventionnel (Powermax, MAXPRO), oxycoupage, jet d’eau conventionnel, certains lasers |
| Modèle de licence | Selon l’offre Hypertherm (consulter un distributeur) | **Abonnement** mensuel, essai de 7 jours |
| Fonctions avancées | Modules optionnels (imbrication avancée, inventaire, intégration ERP…) | Ensemble réduit |

Les modules et prix exacts varient : demandez une démonstration à un distributeur et comparez sur vos propres pièces.

## Quand passer de SheetCam à ProNest

- [ ] Plusieurs heures par jour de programmation ou d’imbrication
- [ ] Coût de la tôle important (inox, aluminium épais) : chaque pour cent d’utilisation compte
- [ ] Besoin de suivre les chutes et l’inventaire
- [ ] Système plasma haute définition dont vous voulez exploiter les fonctions de qualité de trou
- [ ] Soumissions fréquentes demandant des temps de coupe fiables

> [!NOTE] Une imbrication très serrée n’est utile que si la machine la coupe sans déformation ni collision avec des pièces basculées. Validez sur votre table.

## FAQ

### ProNest fonctionne-t-il avec des tables non Hypertherm ?
ProNest prend en charge de nombreuses machines et commandes de différents fabricants, via des configurations machine. Vérifiez la vôtre avec un distributeur.

## À valider en atelier (Michaël)

- Votre expérience ProNest (ou celle de clients) et le seuil de volume qui le justifie.

## Sources

- [Hypertherm — ProNest](https://www.hypertherm.com/solutions/about-our-products/pronest-nesting-software/), consulté le 26 novembre 2026.
- [Hypertherm — ProNest LT](https://www.hypertherm.com/hypertherm/pronest/pronest-lt-cadcam-nesting-software/).
- [Hypertherm — ProNest vs ProNest LT comparison](https://www.hypertherm.com/solutions/about-our-products/pronest-nesting-software/nesting-software-comparison/).
=== en
**ProNest** is Hypertherm’s CAM and nesting software for production sheet cutting. Where a package like [SheetCam](/en/guides/getting-started-sheetcam/) mainly prepares toolpaths, ProNest also manages **sheet utilization**, **remnants**, **orders** and **cost estimating**.

## What a production nesting package brings

| Feature | Benefit |
|---|---|
| Advanced automatic nesting | Better sheet use — see [Nesting](/en/guides/nesting/) |
| Built-in process parameters (maker cut charts) | Speed, height, leads by material and thickness |
| Hole-quality technologies specific to Hypertherm sources | Rounder holes in plasma |
| Common-line cutting, bridging, chaining | Fewer pierces, less time |
| Remnant and sheet inventory management | Reuse, traceability |
| Time and cost estimating | More accurate quotes |

## ProNest or ProNest LT

| | ProNest | ProNest LT |
|---|---|---|
| Audience | Industrial production | Light industrial use |
| Processes | Including high-definition plasma (XPR, HyPerformance), bevel waterjet | Conventional plasma (Powermax, MAXPRO), oxyfuel, conventional waterjet, select lasers |
| Licence model | Per Hypertherm’s offer (ask a distributor) | Monthly **subscription**, 7-day trial |
| Advanced features | Optional modules (advanced nesting, inventory, ERP integration…) | Reduced set |

Exact modules and prices vary: ask a distributor for a demo and compare on your own parts.

## When to move from SheetCam to ProNest

- [ ] Several hours a day of programming or nesting
- [ ] Significant sheet cost (stainless, thick aluminum): every percent of utilization counts
- [ ] Need to track remnants and inventory
- [ ] High-definition plasma whose hole-quality features you want to use
- [ ] Frequent quotes needing reliable cut times

> [!NOTE] Very tight nesting only helps if the machine cuts it without distortion or collisions with tipped parts. Validate on your table.

## FAQ

### Does ProNest work with non-Hypertherm tables?
ProNest supports many machines and controls from different makers through machine configurations. Check yours with a distributor.

## For Michaël to review

- Your ProNest experience (or customers’) and the volume threshold that justifies it.

## Sources

- [Hypertherm — ProNest](https://www.hypertherm.com/solutions/about-our-products/pronest-nesting-software/), consulted November 26, 2026.
- [Hypertherm — ProNest LT](https://www.hypertherm.com/hypertherm/pronest/pronest-lt-cadcam-nesting-software/).
- [Hypertherm — ProNest vs ProNest LT comparison](https://www.hypertherm.com/solutions/about-our-products/pronest-nesting-software/nesting-software-comparison/).
