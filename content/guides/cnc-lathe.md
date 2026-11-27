---
id: cnc-lathe
hub: process
order: 6
nav: Tour CNC | CNC lathe
kicker: Procédé · usinage | Process · machining
level: intermediaire
schema: Article
tags: lathe, turning, css, g96, g97, insert, chuck, threading, mastercam lathe, tool nose radius
related: mastercam-posts-lathe, gcode, feeds-speeds, work-offsets
fr_slug: tour-cnc
en_slug: cnc-lathe
fr_title: Tour CNC : vitesse de coupe constante, plaquettes, correcteurs et filetage
en_title: CNC lathe: constant surface speed, inserts, offsets and threading
fr_desc: Les bases du tournage CNC : G96/G97 et limite de régime, mode diamètre, correcteurs d’outil, rayon de bec, choix des plaquettes, mors et filetage, avec les pièges qui coûtent cher.
en_desc: CNC turning basics: G96/G97 and spindle limit, diameter mode, tool offsets, nose radius, insert choice, jaws and threading, with the costly traps.
---
=== fr
Sur un tour, c’est la pièce qui tourne et l’outil qui se déplace en X (diamètre) et Z (longueur). La programmation suit le plan **G18** (XZ), avec ses propres réflexes : vitesse de coupe constante, rayon de bec, correcteurs d’usure.

## G96, G97 et la limite de régime

- **G96** : vitesse de coupe constante (CSS). La broche accélère quand le diamètre diminue, pour garder la même Vc.
- **G97** : régime constant en tr/min (filetage, perçage au centre).
- **Limite de régime** (souvent `G50 S…` sur les commandes de type Fanuc, `G96 … D…` sur LinuxCNC) : **obligatoire** avec G96, sinon la broche monte au maximum quand l’outil approche du centre.

> [!WARN] Un G96 sans limite de régime, avec une pièce longue ou des mors mal serrés, est l’une des situations les plus dangereuses d’un atelier de tournage. Vérifiez la limite admissible du mandrin et des mors.

## Diamètre ou rayon

La plupart des tours programment X **au diamètre** (LinuxCNC : `G7`). Une erreur de mode double ou divise par deux toutes les cotes en X.

## Correcteurs d’outil

| Correcteur | Contenu |
|---|---|
| Géométrie | Position de la pointe de l’outil par rapport à la référence machine (X, Z) |
| Usure | Petites corrections après mesure de la pièce |
| Rayon de bec et orientation | Pour la compensation de rayon (G41/G42) sur les cônes et rayons |

Corrigez une cote avec l’**usure**, pas en modifiant le programme ou la géométrie.

## Rayon de bec

Une plaquette a un rayon de bec (0,4 ; 0,8 mm…). Sans compensation, les cônes et les rayons sortent faux (la pointe théorique n’est pas le point de contact). Activez la compensation dans le FAO ou la commande, avec l’orientation du bec correcte.

## Choisir la plaquette

Le code ISO des plaquettes (par exemple CNMG 120408) décrit forme, angle de dépouille, tolérance, type, taille, épaisseur et rayon de bec. Le **brise-copeaux** et le **grade de carbure** se choisissent dans le catalogue du fabricant selon la matière (groupes ISO P, M, K, N…) et l’opération (ébauche, finition).

## Filetage

Le cycle de filetage (`G76` sur beaucoup de commandes) synchronise l’avance avec la broche. Les paramètres diffèrent d’une commande à l’autre : utilisez le cycle généré par le FAO pour **votre** post, ou la page du manuel. Régime constant (G97) obligatoire.

## Erreurs fréquentes

- Oublier la limite de régime en G96.
- Corriger la géométrie au lieu de l’usure.
- Pas de compensation de rayon de bec sur un cône précis.
- Pièce trop sortie des mors sans contre-pointe.

## Liste de vérification

- [ ] Limite de régime programmée avec G96 et compatible avec le mandrin et les mors
- [ ] Mode diamètre ou rayon confirmé pour X
- [ ] Correcteurs de géométrie mesurés ; corrections faites dans l’**usure**
- [ ] Rayon de bec et orientation saisis ; compensation active sur cônes et rayons
- [ ] Plaquette, brise-copeaux et grade de carbure adaptés à la matière
- [ ] Filetage en régime constant (G97), cycle du post de **votre** commande
- [ ] Porte-à-faux de la pièce raisonnable, contre-pointe si nécessaire

