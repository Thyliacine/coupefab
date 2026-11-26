---
id: thc-hunting
hub: troubleshooting
order: 20
nav: THC qui oscille ou plonge | THC hunting and diving
kicker: Dépannage · plasma | Troubleshooting · plasma
level: intermediaire
schema: HowTo
tags: thc, torch height control, arc voltage, hunting, diving, anti-dive, corner hold, voids, ihs, ohmic, float switch, tip volts, mach4, firecontrol, qtplasmac
related: cut-charts, plasma-troubleshooting, torchmate-avid, linuxcnc
fr_slug: depannage-thc-oscille-plonge
en_slug: thc-hunting-diving-troubleshooting
fr_title: Dépannage du contrôle de hauteur (THC) : torche qui oscille, plonge ou monte
en_title: Torch height control (THC) troubleshooting: hunting, diving or climbing torch
fr_desc: Pourquoi le THC « chasse », plonge dans les coins ou au-dessus des vides, ou fait monter la torche : tension d’arc, anti-plongée, délai d’activation, consommables usés, mise à la masse. Méthode de diagnostic pas à pas.
en_desc: Why the THC hunts, dives in corners or over voids, or lifts the torch: arc voltage, anti-dive, activation delay, worn consumables, grounding. A step-by-step diagnostic method.
---
=== fr
Le contrôle de hauteur (THC) maintient une **tension d’arc** constante ; comme la tension augmente avec la longueur d’arc, il monte ou descend la torche pour garder la consigne. Mais c’est une mesure **indirecte** de la hauteur : tout ce qui change la tension sans changer la hauteur trompe le THC. Avid CNC résume bien les cas typiques : entrées/sorties, coins serrés, petits trous, et passage au-dessus de vides.

## Symptôme → cause → correctif

| Symptôme | Cause probable | Correctif |
|---|---|---|
| La torche plonge dans les coins | La machine ralentit, la tension monte, le THC descend | Anti-plongée (*anti-dive / corner hold*) basée sur la vitesse ; seuil autour de la vitesse de coupe selon la commande |
| Plongée au-dessus d’une pièce déjà coupée (vide) | Plus de métal sous la torche, tension qui grimpe | Anti-plongée sur variation de tension (*void sensing*), ordre de coupe, éviter de recouper au-dessus des vides |
| Oscillation continue (*hunting*) | Gain/vitesse du THC trop élevés, bruit électrique, consigne instable | Réduire la sensibilité, vérifier masse et câblage, filtres selon le fabricant |
| Torche qui monte peu à peu en cours de coupe | Consommables usés (la tension augmente avec l’usure), consigne trop haute | Changer électrode/buse ; revenir à la charte |
| Torche qui frotte la tôle | Consigne trop basse, tôle gondolée, THC trop lent | Revenir à la tension de la charte, profil matière plus réactif |
| Plongée à l’entrée | THC activé trop tôt, pendant que la vitesse s’établit | Délai d’activation après le perçage (*THC delay*) |
| Comportement erratique partout | Mauvaise mise à la masse, câble de masse endommagé, interférences HF | Masse directe sur la table et la tôle, câbles séparés, procédure du fabricant |

## Méthode de diagnostic

1. **Revenir à la base** : consommables neufs, charte de la source plasma (courant, hauteur, tension, vitesse) ; voir [[cut-charts]].
2. **Vérifier l’IHS** (palpage initial) : la hauteur de perçage dépend d’un bon palpage (ohmique ou flottant).
3. **Couper une ligne droite** sur une tôle plate avec THC actif : si ça oscille déjà, le problème est le réglage ou l’électrique.
4. **Ajouter des coins et des petits trous** : si ça plonge seulement là, c’est l’anti-plongée.
5. **Couper au-dessus d’une rainure déjà coupée** : teste la détection de vide.
6. **Lire le journal** si la commande en a un (Mach4 chez Avid, QtPlasmaC) et marquer les endroits problématiques.

> [!TIP] Bloquez le THC sur les **petits trous** et les petits détails : la vitesse n’y est jamais stable. SheetCam peut le faire par règles de trajet (voir [[torchmate-avid]]), QtPlasmaC par paramètres de trou (voir [[linuxcnc]]).

## Liste de vérification

- [ ] Consommables neufs et conformes à la charte
- [ ] Tension cible = charte (ajustée seulement après essai)
- [ ] Délai d’activation du THC après perçage réglé
- [ ] Anti-plongée active (vitesse et/ou vide)
- [ ] THC bloqué sur petits trous
- [ ] Masse vérifiée (table, tôle, source)

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Monter la sensibilité pour « suivre » la tôle | Oscillation |
| Laisser la même tension de l’électrode neuve à usée | Hauteur qui dérive |
| THC actif sur tout le programme | Plongées aux trous et coins |
| Diviseur de tension mal configuré | Lecture fausse, THC incohérent |

## FAQ

