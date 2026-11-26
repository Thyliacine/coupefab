---
id: centroid-acorn
hub: software
group: control
order: 56
mono: Ac
nav: Centroid Acorn | Centroid Acorn
kicker: Commande PC · Centroid | PC control · Centroid
level: debutant
schema: HowTo
tags: centroid, acorn, acornsix, cnc12, intercon, free, pro, ultimate, licence, license, ethernet, step dir, retrofit, routeur, mill, lathe, plasma
related: masso, planetcnc, linuxcnc, mach
fr_slug: centroid-acorn-cnc12
en_slug: centroid-acorn-cnc12
fr_title: Centroid Acorn et CNC12 : choisir la licence, câbler et démarrer sans se tromper
en_title: Centroid Acorn and CNC12: picking the licence, wiring and starting up right
fr_desc: La carte Acorn de Centroid avec le logiciel CNC12 : niveaux Free, Pro et Ultimate, licence liée au numéro de série, Intercon, démarche de mise en service et pièges d’une rétrofit.
en_desc: Centroid’s Acorn board with CNC12 software: Free, Pro and Ultimate levels, licence tied to the board serial number, Intercon, commissioning steps and retrofit pitfalls.
---
=== fr
La **Centroid Acorn** est une carte de commande à signaux pas/direction reliée par **Ethernet** à un PC qui fait tourner le logiciel **CNC12**. Centroid la propose en ensemble pour fraiseuses, routeurs, tours, plasma et laser. C’est une option courante pour rétrofiter une vieille machine ou motoriser une machine maison avec une interface de type industriel.

## Niveaux de logiciel CNC12

| Fonction | Free | Pro | Ultimate |
|---|---|---|---|
| 3 axes simultanés | Oui | Oui | Oui |
| 4 axes simultanés | Non | Oui | Oui |
| Conversationnel Intercon | Limité à 20 blocs | Illimité | Illimité |
| Compensation de jeu et de vis | Oui | Oui | Oui |

Le niveau Ultimate ajoute d’autres fonctions avancées (voir le tableau officiel). Sans licence, **CNC12 fonctionne au niveau Free**.

> [!WARN] Les licences Pro et Ultimate sont **liées au numéro de série de la carte Acorn**. Une licence ne se transfère pas d’une carte à l’autre : achetez-la pour la carte qui restera sur la machine.

## Démarche de mise en service

1. **Lire la documentation Acorn** (schémas de câblage par type de variateur).
2. **Câbler** l’arrêt d’urgence et les fins de course en premier, puis les variateurs pas/direction.
3. **Installer CNC12** sur le PC, relier la carte par Ethernet et lancer l’assistant de configuration (*Wizard*).
4. **Calibrer** les pas par unité de chaque axe, puis vérifier un déplacement connu avec un comparateur ou une règle.
5. **Régler le référencement** (*homing*) et les limites logicielles.
6. **Choisir le post** CNC12 (Centroid) dans la FAO et faire un essai à vide.

## Liste de vérification

- [ ] Arrêt d’urgence câblé et testé avant toute mise sous tension des moteurs
- [ ] Niveau de licence suffisant pour le nombre d’axes simultanés voulu
- [ ] Pas par unité vérifiés sur une distance mesurée
- [ ] Référencement et limites logicielles actifs
- [ ] Post Centroid sélectionné dans la FAO

## Erreurs fréquentes

- Acheter une licence avant d’avoir choisi la carte définitive (licence non transférable).
- Câbler les moteurs avant l’arrêt d’urgence.
- Croire que le niveau Free pilote un 4e axe en simultané : il faut Pro ou Ultimate.
- Utiliser un post générique « Fanuc » sans vérifier les codes d’outil et de broche attendus par CNC12.

## FAQ

### Acorn ou AcornSix ?
L’AcornSix est la carte à six axes de Centroid ; l’Acorn convient à la plupart des routeurs et fraiseuses à trois ou quatre axes. Comparez sur la page de comparaison des cartes de Centroid.

### Puis-je essayer avant d’acheter une licence ?
Oui : CNC12 tourne au niveau Free sans licence, ce qui suffit pour tester un 3 axes.

