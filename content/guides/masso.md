---
id: masso
hub: software
group: control
order: 58
mono: Ms
nav: Masso G3 | Masso G3
kicker: Commande autonome · Masso | Standalone control · Masso
level: debutant
schema: HowTo
tags: masso, g3, g3 touch, pc-less, sans pc, standalone, routeur, plasma, dthc, laser, lightburn, lathe, mill, lua, wifi, usb
related: centroid-acorn, planetcnc, cnc-router, plasma-cutting
fr_slug: masso-g3-commande-sans-pc
en_slug: masso-g3-pc-less-controller
fr_title: Masso G3 : la commande CNC sans PC pour routeur, plasma, laser et petits tours
en_title: Masso G3: the PC-less CNC controller for routers, plasma, laser and small lathes
fr_desc: Ce que fait la commande autonome Masso G3 et G3 Touch : écran tactile 15 po, chargement par clé USB, 24 V c.c., fraiseuse et routeur jusqu’à 5 axes, tour X/Z, plasma avec DTHC et laser ; démarche de mise en service.
en_desc: What the standalone Masso G3 and G3 Touch controllers do: 15-inch touchscreen, USB loading, 24 VDC, mill/router up to 5 axes, X/Z lathe, plasma with DTHC and laser; commissioning steps.
---
=== fr
La **Masso G3** est une commande CNC **autonome** : matériel et logiciel intégrés, sans PC à maintenir. La version **G3 Touch** ajoute un écran tactile industriel de 15 pouces. Elle vise les routeurs, tables plasma, lasers, fraiseuses et petits tours d’atelier, souvent en rétrofit.

## Fiche rapide (selon Masso)

| Élément | Masso G3 / G3 Touch |
|---|---|
| Ordinateur | Aucun : commande autonome |
| Écran | G3 Touch : 15 po tactile capacitif ; G3 : écran externe |
| Chargement des programmes | Clé USB (Wi-Fi en option avec le module) |
| Alimentation | 24 V c.c. unique, sans ventilateur |
| Axes | Fraiseuse/routeur : 5 axes ; tour : X et Z |
| Signaux moteurs | Pas et direction |
| Procédés | Fraisage, routeur, tour, plasma (DTHC), laser |
| Personnalisation | Scripts Lua |

Le logiciel existe en niveaux **Core, Advanced et Professional** ; vérifiez dans la fiche de spécifications quelles fonctions sont incluses dans chaque niveau.

## Démarche de mise en service

1. **Choisir le guide de démarrage** du procédé (Mill, Lathe, Plasma, Laser) dans la documentation Masso.
2. **Câbler** l’arrêt d’urgence, les capteurs de référencement et les variateurs pas/direction.
3. **Calibrer** chaque axe avec l’assistant, régler le jeu et les limites logicielles.
4. **Configurer le palpage** (plaque, palpeur ou mesureur d’outil) et les origines pièce.
5. **Choisir un post Masso** dans la FAO, charger par clé USB et faire un essai à vide.

> [!NOTE] Pour le plasma, la Masso intègre un contrôle de hauteur numérique (DTHC) avec son module I/O plasma. Suivez le guide Plasma de Masso pour la division de tension et le câblage de la torche.

## Liste de vérification

- [ ] Niveau logiciel adapté (fonctions voulues incluses)
- [ ] Arrêt d’urgence et porte (si présente) testés
- [ ] Axes calibrés sur une distance mesurée
- [ ] Post Masso sélectionné ; codes M de torche ou de laser vérifiés
- [ ] Sauvegarde des réglages faite (fonction Save & Load Settings)

## Erreurs fréquentes

- Supposer qu’un post générique convient : les codes de torche, de laser et d’outil doivent correspondre à la Masso.
- Ne pas sauvegarder les réglages avant une mise à jour logicielle.
- Câbler une sortie TTL (5 V, faible courant) directement sur une charge : utilisez le module relais.

## FAQ

### Pourquoi une commande sans PC ?
Moins de pannes liées au PC (mises à jour, pilotes, virus) et une mise en service plus simple. En contrepartie, l’écosystème est propre à Masso.

