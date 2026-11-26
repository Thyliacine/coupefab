---
id: laser-troubleshooting
hub: troubleshooting
order: 30
nav: Laser : scories et brûlures | Laser: dross and burning
kicker: Dépannage · laser fibre | Troubleshooting · fiber laser
level: intermediaire
schema: HowTo
tags: laser, fiber laser, dross, burr, burning, gouging, focus, nozzle, assist gas, nitrogen, oxygen, protective window, lens, centering
related: fiber-laser, cut-charts, kerf, plasma-troubleshooting
fr_slug: depannage-laser-scories-brulures
en_slug: laser-troubleshooting-dross-burning
fr_title: Dépannage laser fibre : scories, bavures, brûlures et coupe incomplète
en_title: Fiber laser troubleshooting: dross, burrs, burning and incomplete cuts
fr_desc: Symptôme → cause → correctif pour la découpe laser fibre : scories adhérentes, bavure, brûlure des coins, stries, coupe qui ne traverse pas. Buse, centrage, focale, gaz, fenêtre de protection, dans le bon ordre.
en_desc: Symptom → cause → fix for fiber laser cutting: clinging dross, burrs, burned corners, striations, cuts that don’t go through. Nozzle, centering, focus, gas and protective window, in the right order.
---
=== fr
Sur un laser fibre, 80 % des problèmes de qualité viennent de quatre choses que l’opérateur peut vérifier en quelques minutes : **la buse, le centrage du faisceau, la fenêtre de protection et le gaz**. Les paramètres de la table de coupe viennent après. Ce guide suit cet ordre.

> [!WARN] Le faisceau d’un laser fibre (environ 1 µm) est invisible et dangereux pour les yeux, même réfléchi. Les vérifications de buse et de fenêtre se font machine en mode sécurité, selon la procédure du fabricant. Voir [[safety]].

## La règle : vérifier avant de toucher aux paramètres

1. **Buse** : propre, ronde, pas éclaboussée ni déformée ; bon diamètre et bon type (simple ou double) pour la recette.
2. **Centrage** : faire le test de centrage (ruban ou tir sur adhésif) prévu par le fabricant ; un faisceau décentré donne une qualité différente selon la direction de coupe.
3. **Fenêtre de protection** (*protective window*) : inspecter et nettoyer ou remplacer selon la procédure ; une fenêtre tachée absorbe de l’énergie et chauffe.
4. **Gaz** : bonne pression à la buse (pas seulement au régulateur), pureté conforme, aucune fuite ni humidité.
5. **Matière** : nuance, épaisseur réelle, état de surface (calamine, huile, film plastique côté correct).
6. **Recette** : seulement ensuite, revenir à la charte du fabricant et ajuster un paramètre à la fois.

## Tableau symptôme → cause → correctif

| Symptôme | Causes probables | Correctifs à essayer, dans l’ordre |
|---|---|---|
| Scories adhérentes en dessous (acier doux, O₂) | Vitesse trop lente ou trop rapide, focale mal placée, pression d’O₂ inadaptée, buse usée | Vérifier buse et centrage, puis revenir à la recette ; ajuster la focale par petits pas ; ajuster la vitesse |
| Bavure fine et dure en dessous (inox ou alu, N₂) | Pression d’azote insuffisante, focale trop haute, vitesse trop élevée | Vérifier la pression à la buse et la pureté ; descendre légèrement la focale ; réduire un peu la vitesse |
| Coupe qui ne traverse pas | Puissance réelle insuffisante, fenêtre sale, épaisseur supérieure à la recette, vitesse trop élevée | Fenêtre, puis buse ; confirmer l’épaisseur ; réduire la vitesse |
| Brûlure ou cratères dans les coins et petits trous | Trop d’énergie au ralentissement, oxydation excessive à l’O₂ | Activer ou ajuster la gestion des coins (puissance/fréquence en rampe), boucles de coin, recette « petits trous » |
| Stries profondes et irrégulières | Vitesse inadaptée, gaz turbulent (buse abîmée), vibration | Changer la buse, vérifier le centrage, ajuster la vitesse |
| Qualité différente selon la direction | Faisceau décentré, buse ovalisée | Test de centrage, nouvelle buse |
| Bord bleui ou jaune sur inox (N₂) | Contamination d’oxygène dans le gaz, pureté insuffisante | Vérifier pureté, purge des conduites, fuites |
| Perçage qui explose ou éclabousse | Recette de perçage inadaptée, surface sale | Perçage progressif selon la charte, surface propre, hauteur de perçage |

