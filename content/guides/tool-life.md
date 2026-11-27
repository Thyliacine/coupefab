---
id: tool-life
hub: shop
order: 40
nav: Durée de vie des outils | Tool life
kicker: Atelier · outillage | Shop · tooling
level: intermediaire
schema: HowTo
tags: tool life, tool wear, flank wear, crater wear, built-up edge, chipping, notch wear, plastic deformation, taylor, cutting speed, insert, end mill, tool management
related: feeds-speeds, milling-troubleshooting, lathe-finish-chatter, inconel
fr_slug: duree-vie-outils-usure
en_slug: tool-life-wear
fr_title: Durée de vie des outils de coupe : lire l’usure, la prolonger et la gérer
en_title: Cutting tool life: reading wear, extending it and managing it
fr_desc: Usure en dépouille, cratère, arête rapportée, écaillage, entaille, déformation plastique : comment reconnaître chaque mode, sa cause et son correctif, le rôle dominant de la vitesse de coupe, et un système simple de suivi en atelier.
en_desc: Flank wear, crater, built-up edge, chipping, notch, plastic deformation: how to recognize each mode, its cause and fix, the dominant role of cutting speed, and a simple shop tracking system.
---
=== fr
Un outil s’use toujours ; la question est **comment** et **à quelle vitesse**. Selon Sandvik Coromant, l’usure en **dépouille** (*flank wear*), régulière et prévisible, est le mode souhaitable et sert souvent de critère de fin de vie. Tous les autres modes signalent un problème à corriger.

## Lire l’usure

| Mode | À quoi ça ressemble | Causes typiques | Correctif |
|---|---|---|---|
| Usure en dépouille | Bande d’usure régulière sous l’arête | Usure normale ; trop rapide si vitesse trop élevée | Réduire la vitesse, grade de carbure plus résistant à l’usure |
| Cratère | Creux sur la face de coupe | Diffusion/chimie à haute température (vitesse élevée) | Réduire la vitesse, grade revêtu adapté |
| Arête rapportée (BUE) | Matière soudée sur l’arête | Matière collante (alu, inox, cuivre), vitesse/température trop basses | Augmenter la vitesse, arête plus vive, lubrification |
| Écaillage | Petits éclats sur l’arête | Coupe interrompue, vibrations, arête trop fragile | Grade de carbure plus tenace, arête renforcée, rigidité |
| Usure en entaille | Encoche à la profondeur de passe | Écrouissage (inox, superalliages), croûte | Varier la profondeur de passe, angle d’attaque plus faible |
| Déformation plastique | Arête affaissée | Température et effort excessifs | Réduire vitesse/avance, grade plus dur |
| Fissures thermiques | Fissures perpendiculaires à l’arête | Chocs thermiques (arrosage intermittent) | Arrosage continu ou à sec selon la recommandation |

## Ce qui use le plus : la vitesse

Sandvik Coromant indique que la durée de vie dépend surtout de la **vitesse de coupe**, puis de l’avance, et peu de la profondeur de passe. L’équation de **Taylor** (V × Tⁿ = C) formalise ce lien ; elle est utile pour raisonner, mais limitée : les modèles récents ajoutent l’avance et l’épaisseur de copeau.

En pratique : pour gagner de la durée de vie sans perdre de productivité, on **baisse un peu la vitesse et on augmente l’avance** (dans les limites de l’outil et de la finition).

## Démarche d’amélioration

1. **Observer** l’arête usée à la loupe (×10) et identifier le mode.
2. **Corriger la cause** (tableau ci-dessus), un paramètre à la fois.
3. **Mesurer** la durée de vie (pièces, minutes en coupe ou longueur usinée).
4. **Standardiser** : la valeur retenue va dans la bibliothèque d’outils de la FAO et dans la fiche de réglage.

## Système de suivi simple

| Donnée | Pourquoi |
|---|---|
| Référence outil + grade de carbure | Comparer les fournisseurs |
| Matière usinée | La durée de vie n’a de sens que par matière |
| Vitesse, avance, profondeur | Reproduire les conditions |
| Pièces ou minutes par arête | Indicateur principal |
| Mode de fin de vie | Détecter les problèmes (écaillage ≠ usure normale) |

## Liste de vérification

- [ ] Montage rigide, porte-à-faux minimal
- [ ] Faux-rond de l’outil vérifié (fraises)
- [ ] Arrosage adapté (ou air pour certaines opérations)
- [ ] Évacuation des copeaux (pas de recoupe)
- [ ] Changement d’outil planifié avant la rupture

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Attendre la casse pour changer l’outil | Pièce rebutée, porte-outil abîmé |
| Réduire l’avance pour « ménager » l’outil | Frottement, écrouissage, usure plus rapide |
| Ignorer le faux-rond | Une dent travaille pour toutes |
| Changer de grade sans noter les conditions | Comparaison impossible |

## FAQ

