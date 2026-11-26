---
id: cnc-mill
hub: process
order: 5
nav: Fraiseuse CNC | CNC mill
kicker: Procédé · usinage | Process · machining
level: intermediaire
schema: HowTo
tags: mill, vmc, machining, workholding, vise, end mill, adaptive, mastercam, fusion, setup sheet
related: work-offsets, feeds-speeds, mastercam-2d, milling-troubleshooting
fr_slug: fraiseuse-cnc
en_slug: cnc-mill
fr_title: Fraiseuse CNC : de la feuille de réglage à la première pièce bonne
en_title: CNC mill: from setup sheet to the first good part
fr_desc: Le déroulé complet d’un premier programme sur centre d’usinage : FAO, feuille de réglage, montage dans l’étau, outils, origines, essai à blanc, première pièce et contrôle.
en_desc: The complete flow of a first program on a machining centre: CAM, setup sheet, vise setup, tools, offsets, dry run, first article and inspection.
---
=== fr
La fraiseuse CNC (ou centre d’usinage vertical) enlève la matière avec un outil rotatif, en 3 axes ou plus. La différence entre une première pièce bonne et une collision tient presque toujours à la **préparation** : feuille de réglage, outils mesurés, origines vérifiées, essai prudent.

## Le déroulé complet

1. **Analyser le dessin** : cotes critiques, tolérances, état de surface, matière. Voir [Tolérances](/guides/tolerances-cnc/).
2. **Choisir le montage** : étau, mors doux, montage dédié. La pièce doit être tenue fermement et l’outil ne doit jamais croiser le montage.
3. **Programmer dans le FAO** (Mastercam, Fusion, SolidWorks CAM…) : ébauche à engagement constant, finition, perçage, chanfreins. Voir [Mastercam 2D](/guides/mastercam-parcours-2d-dynamic/) et [Fusion](/guides/fusion-fao-debuter/).
4. **Simuler** avec le brut, le montage et le porte-outil réels.
5. **Post-traiter** avec le post de la machine ([Post-processeurs](/guides/post-processeurs/)).
6. **Imprimer la feuille de réglage** : origine, montage, liste d’outils avec longueur de sortie minimale, temps de cycle.
7. **Préparer les outils** : monter, mesurer les longueurs, entrer dans la table d’outils.
8. **Monter la pièce** et prendre l’origine ([Décalages d’origine](/guides/decalages-origine-g54/)).
9. **Essai à blanc** : Z relevé ou mode bloc à bloc, réduction des rapides et de l’avance.
10. **Première pièce** : main sur l’arrêt d’urgence, écoute, contrôle des cotes avant de lancer la série.

## Tenue de pièce : règles simples

- Serrer sur des faces parallèles ; sortir la pièce de l’étau le moins possible.
- Les mors doux usinés tiennent les pièces de forme et donnent une répétabilité.
- Une butée de position fixe rend les pièces suivantes identiques sans reprendre l’origine.

## Outils : l’essentiel

| Outil | Usage |
|---|---|
| Fraise carbure 2 à 3 goujures | Aluminium (grande évacuation) |
| Fraise carbure 4 goujures et plus | Aciers, inox |
| Foret à centrer / pointer | Positionner les trous |
| Foret, taraud, alésoir | Trous et filets |
| Fraise à chanfreiner | Ébavurage programmé |

Les vitesses et avances viennent du fabricant de l’outil ([Avances et vitesses](/guides/avances-vitesses/)).

## Liste de vérification avant le cycle

- [ ] Programme simulé avec montage et porte-outils
- [ ] Outils mesurés, numéros `T` et `H` cohérents
- [ ] Origine réglée dans le bon décalage
- [ ] Arrosage dirigé, copeaux évacués
- [ ] Rapides et avance réduits pour le premier passage

## Erreurs fréquentes

