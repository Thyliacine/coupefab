---
id: plasma-troubleshooting
hub: troubleshooting
order: 1
nav: Dépannage plasma | Plasma troubleshooting
kicker: Dépannage · plasma | Troubleshooting · plasma
level: intermediaire
schema: HowTo
tags: plasma, dross, slag, bevel, angularity, top spatter, arc loss, consumable life, thc, troubleshooting
related: kerf, consumables, lead-ins-pierce, plasma-cutting
fr_slug: depannage-plasma-scories-biseau
en_slug: plasma-troubleshooting-dross-bevel
fr_title: Dépannage plasma : scories, biseau, projections, perte d’arc
en_title: Plasma troubleshooting: dross, bevel, top spatter, arc loss
fr_desc: Identifier le type de scories (basse vitesse, haute vitesse, projections), lire l’angle de coupe, corriger hauteur, vitesse et courant par petits pas, et régler les pertes d’arc et l’usure rapide — d’après les guides Hypertherm.
en_desc: Identify the dross type (low speed, high speed, top spatter), read the cut angle, correct height, speed and current in small steps, and fix arc loss and fast wear — based on Hypertherm’s guides.
codes: pmx-sync, pmx, xpr, esab, lincoln
---
=== fr
La plupart des défauts de coupe plasma viennent de trois variables : **vitesse**, **hauteur** (tension d’arc) et **courant** — plus l’état des consommables. Hypertherm le dit clairement dans ses guides de qualité de coupe. Ce guide suit leur logique : identifier le symptôme, puis corriger une variable à la fois, par petits pas.

## Avant tout : les quatre vérifications de base

1. **Sens de coupe** correct (profils en horaire, trous en antihoraire avec un anneau standard) — voir [Entrées et perçage](/guides/entrees-sorties-percage-plasma/).
2. **Bon procédé** pour la matière et l’épaisseur : ligne exacte de la charte, bons gaz, bons numéros de consommables.
3. **Consommables en bon état** — voir [Consommables](/guides/consommables-plasma-canada/).
4. **Torche d’équerre** avec la tôle, tôle à plat et bien mise à la masse.

## Lire les scories

| Type | À quoi ça ressemble | Cause principale | Correctif (Hypertherm) |
|---|---|---|---|
| Scories basse vitesse | Bourrelet épais et bulleux sous la coupe ; se détache en gros morceaux ; stries verticales | Vitesse trop lente (aussi : courant trop fort, torche trop basse) | Augmenter la vitesse par pas de 5 po/min ; monter la hauteur de 1/16 po ou de 5 V ; baisser le courant par pas de 10 A |
| Scories haute vitesse | Petit cordon dur et fin, difficile à enlever ; stries en « S » | Vitesse trop rapide (aussi : courant trop faible, torche trop haute) | Vérifier d’abord l’usure de la buse ; baisser la vitesse par pas de 5 po/min ; baisser la hauteur ; augmenter le courant sans dépasser 95 % du calibre de la buse |
| Projections sur le dessus | Fines gouttelettes sur l’arête supérieure, faciles à enlever | Buse usée, vitesse trop rapide, torche trop haute | Vérifier la buse ; baisser la vitesse et la hauteur |

Entre les deux extrêmes se trouve une **fenêtre sans scories** : plus étroite en inox et en aluminium, plus large en acier doux. Un peu de scories dans les coins est normal, car la vitesse chute dans les virages.

> [!TIP] Changez **une seule variable** à la fois, coupez une ligne d’essai, notez le résultat. Changer vitesse et hauteur ensemble ne vous apprend rien.

## Lire l’angle de coupe (biseau)

| Constat | Cause probable | Correctif |
|---|---|---|
| Angle négatif (pièce plus large en haut) | Torche trop basse | Monter la hauteur (ou la tension) |
| Angle positif (pièce plus large en bas) | Torche trop haute | Baisser la hauteur (ou la tension) |
| Biseau d’un seul côté | Torche pas d’équerre, ou mauvais sens de coupe | Équerrer la torche ; inverser le sens |
| Biseau qui augmente pendant le travail | Consommables qui s’usent (la tension monte) | Remplacer ; ajuster la tension |

Hypertherm rappelle que la tension d’arc doit être réajustée à mesure que les consommables s’usent pour garder la même hauteur.

## Perte d’arc et coupes interrompues

- **Vitesse beaucoup trop rapide ou trop lente** : l’arc s’éteint (pas assez de métal pour maintenir l’arc transféré).
- **Masse** : pince mal fixée, tôle rouillée, latte isolée par les scories.
- **Air** : pression insuffisante pendant la coupe, eau ou huile dans l’air.
- **THC** qui fait plonger ou monter la torche : verrouiller dans les coins et les trous, régler la coupure par vitesse.
- **Hauteur de perçage ou délai** inadaptés — voir [Entrées et perçage](/guides/entrees-sorties-percage-plasma/).

## Usure rapide des consommables

| Symptôme | Causes fréquentes |
|---|---|
| Électrode creusée vite | Air humide ou huileux, démarrages trop nombreux, arc maintenu hors de la tôle |
| Buse ovalisée | Perçage trop bas, contact avec la tôle (THC), courant au-dessus du calibre |
| Projections collées au bouclier | Hauteur de perçage trop basse, délai trop court |

## Démarche de dépannage

1. Faire les quatre vérifications de base.
2. Identifier le type de scories ou l’angle sur une coupe d’essai droite.
3. Corriger la variable principale (souvent la vitesse) par petits pas.
4. Si sans effet, corriger la hauteur, puis le courant.
5. Si toujours sans effet, remplacer électrode et buse, vérifier l’air.
6. Noter la combinaison qui marche dans la bibliothèque d’outils du FAO.

