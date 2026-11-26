---
id: milling-troubleshooting
hub: troubleshooting
order: 2
nav: Dépannage usinage | Milling troubleshooting
kicker: Dépannage · usinage | Troubleshooting · machining
level: intermediaire
schema: HowTo
tags: chatter, vibration, tool breakage, surface finish, built-up edge, chip evacuation, tool wear, milling, router
related: feeds-speeds, cnc-mill, cnc-router, work-offsets
fr_slug: depannage-usinage-broutage
en_slug: milling-troubleshooting-chatter
fr_title: Dépannage en usinage : broutage, bris d’outil, mauvais fini, cotes qui dérivent
en_title: Machining troubleshooting: chatter, tool breakage, poor finish, drifting sizes
fr_desc: Symptôme → cause → correctif pour le fraisage et le routage : vibrations, outils cassés, arête rapportée, mauvais état de surface, recoupe des copeaux et cotes qui changent en cours de série.
en_desc: Symptom → cause → fix for milling and routing: vibration, broken tools, built-up edge, poor surface finish, chip recutting and sizes that change during a run.
---
=== fr
En usinage, un défaut a rarement une seule cause. La méthode : partir du symptôme, vérifier les causes de la plus probable à la moins probable, changer **une** chose, recouper.

## Broutage (vibrations)

Le broutage laisse des motifs réguliers sur la surface et un son aigu caractéristique.

| Cause | Correctif |
|---|---|
| Outil trop sorti du porte-outil | Réduire la longueur de sortie au minimum nécessaire |
| Pièce mal tenue, paroi mince | Meilleur serrage, appuis, ordre des opérations (laisser de la matière pour la rigidité) |
| Engagement radial trop grand | Parcours à engagement constant (Dynamic, Adaptive) |
| Régime dans une zone instable | Changer le régime de quelques pour cent, à charge de copeau constante |
| Porte-outil usé ou mal serré | Nettoyer cônes et pinces, remplacer la pince |
| Machine peu rigide (routeur, petite fraiseuse) | Engagement réduit plutôt qu’avance réduite à l’aveugle |

## Bris d’outil

| Moment | Cause probable |
|---|---|
| Dès la plongée | Plongée droite avec une fraise qui ne coupe pas au centre ; rampe ou hélice nécessaire |
| En pleine passe | Copeaux recoupés (évacuation), charge trop forte, broutage |
| Dans un coin intérieur | Engagement qui explose dans le coin ; arrondir le parcours, réduire l’engagement |
| Au premier contact | Mauvais correcteur de longueur, mauvais décalage — voir [Décalages](/guides/decalages-origine-g54/) |
| Petit foret | Débourrage absent (G83), avance trop forte |

## Mauvais état de surface

- **Arête rapportée** (matière soudée sur l’arête, surtout en aluminium) : vitesse de coupe plus élevée, outil poli ou revêtu adapté, lubrification.
- **Copeau trop mince** (frottement) : augmenter la charge de copeau — voir l’amincissement dans [Avances et vitesses](/guides/avances-vitesses/).
- **Outil usé** : arête écaillée ou arrondie.
- **Marques de reprise** : passe de finition continue, entrée en arc tangent.

## Copeaux et évacuation

Un copeau qui reste dans la poche est recoupé : chaleur, mauvais fini, casse. Air ou arrosage dirigé dans la coupe, évacuation par paliers, hélice montante au routeur pour les rainures profondes.

## Cotes qui dérivent en série

| Signe | Cause |
|---|---|
| Cotes qui changent progressivement | Usure d’outil → correcteur d’usure |
| Cotes qui changent le matin puis se stabilisent | Dilatation thermique de la machine → réchauffement de broche |
| Cotes aléatoires | Pièce qui bouge dans l’étau, copeaux sous la pièce, butée mal fixée |

## Démarche

1. Écouter et regarder : son, copeaux, état de l’arête.
2. Vérifier la tenue de pièce et la sortie d’outil.
3. Vérifier les paramètres par rapport à la fiche de l’outil.
4. Changer une variable, recouper, noter.

