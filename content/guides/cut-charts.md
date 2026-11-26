---
id: cut-charts
hub: fundamentals
order: 22
nav: Lire une charte de coupe | Reading cut charts
kicker: Fondamentaux · plasma et laser | Fundamentals · plasma and laser
level: debutant
schema: HowTo
tags: cut chart, plasma, arc voltage, pierce height, pierce delay, cut height, kerf, best quality, production, thc, powermax, laser recipe
related: plasma-cutting, lead-ins-pierce, kerf, thc-hunting
fr_slug: lire-charte-de-coupe
en_slug: reading-cut-charts
fr_title: Lire une charte de coupe plasma (et une recette laser) sans se tromper
en_title: How to read a plasma cut chart (and a laser recipe) correctly
fr_desc: Hauteur de coupe, hauteur de perçage, délai, vitesse « meilleure qualité » vs « production », tension d’arc, kerf, débits de gaz : chaque colonne d’une charte Hypertherm expliquée, et comment l’entrer dans SheetCam, Fusion ou la commande.
en_desc: Cut height, pierce height, pierce delay, “best quality” vs “production” speed, arc voltage, kerf, gas flow: every column of a Hypertherm cut chart explained, and how to enter it in SheetCam, Fusion or the control.
---
=== fr
Une charte de coupe (*cut chart*) est le point de départ officiel du fabricant pour une combinaison précise : **procédé, matière, épaisseur, courant (ampérage), gaz et consommables**. Ce n’est pas une promesse : Hypertherm précise que ses chartes sont un bon point de départ, mesurées avec des consommables neufs et une installation conforme, à ajuster selon votre table et votre environnement.

## Étape 1 : choisir la bonne page

1. **Procédé et consommables** : coupe standard, FineCut, gougeage ou marquage — chaque jeu de consommables a ses chartes.
2. **Matière** : acier doux, inox, aluminium.
3. **Courant** (A) : il s’applique à toute la page (sauf FineCut, où il est donné par épaisseur).
4. **Gaz** : air, azote, F5, etc.
5. **Unités** : chaque charte existe en métrique et en impérial ; ne mélangez pas.

## Étape 2 : lire chaque colonne

| Colonne | Ce que c’est | Où l’entrer |
|---|---|---|
| Épaisseur (*Material thickness*) | Épaisseur de la pièce | Choix de la ligne |
| Hauteur de coupe (*Cut height / torch-to-work distance*) | Distance buse (ou écran) ↔ tôle pendant la coupe | Outil plasma de la FAO ou commande |
| Hauteur de perçage initiale (*Initial pierce height*) | Distance au moment de l’amorçage, avant de descendre ; parfois donnée en % de la hauteur de coupe | Outil plasma / commande |
| Délai de perçage (*Pierce delay*) | Temps immobile à la hauteur de perçage pour traverser | Outil plasma / commande |
| Vitesse « meilleure qualité » (*Best quality*) | Point de départ pour le meilleur angle, le moins de scories, le meilleur fini | Avance de coupe |
| Vitesse « production » (*Production*) | Plus rapide (de l’ordre de 70 à 80 % de la vitesse maximale, selon Hypertherm) : plus de pièces, pas forcément la meilleure qualité | Avance de coupe |
| Tension d’arc (*Arc voltage*) | Consigne du contrôle de hauteur (THC) ; plus la torche est haute, plus la tension monte | THC |
| Largeur de saignée (*Kerf width*) | Largeur de matière enlevée, pour la compensation | Kerf de l’outil (voir [[kerf]]) |
| Débit de gaz chaud / froid | Débit pendant la coupe / débit au repos (test de gaz) | Vérification de l’installation |
| *Edge start* | Épaisseur trop forte pour percer : démarrer au bord | Entrées en bordure |

> [!TIP] Hypertherm rappelle que la tension d’arc **augmente avec l’usure des consommables** : pour garder la bonne hauteur, la consigne peut devoir être relevée. Si la qualité baisse en fin de vie d’une électrode, c’est normal ; changez les consommables avant de « corriger » la charte.

