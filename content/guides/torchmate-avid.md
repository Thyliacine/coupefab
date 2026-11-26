---
id: torchmate-avid
hub: software
group: control
order: 67
mono: TA
nav: Torchmate et Avid CNC | Torchmate and Avid CNC
kicker: Logiciel · tables plasma | Software · plasma tables
level: debutant
schema: HowTo
tags: torchmate, accumove, vmd, visual machine designer, torchmate cnc 4, avid cnc, mach4, sheetcam, thc, anti-dive, m62, m63, plasma table
related: sheetcam, mach, thc-hunting, fusion-plasma-posts
fr_slug: torchmate-avid-cnc-plasma
en_slug: torchmate-avid-cnc-plasma
fr_title: Tables plasma Torchmate et Avid CNC : logiciels, posts et contrôle de hauteur
en_title: Torchmate and Avid CNC plasma tables: software, posts and height control
fr_desc: Torchmate (Accumove, VMD, Torchmate CNC 4) et Avid CNC (Mach4 + SheetCam) : quelle chaîne logicielle, quel post, comment activer ou bloquer le THC par opération et régler l’anti-plongée.
en_desc: Torchmate (Accumove, VMD, Torchmate CNC 4) and Avid CNC (Mach4 + SheetCam): which software chain, which post, how to allow or inhibit THC per operation and tune anti-dive.
---
=== fr
Torchmate (Lincoln Electric Cutting Systems) et Avid CNC sont deux marques de tables plasma très présentes dans les petits ateliers nord-américains. Leur point commun : une **chaîne en trois logiciels** — CAO (dessin/DXF), FAO (parcours et G-code) et commande (mouvement et contrôle de hauteur).

## Les chaînes logicielles

| Marque | CAO | FAO | Commande |
|---|---|---|---|
| Avid CNC | Tout logiciel qui exporte un DXF (Avid cite VCarve Pro) | **SheetCam** avec le post et les jeux d’outils Avid | **Mach4** (mouvement et THC) |
| Torchmate (selon génération) | Torchmate CAD ou tout DXF | Torchmate CAD, SheetCam ou Fusion selon le post | **Visual Machine Designer (VMD)** pour Accumove 2 et 3 ; **Torchmate CNC 4.x** pour les générateurs de signaux USB 501A |

> [!WARN] Torchmate avertit sur sa page de téléchargement qu’installer la mauvaise version du logiciel de commande peut **endommager le micrologiciel** du générateur de signaux. Vérifiez votre modèle et contactez le soutien technique avant toute mise à jour.

## Avid CNC : THC par opération dans SheetCam

Avid explique que SheetCam peut écrire, dans le G-code, la vitesse de coupe, la **tension d’arc cible** et des codes pour **autoriser ou bloquer le THC** :

| Besoin | Extrait de code (*code snippet*) de l’opération | Règles de trajet |
|---|---|---|
| THC voulu | `M62P4` (THC autorisé) | Règles par défaut, actives |
| THC non voulu | `M63P4` (THC bloqué) | Aucune |

Les **règles de trajet** (*path rules*) bloquent automatiquement le THC sur certaines géométries (petits trous, coins) où la tension d’arc monte quand la machine ralentit.

## Avid CNC : réglages THC dans Mach4

- **Profil matière** (FLAT, MODERATE, SEVERE) : règle la vitesse du THC et l’anti-plongée ; Avid recommande FLAT sauf tôle très gondolée.
- **Sensibilité haut / bas** : 100 = valeurs précalculées ; à modifier seulement si le profil ne suffit pas.
- **Journal THC** : enregistre la tension pendant la coupe ; on peut **marquer** le journal à un endroit problématique pour le diagnostic.

Avid rappelle que la tension d’arc est une mesure **indirecte** de la hauteur : elle grimpe aux entrées/sorties, dans les coins serrés, les petits trous et au-dessus des vides (pièces déjà coupées). Sans anti-plongée, le THC réagit en **descendant la torche**. Voir [[thc-hunting]].

## Torchmate : à retenir

- Identifier la génération de commande (Accumove 2, 3 ou plus récent ; générateur USB 501A) avant de choisir logiciel et post.
- VMD propose une bibliothèque de formes simples et la répétition de pièces sans CAO.
- Dans Fusion, la bibliothèque contient un post *Torchmate 3.0 Mill/Plasma* ; d’autres commandes demandent des codes M d’allumage particuliers : validez avec Torchmate (voir [[fusion-plasma-posts]]).

## Liste de vérification de mise en service

- [ ] Version exacte de la commande et du logiciel notée
- [ ] Post fourni par le fabricant installé dans la FAO
- [ ] Outils plasma créés à partir de la charte de la source plasma (voir [[cut-charts]])
- [ ] THC autorisé/bloqué selon l’opération ; anti-plongée active
- [ ] Coupe test, journal THC conservé si problème

## Erreurs fréquentes

| Erreur | Correctif |
|---|---|
| Post générique au lieu du post de la marque | Installer le post officiel |
| THC actif sur les petits trous | Règles de trajet ou M63P4 sur l’opération |
| Mise à jour de logiciel sans vérifier la compatibilité | Contacter le soutien Torchmate d’abord |
| Profil SEVERE par défaut | Revenir à FLAT, puis ajuster |

## FAQ

### Puis-je utiliser Fusion avec une Avid ?
Avid documente surtout SheetCam ; un post Fusion compatible Mach4 plasma peut fonctionner, mais les codes THC d’Avid doivent être reproduits. SheetCam reste la voie documentée.

