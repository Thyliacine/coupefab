---
id: swiss-turn-mill
hub: process
order: 50
nav: Tour-fraiseur et décolleteuse suisse | Turn-mill and Swiss-type
kicker: Procédé · tournage multitâche | Process · multitasking turning
level: avance
schema: Article
tags: swiss, swiss-type, sliding headstock, guide bushing, turn-mill, multitasking, b-axis, sub-spindle, live tooling, c-axis, y-axis, bar feeder, done-in-one
related: cnc-lathe, five-axis, free-machining-12l14, mastercam-posts-lathe
fr_slug: tour-fraiseur-decolleteuse-suisse
en_slug: turn-mill-swiss-type-lathes
fr_title: Tours-fraiseurs et décolleteuses de type suisse : principes, différences et choix
en_title: Turn-mill machines and Swiss-type lathes: principles, differences and choosing
fr_desc: Poupée mobile et canon de guidage (suisse), axe B et contre-broche (tour-fraiseur), outils motorisés, axes C et Y : comment fonctionnent ces machines, pour quelles pièces, et ce que ça change en programmation FAO.
en_desc: Sliding headstock and guide bushing (Swiss), B-axis and sub-spindle (turn-mill), live tooling, C and Y axes: how these machines work, which parts they suit, and what changes in CAM programming.
---
=== fr
Un tour CNC classique tourne et fait des opérations simples. Dès qu’on ajoute des **outils motorisés**, un **axe C** (indexation de la broche), un **axe Y**, une **contre-broche** ou une **tête B**, on parle de machine **multitâche** : la pièce sort finie en une seule prise (*done-in-one*). Les décolleteuses **de type suisse** sont une famille particulière, faite pour les pièces longues et fines.

## Les deux familles

| Critère | Décolleteuse de type suisse | Tour-fraiseur (turn-mill) |
|---|---|---|
| Principe | **Poupée mobile** : la barre avance à travers un **canon de guidage** ; l’outil coupe à quelques millimètres du support | Poupée fixe, la pièce est en porte-à-faux depuis le mandrin |
| Pièces idéales | Longues et fines, petits diamètres, grandes séries (médical, connectique, horlogerie, vis) | Pièces prismatiques et tournées complexes, plus gros diamètres, petites et moyennes séries |
| Points forts | Pas de flexion de la pièce, cadence, précision | Tête B (fraisage incliné), grande polyvalence, contre-broche |
| Contraintes | Barre rectifiée souvent nécessaire (tolérance du canon), réglage pointu | Coût, programmation et simulation exigeantes |

Modern Machine Shop résume la distinction : le canon de guidage sert à la **stabilité**, l’axe B à la **flexibilité angulaire** ; certaines suisses récentes ont les deux.

## Axes et options à connaître

| Élément | Rôle |
|---|---|
| Outils motorisés (*live tooling*) | Percer, fraiser, tarauder hors de l’axe |
| Axe C | Indexer ou interpoler la rotation de la broche (méplats, trous radiaux) |
| Axe Y | Décaler l’outil hors du centre (rainures, poches excentrées) |
| Contre-broche | Reprendre la pièce pour usiner l’arrière |
| Tête B | Incliner la broche de fraisage (trous et surfaces inclinés) |
| Ravitailleur de barres | Alimentation continue, production sans surveillance |

## Programmation

- La FAO doit connaître **la machine réelle** (cinématique, canaux, synchronisation des tourelles) : Mastercam Swiss Expert, Esprit, GibbsCAM ou les modules multitâches d’autres FAO (voir [[esprit]] et [[gibbscam]]).
- **Simulation machine complète** indispensable (collisions entre tourelles, broche et contre-broche).
- Post-processeur certifié pour le modèle exact (voir [[post-processors]]).
- Sur suisse, beaucoup de programmes sont encore écrits ou retouchés à la main par canal.

## Liste de vérification avant d’investir

- [ ] Famille de pièces (longueur/diamètre, quantités, tolérances)
- [ ] Matières (décolletage : 12L14, 303, laiton C360 — voir [[free-machining-12l14]])
- [ ] Barre rectifiée nécessaire ? Coût matière
- [ ] FAO et post disponibles pour le modèle
- [ ] Compétences de réglage dans l’équipe (voir [[careers-quebec]])

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Acheter une suisse pour des pièces courtes et grosses | Machine sous-utilisée, réglage lourd |
| Barre hors tolérance dans le canon | Vibrations, mauvaise précision ou grippage |
| Programmer sans simulation de la machine | Collision entre tourelles |
| Post générique | Synchronisation des canaux fausse |

## FAQ