## Étape 3 : transposer dans votre logiciel

- **SheetCam** : un outil plasma par combinaison (matière/épaisseur/A) avec kerf, avance, hauteurs, délai, tension. Voir [[sheetcam]].
- **Fusion** : la bibliothèque d’outils de coupe stocke kerf et avance ; les hauteurs et le THC sont souvent des propriétés du post. Voir [[fusion-plasma-posts]].
- **FireControl, LinuxCNC/QtPlasmaC, Phoenix** : tables de matériaux dans la commande. Voir [[firecontrol]], [[linuxcnc]] et [[hypertherm-edge-phoenix]].

## Étape 4 : valider sur une chute

- [ ] Consommables neufs ou en bon état, du bon type
- [ ] Pression/débit conformes à la charte, air propre et sec
- [ ] Coupe d’essai : un carré et un trou, à la vitesse « meilleure qualité »
- [ ] Mesurer la pièce (kerf réel) et observer scories et biseau
- [ ] Ajuster **un** paramètre à la fois et noter le résultat

## Et pour un laser fibre ?

Les « recettes » laser sont propres à chaque machine et source (puissance, focale, buse, gaz, pression, fréquence). La logique est la même : point de départ du fabricant, essai, correction d’un paramètre à la fois. Voir [[laser-troubleshooting]].

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Prendre la charte d’un autre courant ou d’autres consommables | Kerf, vitesse et tension faux dès le départ |
| Percer trop bas | Consommables abîmés ; Hypertherm cite le perçage trop bas comme première cause d’usure prématurée |
| Couper à la vitesse « production » quand on veut un bord propre | Plus de biseau ou de scories |
| Laisser la tension d’arc fixe quand les consommables s’usent | La torche descend ou monte, la qualité dérive |

## FAQ

### Pourquoi la tension d’arc change-t-elle la hauteur ?
Le THC maintient une tension constante ; comme la tension augmente avec la distance, une consigne plus haute fait monter la torche. Voir [[thc-hunting]].

### Ma table ne tient pas la vitesse de la charte dans les petits détails : que faire ?
C’est fréquent : la machine ralentit dans les coins et les trous. Utilisez la gestion des coins (anti-plongée / *corner hold*) de la commande et les stratégies de petits trous ; voir [[lead-ins-pierce]].

## À valider en atelier (Michaël)

- Votre façon d’organiser les outils plasma dans SheetCam (nomenclature, une ligne par épaisseur).
- Les écarts que vous constatez entre charte et réglage final sur votre table.

## Sources