### Masso ou Acorn ?
Masso est autonome ; [[centroid-acorn]] utilise un PC avec CNC12. Pour une carte PC très flexible, voir aussi [[planetcnc]].

### Masso convient-elle à une table plasma ?
Oui, avec le DTHC et le module plasma ; voir [[plasma-cutting]] pour les réglages de coupe.

## À valider en atelier (Michaël)

- Retour d’expérience sur une Masso en plasma ou routeur.
- Niveau logiciel conseillé par procédé.

## Sources

- [MASSO — G3 et G3 Touch](https://www.masso.com.au/masso-controllers/) : écran 15 po, clé USB, 24 V c.c., sans ventilateur, autonome. Consulté le 26 novembre 2026.
- [MASSO Documentation — G3 Series](https://docs.masso.com.au/MASSO_FAQ/masso_g3_series) : 5 axes fraiseuse, X/Z tour, niveaux Core/Advanced/Professional, DTHC plasma, laser, Lua.

=== en
The **Masso G3** is a **standalone** CNC controller: integrated hardware and software, no PC to maintain. The **G3 Touch** version adds a 15-inch industrial touchscreen. It targets shop routers, plasma tables, lasers, mills and small lathes, often as a retrofit.

## Quick facts (per Masso)

| Item | Masso G3 / G3 Touch |
|---|---|
| Computer | None: standalone controller |
| Screen | G3 Touch: 15-inch capacitive touch; G3: external screen |
| Loading programs | USB flash drive (Wi-Fi optional with the module) |
| Power | Single 24 VDC, fanless |
| Axes | Mill/router: 5 axes; lathe: X and Z |
| Motor signals | Step and direction |
| Processes | Milling, router, lathe, plasma (DTHC), laser |
| Customization | Lua scripts |

The software comes in **Core, Advanced and Professional** levels; check the specification sheet for which features each level includes.

## Commissioning steps

1. **Pick the quick-start guide** for the process (Mill, Lathe, Plasma, Laser) in the Masso documentation.
2. **Wire** the E-stop, homing sensors and step/direction drives.
3. **Calibrate** each axis with the wizard, set backlash and soft limits.
4. **Set up probing** (touch plate, probe or tool setter) and work offsets.
5. **Pick a Masso post** in CAM, load from USB and do a dry run.

> [!NOTE] For plasma, Masso has digital torch height control (DTHC) with its plasma I/O module. Follow Masso’s Plasma guide for the voltage divider and torch wiring.

## Checklist

- [ ] Software level fits (needed features included)
- [ ] E-stop and door (if present) tested
- [ ] Axes calibrated over a measured distance
- [ ] Masso post selected; torch or laser M-codes checked
- [ ] Settings backed up (Save & Load Settings)

## Common mistakes

- Assuming a generic post works: torch, laser and tool codes must match Masso.
- Not backing up settings before a software update.
- Wiring a TTL output (5 V, low current) straight to a load: use the relay module.

## FAQ

### Why a PC-less controller?
Fewer PC-related failures (updates, drivers, viruses) and simpler commissioning. The trade-off is a Masso-specific ecosystem.

### Masso or Acorn?
Masso is standalone; [[centroid-acorn]] uses a PC with CNC12. For a very flexible PC-based board, see also [[planetcnc]].

### Does Masso suit a plasma table?
Yes, with the DTHC and plasma module; see [[plasma-cutting]] for cut settings.

## For Michaël to review

- Hands-on feedback on a Masso for plasma or router.
- Recommended software level per process.

## Sources

- [MASSO — G3 and G3 Touch](https://www.masso.com.au/masso-controllers/): 15-inch screen, USB drive, 24 VDC, fanless, standalone. Consulted November 26, 2026.
- [MASSO Documentation — G3 Series](https://docs.masso.com.au/MASSO_FAQ/masso_g3_series): mill 5 axes, lathe X/Z, Core/Advanced/Professional levels, plasma DTHC, laser, Lua.