- Longueur de sortie d’outil insuffisante : le porte-outil touche la pièce.
- Mauvais décalage ou correcteur de longueur — voir [Décalages](/guides/decalages-origine-g54/).
- Évacuation des copeaux négligée en poche profonde : recoupe, casse. Voir [Dépannage usinage](/guides/depannage-usinage-broutage/).

## FAQ

### 3 axes, 3+2 ou 5 axes ?
La plupart des pièces se font en 3 axes avec plusieurs montages. Le 3+2 (positionnement) réduit les montages ; le 5 axes continu sert aux formes complexes.

## Sources

- [LinuxCNC — Coordinate systems](https://linuxcnc.org/docs/stable/html/gcode/coordinates.html), consulté le 26 novembre 2026.
- [Sandvik Coromant — Milling formulas](https://www.sandvik.coromant.com/en-us/knowledge/machining-formulas-definitions/milling-formulas-definitions).
=== en
A CNC mill (or vertical machining centre) removes material with a rotating tool, in 3 or more axes. The difference between a good first part and a crash almost always comes down to **preparation**: setup sheet, measured tools, verified offsets, cautious prove-out.

## The complete flow

1. **Read the drawing**: critical dimensions, tolerances, finish, material. See [Tolerances](/en/guides/cnc-tolerances/).
2. **Choose workholding**: vise, soft jaws, dedicated fixture. The part must be held firmly and the tool must never cross the fixture.
3. **Program in CAM** (Mastercam, Fusion, SolidWorks CAM…): constant-engagement roughing, finishing, drilling, chamfers. See [Mastercam 2D](/en/guides/mastercam-2d-toolpaths-dynamic-milling/) and [Fusion](/en/guides/fusion-cam-getting-started/).
4. **Simulate** with the real stock, fixture and holder.
5. **Post** with the machine’s post ([Post processors](/en/guides/post-processors/)).
6. **Print the setup sheet**: zero, fixture, tool list with minimum stick-out, cycle time.
7. **Prepare tools**: assemble, measure lengths, enter in the tool table.
8. **Mount the part** and set zero ([Work offsets](/en/guides/work-offsets-g54/)).
9. **Dry run**: Z raised or single block, rapids and feed reduced.
10. **First article**: hand on the E-stop, listen, inspect dimensions before running the batch.

## Workholding: simple rules

- Clamp on parallel faces; keep the part as low in the vise as possible.
- Machined soft jaws hold shaped parts and give repeatability.
- A fixed stop makes following parts identical without re-picking zero.

## Tools: the essentials

| Tool | Use |
|---|---|
| 2–3 flute carbide end mill | Aluminum (big chip room) |
| 4+ flute carbide end mill | Steels, stainless |
| Spot drill | Locate holes |
| Drill, tap, reamer | Holes and threads |
| Chamfer mill | Programmed deburring |

Speeds and feeds come from the tool maker ([Feeds and speeds](/en/guides/feeds-and-speeds/)).

## Pre-cycle checklist

- [ ] Program simulated with fixture and holders
- [ ] Tools measured, `T` and `H` numbers consistent
- [ ] Zero set in the right offset
- [ ] Coolant aimed, chips evacuated
- [ ] Rapids and feed reduced for the first pass

## Common mistakes

- Not enough tool stick-out: the holder hits the part.
- Wrong offset or length comp — see [Work offsets](/en/guides/work-offsets-g54/).
- Neglected chip evacuation in a deep pocket: recutting, breakage. See [Milling troubleshooting](/en/guides/milling-troubleshooting-chatter/).

## FAQ

### 3-axis, 3+2 or 5-axis?
Most parts are made in 3 axes with several setups. 3+2 (positioning) reduces setups; continuous 5-axis is for complex shapes.

## Sources

- [LinuxCNC — Coordinate systems](https://linuxcnc.org/docs/stable/html/gcode/coordinates.html), consulted November 26, 2026.
- [Sandvik Coromant — Milling formulas](https://www.sandvik.coromant.com/en-us/knowledge/machining-formulas-definitions/milling-formulas-definitions).