## Gaz d’assistance : rappel utile au dépannage

| Gaz | Usage courant | Effet sur le bord |
|---|---|---|
| Oxygène (O₂) | Acier doux, surtout en épaisseur | Réaction exothermique, bord oxydé (couche d’oxyde à enlever avant peinture ou soudure selon le cas) |
| Azote (N₂) | Inox, aluminium, acier doux mince quand on veut un bord propre | Bord non oxydé ; demande plus de pression et de débit |
| Air comprimé | Matières minces selon la machine | Compromis coût/qualité ; dépend d’un air propre et sec |

Les pressions, diamètres de buse et focales exacts sont propres à chaque machine et à chaque source : utilisez la charte de votre fabricant (voir [[cut-charts]]).

## Liste de vérification de début de quart

- [ ] Buse inspectée, bon diamètre pour la recette du jour
- [ ] Test de centrage fait après tout changement de buse ou choc
- [ ] Fenêtre de protection inspectée
- [ ] Pressions de gaz lues et réserves suffisantes
- [ ] Calibration du capteur de hauteur (capacitif) faite selon la procédure
- [ ] Coupe d’essai sur une chute de la même tôle avant la série

## Erreurs fréquentes

| Erreur | Pourquoi c’est un problème |
|---|---|
| Changer trois paramètres à la fois | On ne sait plus lequel a réglé (ou empiré) le problème |
| Monter la puissance pour « forcer » | Masque une fenêtre sale ou un mauvais centrage, et chauffe davantage l’optique |
| Ignorer la tôle (calamine, film) | La meilleure recette ne compense pas une matière hors norme |
| Ne pas noter le correctif | Le même problème revient au prochain quart |

## FAQ

### Pourquoi la coupe est belle d’un côté de la pièce et pas de l’autre ?
C’est presque toujours le centrage du faisceau dans la buse ou une buse ovalisée : le flux de gaz n’est plus symétrique. Faites le test de centrage et changez la buse.

### Faut-il nettoyer la lentille ?
Sur la plupart des têtes de coupe, l’opérateur n’intervient que sur la **fenêtre de protection** ; la lentille de focalisation est protégée et ne s’ouvre que selon la procédure du fabricant, en environnement propre.

### Mes scories partent au marteau : est-ce acceptable ?
Ça dépend de la spécification de la pièce. Si on doit ébavurer chaque pièce, le coût de main-d’œuvre dépasse souvent le gain de vitesse ; voir [[deburring]].

## À valider en atelier (Michaël)

- L’ordre de vérification utilisé sur vos machines et la fréquence de remplacement des fenêtres.
- Vos cas réels de scories sur acier doux à l’O₂ et leur correctif.

## Sources

