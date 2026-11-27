---
id: fixturing
hub: shop
order: 44
nav: Montage et serrage | Fixturing and workholding
kicker: Atelier · montage | Shop · workholding
level: intermediaire
schema: HowTo
tags: fixturing, workholding, montage, serrage, étau, vise, kurt, mors doux, soft jaws, parallèles, parallels, dummy part, jaw lift, 3-2-1, butée, stop, répétabilité, 5 axes
related: cnc-mill, five-axis, work-offsets, tolerances
fr_slug: montage-serrage-etau-mors-doux
en_slug: fixturing-workholding-vise-soft-jaws
fr_title: Montage et serrage : étau, mors doux et butées pour des pièces répétables
en_title: Fixturing and workholding: vises, soft jaws and stops for repeatable parts
fr_desc: Serrer correctement dans un étau (centrage, hauteur, pièce factice), utiliser parallèles et mors doux, poser des butées pour la répétabilité, et préparer un montage pour le 5 axes.
en_desc: Clamping correctly in a vise (centering, height, dummy part), using parallels and soft jaws, adding stops for repeatability, and preparing a fixture for 5-axis work.
---
=== fr
Le montage décide de la précision avant même le premier copeau. Une pièce qui bouge, un mors qui se soulève ou une butée absente coûtent plus cher qu’un mauvais outil. Ce guide couvre l’étau de fraisage, l’outil de serrage le plus courant en atelier, puis les montages dédiés.

## Serrer correctement dans un étau

D’après le manuel des étaux Kurt :

1. **Monter l’étau** sur une table propre et plane ; nettoyer le dessous de l’étau.
2. **Centrer la pièce** dans les mors, appuyée sur les glissières ou sur des parallèles.
3. **Hauteur** : avec des parallèles ou des mors à gradins, le dessous de la pièce doit rester **au niveau ou sous le haut des mors**. Serrer trop haut ou d’un seul côté fait soulever le mors mobile (*jaw lift*) et fait perdre la précision.
4. **Serrage d’un seul côté** : obligatoire d’ajouter une **pièce factice** (*dummy*) de même épaisseur de l’autre côté.
5. **Couple** : utiliser la manivelle fournie. Rallonges, clés à chocs, barres de levier et coups de marteau abîment la vis et la butée à billes. Besoin de plus de force ? Il faut un étau plus gros.
6. **Plaques de mors** : toujours les utiliser pour protéger les surfaces d’appui des mors.

> [!WARN] Un mors qui se soulève donne une pièce qui n’est plus d’équerre, sans signe évident pendant l’usinage. Vérifiez au comparateur après serrage sur une pièce critique.

## Mors doux

Les **mors doux** (aluminium ou acier doux) sont usinés sur la machine à la forme de la pièce. Ils servent pour :

- les pièces de forme ou déjà usinées (deuxième opération) ;
- les séries, avec une butée intégrée ;
- les pièces fragiles qu’il ne faut pas marquer.

Bonne pratique d’atelier (ce n’est pas une consigne tirée du manuel Kurt) : usiner les mors **serrés sur une cale** à la même force de serrage que la production, pour que la forme corresponde à l’état serré.

## Répétabilité : butées et origines

- **Butée fixe** sur le mors fixe ou l’étau : chaque pièce se place au même endroit, l’origine (voir [[work-offsets]]) reste valide.
- **Principe 3-2-1** pour les montages dédiés : trois appuis définissent un plan, deux une ligne, un un point ; le serrage pousse la pièce vers ces appuis, jamais contre eux.
- **Repérer** les montages (numéro, origine, programme) pour les remonter sans re-palper.

## Montage pour le 5 axes

En 5 axes, l’accès à la pièce compte autant que la force de serrage. Étaux 5 axes, queues d’aronde et montages surélevés dégagent l’outil des mors et de la table. Simulez toujours le montage dans la FAO (voir [[five-axis]]).

## Liste de vérification

- [ ] Étau propre, aligné au comparateur
- [ ] Pièce centrée, dessous au niveau ou sous le haut des mors
- [ ] Pièce factice si serrage d’un seul côté
- [ ] Butée en place pour les séries
- [ ] Montage modélisé dans la FAO (collisions)

## Erreurs fréquentes

- Serrer une pièce minuscule tout en haut des mors : soulèvement et vibrations.
- Frapper la pièce sur les parallèles au marteau après serrage complet : serrer légèrement, asseoir, puis serrer.
- Oublier les copeaux sous la pièce ou les parallèles.
- Usiner des mors doux sans cale ni serrage : la forme ne correspond plus une fois serrée.

## FAQ

### Mors doux en aluminium ou en acier ?
Aluminium pour usiner vite et protéger les pièces ; acier doux pour les séries longues ou les pièces lourdes.

