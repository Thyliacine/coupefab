---
id: lathe-finish-chatter
hub: shop
order: 42
nav: Tournage : fini et vibrations | Turning: finish and chatter
kicker: Atelier · tournage | Shop · turning
level: intermediaire
schema: HowTo
tags: tournage, turning, chatter, vibration, broutage, surface finish, fini de surface, ra, nose radius, rayon de bec, wiper, planeur, overhang, porte-à-faux, boring bar, barre d’alésage, centre height, hauteur de centre
related: cnc-lathe, tool-life, feeds-speeds, tolerances
fr_slug: tournage-fini-surface-vibrations
en_slug: turning-surface-finish-chatter
fr_title: Tournage : obtenir un bon fini et éliminer les vibrations (broutage)
en_title: Turning: getting a good surface finish and eliminating chatter
fr_desc: Rayon de bec, avance et plaquettes planeuses (wiper) pour le fini ; angle d’attaque, profondeur de passe, porte-à-faux et hauteur de centre contre les vibrations ; tableau de diagnostic tiré des recommandations Sandvik Coromant.
en_desc: Nose radius, feed and wiper inserts for finish; entering angle, depth of cut, overhang and centre height against chatter; a diagnosis table based on Sandvik Coromant’s recommendations.
---
=== fr
Un mauvais fini en tournage vient presque toujours de l’une de deux causes : **la géométrie** (avance trop forte pour le rayon de bec, copeaux qui frottent la pièce, usure) ou **les vibrations** (broutage) dues à un manque de rigidité ou à des efforts radiaux trop élevés. Ce guide aide à distinguer les deux et à corriger dans le bon ordre.

## Fini de surface : avance, rayon de bec et plaquettes planeuses

À rayon de bec égal, **le fini se dégrade vite quand l’avance augmente**. Les plaquettes **planeuses** (*wiper*) lissent la surface et permettent d’avancer plus vite à fini égal, surtout en chariotage et dressage rectilignes.

Exemples tirés du tableau Sandvik Coromant (valeurs théoriques pour les rayons standard, mesurées dans un acier faiblement allié pour les planeuses) :

| Avance (mm/tr) | Standard r 0,8 mm — Ra (µm) | Planeuse r 0,8 mm — Ra (µm) |
|---|---|---|
| 0,15 | 0,70 | 0,25 |
| 0,20 | 1,25 | 0,35 |
| 0,30 | 3,23 | 0,55 |
| 0,40 | 5,75 | 0,70 |

> [!TIP] Pour améliorer le fini : planeuse ou rayon plus grand, puis réduire l’avance. Mais un grand rayon augmente les efforts radiaux et favorise les vibrations : c’est un compromis.

## Vibrations : les causes et leurs correctifs

| Symptôme / cause | Correctif (Sandvik Coromant) |
|---|---|
| Efforts radiaux élevés, surtout en alésage | Angle d’attaque plus grand (KAPR 90°) ; rayon de bec plus petit |
| Profondeur de passe trop faible, la plaquette frotte | Augmenter la profondeur ; prendre une passe plus grande que le rayon de bec |
| Géométrie qui crée de grands efforts | Géométrie positive ; réduire l’avance |
| Porte-à-faux long | Réduire le porte-à-faux ; plus gros diamètre de barre ; barre carbure ou antivibratoire |
| Serrage de la barre insuffisant | Allonger la longueur de serrage (au moins 3 × le diamètre de la barre) |
| Outil mal positionné | Vérifier la hauteur de centre |
| Usure en dépouille excessive | Nuance plus résistante à l’usure ou vitesse réduite |

## Démarche de diagnostic

1. **Regarder la surface** : marques régulières et sonores = vibrations ; surface « poilue » ou rayée = copeaux ou usure.
2. **Vérifier l’arête** à la loupe : usure en dépouille, arête rapportée, écaillage (voir [[tool-life]]).
3. **Réduire le porte-à-faux** de l’outil et de la pièce ; ajouter la contre-pointe si la pièce est longue.
4. **Ajuster la géométrie** : profondeur > rayon de bec, angle d’attaque près de 90°, rayon plus petit si ça vibre.
5. **Ajuster les conditions** : avance et vitesse recommandées par le fabricant de plaquettes (voir [[feeds-speeds]]).

## Liste de vérification

- [ ] Hauteur de centre vérifiée
- [ ] Porte-à-faux minimal ; barre d’alésage serrée sur au moins 3 × son diamètre
- [ ] Profondeur de passe plus grande que le rayon de bec
- [ ] Plaquette planeuse envisagée pour la finition
- [ ] Arrosage dirigé sur la zone de coupe en finition

## Erreurs fréquentes

- Réduire la profondeur de passe pour « calmer » les vibrations : une passe trop fine fait frotter la plaquette et vibre davantage.
- Choisir un grand rayon de bec en alésage long.
- Ignorer l’usure : une arête usée change le fini avant de casser.
- Corriger le fini en baissant la vitesse alors que l’arête rapportée demande plutôt d’augmenter la vitesse.

## FAQ