## FAQ

### Faut-il un FAO pour le tour ?
Les cycles de la commande (ébauche, finition, filetage) suffisent pour beaucoup de pièces simples. Pour les profils complexes et le tour-fraiseur, un FAO (Mastercam Lathe, Fusion, SolidWorks CAM Professional) fait gagner du temps. Voir [Mastercam : posts et tour](/guides/mastercam-post-tour/).

## Sources

- [LinuxCNC — Lathe user information](https://linuxcnc.org/docs/stable/html/lathe/lathe-user.html), consulté le 26 novembre 2026.
- [LinuxCNC — G-codes (G7, G8, G96, G97, G76)](https://linuxcnc.org/docs/stable/html/gcode/g-code.html).
- [Sandvik Coromant — Turning formulas](https://www.sandvik.coromant.com/en-us/knowledge/machining-formulas-definitions/turning-formulas-definitions).
=== en
On a lathe, the part spins and the tool moves in X (diameter) and Z (length). Programming uses the **G18** (XZ) plane, with its own habits: constant surface speed, nose radius, wear offsets.

## G96, G97 and the spindle limit

- **G96**: constant surface speed (CSS). The spindle speeds up as diameter shrinks, to hold the same Vc.
- **G97**: constant rpm (threading, centre drilling).
- **Spindle limit** (often `G50 S…` on Fanuc-style controls, `G96 … D…` on LinuxCNC): **mandatory** with G96, or the spindle climbs to max as the tool nears centre.

> [!WARN] G96 with no spindle limit, with a long part or poorly clamped jaws, is one of the most dangerous situations in a turning shop. Check the allowable speed of the chuck and jaws.

## Diameter or radius

Most lathes program X **on diameter** (LinuxCNC: `G7`). A mode mistake doubles or halves every X dimension.

## Tool offsets

| Offset | Content |
|---|---|
| Geometry | Tool tip position relative to machine reference (X, Z) |
| Wear | Small corrections after measuring the part |
| Nose radius and orientation | For radius compensation (G41/G42) on tapers and radii |

Correct a size with **wear**, not by editing the program or geometry.

## Nose radius

An insert has a nose radius (0.4, 0.8 mm…). Without compensation, tapers and radii come out wrong (the theoretical tip is not the contact point). Enable compensation in CAM or the control, with the correct tip orientation.

## Choosing the insert

The ISO insert code (for example CNMG 120408) describes shape, clearance angle, tolerance, type, size, thickness and nose radius. **Chipbreaker** and **grade** are chosen from the maker’s catalogue by material (ISO groups P, M, K, N…) and operation (roughing, finishing).

## Threading

The threading cycle (`G76` on many controls) syncs feed with the spindle. Parameters differ between controls: use the cycle CAM generates for **your** post, or the manual page. Constant rpm (G97) required.

## Common mistakes

- Forgetting the spindle limit in G96.
- Correcting geometry instead of wear.
- No nose radius compensation on a precise taper.
- Part sticking too far out of the jaws without a tailstock.

## Checklist

- [ ] Spindle speed limit programmed with G96 and within the chuck and jaw rating
- [ ] Diameter or radius mode confirmed for X
- [ ] Geometry offsets measured; corrections made in **wear**
- [ ] Nose radius and orientation entered; compensation on for tapers and radii
- [ ] Insert, chipbreaker and carbide grade suited to the material
- [ ] Threading at constant rpm (G97), cycle from **your** control’s post
- [ ] Reasonable part stick-out, tailstock if needed

## FAQ

### Do I need CAM for the lathe?
Control cycles (roughing, finishing, threading) are enough for many simple parts. For complex profiles and mill-turn, CAM (Mastercam Lathe, Fusion, SolidWorks CAM Professional) saves time. See [Mastercam: posts and lathe](/en/guides/mastercam-posts-and-lathe/).

## Sources

- [LinuxCNC — Lathe user information](https://linuxcnc.org/docs/stable/html/lathe/lathe-user.html), consulted November 26, 2026.
- [LinuxCNC — G-codes (G7, G8, G96, G97, G76)](https://linuxcnc.org/docs/stable/html/gcode/g-code.html).
- [Sandvik Coromant — Turning formulas](https://www.sandvik.coromant.com/en-us/knowledge/machining-formulas-definitions/turning-formulas-definitions).