### Acorn ou Masso ?
L’Acorn demande un PC ; le Masso est autonome (sans PC). Voir [[masso]] et [[planetcnc]].

## À valider en atelier (Michaël)

- Expérience réelle de rétrofit Acorn (variateurs, temps de mise en service).
- Niveau de licence recommandé selon le type de machine.

## Sources

- [Centroid — Acorn CNC Controller (boutique)](https://shopcentroidcnc.com/acorn-cnc-controller/), consulté le 26 novembre 2026.
- [Centroid — CNC12 Software Options](https://www.centroidcnc.com/centroid_diy/software_options.html) : tableau Free, Pro, Ultimate.
- [Centroid — Acorn FAQ](https://centroidcnc.com/centroid_diy/acorn_faq.html) : licence liée au numéro de série, fonctionnement Free sans licence.
- [Centroid — Documentation Acorn (PDF)](https://www.centroidcnc.com/centroid_diy/downloads/acorn_documentation/centroid_acorn_cnc_controller.pdf).

=== en
The **Centroid Acorn** is a step/direction control board connected over **Ethernet** to a PC running **CNC12** software. Centroid sells it as kits for mills, routers, lathes, plasma and laser. It is a common way to retrofit an old machine or motorize a home-built one with an industrial-style interface.

## CNC12 software levels

| Feature | Free | Pro | Ultimate |
|---|---|---|---|
| 3-axis simultaneous | Yes | Yes | Yes |
| 4-axis simultaneous | No | Yes | Yes |
| Intercon conversational | Limited to 20 blocks | Unlimited | Unlimited |
| Backlash and screw compensation | Yes | Yes | Yes |

Ultimate adds further advanced features (see the official table). Without a licence, **CNC12 runs at the Free level**.

> [!WARN] Pro and Ultimate licences are **tied to the Acorn board’s serial number**. A licence does not move from one board to another: buy it for the board that will stay on the machine.

## Commissioning steps

1. **Read the Acorn documentation** (wiring diagrams by drive type).
2. **Wire** the E-stop and limit switches first, then the step/direction drives.
3. **Install CNC12** on the PC, connect the board over Ethernet and run the setup *Wizard*.
4. **Calibrate** steps per unit on each axis, then check a known move with an indicator or rule.
5. **Set up homing** and soft limits.
6. **Pick the CNC12 (Centroid) post** in CAM and do a dry run.

## Checklist

- [ ] E-stop wired and tested before powering the motors
- [ ] Licence level matches the number of simultaneous axes needed
- [ ] Steps per unit checked over a measured distance
- [ ] Homing and soft limits active
- [ ] Centroid post selected in CAM

## Common mistakes

- Buying a licence before settling on the final board (non-transferable).
- Wiring motors before the E-stop.
- Expecting the Free level to run a simultaneous 4th axis: that needs Pro or Ultimate.
- Using a generic “Fanuc” post without checking the tool and spindle codes CNC12 expects.

## FAQ

### Acorn or AcornSix?
AcornSix is Centroid’s six-axis board; Acorn suits most three- and four-axis routers and mills. Compare on Centroid’s board comparison page.

### Can I try before buying a licence?
Yes: CNC12 runs at the Free level without a licence, enough to test a 3-axis machine.

### Acorn or Masso?
Acorn needs a PC; Masso is standalone (PC-less). See [[masso]] and [[planetcnc]].

## For Michaël to review

- Real Acorn retrofit experience (drives, commissioning time).
- Recommended licence level by machine type.

## Sources

- [Centroid — Acorn CNC Controller (store)](https://shopcentroidcnc.com/acorn-cnc-controller/), consulted November 26, 2026.
- [Centroid — CNC12 Software Options](https://www.centroidcnc.com/centroid_diy/software_options.html): Free, Pro, Ultimate table.
- [Centroid — Acorn FAQ](https://centroidcnc.com/centroid_diy/acorn_faq.html): licence tied to serial number, Free operation without a licence.
- [Centroid — Acorn documentation (PDF)](https://www.centroidcnc.com/centroid_diy/downloads/acorn_documentation/centroid_acorn_cnc_controller.pdf).