### Faut-il toujours utiliser le THC ?
Pas sur des pièces très petites ou des tôles très minces et bien planes, où la hauteur fixe après palpage peut suffire. Sur de grandes tôles gondolées, oui.

### Ma tension affichée n’est pas celle de la charte : erreur ?
Pas forcément : diviseur, câblage et usure modifient la lecture. Ce qui compte, c’est la qualité de coupe et la hauteur réelle (vérifiez à la jauge).

## À valider en atelier (Michaël)

- Vos réglages d’anti-plongée par commande (FireControl, Mach4, QtPlasmaC).
- Les cas de masse/HF déjà rencontrés.

## Sources

- [Avid CNC — Mach4 Plasma Users Guide (théorie et réglage du THC)](https://www.avidcnc.com/support/instructions/software/plasmaUsersGuide/), consulté le 26 novembre 2026.
- [Hypertherm — Torch height control for plasma cutting](https://www.hypertherm.com/resources/more-resources/articles/torch-height-control-for-plasma-cutting/), consulté le 26 novembre 2026.
- [LinuxCNC — QtPlasmaC documentation](https://linuxcnc.org/docs/stable/html/plasma/qtplasmac.html), consulté le 26 novembre 2026.
=== en
Torch height control (THC) holds a constant **arc voltage**; since voltage rises with arc length, it moves the torch up or down to keep the setpoint. But it’s an **indirect** height measurement: anything that changes voltage without changing height fools the THC. Avid CNC sums up the typical cases well: lead-ins/outs, tight corners, small holes, and moving over voids.

## Symptom → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Torch dives in corners | Machine slows, voltage rises, THC goes down | Velocity-based anti-dive (corner hold); threshold near cut speed depending on the control |
| Dives over an already-cut part (void) | No metal under the torch, voltage climbs | Voltage-change anti-dive (void sensing), cut order, avoid crossing voids |
| Constant oscillation (hunting) | THC gain/speed too high, electrical noise, unstable setpoint | Reduce sensitivity, check ground and wiring, filtering per the manufacturer |
| Torch slowly climbs during the cut | Worn consumables (voltage rises with wear), setpoint too high | Replace electrode/nozzle; back to the chart |
| Torch drags on the plate | Setpoint too low, warped sheet, THC too slow | Back to chart voltage, more responsive material profile |
| Dive at the lead-in | THC activated too early, while speed builds | Activation delay after pierce (THC delay) |
| Erratic behaviour everywhere | Poor grounding, damaged ground cable, HF interference | Direct ground on table and plate, separated cables, manufacturer’s procedure |

## Diagnostic method

1. **Back to basics**: new consumables, plasma source chart (current, height, voltage, speed); see [[cut-charts]].
2. **Check IHS** (initial height sensing): pierce height depends on good sensing (ohmic or float).
3. **Cut a straight line** on a flat sheet with THC on: if it already oscillates, it’s tuning or electrical.
4. **Add corners and small holes**: if it only dives there, it’s anti-dive.
5. **Cut across an already-cut slot**: tests void detection.
6. **Read the log** if the control has one (Mach4 at Avid, QtPlasmaC) and mark problem spots.

> [!TIP] Inhibit THC on **small holes** and small details: speed is never stable there. SheetCam can do it with path rules (see [[torchmate-avid]]), QtPlasmaC with hole settings (see [[linuxcnc]]).

## Checklist

- [ ] New consumables matching the chart
- [ ] Target voltage = chart (adjusted only after testing)
- [ ] THC activation delay after pierce set
- [ ] Anti-dive enabled (velocity and/or void)
- [ ] THC inhibited on small holes
- [ ] Ground checked (table, plate, power source)

## Common mistakes

| Mistake | Consequence |
|---|---|
| Raising sensitivity to “follow” the sheet | Oscillation |
| Same voltage from new to worn electrode | Height drifts |
| THC active for the whole program | Dives at holes and corners |
| Voltage divider misconfigured | Wrong reading, inconsistent THC |

## FAQ

### Should THC always be used?
Not on very small parts or very thin, flat sheets, where fixed height after sensing can be enough. On large warped sheets, yes.

### My displayed voltage isn’t the chart’s: is that wrong?
Not necessarily: divider, wiring and wear change the reading. What matters is cut quality and actual height (check with a gauge).

## For Michaël to review

- Your anti-dive settings per control (FireControl, Mach4, QtPlasmaC).
- Ground/HF cases you’ve run into.

## Sources

- [Avid CNC — Mach4 Plasma Users Guide (THC theory and tuning)](https://www.avidcnc.com/support/instructions/software/plasmaUsersGuide/), consulted November 26, 2026.
- [Hypertherm — Torch height control for plasma cutting](https://www.hypertherm.com/resources/more-resources/articles/torch-height-control-for-plasma-cutting/), consulted November 26, 2026.
- [LinuxCNC — QtPlasmaC documentation](https://linuxcnc.org/docs/stable/html/plasma/qtplasmac.html), consulted November 26, 2026.
