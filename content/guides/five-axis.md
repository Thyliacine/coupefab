---
id: five-axis
hub: process
order: 48
nav: Usinage 5 axes | 5-axis machining
kicker: Procédé · fraisage avancé | Process · advanced milling
level: avance
schema: Article
tags: 5-axis, five axis, 3+2, positional, simultaneous, trunnion, table-table, head-head, head-table, rtcp, tcpc, g43.4, tilted work plane, g68.2, cycle 800, collision, fixturing
related: cnc-mill, esprit, work-offsets, fixturing
fr_slug: usinage-5-axes
en_slug: five-axis-machining
fr_title: Usinage 5 axes : 3+2 ou continu, cinématiques, RTCP et plans inclinés
en_title: 5-axis machining: 3+2 or simultaneous, kinematics, RTCP and tilted planes
fr_desc: La différence entre 5 axes positionnel (3+2) et continu, les cinématiques table-table, tête-tête et tête-table, le RTCP (G43.4) et les plans inclinés (G68.2, CYCLE800), et ce qu’il faut pour réussir : FAO, post, simulation, montage.
en_desc: The difference between positional (3+2) and simultaneous 5-axis, table-table, head-head and head-table kinematics, RTCP (G43.4) and tilted planes (G68.2, CYCLE800), and what it takes to succeed: CAM, post, simulation, fixturing.
---
=== fr
Une machine 5 axes ajoute deux axes **rotatifs** aux trois axes linéaires. Mais « faire du 5 axes » recouvre deux pratiques très différentes : le **positionnel (3+2)** — la majorité des pièces — et le **continu** (5 axes simultanés), indispensable pour les surfaces gauches.

## 3+2 ou continu ?

| Critère | 3+2 (positionnel) | 5 axes continu |
|---|---|---|
| Principe | Les axes rotatifs s’orientent puis se **bloquent** ; on usine en X/Y/Z dans un plan incliné | Les cinq axes bougent **ensemble** pendant la coupe |
| Pièces | Faces et trous inclinés, plusieurs faces en une prise | Aubes, turbines, moules, surfaces sculptées, usinage en roulant (*swarf*) |
| Avantages | Rigidité, outils courts, programmation plus simple | Accès complet, outils courts même en cavité profonde, meilleur fini |
| Exigences | FAO 3+2, plan incliné à la commande | FAO multi-axes, simulation machine, post certifié |

## Les cinématiques

| Type | Ce qui bouge | Pour |
|---|---|---|
| Table-table (berceau / *trunnion*) | La pièce bascule et tourne | Pièces petites et moyennes, très répandu |
| Tête-tête | L’outil bascule et tourne, la pièce reste fixe | Grandes pièces lourdes |
| Tête-table | Un axe dans la tête, un dans la table | Compromis |

## RTCP et plans inclinés

- **RTCP / TCPC** (Fanuc **G43.4**, équivalents chez Heidenhain, Siemens…) : la commande compense les pivots et la longueur d’outil pour que la **pointe de l’outil** suive la trajectoire programmée. Indispensable en continu ; il rend aussi les programmes moins dépendants de la position exacte de la pièce.
- **Plans inclinés** (*tilted work plane* : Fanuc **G68.2**, Siemens **CYCLE800**, Heidenhain PLANE) : la commande définit un repère incliné pour le 3+2.

Ces fonctions sont des options de commande : vérifiez qu’elles sont actives sur votre machine (voir [[fanuc]], [[haas]] et [[siemens-sinumerik]]).

## Ce qu’il faut pour réussir

1. **FAO** multi-axes avec la machine définie (voir [[esprit]], [[mastercam-2d]] et les autres modules 5 axes).
2. **Post** certifié pour la cinématique exacte (voir [[post-processors]]).
3. **Simulation machine** complète : collisions tête/table/montage, limites d’axes.
4. **Montage** dégagé : étaux 5 axes, queues d’aronde, montages surélevés (voir [[fixturing]]).
5. **Calibration** des centres de rotation (cycles de palpage fournis par le fabricant).

## Liste de vérification avant la première pièce

- [ ] Options RTCP / plan incliné actives
- [ ] Centres de rotation calibrés
- [ ] Simulation sans collision, avec le vrai montage et le vrai porte-outil
- [ ] Premier passage à vitesse réduite et au-dessus de la pièce
- [ ] Origines (G54…) cohérentes avec la FAO (voir [[work-offsets]])

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Simuler sans le montage ni le porte-outil | Collision réelle |
| Post « 5 axes générique » | Mouvements rotatifs inattendus, pièce rebutée |
| Faire du continu là où le 3+2 suffit | Programmation plus longue, rigidité moindre |
| Centres de rotation non calibrés | Erreurs de position sur les faces inclinées |

## FAQ

### Une 4e axe suffit-elle ?
Pour les pièces cylindriques ou à faces autour d’un axe, souvent oui ; le 5 axes devient utile pour les faces composées et les surfaces gauches.