- [Hypertherm — Powermax45/65/85/105 SYNC Cut Charts Guide (810500MU)](https://xnet.hypertherm.com/Xnet/library/download/?file=HYP254756), consulté le 26 novembre 2026.
- [Hypertherm — Torch height control for plasma cutting](https://www.hypertherm.com/resources/more-resources/articles/torch-height-control-for-plasma-cutting/), consulté le 26 novembre 2026.
- [Hypertherm — Basic tips to improve plasma cut quality](https://www.hypertherm.com/resources/more-resources/articles/basic-tips-to-improve-plasma-cut-quality/), consulté le 26 novembre 2026.
=== en
A cut chart is the manufacturer’s official starting point for one exact combination: **process, material, thickness, current (amperage), gas and consumables**. It is not a promise: Hypertherm states its charts are a good starting point, collected with new consumables and a compliant installation, to be adjusted for your table and environment.

## Step 1: pick the right page

1. **Process and consumables**: standard cutting, FineCut, gouging or marking — each consumable set has its own charts.
2. **Material**: mild steel, stainless, aluminum.
3. **Current** (A): applies to the whole page (except FineCut, where it is listed per thickness).
4. **Gas**: air, nitrogen, F5, etc.
5. **Units**: every chart exists in metric and imperial; don’t mix them.

## Step 2: read each column

| Column | What it is | Where it goes |
|---|---|---|
| Material thickness | Workpiece thickness | Picks the row |
| Cut height / torch-to-work distance | Nozzle (or shield) ↔ plate distance while cutting | CAM plasma tool or control |
| Initial pierce height | Distance when the torch fires, before descending; sometimes given as % of cut height | Plasma tool / control |
| Pierce delay | Time stationary at pierce height to get through | Plasma tool / control |
| Best quality speed | Starting point for best angle, least dross, best finish | Cut feed |
| Production speed | Faster (around 70–80% of maximum speed, per Hypertherm): more parts, not necessarily best quality | Cut feed |
| Arc voltage | Torch height control (THC) setpoint; the higher the torch, the higher the voltage | THC |
| Kerf width | Width of material removed, for compensation | Tool kerf (see [[kerf]]) |
| Hot / cold gas flow | Flow while cutting / flow at rest (gas test) | Installation check |
| Edge start | Too thick to pierce: start from the edge | Edge lead-ins |

> [!TIP] Hypertherm notes that arc voltage **rises as consumables wear**: to keep the right height, the setpoint may need to go up. If quality drops at the end of an electrode’s life, that’s normal; replace consumables before “correcting” the chart.

## Step 3: transfer it into your software

- **SheetCam**: one plasma tool per combination (material/thickness/A) with kerf, feed, heights, delay, voltage. See [[sheetcam]].
- **Fusion**: the cutting tool library stores kerf and feed; heights and THC are often post properties. See [[fusion-plasma-posts]].
- **FireControl, LinuxCNC/QtPlasmaC, Phoenix**: material tables in the control. See [[firecontrol]], [[linuxcnc]] and [[hypertherm-edge-phoenix]].

## Step 4: validate on a drop

- [ ] New or good consumables, the right type
- [ ] Pressure/flow per the chart, clean and dry air
- [ ] Test cut: a square and a hole, at best quality speed
- [ ] Measure the part (real kerf) and look at dross and bevel
- [ ] Change **one** parameter at a time and write down the result

## What about a fiber laser?

Laser “recipes” are specific to each machine and source (power, focus, nozzle, gas, pressure, frequency). The logic is the same: manufacturer’s starting point, test, change one parameter at a time. See [[laser-troubleshooting]].

## Common mistakes

| Mistake | Consequence |
|---|---|
| Using the chart for another current or other consumables | Kerf, speed and voltage wrong from the start |
| Piercing too low | Damaged consumables; Hypertherm calls piercing too low the number one cause of premature wear |
| Cutting at production speed when you need a clean edge | More bevel or dross |
| Leaving arc voltage fixed as consumables wear | The torch drifts down or up, quality drifts |

## FAQ

### Why does arc voltage change the height?
The THC holds a constant voltage; since voltage rises with distance, a higher setpoint lifts the torch. See [[thc-hunting]].

### My table can’t hold chart speed in small details: what now?
Common: the machine slows in corners and holes. Use the control’s corner handling (anti-dive / corner hold) and small-hole strategies; see [[lead-ins-pierce]].

## For Michaël to review

- How you organize plasma tools in SheetCam (naming, one line per thickness).
- The gaps you see between chart and final settings on your table.

## Sources

- [Hypertherm — Powermax45/65/85/105 SYNC Cut Charts Guide (810500MU)](https://xnet.hypertherm.com/Xnet/library/download/?file=HYP254756), consulted November 26, 2026.
- [Hypertherm — Torch height control for plasma cutting](https://www.hypertherm.com/resources/more-resources/articles/torch-height-control-for-plasma-cutting/), consulted November 26, 2026.
- [Hypertherm — Basic tips to improve plasma cut quality](https://www.hypertherm.com/resources/more-resources/articles/basic-tips-to-improve-plasma-cut-quality/), consulted November 26, 2026.
