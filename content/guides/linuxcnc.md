---
id: linuxcnc
hub: software
group: control
order: 20
mono: LX
nav: LinuxCNC / QtPlasmaC | LinuxCNC / QtPlasmaC
kicker: Logiciel libre · commande | Open source · control
level: avance
schema: HowTo
tags: linuxcnc, qtplasmac, plasma, thc, vad, anti-dive, mesa, open source, control, hal
related: plasma-cutting, lead-ins-pierce, mach, plasma-troubleshooting
fr_slug: linuxcnc-qtplasmac
en_slug: linuxcnc-qtplasmac
fr_title: LinuxCNC et QtPlasmaC : commande libre pour table plasma, avec contrôle de hauteur
en_title: LinuxCNC and QtPlasmaC: open-source control for plasma tables, with height control
fr_desc: Ce qu’est LinuxCNC, le matériel habituel (cartes Mesa), l’interface QtPlasmaC pour le plasma, son contrôle de hauteur (THC), le seuil anti-plongée VAD et la démarche de mise en service.
en_desc: What LinuxCNC is, typical hardware (Mesa cards), the QtPlasmaC interface for plasma, its torch height control (THC), the VAD anti-dive threshold and the commissioning steps.
---
=== fr
**LinuxCNC** est un logiciel de commande CNC **libre** qui génère les mouvements en temps réel. Il pilote fraiseuses, tours, routeurs et tables plasma. **QtPlasmaC** est son interface dédiée au plasma, intégrée à la distribution.

## Matériel typique

| Élément | Exemples |
|---|---|
| PC | PC dédié avec noyau temps réel (image LinuxCNC officielle) |
| Interface | Cartes **Mesa** (Ethernet ou PCI) — recommandées pour le plasma |
| Mesure de tension d’arc | Carte isolée (par exemple Mesa THCAD) ou mode de contrôle sans mesure selon le matériel |
| Source plasma | Avec sortie de tension d’arc divisée |

## QtPlasmaC en bref

- Interface tactile ou clavier, réglages de coupe par **matériau** (fichier de matériaux : hauteurs de perçage et de coupe, délai, vitesse, ampérage, tension).
- **Contrôle de hauteur (THC)** : activation après un délai fixe ou **automatique** quand la tension se stabilise.
- **Anti-plongée** : seuil **VAD** (velocity anti-dive) — le THC est gelé quand la vitesse réelle tombe sous un pourcentage de la vitesse programmée (coins, petits trous).
- Gestion des trous et arcs, coupe à partir d’une ligne, reprise après perte d’arc, sondage de hauteur initial (ohmique ou flottant).

> [!TIP] Le gel du THC dans les coins et les petits trous évite que la torche plonge quand la tension d’arc monte au ralentissement. Voir [Entrées, sorties et perçage](/guides/entrees-sorties-percage-plasma/).

## Mise en service

1. Installer l’image LinuxCNC officielle ; tester la **latence** du PC.
2. Configurer la carte Mesa avec l’assistant de configuration (PnCconf ou l’outil de votre carte).
3. Lancer l’assistant **QtPlasmaC** de configuration : axes, entrées, mode de mesure d’arc.
4. Régler moteurs, fins de course et prise d’origine ; vérifier les dimensions sur une pièce test.
5. Créer le **fichier de matériaux** à partir des tableaux de coupe de votre source.
6. Choisir un **post** FAO compatible QtPlasmaC (SheetCam en propose un ; Fusion aussi selon la version).
7. Coupes d’essai, puis ajustement du THC.

## Erreurs fréquentes

| Erreur | Correctif |
|---|---|
| PC à latence élevée | Changer de PC ou utiliser une carte Ethernet Mesa |
| Tension d’arc bruitée | Câblage blindé, masse correcte, carte isolée |
| THC actif dans les coins | Régler le seuil VAD |
| Post non compatible | Utiliser le post QtPlasmaC de la FAO |

## FAQ

### LinuxCNC est-il plus difficile que Mach ?
La configuration initiale demande plus de lecture, mais la documentation QtPlasmaC est détaillée et le logiciel est gratuit et maintenu.

## À valider en atelier (Michaël)

- Votre fichier de matériaux de départ si vous utilisez QtPlasmaC.

## Sources

- [LinuxCNC — QtPlasmaC (documentation stable)](https://linuxcnc.org/docs/stable/html/plasma/qtplasmac.html), consulté le 26 novembre 2026.
- [LinuxCNC — Site officiel](https://linuxcnc.org/).
- [Mesa Electronics](https://store.mesanet.com/).
=== en
**LinuxCNC** is **open-source** CNC control software that generates motion in real time. It drives mills, lathes, routers and plasma tables. **QtPlasmaC** is its plasma interface, included in the distribution.

## Typical hardware

| Item | Examples |
|---|---|
| PC | Dedicated PC with real-time kernel (official LinuxCNC image) |
| Interface | **Mesa** cards (Ethernet or PCI) — recommended for plasma |
| Arc voltage sensing | Isolated card (for example Mesa THCAD) or a no-sensing mode depending on hardware |
| Plasma source | With divided arc voltage output |

## QtPlasmaC in brief

- Touch or keyboard interface, cut settings per **material** (materials file: pierce and cut heights, delay, speed, amperage, voltage).
- **Torch height control (THC)**: enabled after a fixed delay or **automatically** when voltage settles.
- **Anti-dive**: **VAD** threshold (velocity anti-dive) — THC is frozen when actual speed drops below a percentage of programmed speed (corners, small holes).
- Hole and arc handling, cut from line, recovery after arc loss, initial height probing (ohmic or float).

> [!TIP] Freezing THC in corners and small holes stops the torch from diving when arc voltage rises during slowdown. See [Lead-ins and pierce height](/en/guides/lead-ins-pierce-height/).

## Commissioning

1. Install the official LinuxCNC image; test PC **latency**.
2. Configure the Mesa card with the configuration wizard (PnCconf or your card’s tool).
3. Run the **QtPlasmaC** configuration wizard: axes, inputs, arc sensing mode.
4. Set motors, limits and homing; check dimensions on a test part.
5. Build the **materials file** from your source’s cut charts.
6. Pick a QtPlasmaC-compatible CAM **post** (SheetCam offers one; Fusion too depending on version).
7. Test cuts, then tune THC.

## Common mistakes

| Mistake | Fix |
|---|---|
| High-latency PC | Change PC or use a Mesa Ethernet card |
| Noisy arc voltage | Shielded wiring, proper ground, isolated card |
| THC active in corners | Set the VAD threshold |
| Incompatible post | Use the CAM’s QtPlasmaC post |

## FAQ

### Is LinuxCNC harder than Mach?
Initial setup takes more reading, but QtPlasmaC documentation is detailed and the software is free and maintained.

## For Michaël to review

- Your starter materials file if you use QtPlasmaC.

## Sources

- [LinuxCNC — QtPlasmaC (stable documentation)](https://linuxcnc.org/docs/stable/html/plasma/qtplasmac.html), consulted November 26, 2026.
- [LinuxCNC — Official site](https://linuxcnc.org/).
- [Mesa Electronics](https://store.mesanet.com/).