### Faut-il commencer par le continu ?
Non : la plupart des ateliers rentabilisent d’abord le 3+2 (moins de prises, moins de montages).

## À valider en atelier (Michaël)

- Les machines 5 axes de votre réseau et la part de 3+2 vs continu.

## Sources

- [Okuma — 5-axis machining guide](https://www.okuma.com/guides/5-axis-machining-guide), consulté le 26 novembre 2026.
- [Siemens — SINUMERIK live: programming dynamic 5-axis machining (PDF)](https://static.dc.siemens.com/cnc4you/tips-n-tricks/SINUMERIK-live/Sinumerik-live_Programming-dynamic-5-axis-machining-directly-in-SINUMERIK-Operate.pdf), consulté le 26 novembre 2026.
- [Zappettini Consulting — 4th/5th axis, tilted work planes and TCP](https://zappettiniconsulting.com/wiki/five-axis-twp-tcpm), consulté le 26 novembre 2026.
=== en
A 5-axis machine adds two **rotary** axes to the three linear axes. But “doing 5-axis” covers two very different practices: **positional (3+2)** — most parts — and **simultaneous** 5-axis, essential for freeform surfaces.

## 3+2 or simultaneous?

| Criterion | 3+2 (positional) | Simultaneous 5-axis |
|---|---|---|
| Principle | Rotary axes orient then **lock**; you machine in X/Y/Z in a tilted plane | All five axes move **together** while cutting |
| Parts | Angled faces and holes, several faces in one setup | Blades, impellers, molds, sculpted surfaces, swarf cutting |
| Advantages | Rigidity, short tools, simpler programming | Full access, short tools even in deep cavities, better finish |
| Requirements | 3+2 CAM, tilted plane on the control | Multi-axis CAM, machine simulation, certified post |

## Kinematics

| Type | What moves | For |
|---|---|---|
| Table-table (trunnion) | The part tilts and rotates | Small and medium parts, very common |
| Head-head | The tool tilts and rotates, the part stays put | Large, heavy parts |
| Head-table | One axis in the head, one in the table | Compromise |

## RTCP and tilted planes

- **RTCP / TCPC** (Fanuc **G43.4**, equivalents on Heidenhain, Siemens…): the control compensates pivots and tool length so the **tool tip** follows the programmed path. Essential for simultaneous work; it also makes programs less dependent on the exact part position.
- **Tilted work planes** (Fanuc **G68.2**, Siemens **CYCLE800**, Heidenhain PLANE): the control defines a tilted frame for 3+2.

These are control options: check they’re enabled on your machine (see [[fanuc]], [[haas]] and [[siemens-sinumerik]]).

## What it takes to succeed

1. **Multi-axis CAM** with the machine defined (see [[esprit]], [[mastercam-2d]] and other 5-axis modules).
2. A **post** certified for the exact kinematics (see [[post-processors]]).
3. Full **machine simulation**: head/table/fixture collisions, axis limits.
4. **Clearance-friendly fixturing**: 5-axis vises, dovetails, raised fixtures (see [[fixturing]]).
5. **Calibration** of rotary centres (manufacturer’s probing cycles).

## Checklist before the first part

- [ ] RTCP / tilted plane options enabled
- [ ] Rotary centres calibrated
- [ ] Collision-free simulation with the real fixture and holder
- [ ] First run at reduced speed and above the part
- [ ] Origins (G54…) consistent with CAM (see [[work-offsets]])

## Common mistakes

| Mistake | Consequence |
|---|---|
| Simulating without the fixture or holder | Real collision |
| “Generic 5-axis” post | Unexpected rotary moves, scrapped part |
| Simultaneous where 3+2 would do | Longer programming, less rigidity |
| Uncalibrated rotary centres | Position errors on angled faces |

## FAQ

### Is a 4th axis enough?
For cylindrical parts or faces around one axis, often yes; 5-axis pays off for compound faces and freeform surfaces.

### Should you start with simultaneous?
No: most shops first get their return from 3+2 (fewer setups, fewer fixtures).

## For Michaël to review

- The 5-axis machines in your network and the share of 3+2 vs simultaneous.

## Sources

- [Okuma — 5-axis machining guide](https://www.okuma.com/guides/5-axis-machining-guide), consulted November 26, 2026.
- [Siemens — SINUMERIK live: programming dynamic 5-axis machining (PDF)](https://static.dc.siemens.com/cnc4you/tips-n-tricks/SINUMERIK-live/Sinumerik-live_Programming-dynamic-5-axis-machining-directly-in-SINUMERIK-Operate.pdf), consulted November 26, 2026.
- [Zappettini Consulting — 4th/5th axis, tilted work planes and TCP](https://zappettiniconsulting.com/wiki/five-axis-twp-tcpm), consulted November 26, 2026.