### Pourquoi ça vibre surtout en alésage ?
La barre d’alésage est en porte-à-faux. Plus elle sort, plus elle fléchit. Réduisez le porte-à-faux et choisissez une barre carbure ou antivibratoire pour les grandes longueurs.

### Planeuse partout ?
Elle est conçue surtout pour le chariotage et le dressage rectilignes. Sur des profils complexes, l’effet est moindre.

### Quelle rugosité viser ?
Celle du dessin. Voir [[tolerances]] pour lier rugosité et procédé.

## À valider en atelier (Michaël)

- Plaquettes et nuances qui fonctionnent sur nos tours, par matière.
- Longueurs de barre d’alésage maximales en pratique.

## Sources

- [Sandvik Coromant — Troubleshooting in turning](https://www.sandvik.coromant.com/en-us/knowledge/general-turning/troubleshooting-turning) : causes et correctifs des vibrations et du mauvais fini. Consulté le 26 novembre 2026.
- [Sandvik Coromant — How to achieve good component quality in turning](https://www.sandvik.coromant.com/en-us/knowledge/general-turning/how-to-achieve-good-component-quality-in-turning) : tableau Ra standard/planeuse, profondeur > rayon de bec, serrage de la barre ≥ 3 × D.

=== en
Poor finish in turning almost always comes from one of two causes: **geometry** (feed too high for the nose radius, chips rubbing the part, wear) or **vibration** (chatter) from a lack of rigidity or high radial forces. This guide helps tell them apart and fix them in the right order.

## Surface finish: feed, nose radius and wiper inserts

For a given nose radius, **finish gets worse quickly as feed goes up**. **Wiper** inserts smooth the surface and allow higher feed at the same finish, mainly in straight longitudinal turning and facing.

Examples from Sandvik Coromant’s table (theoretical values for standard radii, measured in low-alloy steel for wipers):

| Feed (mm/rev) | Standard r 0.8 mm — Ra (µm) | Wiper r 0.8 mm — Ra (µm) |
|---|---|---|
| 0.15 | 0.70 | 0.25 |
| 0.20 | 1.25 | 0.35 |
| 0.30 | 3.23 | 0.55 |
| 0.40 | 5.75 | 0.70 |

> [!TIP] To improve finish: a wiper or larger radius, then lower feed. But a large radius raises radial forces and encourages chatter: it is a trade-off.

## Chatter: causes and fixes

| Symptom / cause | Fix (Sandvik Coromant) |
|---|---|
| High radial forces, especially boring | Larger entering angle (KAPR 90°); smaller nose radius |
| Depth of cut too small, insert rubs | Increase depth; cut deeper than the nose radius |
| Geometry creating high forces | Positive geometry; reduce feed |
| Long overhang | Reduce overhang; larger bar diameter; carbide or damped bar |
| Weak bar clamping | Longer clamping length (at least 3 × bar diameter) |
| Tool incorrectly positioned | Check centre height |
| Excessive flank wear | More wear-resistant grade or lower speed |

## Diagnosis routine

1. **Look at the surface**: regular, noisy marks = chatter; “hairy” or scratched surface = chips or wear.
2. **Check the edge** with a loupe: flank wear, built-up edge, chipping (see [[tool-life]]).
3. **Reduce overhang** of tool and part; add the tailstock on long parts.
4. **Adjust geometry**: depth > nose radius, entering angle near 90°, smaller radius if it chatters.
5. **Adjust conditions**: feed and speed recommended by the insert maker (see [[feeds-speeds]]).

## Checklist

- [ ] Centre height checked
- [ ] Minimal overhang; boring bar clamped over at least 3 × its diameter
- [ ] Depth of cut larger than the nose radius
- [ ] Wiper insert considered for finishing
- [ ] Coolant aimed at the cutting zone when finishing

## Common mistakes

- Reducing depth of cut to “calm” chatter: too light a cut makes the insert rub and chatter more.
- Picking a large nose radius for long boring.
- Ignoring wear: a worn edge changes the finish before it breaks.
- Fixing finish by lowering speed when built-up edge actually calls for more speed.

## FAQ

### Why does it chatter mostly when boring?
The boring bar is overhung. The further it sticks out, the more it deflects. Reduce overhang and use a carbide or damped bar for long reaches.

### Wipers everywhere?
They are designed mainly for straight turning and facing. On complex profiles the effect is smaller.

### What roughness should I aim for?
Whatever the drawing says. See [[tolerances]] to link roughness and process.

## For Michaël to review

- Inserts and grades that work on our lathes, by material.
- Maximum practical boring-bar reach.

## Sources

- [Sandvik Coromant — Troubleshooting in turning](https://www.sandvik.coromant.com/en-us/knowledge/general-turning/troubleshooting-turning): causes and fixes for chatter and poor finish. Consulted November 26, 2026.
- [Sandvik Coromant — How to achieve good component quality in turning](https://www.sandvik.coromant.com/en-us/knowledge/general-turning/how-to-achieve-good-component-quality-in-turning): standard/wiper Ra table, depth > nose radius, bar clamping ≥ 3 × D.