### Ma tension d’arc affichée ne correspond pas à la charte : est-ce grave ?
L’affichage varie avec les consommables et la machine ; partez de la charte, puis ajustez la cible selon la qualité observée.

## À valider en atelier (Michaël)

- Vos réglages Mach4 (profil, sensibilités) sur une Avid réelle.
- Les générations Torchmate rencontrées chez vos clients.

## Sources

- [Avid CNC — Plasma introduction (CAD, SheetCam, Mach4)](https://www.avidcnc.com/support/instructions/software/plasma/), consulté le 26 novembre 2026.
- [Avid CNC — Mach4 Plasma Users Guide (THC, anti-plongée)](https://www.avidcnc.com/support/instructions/software/plasmaUsersGuide/), consulté le 26 novembre 2026.
- [Avid CNC — SheetCam Software Setup (M62P4/M63P4)](https://www.avidcnc.com/support/instructions/software/sheetcamSoftwareSetup/), consulté le 26 novembre 2026.
- [Torchmate — Driver Software Downloads (VMD, Torchmate CNC 4)](https://torchmate.com/training-header/driver-software/driver-software-downloads), consulté le 26 novembre 2026.
=== en
Torchmate (Lincoln Electric Cutting Systems) and Avid CNC are two plasma table brands common in small North American shops. What they share: a **three-program chain** — CAD (drawing/DXF), CAM (toolpaths and G-code) and control (motion and height control).

## The software chains

| Brand | CAD | CAM | Control |
|---|---|---|---|
| Avid CNC | Any software that exports DXF (Avid mentions VCarve Pro) | **SheetCam** with Avid’s post and toolsets | **Mach4** (motion and THC) |
| Torchmate (by generation) | Torchmate CAD or any DXF | Torchmate CAD, SheetCam or Fusion depending on the post | **Visual Machine Designer (VMD)** for Accumove 2 and 3; **Torchmate CNC 4.x** for USB 501A signal generators |

> [!WARN] Torchmate warns on its download page that installing the wrong control software version can **damage the signal generator’s firmware**. Check your model and contact tech support before any upgrade.

## Avid CNC: THC per operation in SheetCam

Avid explains that SheetCam can write cut speed, **target arc voltage** and codes to **allow or inhibit THC** into the G-code:

| Need | Operation code snippet | Path rules |
|---|---|---|
| THC wanted | `M62P4` (THC allowed) | Default rules, enabled |
| THC not wanted | `M63P4` (THC inhibited) | None |

**Path rules** automatically inhibit THC on some geometry (small holes, corners) where arc voltage rises as the machine slows.

## Avid CNC: THC settings in Mach4

- **Material profile** (FLAT, MODERATE, SEVERE): sets THC speed and anti-dive; Avid recommends FLAT unless the sheet is badly warped.
- **Up / down sensitivity**: 100 = precalculated values; change only if the profile isn’t enough.
- **THC log**: records voltage while cutting; you can **mark** the log at a problem spot for diagnosis.

Avid points out that arc voltage is an **indirect** height measurement: it climbs at lead-ins/outs, tight corners, small holes and over voids (already-cut parts). Without anti-dive, the THC responds by **driving the torch down**. See [[thc-hunting]].

## Torchmate: what to remember

- Identify the control generation (Accumove 2, 3 or newer; USB 501A signal generator) before choosing software and post.
- VMD offers a basic shape library and part arrays without CAD.
- In Fusion, the library includes a *Torchmate 3.0 Mill/Plasma* post; other controls need specific torch M-codes: validate with Torchmate (see [[fusion-plasma-posts]]).

## Commissioning checklist

- [ ] Exact control and software version written down
- [ ] Manufacturer’s post installed in CAM
- [ ] Plasma tools built from the plasma source’s chart (see [[cut-charts]])
- [ ] THC allowed/inhibited per operation; anti-dive on
- [ ] Test cut, THC log kept if there’s a problem

## Common mistakes

| Mistake | Fix |
|---|---|
| Generic post instead of the brand’s post | Install the official post |
| THC active on small holes | Path rules or M63P4 on the operation |
| Software upgrade without checking compatibility | Contact Torchmate support first |
| SEVERE profile by default | Go back to FLAT, then adjust |

## FAQ

### Can I use Fusion with an Avid?
Avid mainly documents SheetCam; a Fusion post compatible with Mach4 plasma can work, but Avid’s THC codes must be reproduced. SheetCam is the documented path.

### My displayed arc voltage doesn’t match the chart: is that bad?
The reading varies with consumables and machine; start from the chart, then adjust the target to the quality you see.

## For Michaël to review

- Your Mach4 settings (profile, sensitivities) on a real Avid.
- The Torchmate generations you meet at customers.

## Sources

- [Avid CNC — Plasma introduction (CAD, SheetCam, Mach4)](https://www.avidcnc.com/support/instructions/software/plasma/), consulted November 26, 2026.
- [Avid CNC — Mach4 Plasma Users Guide (THC, anti-dive)](https://www.avidcnc.com/support/instructions/software/plasmaUsersGuide/), consulted November 26, 2026.
- [Avid CNC — SheetCam Software Setup (M62P4/M63P4)](https://www.avidcnc.com/support/instructions/software/sheetcamSoftwareSetup/), consulted November 26, 2026.
- [Torchmate — Driver Software Downloads (VMD, Torchmate CNC 4)](https://torchmate.com/training-header/driver-software/driver-software-downloads), consulted November 26, 2026.