## FAQ

### Faut-il ralentir quand ça broute ?
Pas automatiquement. Souvent, réduire l’engagement radial, raccourcir l’outil ou décaler légèrement le régime règle mieux le problème que réduire l’avance, qui peut amincir le copeau et faire frotter l’outil.

## À valider en atelier (Michaël)

- Les causes de bris que vous voyez le plus souvent.

## Sources

- [Sandvik Coromant — Milling formulas and definitions](https://www.sandvik.coromant.com/en-us/knowledge/machining-formulas-definitions/milling-formulas-definitions), consulté le 26 novembre 2026.
- [Harvey Performance — Chip thinning](https://www.harveyperformance.com/in-the-loupe/combat-chip-thinning/).
- [LinuxCNC — G-codes (G83 débourrage)](https://linuxcnc.org/docs/stable/html/gcode/g-code.html).
=== en
In machining, a defect rarely has a single cause. The method: start from the symptom, check causes from most to least likely, change **one** thing, recut.

## Chatter (vibration)

Chatter leaves regular patterns on the surface and a characteristic high-pitched sound.

| Cause | Fix |
|---|---|
| Too much tool stick-out | Reduce stick-out to the minimum needed |
| Part poorly held, thin wall | Better clamping, supports, operation order (leave material for rigidity) |
| Too much radial engagement | Constant-engagement paths (Dynamic, Adaptive) |
| Spindle speed in an unstable zone | Shift rpm by a few percent, at constant chip load |
| Worn or poorly clamped holder | Clean tapers and collets, replace the collet |
| Low-rigidity machine (router, small mill) | Less engagement rather than blindly less feed |

## Tool breakage

| When | Likely cause |
|---|---|
| On the plunge | Straight plunge with a non-centre-cutting end mill; ramp or helix needed |
| Mid-pass | Recut chips (evacuation), overload, chatter |
| In an inside corner | Engagement spikes in the corner; round the path, reduce engagement |
| On first contact | Wrong length comp, wrong offset — see [Work offsets](/en/guides/work-offsets-g54/) |
| Small drill | No pecking (G83), feed too high |

## Poor surface finish

- **Built-up edge** (material welded to the edge, especially aluminum): higher cutting speed, polished or suitable coated tool, lubrication.
- **Chip too thin** (rubbing): increase chip load — see chip thinning in [Feeds and speeds](/en/guides/feeds-and-speeds/).
- **Worn tool**: chipped or rounded edge.
- **Witness marks**: continuous finishing pass, tangent arc entry.

## Chips and evacuation

A chip left in the pocket gets recut: heat, poor finish, breakage. Air or coolant aimed into the cut, stepped evacuation, up-cut bits on routers for deep slots.

## Sizes drifting during a run

| Sign | Cause |
|---|---|
| Sizes change gradually | Tool wear → wear offset |
| Sizes change in the morning then settle | Machine thermal growth → spindle warm-up |
| Random sizes | Part moving in the vise, chips under the part, loose stop |

## Procedure

1. Listen and look: sound, chips, edge condition.
2. Check workholding and tool stick-out.
3. Check parameters against the tool sheet.
4. Change one variable, recut, note.

## FAQ

### Should I slow down when it chatters?
Not automatically. Reducing radial engagement, shortening the tool or shifting rpm slightly often fixes it better than reducing feed, which can thin the chip and make the tool rub.

## For Michaël to review

- The breakage causes you see most often.

## Sources

- [Sandvik Coromant — Milling formulas and definitions](https://www.sandvik.coromant.com/en-us/knowledge/machining-formulas-definitions/milling-formulas-definitions), consulted November 26, 2026.
- [Harvey Performance — Chip thinning](https://www.harveyperformance.com/in-the-loupe/combat-chip-thinning/).
- [LinuxCNC — G-codes (G83 peck drilling)](https://linuxcnc.org/docs/stable/html/gcode/g-code.html).
