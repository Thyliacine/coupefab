---
id: canned-cycles
hub: fundamentals
order: 40
nav: Cycles de perçage G81–G89 | Canned cycles G81–G89
kicker: Fondamentaux · G-code | Fundamentals · G-code
level: intermediaire
schema: HowTo
tags: canned cycles, cycles fixes, g81, g82, g83, g73, g84, g85, g86, g80, g98, g99, r plane, plan r, peck drilling, perçage débourrage, spot drill, boring, alésage, l repeat
related: gcode, threading, haas, fanuc
fr_slug: cycles-percage-g81-g83
en_slug: canned-cycles-g81-g83
fr_title: Cycles fixes de perçage (G81, G82, G83, G84…) : plans R, G98/G99 et pièges
en_title: Drilling canned cycles (G81, G82, G83, G84…): R planes, G98/G99 and pitfalls
fr_desc: Comment fonctionnent les cycles fixes de perçage, taraudage et alésage, la différence entre G98 et G99, l’annulation par G80 et les erreurs qui cassent des outils.
en_desc: How drilling, tapping and boring canned cycles work, the difference between G98 and G99, cancelling with G80, and the mistakes that break tools.
---
=== fr
Les **cycles fixes** regroupent en une ligne les mouvements répétitifs en Z : perçage, taraudage, alésage. Une fois appelé, le cycle est **modal** : il se répète à chaque nouvelle position X/Y jusqu’à `G80`. Les exemples suivent le dialecte Haas/Fanuc ; vérifiez les détails dans le manuel de votre commande.

## Les cinq étapes d’un cycle

1. Positionnement en X et Y (en rapide).
2. Rapide jusqu’au **plan R**.
3. Perçage, taraudage ou alésage selon le cycle.
4. Action au fond du trou (pause, arrêt de broche…).
5. Retour au plan R (`G99`) ou au point de départ (`G98`).

## Les cycles courants

| Code | Mouvement | Usage |
|---|---|---|
| `G81` | Avance, retour rapide | Perçage simple |
| `G82` | Avance, pause, retour rapide | Pointage, lamage |
| `G83` | Avance par débourrages (`Q`), retour rapide | Perçage profond |
| `G73` | Débourrage court (brise-copeaux) | Perçage à grande vitesse |
| `G84` | Avance, inversion de broche, sortie en avance | Taraudage à droite (voir [[threading]]) |
| `G85` | Avance aller et retour | Alésage à l’alésoir |
| `G86` | Avance, arrêt broche, retour rapide | Alésage |
| `G80` | — | Annule le cycle |

## G98 ou G99 ?

- **G99** : retour au plan R entre les trous. Plus rapide, à utiliser quand rien ne dépasse entre les trous.
- **G98** : retour au Z de départ. À utiliser pour passer par-dessus un mors, une bride ou un épaulement.

```gcode
T3 M06 (FORET 6.8)
G90 G54 G00 X10. Y10. S1800 M03
G43 H03 Z25. M08
G83 G99 Z-20. R2. Q3. F150.
X30.
X50.
G98 X50. Y40. (remonte au Z initial avant de franchir la bride)
X10. Y40.
G80 G00 Z25. M09
```

## Liste de vérification

- [ ] Plan R au-dessus de la pièce, pas dans la matière
- [ ] `G98` pour franchir brides et mors
- [ ] `Q` de débourrage adapté au diamètre et à la matière
- [ ] `G80` avant tout mouvement hors cycle
- [ ] Profondeur `Z` incluant la pointe du foret si le trou doit être traversant

## Erreurs fréquentes

- Oublier `G80` : le mouvement X/Y suivant déclenche un trou de plus.
- `G99` avec une bride entre deux trous : collision.
- Oublier la longueur de pointe du foret (118° ou 135°) dans la profondeur.
- Plan R calculé en incrémental par erreur.

## FAQ

