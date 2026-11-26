---
id: planetcnc
hub: software
group: control
order: 60
mono: Pl
nav: PlanetCNC TNG | PlanetCNC TNG
kicker: Commande PC · PlanetCNC | PC control · PlanetCNC
level: intermediaire
schema: HowTo
tags: planetcnc, tng, mk3, mk3/9, mk3/4, usb, ethernet, step dir, licence, license, breakout board, parallel port, routeur, mill, lathe, plasma
related: centroid-acorn, masso, mach, linuxcnc
fr_slug: planetcnc-tng-mk3
en_slug: planetcnc-tng-mk3
fr_title: PlanetCNC TNG et contrôleurs Mk3 : remplacer le port parallèle et piloter jusqu’à 9 axes
en_title: PlanetCNC TNG and Mk3 controllers: replacing the parallel port and driving up to 9 axes
fr_desc: Le contrôleur PlanetCNC Mk3/9 (USB ou Ethernet, 9 axes pas/direction) et le logiciel TNG : licence obligatoire, limite de 25 mouvements sans licence, démarche de mise en service et pièges.
en_desc: The PlanetCNC Mk3/9 controller (USB or Ethernet, 9 step/direction axes) and TNG software: licence required, 25-move limit without one, commissioning steps and pitfalls.
---
=== fr
**PlanetCNC** fabrique des contrôleurs de mouvement qui relient un PC aux variateurs pas/direction par **USB ou Ethernet**, et le logiciel **TNG** qui les pilote. C’est une solution complète (matériel + logiciel) souvent choisie pour remplacer une vieille carte à port parallèle sur un routeur, une fraiseuse ou une table plasma.

## Fiche rapide (selon PlanetCNC)

| Élément | Contrôleur Mk3/9 |
|---|---|
| Liaison au PC | USB ou Ethernet |
| Axes | Jusqu’à 9, moteurs pas à pas ou servos (pas/direction) |
| Sorties | 8 sorties numériques, dont 3 PWM ; sorties servo RC |
| Entrées | 8 entrées de fins de course |
| Logiciel | PlanetCNC TNG, conçu uniquement pour les contrôleurs PlanetCNC |
| Licence | Obligatoire : sans licence, limité à 25 mouvements |

> [!NOTE] TNG ne fonctionne qu’avec des contrôleurs PlanetCNC, et le contrôleur demande une **licence** pour usiner de vraies pièces. Prévoyez-la dans le budget.

## Démarche de mise en service

1. **Installer TNG** et brancher le contrôleur en USB (ou Ethernet).
2. **Activer la licence** sur le contrôleur.
3. **Câbler** l’arrêt d’urgence, les fins de course et les variateurs ; vérifier le sens et le nombre de pas par unité de chaque axe.
4. **Configurer le référencement**, les limites logicielles et la broche (sortie PWM ou relais).
5. **Choisir un post PlanetCNC** (ou un post de type Fanuc vérifié) dans la FAO et faire un essai à vide.

## Liste de vérification

- [ ] Licence active (sinon 25 mouvements seulement)
- [ ] Arrêt d’urgence testé
- [ ] Pas par unité vérifiés sur une distance mesurée
- [ ] Référencement et limites logicielles actifs
- [ ] Post vérifié sur un programme court

## Erreurs fréquentes

- Croire que le contrôleur est défectueux alors qu’il s’arrête faute de licence.
- Brancher une charge directement sur une sortie numérique sans relais adapté.
- Mélanger des unités entre la FAO et TNG.

## FAQ

### Pourquoi remplacer un port parallèle ?
Les PC récents n’en ont plus et la synchronisation dépend du PC. Un contrôleur de mouvement externe génère les impulsions lui-même.

### PlanetCNC, Acorn ou Masso ?
PlanetCNC et [[centroid-acorn]] utilisent un PC ; [[masso]] est autonome. PlanetCNC se distingue par le nombre d’axes (jusqu’à 9) et la liaison USB ou Ethernet.

### Puis-je garder Mach3 ?
Non : TNG est le logiciel de ces contrôleurs. Voir [[mach]] pour l’écosystème Mach.

## À valider en atelier (Michaël)

- Expérience avec un contrôleur PlanetCNC et post FAO utilisé.
- Câblage de la broche (PWM ou VFD Modbus) recommandé.

## Sources

- [PlanetCNC — CNC controller Mk3 (9 axis)](https://shop.planet-cnc.com/product/cnc-controller-mk39/) : USB/Ethernet, 9 axes, 8 sorties, 8 entrées de fin de course, licence requise, limite de 25 mouvements. Consulté le 26 novembre 2026.
- [PlanetCNC TNG — Introduction](https://cnc.zone/tng/introduction) : remplacement du port parallèle, TNG uniquement pour contrôleurs PlanetCNC.
- [PlanetCNC — Licence du contrôleur](https://shop.planet-cnc.com/product/planetcnc-controller-license/).

=== en
**PlanetCNC** makes motion controllers that link a PC to step/direction drives over **USB or Ethernet**, and the **TNG** software that runs them. It is a complete solution (hardware + software) often chosen to replace an old parallel-port board on a router, mill or plasma table.

## Quick facts (per PlanetCNC)

| Item | Mk3/9 controller |
|---|---|
| PC link | USB or Ethernet |
| Axes | Up to 9, stepper or servo (step/direction) |
| Outputs | 8 digital outputs, 3 of them PWM; RC servo outputs |
| Inputs | 8 limit-switch inputs |
| Software | PlanetCNC TNG, built only for PlanetCNC controllers |
| Licence | Required: without one, limited to 25 moves |

> [!NOTE] TNG only works with PlanetCNC controllers, and the controller needs a **licence** to cut real parts. Budget for it.

## Commissioning steps

1. **Install TNG** and plug the controller in over USB (or Ethernet).
2. **Activate the licence** on the controller.
3. **Wire** the E-stop, limit switches and drives; check direction and steps per unit on each axis.
4. **Set up homing**, soft limits and the spindle (PWM output or relay).
5. **Pick a PlanetCNC post** (or a checked Fanuc-style post) in CAM and do a dry run.

## Checklist

- [ ] Licence active (otherwise only 25 moves)
- [ ] E-stop tested
- [ ] Steps per unit checked over a measured distance
- [ ] Homing and soft limits active
- [ ] Post checked on a short program

## Common mistakes

- Thinking the controller is faulty when it stops for lack of a licence.
- Driving a load straight from a digital output without a suitable relay.
- Mixing units between CAM and TNG.

## FAQ

### Why replace a parallel port?
Modern PCs no longer have one, and timing depends on the PC. An external motion controller generates the pulses itself.

### PlanetCNC, Acorn or Masso?
PlanetCNC and [[centroid-acorn]] use a PC; [[masso]] is standalone. PlanetCNC stands out for axis count (up to 9) and USB or Ethernet connection.

### Can I keep Mach3?
No: TNG is the software for these controllers. See [[mach]] for the Mach ecosystem.

## For Michaël to review

- Experience with a PlanetCNC controller and the CAM post used.
- Recommended spindle wiring (PWM or VFD Modbus).

## Sources

- [PlanetCNC — CNC controller Mk3 (9 axis)](https://shop.planet-cnc.com/product/cnc-controller-mk39/): USB/Ethernet, 9 axes, 8 outputs, 8 limit inputs, licence required, 25-move limit. Consulted November 26, 2026.
- [PlanetCNC TNG — Introduction](https://cnc.zone/tng/introduction): parallel-port replacement, TNG only for PlanetCNC controllers.
- [PlanetCNC — Controller licence](https://shop.planet-cnc.com/product/planetcnc-controller-license/).
