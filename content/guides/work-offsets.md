---
id: work-offsets
hub: fundamentals
order: 3
nav: Décalages d’origine (G54) | Work offsets (G54)
kicker: Fondamentaux · usinage | Fundamentals · machining
level: debutant
schema: HowTo
tags: g54, work offset, wcs, tool length, probing, mill, router, lathe
related: gcode, cnc-mill, cnc-router, post-processors
fr_slug: decalages-origine-g54
en_slug: work-offsets-g54
fr_title: Décalages d’origine (G54 à G59) et longueurs d’outil, sans se tromper
en_title: Work offsets (G54–G59) and tool lengths, without mistakes
fr_desc: Coordonnées machine, origine pièce, G54–G59, longueur d’outil G43 : comment ils s’additionnent, comment prendre une origine, et les erreurs qui cassent des outils.
en_desc: Machine coordinates, work zero, G54–G59, G43 tool length: how they stack up, how to set a work zero, and the mistakes that break tools.
---
=== fr
Une machine CNC connaît sa propre position (**coordonnées machine**, fixées par la prise d’origine machine — le *homing*). Votre programme, lui, est écrit depuis un point de la pièce (**origine pièce**). Le **décalage d’origine** (work offset) fait le lien entre les deux. Comprendre comment les décalages s’additionnent évite la majorité des collisions.

## Ce qui s’additionne

| Couche | Code | Qui la règle |
|---|---|---|
| Coordonnées machine | `G53` | Le *homing* (contacteurs ou index) |
| Décalage d’origine pièce | `G54`…`G59` (plus étendus selon la commande) | L’opérateur, au palpeur ou au chant |
| Longueur d’outil | `G43 H…` | Le présetteur, le palpeur d’outil ou l’opérateur |
| Rayon d’outil (si compensation) | `G41/G42 D…` | Table d’outils |
| Décalage temporaire | `G92` | À éviter, ou à annuler explicitement |

Position réelle de l’outil = position programmée + décalage d’origine + longueur (et rayon) d’outil. LinuxCNC documente précisément cet empilement dans sa page *Coordinate systems*.

## Prendre une origine pièce (fraiseuse ou routeur)

1. **Faire le homing** de la machine à la mise sous tension, avant tout décalage.
2. **Choisir le point zéro** que le programmeur a choisi dans le FAO (coin, centre, dessus de la pièce). Il doit figurer sur la feuille de réglage.
3. **X et Y** : palpeur 3D, chercheur d’arête ou outil au papier sur deux faces ; compensez le rayon du palpeur ou de l’outil.
4. **Z** : sur le dessus de la pièce (ou sur la table, selon la convention), avec palpeur, cale ou plaque de touche de hauteur connue.
5. **Enregistrer** dans le bon décalage (`G54` par exemple) — pas dans un autre registre par erreur.
6. **Vérifier** : en MDI, `G54 G0 X0 Y0` puis descendre en Z lentement avec la réduction d’avance, jusqu’à une hauteur sûre au-dessus du zéro.

## Longueurs d’outil : deux philosophies

- **Longueur réelle** mesurée depuis la face de broche (présetteur ou palpeur d’outil) : le Z de `G54` est mesuré une fois, les outils sont interchangeables.
- **Longueur relative** à un outil maître : plus simple sans présetteur, mais tout dépend de l’outil maître.

Ne mélangez pas les deux philosophies sur une même machine sans les documenter.

> [!WARN] Un `G43` oublié, ou un `H` qui ne correspond pas au `T` (par exemple `T3 M6` puis `G43 H1`), fait plonger l’outil de la différence de longueur. Faites afficher les correcteurs actifs avant la première passe.

## Plusieurs pièces : G54, G55, G56…

Un étau par décalage permet de lancer le même programme sur plusieurs postes. Le FAO assigne un décalage par réglage ; la commande les garde en mémoire. Sur un routeur, `G54` sert souvent au dessus de la tôle et `G55` au dessus de la table martyre (pour les coupes traversantes) — à documenter.

## Tour et plasma

- **Tour** : l’origine Z est généralement la face finie de la pièce ; X est le centre de la broche (diamètre). Les correcteurs d’outil portent les deux.
- **Plasma** : le Z est en général géré par le palpage de hauteur initial (IHS) à chaque perçage ; l’origine X/Y est souvent un coin de la tôle, réglé par déplacement manuel.

## Erreurs fréquentes

- Régler le zéro avant le *homing* : le décalage n’a aucune référence fiable.
- Enregistrer l’origine dans `G55` alors que le programme appelle `G54`.
- Oublier le rayon du palpeur ou de la fraise dans la prise d’origine X/Y.
- Laisser un `G92` actif d’une séance précédente.

## Liste de vérification avant le cycle

- [ ] Machine référencée (homing fait)
- [ ] Décalage appelé par le programme = décalage réglé
- [ ] Longueurs d’outil à jour, `H` = `T`
- [ ] Aucun `G92` actif
- [ ] Premier mouvement vérifié lentement, à hauteur sûre