### Dois-je démarrer la broche avant G84 ?
Sur Haas, le cycle `G84` démarre la broche lui-même. Sur d’autres commandes, vérifiez le manuel.

### Comment répéter un trou à pas constant ?
En `G91` avec un compteur `L` (Haas) : chaque répétition déplace d’un pas et refait le cycle.

## À valider en atelier (Michaël)

- Valeurs `Q` habituelles par diamètre et matière.
- Comportement des cycles sur nos commandes non Haas.

## Sources

- [Haas — Mill Programming Workbook (PDF)](https://haascnc.com/content/dam/haascnc/en/service/reference/programming-workbooks/mill---programming-workbook.pdf) : cinq étapes d’un cycle, G98/G99, tableau G81–G89, répétition `L`, G84. Consulté le 26 novembre 2026.
- [LinuxCNC — G-codes (cycles G81–G89)](https://linuxcnc.org/docs/stable/html/gcode/g-code.html).

=== en
**Canned cycles** pack repetitive Z moves into one line: drilling, tapping, boring. Once called, the cycle is **modal**: it repeats at each new X/Y position until `G80`. The examples follow the Haas/Fanuc dialect; check details in your control’s manual.

## The five steps of a cycle

1. X and Y positioning (rapid).
2. Rapid to the **R plane**.
3. Drilling, tapping or boring depending on the cycle.
4. Action at the bottom of the hole (dwell, spindle stop…).
5. Return to the R plane (`G99`) or the starting point (`G98`).

## Common cycles

| Code | Motion | Use |
|---|---|---|
| `G81` | Feed in, rapid out | Plain drilling |
| `G82` | Feed in, dwell, rapid out | Spot drilling, counterboring |
| `G83` | Feed in pecks (`Q`), rapid out | Deep drilling |
| `G73` | Short peck (chip break) | High-speed drilling |
| `G84` | Feed in, spindle reverse, feed out | Right-hand tapping (see [[threading]]) |
| `G85` | Feed in and out | Reaming |
| `G86` | Feed in, spindle stop, rapid out | Boring |
| `G80` | — | Cancels the cycle |

## G98 or G99?

- **G99**: return to the R plane between holes. Faster; use it when nothing sticks up between holes.
- **G98**: return to the starting Z. Use it to clear a jaw, clamp or shoulder.

```gcode
T3 M06 (6.8 DRILL)
G90 G54 G00 X10. Y10. S1800 M03
G43 H03 Z25. M08
G83 G99 Z-20. R2. Q3. F150.
X30.
X50.
G98 X50. Y40. (back to initial Z before clearing the clamp)
X10. Y40.
G80 G00 Z25. M09
```

## Checklist

- [ ] R plane above the part, not in the material
- [ ] `G98` to clear clamps and jaws
- [ ] Peck `Q` suited to diameter and material
- [ ] `G80` before any non-cycle move
- [ ] `Z` depth includes the drill point if the hole must go through

## Common mistakes

- Forgetting `G80`: the next X/Y move drills an extra hole.
- `G99` with a clamp between two holes: crash.
- Forgetting the drill point length (118° or 135°) in the depth.
- R plane computed in incremental by mistake.

## FAQ

### Do I start the spindle before G84?
On Haas, the `G84` cycle starts the spindle itself. On other controls, check the manual.

### How do I repeat a hole at a fixed pitch?
In `G91` with an `L` count (Haas): each repeat moves one pitch and runs the cycle again.

## For Michaël to review

- Usual `Q` values by diameter and material.
- Cycle behaviour on our non-Haas controls.

## Sources

- [Haas — Mill Programming Workbook (PDF)](https://haascnc.com/content/dam/haascnc/en/service/reference/programming-workbooks/mill---programming-workbook.pdf): five steps of a cycle, G98/G99, G81–G89 table, `L` repeat, G84. Consulted November 26, 2026.
- [LinuxCNC — G-codes (G81–G89 cycles)](https://linuxcnc.org/docs/stable/html/gcode/g-code.html).