### Peut-on faire de la suisse sans canon de guidage ?
Plusieurs suisses permettent de travailler **sans canon** pour utiliser de la barre non rectifiée et réduire la chute, au prix d’une rigidité moindre sur les pièces longues.

### Un tour avec outils motorisés est-il un tour-fraiseur ?
Au sens large, oui (machine multitâche) ; on réserve souvent « tour-fraiseur » aux machines avec tête B et capacités de fraisage importantes.

## À valider en atelier (Michaël)

- Les machines multitâches présentes chez vos clients et leurs familles de pièces.

## Sources

- [Modern Machine Shop — Swiss-types offer advantages beyond watchmaking](https://www.mmsonline.com/articles/swiss-types-offer-advantages-beyond-watchmaking), consulté le 26 novembre 2026.
- [Modern Machine Shop — Turn-mills 101](https://www.mmsonline.com/articles/turn-mills-101), consulté le 26 novembre 2026.
- [Modern Machine Shop — Turn-mills: being about the B-axis](https://www.mmsonline.com/articles/turn-mills-being-about-the-b-axis), consulté le 26 novembre 2026.
=== en
A basic CNC lathe turns and does simple operations. Add **live tooling**, a **C axis** (spindle indexing), a **Y axis**, a **sub-spindle** or a **B head**, and it becomes a **multitasking** machine: the part comes off finished in one setup (done-in-one). **Swiss-type** lathes are a special family, built for long, slender parts.

## The two families

| Criterion | Swiss-type lathe | Turn-mill |
|---|---|---|
| Principle | **Sliding headstock**: the bar feeds through a **guide bushing**; the tool cuts a few millimetres from the support | Fixed headstock, part overhangs from the chuck |
| Ideal parts | Long and slender, small diameters, high volume (medical, connectors, watchmaking, screws) | Complex prismatic and turned parts, larger diameters, small and medium runs |
| Strengths | No part deflection, throughput, precision | B head (angled milling), versatility, sub-spindle |
| Constraints | Ground bar often needed (bushing tolerance), demanding setup | Cost, demanding programming and simulation |

Modern Machine Shop sums up the distinction: the guide bushing is for **stability**, the B axis for **angular flexibility**; some recent Swiss machines have both.

## Axes and options to know

| Element | Role |
|---|---|
| Live tooling | Drill, mill, tap off-axis |
| C axis | Index or interpolate spindle rotation (flats, radial holes) |
| Y axis | Offset the tool off-centre (slots, off-centre pockets) |
| Sub-spindle | Transfer the part to machine the back |
| B head | Tilt the milling spindle (angled holes and faces) |
| Bar feeder | Continuous feed, unattended production |

## Programming

- CAM must know **the real machine** (kinematics, channels, turret synchronization): Mastercam Swiss Expert, Esprit, GibbsCAM or other CAMs’ multitasking modules (see [[esprit]] and [[gibbscam]]).
- **Full machine simulation** is essential (collisions between turrets, spindle and sub-spindle).
- A certified post for the exact model (see [[post-processors]]).
- On Swiss machines, many programs are still written or edited by hand per channel.

## Checklist before investing

- [ ] Part family (length/diameter, quantities, tolerances)
- [ ] Materials (screw machining: 12L14, 303, C360 brass — see [[free-machining-12l14]])
- [ ] Ground bar needed? Material cost
- [ ] CAM and post available for the model
- [ ] Setup skills in the team (see [[careers-quebec]])

## Common mistakes

| Mistake | Consequence |
|---|---|
| Buying a Swiss for short, large parts | Under-used machine, heavy setup |
| Bar out of tolerance in the bushing | Vibration, poor precision or seizing |
| Programming without machine simulation | Turret collision |
| Generic post | Wrong channel synchronization |

## FAQ

### Can a Swiss run without a guide bushing?
Several Swiss machines can run **guide-bushing-less** to use unground bar and reduce remnant, at the cost of rigidity on long parts.

### Is a lathe with live tools a turn-mill?
Broadly yes (a multitasking machine); “turn-mill” usually means machines with a B head and serious milling capacity.

## For Michaël to review

- The multitasking machines at your customers and their part families.

## Sources

- [Modern Machine Shop — Swiss-types offer advantages beyond watchmaking](https://www.mmsonline.com/articles/swiss-types-offer-advantages-beyond-watchmaking), consulted November 26, 2026.
- [Modern Machine Shop — Turn-mills 101](https://www.mmsonline.com/articles/turn-mills-101), consulted November 26, 2026.
- [Modern Machine Shop — Turn-mills: being about the B-axis](https://www.mmsonline.com/articles/turn-mills-being-about-the-b-axis), consulted November 26, 2026.