## FAQ

### Pourquoi plus de scories en fin de tôle ?
La tôle chauffe pendant le travail ; Hypertherm note que davantage de scories peut se former sur les coupes suivantes. Répartissez les coupes sur la tôle ([Imbrication](/guides/imbrication/)).

### Le grade (l’alliage) compte-t-il ?
Oui : composition chimique, état de surface et planéité changent la fenêtre sans scories, même à épaisseur égale.

## À valider en atelier (Michaël)

- Vos symptômes les plus fréquents et leurs vraies causes sur vos tables.
- Photos de coupons (scories basse et haute vitesse) à ajouter au guide.

## Sources

- [Hypertherm — How to troubleshoot cut quality problems: too much dross](https://www.hypertherm.com/resources/system-support/maintenance-and-use/cut-quality/too-much-dross/), consulté le 26 novembre 2026.
- [Hypertherm — How to improve plasma cut quality (HYP105860, PDF)](https://xnet.hypertherm.com/Xnet/library/download/?file=HYP105860).
- [Hypertherm — Basic tips to improve plasma cut quality](https://www.hypertherm.com/resources/more-resources/articles/basic-tips-to-improve-plasma-cut-quality/).
=== en
Most plasma cut defects come from three variables: **speed**, **height** (arc voltage) and **current** — plus consumable condition. Hypertherm says so clearly in its cut-quality guides. This guide follows their logic: identify the symptom, then correct one variable at a time, in small steps.

## First: the four basic checks

1. **Correct cut direction** (profiles clockwise, holes counter-clockwise with a standard swirl ring) — see [Lead-ins and pierce](/en/guides/lead-ins-pierce-height/).
2. **Right process** for material and thickness: exact chart row, right gases, right consumable part numbers.
3. **Consumables in good shape** — see [Consumables](/en/guides/plasma-consumables-canada/).
4. **Torch square** to the plate, plate flat and well grounded.

## Reading dross

| Type | What it looks like | Main cause | Fix (Hypertherm) |
|---|---|---|---|
| Low-speed dross | Thick, bubbly bead under the cut; comes off in big chunks; vertical lag lines | Speed too slow (also: current too high, torch too low) | Increase speed in 5 ipm steps; raise height by 1/16 in or 5 V; lower current in 10 A steps |
| High-speed dross | Small, hard, thin bead, hard to remove; “S” lag lines | Speed too fast (also: current too low, torch too high) | Check nozzle wear first; lower speed in 5 ipm steps; lower height; raise current without exceeding 95% of the nozzle rating |
| Top spatter | Fine droplets on the top edge, easy to remove | Worn nozzle, speed too fast, torch too high | Check the nozzle; reduce speed and height |

Between the extremes lies a **dross-free window**: narrower on stainless and aluminum, wider on mild steel. A little dross in corners is normal, as speed drops through turns.

> [!TIP] Change **one variable** at a time, cut a test line, note the result. Changing speed and height together teaches you nothing.

## Reading the cut angle (bevel)

| Observation | Likely cause | Fix |
|---|---|---|
| Negative angle (part wider at top) | Torch too low | Raise height (or voltage) |
| Positive angle (part wider at bottom) | Torch too high | Lower height (or voltage) |
| Bevel on one side only | Torch not square, or wrong cut direction | Square the torch; reverse direction |
| Bevel growing during the job | Consumables wearing (voltage rises) | Replace; adjust voltage |

Hypertherm notes that arc voltage must be readjusted as consumables wear to keep the same height.

## Arc loss and interrupted cuts

- **Speed far too fast or slow**: the arc goes out (not enough metal to sustain a transferred arc).
- **Ground**: loose clamp, rusty plate, slat insulated by slag.
- **Air**: pressure drops during the cut, water or oil in the air.
- **THC** diving or climbing: lock it in corners and holes, set the speed cutoff.
- **Pierce height or delay** wrong — see [Lead-ins and pierce](/en/guides/lead-ins-pierce-height/).

## Fast consumable wear

| Symptom | Frequent causes |
|---|---|
| Electrode pits fast | Wet or oily air, too many starts, arc held off the plate |
| Nozzle orifice oval | Piercing too low, plate contact (THC), current above rating |
| Spatter stuck to the shield | Pierce height too low, delay too short |

## Troubleshooting procedure

1. Do the four basic checks.
2. Identify the dross type or angle on a straight test cut.
3. Correct the main variable (often speed) in small steps.
4. If no effect, correct height, then current.
5. Still no effect: replace electrode and nozzle, check the air.
6. Save the working combination in the CAM tool library.

## FAQ

### Why more dross near the end of the sheet?
The plate heats up during the job; Hypertherm notes more dross may form on later cuts. Spread cuts across the sheet ([Nesting](/en/guides/nesting/)).

### Does the grade matter?
Yes: chemistry, surface condition and flatness change the dross-free window, even at the same thickness.

## For Michaël to review

- Your most frequent symptoms and their real causes on your tables.
- Coupon photos (low- and high-speed dross) to add to the guide.

## Sources

- [Hypertherm — How to troubleshoot cut quality problems: too much dross](https://www.hypertherm.com/resources/system-support/maintenance-and-use/cut-quality/too-much-dross/), consulted November 26, 2026.
- [Hypertherm — How to improve plasma cut quality (HYP105860, PDF)](https://xnet.hypertherm.com/Xnet/library/download/?file=HYP105860).
- [Hypertherm — Basic tips to improve plasma cut quality](https://www.hypertherm.com/resources/more-resources/articles/basic-tips-to-improve-plasma-cut-quality/).