### Comment savoir si mon mors se soulève ?
Comparateur sur le haut du mors mobile pendant le serrage, ou contrôle d’équerre de la pièce après usinage.

### Quand passer à un montage dédié ?
Quand l’étau ne tient pas la pièce de façon stable, quand plusieurs pièces par cycle sont rentables, ou pour le 5 axes.

## À valider en atelier (Michaël)

- Étaux et systèmes de montage utilisés chez nous (marques, mors doux).
- Couple de serrage habituel par type de pièce.

## Sources

- [Kurt Workholding — Manuel de l’étau D100 AngLock (PDF)](https://www.kurtworkholding.com/wp-content/uploads/2026/03/Kurt_D100_Manual_2026-03-24.pdf) : montage, centrage, hauteur des parallèles, pièce factice, manivelle seulement, plaques de mors. Consulté le 26 novembre 2026.
- [Kurt Workholding — How to Machine Better Parts with Soft Jaws (webinaire)](https://www.kurtworkholding.com/workholding-tips/how-to-machine-better-parts-with-soft-jaws-webinar/).

=== en
Fixturing decides accuracy before the first chip. A part that moves, a jaw that lifts or a missing stop costs more than a poor tool. This guide covers the milling vise, the most common workholding in shops, then dedicated fixtures.

## Clamping correctly in a vise

Per the Kurt vise manual:

1. **Mount the vise** on a clean, flat table; clean the underside of the vise.
2. **Center the part** in the jaws, resting on the ways or on parallels.
3. **Height**: with parallels or step jaws, the bottom of the part must stay **at or below the top of the jaws**. Clamping too high or on one side lifts the movable jaw (*jaw lift*) and costs accuracy.
4. **One-sided clamping**: you must add a **dummy part** of the same thickness on the other side.
5. **Torque**: use the supplied handle. Extensions, impact wrenches, breaker bars and hammer strikes damage the screw and thrust bearing. Need more force? You need a larger vise.
6. **Jaw plates**: always use them to protect the jaws’ mounting surfaces.

> [!WARN] A lifting jaw gives a part that is no longer square, with no obvious sign during machining. Check with an indicator after clamping on a critical part.

## Soft jaws

**Soft jaws** (aluminum or mild steel) are machined on the machine to the part’s shape. Use them for:

- shaped or already-machined parts (second operation);
- production runs, with a built-in stop;
- delicate parts that must not be marked.

Common shop practice (not an instruction from the Kurt manual): machine the jaws **clamped on a spacer** at the same clamping force as production, so the shape matches the clamped state.

## Repeatability: stops and offsets

- **Fixed stop** on the solid jaw or vise: every part sits in the same place, and the work offset (see [[work-offsets]]) stays valid.
- **3-2-1 principle** for dedicated fixtures: three supports define a plane, two a line, one a point; clamping pushes the part toward these locators, never against them.
- **Label** fixtures (number, offset, program) so they can be reinstalled without re-probing.

## Fixturing for 5-axis

On 5-axis, access to the part matters as much as clamping force. 5-axis vises, dovetails and raised fixtures keep the tool clear of the jaws and table. Always simulate the fixture in CAM (see [[five-axis]]).

## Checklist

- [ ] Vise clean, indicated in
- [ ] Part centered, bottom at or below the top of the jaws
- [ ] Dummy part if clamping on one side
- [ ] Stop in place for production runs
- [ ] Fixture modeled in CAM (collisions)

## Common mistakes

- Clamping a tiny part at the very top of the jaws: lift and chatter.
- Hammering the part onto parallels after full clamping: snug, seat, then tighten.
- Leaving chips under the part or parallels.
- Machining soft jaws without a spacer or clamping: the shape no longer matches once clamped.

## FAQ

### Aluminum or steel soft jaws?
Aluminum to machine fast and protect parts; mild steel for long runs or heavy parts.

### How do I know if my jaw lifts?
An indicator on top of the movable jaw while clamping, or a squareness check on the part after machining.

### When should I move to a dedicated fixture?
When the vise can’t hold the part stably, when several parts per cycle pay off, or for 5-axis.

## For Michaël to review

- Vises and fixturing systems we use (brands, soft jaws).
- Usual clamping torque by part type.

## Sources

- [Kurt Workholding — D100 AngLock vise manual (PDF)](https://www.kurtworkholding.com/wp-content/uploads/2026/03/Kurt_D100_Manual_2026-03-24.pdf): mounting, centering, parallel height, dummy part, handle only, jaw plates. Consulted November 26, 2026.
- [Kurt Workholding — How to Machine Better Parts with Soft Jaws (webinar)](https://www.kurtworkholding.com/workholding-tips/how-to-machine-better-parts-with-soft-jaws-webinar/).
