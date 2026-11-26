---
id: probing
hub: shop
order: 46
nav: Palpage sur machine | On-machine probing
kicker: Atelier · palpage | Shop · probing
level: intermediaire
schema: HowTo
tags: probing, palpage, palpeur, touch probe, tool setter, mesureur d'outil, renishaw, work offset, origine, broken tool detection, bris d'outil, in-process, process control, productive process pyramid
related: work-offsets, fixturing, measuring-inspection, haas
fr_slug: palpage-machine-palpeur-outil
en_slug: on-machine-probing
fr_title: Palpage sur machine : régler pièces et outils automatiquement et détecter les bris
en_title: On-machine probing: setting parts and tools automatically and catching breakage
fr_desc: À quoi servent le palpeur de pièce et le mesureur d’outil, les quatre niveaux de maîtrise du procédé de Renishaw, et une démarche pour mettre le palpage en place dans un atelier.
en_desc: What a part probe and a tool setter do, Renishaw’s four layers of process control, and a routine to bring probing into a shop.
---
=== fr
Un **palpeur de pièce** (dans la broche) et un **mesureur d’outil** (sur la table) remplacent les mesures manuelles par des cycles programmés. Résultat : moins d’erreurs de saisie, des réglages plus rapides et des bris d’outil détectés avant qu’ils ne gâchent une série.

## Ce que mesure chaque appareil

| Appareil | Mesure | Sert à |
|---|---|---|
| **Mesureur d’outil** | Longueur depuis la ligne de jauge de la broche ; diamètre en rotation | Correcteurs de longueur et de rayon ; détection de bris |
| **Palpeur de pièce** | Position d’une référence, orientation, dimensions du brut | Origine pièce (G54…), rotation de repère, contrôle de la matière |

Renishaw indique qu’un réglage automatisé par palpage peut être **jusqu’à 10 fois plus rapide** que les méthodes manuelles, et surtout prévisible.

## Les quatre niveaux de maîtrise (Renishaw)

1. **Fondation du procédé** : conditions stables (machine en bon état, contrôlée) avant l’usinage.
2. **Réglage du procédé** : position de la pièce, dimensions des outils, origines — pour que la première pièce soit bonne.
3. **Contrôle en cours d’usinage** : usure d’outil et dérive thermique compensées pendant la coupe.
4. **Surveillance après usinage** : vérifier le procédé et la pièce par rapport aux spécifications (souvent hors machine).

## Démarche de mise en place

1. **Mesureur d’outil d’abord** : longueurs automatiques, contrôle de bris sur les petits outils.
2. **Palpeur de pièce** : cycles de coin, de centre d’alésage et de dessus de pièce pour régler l’origine.
3. **Étalonner** le palpeur (longueur et rayon de bille effectifs) sur une bague étalon.
4. **Intégrer au programme** : réglage d’origine en début de cycle, contrôle de bris après les outils fragiles.
5. **Mesure en cours de cycle** sur les cotes critiques, avec correction automatique de l’usure si la commande le permet.

## Liste de vérification

- [ ] Palpeur étalonné après chaque changement de stylet
- [ ] Cycles de palpage de la commande activés (option)
- [ ] Contrôle de bris sur les outils fragiles et les forets de petit diamètre
- [ ] Origine palpée vérifiée sur la première pièce

## Erreurs fréquentes

- Ne jamais étalonner le palpeur : chaque mesure porte l’erreur.
- Palper une surface sale ou couverte de copeaux.
- Mesurer les outils hors machine sans tenir compte du serrage, du faux-rond et de la dilatation de la broche.

## FAQ

### Mesureur d’outil ou préréglage hors machine ?
Le préréglage hors machine libère la broche, mais ne voit pas le faux-rond, le serrage ni l’effet thermique de la broche ; le mesureur sur machine, si.

### Combien de fois vérifier les bris ?
Selon l’expérience : plus souvent pour les petits outils et ceux qui cassent le plus.

