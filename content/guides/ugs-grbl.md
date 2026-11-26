---
id: ugs-grbl
hub: software
group: control
order: 40
mono: gr
nav: UGS / grbl | UGS / grbl
kicker: Logiciel libre · commande | Open source · control
level: debutant
schema: HowTo
tags: ugs, universal gcode sender, grbl, grblhal, router, laser, settings, $$, homing, jogging, probe
related: cnc-router, vectric, freecad-cam, work-offsets
fr_slug: ugs-grbl
en_slug: ugs-grbl
fr_title: UGS et grbl : connecter, régler et lancer un travail sur un petit routeur CNC
en_title: UGS and grbl: connect, set up and run a job on a small CNC router
fr_desc: Universal Gcode Sender avec grbl ou grblHAL : connexion, assistant de configuration, paramètres $$, prise d’origine, déplacement manuel, zéro de travail, sonde et envoi du programme.
en_desc: Universal Gcode Sender with grbl or grblHAL: connecting, setup wizard, $$ settings, homing, jogging, work zero, probing and sending the program.
---
=== fr
**grbl** est un micrologiciel libre qui transforme une petite carte (souvent Arduino) en commande CNC ; **grblHAL** en est l’évolution pour des cartes 32 bits plus puissantes. **Universal Gcode Sender (UGS)** est l’interface libre la plus utilisée pour les piloter depuis un PC.

## Compatibilité

| Micrologiciel | UGS |
|---|---|
| grbl 1.1 | Pris en charge |
| grblHAL | Pris en charge à partir de UGS 2.1.27, en mode compatible grbl 1.1 |

## Démarche

1. Installer **UGS Platform** (ou UGS Classic) ; brancher la machine en USB.
2. Choisir le micrologiciel, le port et la vitesse (souvent 115 200 bauds) ; **Connecter**.
3. Lancer l’**assistant de configuration** : sens des moteurs, pas par millimètre, fins de course, prise d’origine, limites logicielles.
4. Vérifier les paramètres avec `$$` (liste des réglages grbl).
5. **Prise d’origine** (`$H`) si la machine a des fins de course.
6. Déplacer manuellement (jog) jusqu’au point zéro de la pièce ; **remettre à zéro** X, Y, Z (zéro de travail) — ou utiliser une **sonde** pour le Z.
7. Ouvrir le G-code (post grbl de la FAO : [Vectric](/guides/vectric-vcarve-aspire/), [Fusion](/guides/fusion-fao-debuter/), [FreeCAD](/guides/freecad-cam/)) ; vérifier la visualisation.
8. **Envoyer**, la main près de l’arrêt d’urgence.

## Paramètres grbl à connaître

| Paramètre | Rôle |
|---|---|
| `$100`–`$102` | Pas par mm (X, Y, Z) |
| `$110`–`$112` | Vitesse maximale |
| `$120`–`$122` | Accélération |
| `$20` / `$21` | Limites logicielles / matérielles |
| `$22` | Activation de la prise d’origine |
| `$130`–`$132` | Course maximale |

> [!TIP] Notez vos `$$` dans un fichier : après une mise à jour de micrologiciel ou un remplacement de carte, vous retrouverez la machine en quelques minutes.

## Erreurs fréquentes

| Message ou symptôme | Cause habituelle |
|---|---|
| ALARM après la mise sous tension | Prise d’origine requise (`$22=1`) : lancer `$H` |
| ALARM:2 (limite logicielle) | Le programme sort de la course, ou zéro mal placé |
| Pièce à la mauvaise taille | Pas par mm faux ; calibrer sur une grande distance |
| Commande non reconnue | Post non grbl (codes non pris en charge) |

## FAQ

### grbl peut-il piloter une table plasma ?
Oui pour des montages simples, mais sans contrôle de hauteur natif. Pour le plasma, préférez une commande avec THC — voir [LinuxCNC/QtPlasmaC](/guides/linuxcnc-qtplasmac/) ou [FireControl](/guides/firecontrol-langmuir/).

## À valider en atelier (Michaël)

- Rien de spécifique ; vérifier la cohérence avec vos machines.

## Sources

- [Universal Gcode Sender — site officiel](https://winder.github.io/ugs_website/), consulté le 26 novembre 2026.
- [grbl — Wiki, configuration](https://github.com/gnea/grbl/wiki/Grbl-v1.1-Configuration).
- [grblHAL](https://github.com/grblHAL).
=== en
**grbl** is open-source firmware that turns a small board (often Arduino) into a CNC control; **grblHAL** is its evolution for more powerful 32-bit boards. **Universal Gcode Sender (UGS)** is the most used open-source interface to drive them from a PC.

## Compatibility

| Firmware | UGS |
|---|---|
| grbl 1.1 | Supported |
| grblHAL | Supported from UGS 2.1.27, in grbl 1.1-compatible mode |

## Workflow

1. Install **UGS Platform** (or UGS Classic); plug the machine in over USB.
2. Pick firmware, port and baud rate (often 115,200); **Connect**.
3. Run the **setup wizard**: motor direction, steps per millimetre, limit switches, homing, soft limits.
4. Check settings with `$$` (grbl settings list).
5. **Home** (`$H`) if the machine has limit switches.
6. Jog to the part zero point; **reset zero** on X, Y, Z (work zero) — or use a **probe** for Z.
7. Open the G-code (CAM grbl post: [Vectric](/en/guides/vectric-vcarve-aspire/), [Fusion](/en/guides/fusion-cam-getting-started/), [FreeCAD](/en/guides/freecad-cam/)); check the visualizer.
8. **Send**, hand near the emergency stop.

## grbl settings to know

| Setting | Role |
|---|---|
| `$100`–`$102` | Steps per mm (X, Y, Z) |
| `$110`–`$112` | Max rate |
| `$120`–`$122` | Acceleration |
| `$20` / `$21` | Soft / hard limits |
| `$22` | Homing enable |
| `$130`–`$132` | Max travel |

> [!TIP] Save your `$$` to a file: after a firmware update or board swap, you’ll have the machine back in minutes.

## Common mistakes

| Message or symptom | Usual cause |
|---|---|
| ALARM after power-up | Homing required (`$22=1`): run `$H` |
| ALARM:2 (soft limit) | Program exceeds travel, or zero misplaced |
| Part the wrong size | Wrong steps per mm; calibrate over a long distance |
| Unsupported command | Non-grbl post (unsupported codes) |

## FAQ

### Can grbl drive a plasma table?
Yes for simple builds, but with no native height control. For plasma, prefer a control with THC — see [LinuxCNC/QtPlasmaC](/en/guides/linuxcnc-qtplasmac/) or [FireControl](/en/guides/firecontrol-langmuir/).

## For Michaël to review

- Nothing specific; check consistency with your machines.

## Sources

- [Universal Gcode Sender — official site](https://winder.github.io/ugs_website/), consulted November 26, 2026.
- [grbl — Wiki, configuration](https://github.com/gnea/grbl/wiki/Grbl-v1.1-Configuration).
- [grblHAL](https://github.com/grblHAL).