## FAQ

### Quelle différence entre G53 et G28 ?
`G53` déplace en coordonnées machine absolues, le temps d’une ligne. `G28` passe par un point intermédiaire puis va à une position de référence enregistrée ; l’ordre et le mode `G90/G91` comptent.

### Combien de décalages existent ?
`G54` à `G59` partout ; beaucoup de commandes ajoutent des décalages étendus (`G59.1`–`G59.3` sur LinuxCNC, `G54.1 P…` sur des commandes de type Fanuc).

## À valider en atelier (Michaël)

- Votre convention de zéro sur les tables plasma (coin de tôle, butées, laser de pointage).
- Méthode de longueur d’outil utilisée dans vos ateliers.

## Sources

- [LinuxCNC — Coordinate systems](https://linuxcnc.org/docs/stable/html/gcode/coordinates.html), consulté le 26 novembre 2026.
- [LinuxCNC — Tool compensation](https://linuxcnc.org/docs/stable/html/gcode/tool-compensation.html).
- [LinuxCNC — G-codes (G43, G53, G54–G59, G92)](https://linuxcnc.org/docs/stable/html/gcode/g-code.html).
=== en
A CNC machine knows its own position (**machine coordinates**, set by homing). Your program is written from a point on the part (**work zero**). The **work offset** links the two. Understanding how offsets stack up prevents most crashes.

## What stacks up

| Layer | Code | Who sets it |
|---|---|---|
| Machine coordinates | `G53` | Homing (switches or index) |
| Work offset | `G54`…`G59` (more on some controls) | The operator, by probe or edge |
| Tool length | `G43 H…` | Presetter, tool setter or operator |
| Tool radius (if compensating) | `G41/G42 D…` | Tool table |
| Temporary offset | `G92` | Avoid, or cancel explicitly |

Actual tool position = programmed position + work offset + tool length (and radius). LinuxCNC documents this stack precisely on its *Coordinate systems* page.

## Setting a work zero (mill or router)

1. **Home** the machine at power-up, before any offset.
2. **Pick the zero point** the programmer chose in CAM (corner, centre, top of part). It must be on the setup sheet.
3. **X and Y**: 3D probe, edge finder or tool-and-paper on two faces; account for the probe or tool radius.
4. **Z**: on top of the part (or the table, per convention), with a probe, gauge block or touch plate of known height.
5. **Store** in the right offset (`G54` for example) — not in another register by mistake.
6. **Verify**: in MDI, `G54 G0 X0 Y0`, then step Z down slowly with feed override to a safe height above zero.

## Tool lengths: two philosophies

- **True length** measured from the spindle face (presetter or tool setter): the `G54` Z is measured once, tools are interchangeable.
- **Length relative** to a master tool: simpler without a presetter, but everything depends on the master tool.

Do not mix both on the same machine without documenting it.

> [!WARN] A forgotten `G43`, or an `H` that does not match the `T` (for example `T3 M6` then `G43 H1`), plunges the tool by the length difference. Display the active offsets before the first pass.

## Several parts: G54, G55, G56…

One vise per offset lets you run the same program on several stations. CAM assigns one offset per setup; the control stores them. On a router, `G54` often refers to the top of the sheet and `G55` to the spoilboard top (for through cuts) — document it.

## Lathe and plasma

- **Lathe**: Z zero is usually the finished face; X is spindle centre (diameter). Tool offsets carry both.
- **Plasma**: Z is generally handled by initial height sensing (IHS) at each pierce; X/Y zero is often a sheet corner set by jogging.

## Common mistakes

- Setting zero before homing: the offset has no reliable reference.
- Storing zero in `G55` while the program calls `G54`.
- Forgetting the probe or cutter radius when picking up X/Y.
- Leaving a `G92` active from a previous session.

## Pre-cycle checklist

- [ ] Machine homed
- [ ] Offset called by the program = offset set
- [ ] Tool lengths current, `H` = `T`
- [ ] No `G92` active
- [ ] First move checked slowly at a safe height

## FAQ

### What is the difference between G53 and G28?
`G53` moves in absolute machine coordinates for one line. `G28` goes through an intermediate point then to a stored reference position; order and `G90/G91` mode matter.

### How many offsets are there?
`G54` to `G59` everywhere; many controls add extended offsets (`G59.1`–`G59.3` on LinuxCNC, `G54.1 P…` on Fanuc-style controls).

## For Michaël to review

- Your zero convention on plasma tables (sheet corner, stops, laser pointer).
- The tool length method used in your shops.

## Sources

- [LinuxCNC — Coordinate systems](https://linuxcnc.org/docs/stable/html/gcode/coordinates.html), consulted November 26, 2026.
- [LinuxCNC — Tool compensation](https://linuxcnc.org/docs/stable/html/gcode/tool-compensation.html).
- [LinuxCNC — G-codes (G43, G53, G54–G59, G92)](https://linuxcnc.org/docs/stable/html/gcode/g-code.html).