## À valider en atelier (Michaël)

- Palpeurs et mesureurs installés sur nos machines.
- Cycles de palpage utilisés au quotidien.

## Sources

- [Renishaw — Process setting](https://www.renishaw.com/en/process-setting--14158) : mesure d’outil et de pièce, jusqu’à 10 fois plus rapide. Consulté le 26 novembre 2026.
- [Renishaw — When do I probe?](https://www.renishaw.com/en/when-do-i-probe--12477) : niveaux de maîtrise du procédé.
- [Renishaw — Machine tool probes for workpiece set-up and inspection](https://www.renishaw.com/en/machine-tool-probes-for-workpiece-set-up-and-inspection--6075) : avantages du palpage.
- [Renishaw — Livre blanc TE500 : réglage d’outil et détection de bris (PDF)](https://www.renishaw.com/resourcecentre/download/white-paper-te500-tool-setting-and-broken-tool-detection--140170?userLanguage=en) : limites du préréglage hors machine, fréquence des contrôles de bris.

=== en
A **part probe** (in the spindle) and a **tool setter** (on the table) replace manual measuring with programmed cycles. The result: fewer typing errors, faster setups, and broken tools caught before they ruin a batch.

## What each device measures

| Device | Measures | Used for |
|---|---|---|
| **Tool setter** | Length from the spindle gauge line; diameter while spinning | Length and radius offsets; breakage detection |
| **Part probe** | Datum position, orientation, stock size | Work offset (G54…), coordinate rotation, stock check |

Renishaw says automated setting by probing can be **up to 10 times faster** than manual methods, and above all predictable.

## The four layers of control (Renishaw)

1. **Process foundation**: stable conditions (machine in good, checked condition) before machining.
2. **Process setting**: part location, tool sizes, offsets — so the first part is right.
3. **In-process control**: tool wear and thermal drift compensated during cutting.
4. **Post-process monitoring**: check the process and part against specification (often off-machine).

## Rollout routine

1. **Tool setter first**: automatic lengths, breakage checks on small tools.
2. **Part probe**: corner, bore-center and top-of-part cycles to set the work offset.
3. **Calibrate** the probe (effective length and ball radius) on a ring gauge.
4. **Build it into the program**: offset setting at cycle start, breakage check after fragile tools.
5. **In-cycle measurement** on critical sizes, with automatic wear correction if the control allows.

## Checklist

- [ ] Probe calibrated after every stylus change
- [ ] Control probing cycles enabled (option)
- [ ] Breakage checks on fragile tools and small drills
- [ ] Probed offset verified on the first part

## Common mistakes

- Never calibrating the probe: every measurement carries the error.
- Probing a dirty or chip-covered surface.
- Measuring tools off-machine without accounting for clamping, runout and spindle growth.

## FAQ

### Tool setter or off-machine presetter?
A presetter frees the spindle but can’t see runout, clamping or the spindle’s thermal effects; an on-machine setter can.

### How often should I check for breakage?
By experience: more often for small tools and the ones that break most.

## For Michaël to review

- Probes and tool setters installed on our machines.
- Probing cycles used day to day.

## Sources

- [Renishaw — Process setting](https://www.renishaw.com/en/process-setting--14158): tool and part setting, up to 10× faster. Consulted November 26, 2026.
- [Renishaw — When do I probe?](https://www.renishaw.com/en/when-do-i-probe--12477): process control layers.
- [Renishaw — Machine tool probes for workpiece set-up and inspection](https://www.renishaw.com/en/machine-tool-probes-for-workpiece-set-up-and-inspection--6075): benefits of probing.
- [Renishaw — TE500 white paper: tool setting and broken tool detection (PDF)](https://www.renishaw.com/resourcecentre/download/white-paper-te500-tool-setting-and-broken-tool-detection--140170?userLanguage=en): limits of off-machine presetting, breakage-check frequency.