### Faut-il toujours arroser ?
Non : certaines opérations de fraisage en carbure tolèrent mieux l’air ou le sec (moins de chocs thermiques). Suivez la recommandation du fabricant de l’outil.

### Pourquoi une fraise neuve casse-t-elle tout de suite ?
Souvent faux-rond, porte-à-faux, entrée trop brutale ou copeau trop épais ; voir [[milling-troubleshooting]].

## À valider en atelier (Michaël)

- Votre méthode de suivi de durée de vie et vos critères de changement d’outil.

## Sources

- [Sandvik Coromant — Wear on cutting edges](https://www.sandvik.coromant.com/en-us/knowledge/materials/wear-on-cutting-edges), consulté le 26 novembre 2026.
- [Sandvik Coromant — How to improve tool life in turning](https://www.sandvik.coromant.com/en-us/knowledge/general-turning/how-to-improve-tool-life-in-turning), consulté le 26 novembre 2026.
- [Johansson et al. — Assessment of different tool life models (Université de Lund, PDF)](https://lup.lub.lu.se/search/files/61985840/Assessment_of_different_tool_life_models_submitted_manuscript.pdf), consulté le 26 novembre 2026.
=== en
A tool always wears; the question is **how** and **how fast**. Per Sandvik Coromant, **flank wear**, steady and predictable, is the desirable mode and often serves as the end-of-life criterion. Every other mode signals a problem to fix.

## Reading wear

| Mode | What it looks like | Typical causes | Fix |
|---|---|---|---|
| Flank wear | Even wear band below the edge | Normal wear; too fast if speed is too high | Reduce speed, more wear-resistant grade |
| Crater | Hollow on the rake face | Diffusion/chemistry at high temperature (high speed) | Reduce speed, suitable coated grade |
| Built-up edge (BUE) | Material welded on the edge | Sticky materials (aluminum, stainless, copper), speed/temperature too low | Raise speed, sharper edge, lubrication |
| Chipping | Small chips off the edge | Interrupted cuts, vibration, edge too fragile | Tougher grade, stronger edge prep, rigidity |
| Notch wear | Notch at depth-of-cut line | Work hardening (stainless, superalloys), scale | Vary depth of cut, smaller lead angle |
| Plastic deformation | Sagging edge | Excessive temperature and force | Reduce speed/feed, harder grade |
| Thermal cracks | Cracks perpendicular to the edge | Thermal shock (intermittent coolant) | Continuous coolant or dry per recommendation |

## What wears most: speed

Sandvik Coromant states tool life depends mostly on **cutting speed**, then feed, and little on depth of cut. **Taylor’s** equation (V × Tⁿ = C) formalizes the link; useful for reasoning, but limited: newer models add feed and chip thickness.

In practice: to gain tool life without losing productivity, **lower speed a little and raise feed** (within tool and finish limits).

## Improvement approach

1. **Look** at the worn edge with a loupe (×10) and identify the mode.
2. **Fix the cause** (table above), one parameter at a time.
3. **Measure** tool life (parts, minutes in cut or length machined).
4. **Standardize**: the chosen value goes into the CAM tool library and the setup sheet.

## Simple tracking system

| Data | Why |
|---|---|
| Tool reference + grade | Compare suppliers |
| Material machined | Tool life only means something per material |
| Speed, feed, depth | Reproduce conditions |
| Parts or minutes per edge | Main indicator |
| End-of-life mode | Spot problems (chipping ≠ normal wear) |

## Checklist

- [ ] Rigid setup, minimal stick-out
- [ ] Tool runout checked (end mills)
- [ ] Suitable coolant (or air for some operations)
- [ ] Chip evacuation (no re-cutting)
- [ ] Planned tool change before breakage

## Common mistakes

| Mistake | Consequence |
|---|---|
| Waiting for breakage to change the tool | Scrapped part, damaged holder |
| Reducing feed to “spare” the tool | Rubbing, work hardening, faster wear |
| Ignoring runout | One flute does all the work |
| Changing grade without recording conditions | No valid comparison |

## FAQ

### Should you always use coolant?
No: some carbide milling operations do better with air or dry (less thermal shock). Follow the tool maker’s recommendation.

### Why does a new end mill break right away?
Often runout, stick-out, too abrupt an entry or too thick a chip; see [[milling-troubleshooting]].

## For Michaël to review

- Your tool life tracking method and tool change criteria.

## Sources

- [Sandvik Coromant — Wear on cutting edges](https://www.sandvik.coromant.com/en-us/knowledge/materials/wear-on-cutting-edges), consulted November 26, 2026.
- [Sandvik Coromant — How to improve tool life in turning](https://www.sandvik.coromant.com/en-us/knowledge/general-turning/how-to-improve-tool-life-in-turning), consulted November 26, 2026.
- [Johansson et al. — Assessment of different tool life models (Lund University, PDF)](https://lup.lub.lu.se/search/files/61985840/Assessment_of_different_tool_life_models_submitted_manuscript.pdf), consulted November 26, 2026.
