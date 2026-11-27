---
id: mach
hub: software
group: control
order: 10
mono: M4
nav: Mach3 / Mach4 | Mach3 / Mach4
kicker: Logiciel · commande | Software · control
level: intermediaire
schema: Article
tags: mach3, mach4, machpro, machlabs, newfangled, control software, motion controller, ess, plasma, thc, screen set
related: linuxcnc, post-processors, gcode, ugs-grbl
fr_slug: mach3-mach4
en_slug: mach3-mach4
fr_title: Mach3, Mach4 et MachPro : où en est le logiciel de commande CNC sur PC
en_title: Mach3, Mach4 and MachPro: where the PC CNC control software stands
fr_desc: Statut actuel de Mach3 (plus mis à jour), Mach4 Hobby et Industrial (maintenance) et MachPro, rôle du contrôleur de mouvement, et ce qu’il faut vérifier avant de moderniser une vieille machine sous Mach3.
en_desc: Current status of Mach3 (no longer updated), Mach4 Hobby and Industrial (maintenance) and MachPro, the role of the motion controller, and what to check before upgrading an old Mach3 machine.
codes: mach
---
=== fr
La famille **Mach** pilote depuis longtemps des tables plasma, routeurs et fraiseuses converties à partir d’un PC Windows. Beaucoup de machines usagées tournent encore sous Mach3 : savoir où en est le produit aide à décider entre garder, migrer ou changer de commande.

## Statut des versions (au 26 novembre 2026)

| Produit | Statut |
|---|---|
| **Mach3** | N’est plus mis à jour |
| **Mach4 Hobby / Industrial** | Produits historiques en mode maintenance |
| **MachPro** | Nouveau produit de l’éditeur, désormais **MachLabs** |

Consultez mach-labs.com pour les licences et la compatibilité actuelles.

## Comment ça marche

Mach interprète le G-code et envoie les mouvements à un **contrôleur de mouvement** externe (Ethernet SmoothStepper, cartes de fabricants, etc.) qui génère les impulsions des moteurs. Le port parallèle d’origine de Mach3 a pratiquement disparu des PC récents.

> [!WARN] Le **plugin** du contrôleur de mouvement doit être compatible avec la version exacte de Mach. Vérifiez la liste du fabricant du contrôleur avant toute mise à niveau.

## Garder, migrer ou remplacer

| Situation | Piste |
|---|---|
| Machine Mach3 qui fonctionne, PC stable | Garder ; sauvegarder le profil (XML), les macros et la licence |
| Besoin de nouvelles fonctions, matériel récent | Évaluer MachPro avec votre contrôleur |
| Plasma avec contrôle de hauteur | Vérifier la compatibilité THC (plugin, écran) avant de changer |
| Envie de logiciel libre | [LinuxCNC](/guides/linuxcnc-qtplasmac/) |
| Petit routeur ou laser | Une carte grbl/grblHAL avec [UGS](/guides/ugs-grbl/) |

## Avant de toucher à une machine sous Mach3

- [ ] Copier tout le dossier Mach3 (profils, macros, écrans, licence)
- [ ] Noter le contrôleur de mouvement, son plugin et ses réglages
- [ ] Noter les réglages moteurs (pas par unité, vitesse, accélération) et les entrées/sorties
- [ ] Garder le post FAO utilisé (SheetCam, Fusion…) — voir [Post-processeurs](/guides/post-processeurs/)

## FAQ

### Puis-je installer Mach3 sur Windows 11 ?
Mach3 date d’une époque Windows bien antérieure et n’est plus mis à jour ; la compatibilité dépend surtout du contrôleur de mouvement et de son plugin. Testez avant de remplacer un PC qui fonctionne.

## À valider en atelier (Michaël)

- Retour sur une migration Mach3 réelle.

## Sources

- [MachLabs (Mach3, Mach4, MachPro)](https://www.mach-labs.com/), consulté le 26 novembre 2026.
- [Warp9 TD — Ethernet SmoothStepper](https://warp9td.com/).
=== en
The **Mach** family has long driven plasma tables, routers and converted mills from a Windows PC. Many used machines still run Mach3: knowing where the product stands helps decide whether to keep, migrate or change controls.

## Version status (as of November 26, 2026)

| Product | Status |
|---|---|
| **Mach3** | No longer updated |
| **Mach4 Hobby / Industrial** | Legacy products in maintenance mode |
| **MachPro** | The publisher’s new product, now **MachLabs** |

See mach-labs.com for current licences and compatibility.

## How it works

Mach interprets G-code and sends moves to an external **motion controller** (Ethernet SmoothStepper, maker boards, etc.) that generates motor pulses. Mach3’s original parallel port has practically vanished from modern PCs.

> [!WARN] The motion controller’s **plugin** must be compatible with the exact Mach version. Check the controller maker’s list before any upgrade.

## Keep, migrate or replace

| Situation | Option |
|---|---|
| Working Mach3 machine, stable PC | Keep; back up the profile (XML), macros and licence |
| Need new features, recent hardware | Evaluate MachPro with your controller |
| Plasma with height control | Check THC compatibility (plugin, screen) before changing |
| Want open source | [LinuxCNC](/en/guides/linuxcnc-qtplasmac/) |
| Small router or laser | A grbl/grblHAL board with [UGS](/en/guides/ugs-grbl/) |

## Before touching a Mach3 machine

- [ ] Copy the whole Mach3 folder (profiles, macros, screens, licence)
- [ ] Note the motion controller, its plugin and settings
- [ ] Note motor settings (steps per unit, velocity, acceleration) and inputs/outputs
- [ ] Keep the CAM post used (SheetCam, Fusion…) — see [Post processors](/en/guides/post-processors/)

## FAQ

### Can I install Mach3 on Windows 11?
Mach3 dates from a much older Windows era and is no longer updated; compatibility depends mostly on the motion controller and its plugin. Test before replacing a PC that works.

## For Michaël to review

- Feedback from a real Mach3 migration.

## Sources

- [MachLabs (Mach3, Mach4, MachPro)](https://www.mach-labs.com/), consulted November 26, 2026.
- [Warp9 TD — Ethernet SmoothStepper](https://warp9td.com/).