- [TRUMPF — Découpe laser : principes et gaz de coupe](https://www.trumpf.com/fr_CA/solutions/applications/decoupe-laser/), consulté le 26 novembre 2026.
- [IPG Photonics — Laser cutting](https://www.ipgphotonics.com/en/applications/materials-processing/cutting), consulté le 26 novembre 2026.
- [Precitec — Têtes de découpe laser (entretien de la fenêtre de protection)](https://www.precitec.com/laser-cutting/), consulté le 26 novembre 2026.
- [CNESST — Sécurité des machines](https://www.cnesst.gouv.qc.ca/fr/prevention-securite/identifier-corriger-risques/liste-informations-prevention/securite-machines), consulté le 26 novembre 2026.
=== en
On a fiber laser, most quality problems come from four things the operator can check in minutes: **the nozzle, beam centering, the protective window and the gas**. Cut chart parameters come after. This guide follows that order.

> [!WARN] A fiber laser beam (about 1 µm) is invisible and dangerous to the eyes, even when reflected. Nozzle and window checks are done with the machine in its safe mode, following the manufacturer’s procedure. See [[safety]].

## The rule: check before you touch parameters

1. **Nozzle**: clean, round, not spattered or deformed; correct diameter and type (single or double) for the recipe.
2. **Centering**: run the manufacturer’s centering test (tape shot); an off-centre beam gives different quality depending on cut direction.
3. **Protective window**: inspect and clean or replace per procedure; a stained window absorbs energy and heats up.
4. **Gas**: right pressure at the nozzle (not just at the regulator), required purity, no leaks or moisture.
5. **Material**: grade, actual thickness, surface condition (mill scale, oil, protective film on the right side).
6. **Recipe**: only then go back to the manufacturer’s chart and change one parameter at a time.

## Symptom → cause → fix table

| Symptom | Likely causes | Fixes to try, in order |
|---|---|---|
| Clinging dross underneath (mild steel, O₂) | Speed too slow or too fast, focus misplaced, O₂ pressure off, worn nozzle | Check nozzle and centering, return to the recipe; adjust focus in small steps; adjust speed |
| Fine, hard burr underneath (stainless or aluminum, N₂) | Nitrogen pressure too low, focus too high, speed too high | Check pressure at the nozzle and purity; lower focus slightly; reduce speed a little |
| Cut doesn’t go through | Not enough real power, dirty window, thicker than the recipe, speed too high | Window, then nozzle; confirm thickness; reduce speed |
| Burning or craters at corners and small holes | Too much energy during slowdown, excess oxidation with O₂ | Enable or tune corner control (power/frequency ramping), corner loops, a “small holes” recipe |
| Deep, irregular striations | Wrong speed, turbulent gas (damaged nozzle), vibration | Replace the nozzle, check centering, adjust speed |
| Quality differs by direction | Off-centre beam, oval nozzle | Centering test, new nozzle |
| Blue or yellow edge on stainless (N₂) | Oxygen contamination in the gas, low purity | Check purity, purge lines, leaks |
| Pierce blows out or spatters | Wrong pierce recipe, dirty surface | Stepped pierce per chart, clean surface, pierce height |

## Assist gas: a troubleshooting refresher

| Gas | Typical use | Effect on the edge |
|---|---|---|
| Oxygen (O₂) | Mild steel, especially thicker | Exothermic reaction, oxidized edge (oxide layer may need removal before paint or welding) |
| Nitrogen (N₂) | Stainless, aluminum, thin mild steel when a clean edge is needed | Oxide-free edge; needs more pressure and flow |
| Compressed air | Thin material depending on the machine | Cost/quality compromise; depends on clean, dry air |

Exact pressures, nozzle sizes and focus positions are specific to each machine and source: use your manufacturer’s chart (see [[cut-charts]]).

## Start-of-shift checklist

- [ ] Nozzle inspected, right diameter for today’s recipe
- [ ] Centering test done after any nozzle change or crash
- [ ] Protective window inspected
- [ ] Gas pressures read and supply sufficient
- [ ] Height sensor (capacitive) calibration done per procedure
- [ ] Test cut on a drop of the same sheet before the run

## Common mistakes

| Mistake | Why it hurts |
|---|---|
| Changing three parameters at once | You no longer know which one fixed (or worsened) the problem |
| Turning power up to “force” it | Hides a dirty window or bad centering, and heats the optics more |
| Ignoring the sheet (scale, film) | The best recipe can’t make up for off-spec material |
| Not writing down the fix | The same problem returns next shift |

## FAQ

### Why is the cut good on one side of the part and not the other?
It is almost always beam centering in the nozzle or an oval nozzle: gas flow is no longer symmetrical. Run the centering test and replace the nozzle.

### Should I clean the lens?
On most cutting heads the operator only services the **protective window**; the focusing lens is protected and is opened only per the manufacturer’s procedure, in a clean environment.

### The dross knocks off with a hammer: is that acceptable?
It depends on the part spec. If every part needs deburring, labour usually costs more than the speed gained; see [[deburring]].

## For Michaël to review

- The check order used on your machines and how often windows are replaced.
- Your real cases of dross on mild steel with O₂ and their fix.

## Sources

- [TRUMPF — Laser cutting: principles and cutting gases](https://www.trumpf.com/en_CA/solutions/applications/laser-cutting/), consulted November 26, 2026.
- [IPG Photonics — Laser cutting](https://www.ipgphotonics.com/en/applications/materials-processing/cutting), consulted November 26, 2026.
- [Precitec — Laser cutting heads (protective window maintenance)](https://www.precitec.com/laser-cutting/), consulted November 26, 2026.
- [CNESST — Machine safety (French)](https://www.cnesst.gouv.qc.ca/fr/prevention-securite/identifier-corriger-risques/liste-informations-prevention/securite-machines), consulted November 26, 2026.
