---
id: measuring-inspection
hub: shop
order: 48
nav: Mesure et contrôle | Measuring and inspection
kicker: Atelier · métrologie | Shop · inspection
level: debutant
schema: HowTo
tags: measuring, mesure, inspection, contrôle, métrologie, caliper, pied à coulisse, micrometer, micromètre, abbe, parallax, parallaxe, thermal expansion, dilatation, first article, première pièce, gauge, jauge
related: tolerances, probing, fixturing, lathe-finish-chatter
fr_slug: mesure-controle-pied-a-coulisse-micrometre
en_slug: measuring-inspection-caliper-micrometer
fr_title: Mesure et contrôle en atelier : pied à coulisse, micromètre et erreurs à éviter
en_title: Shop measuring and inspection: calipers, micrometers and the errors to avoid
fr_desc: Choisir l’instrument selon la tolérance, comprendre le principe d’Abbe, éviter les erreurs de force, de parallaxe et de température, et organiser le contrôle de première pièce.
en_desc: Choosing the instrument for the tolerance, understanding Abbe’s principle, avoiding force, parallax and temperature errors, and organizing first-article inspection.
---
=== fr
Une pièce n’est bonne que si on peut le **prouver par la mesure**. Le pied à coulisse est pratique, mais il n’est pas l’instrument de toutes les tolérances. Ce guide résume les règles de base, d’après le guide de Mitutoyo.

## Choisir l’instrument

| Instrument | Points forts | Limites |
|---|---|---|
| **Pied à coulisse** | Polyvalent : extérieur, intérieur, profondeur | Ne respecte pas le principe d’Abbe ; sensible à la force et au basculement du bec |
| **Micromètre** | Échelle dans l’axe de mesure (principe d’Abbe respecté), cliquet de force | Une plage par instrument |
| **Comparateur** | Écarts, faux-rond, alignement | Mesure relative |
| **Jauges entre / n’entre pas** | Rapide et sans interprétation en production | Pas de valeur chiffrée |

> [!NOTE] **Résolution ≠ précision.** Un affichage à 0,01 mm ne garantit pas une mesure juste à 0,01 mm ; tout dépend de l’instrument et de la façon de l’utiliser.

## Le principe d’Abbe

« La précision maximale est obtenue quand l’échelle et l’axe de mesure sont confondus. » Le micromètre respecte ce principe ; pas le pied à coulisse. Si le bec mobile bascule (force excessive, guide usé), l’erreur grandit avec la distance entre l’échelle et le point de contact.

Exemple de Mitutoyo : un basculement de 0,01 mm sur 50 mm, avec des becs de 40 mm, donne une erreur de **0,008 mm** au bout des becs.

## Les sources d’erreur au pied à coulisse

1. **Force de mesure** : pas de dispositif de force constante ; mesurer avec une force légère et régulière.
2. **Bout des becs** : mesurer le plus près possible de la règle, pas avec la pointe.
3. **Parallaxe** (vernier) : lire bien en face.
4. **Température** : écart entre l’instrument et la pièce, pièce chaude sortant de la machine.
5. **Petits alésages** : épaisseur des becs intérieurs ; enfoncer les becs au maximum.

## Contrôle de première pièce

- [ ] Instruments étalonnés et à zéro
- [ ] Pièce et instrument à la même température
- [ ] Cotes critiques mesurées avec l’instrument adapté (micromètre, jauge)
- [ ] Résultats notés avec le numéro de plan et la révision
- [ ] Correcteurs d’usure ajustés avant la série

## Erreurs fréquentes

- Valider une tolérance de ±0,01 mm au pied à coulisse.
- Mesurer une pièce chaude et la retrouver hors cote une fois refroidie.
- Serrer fort le pied à coulisse « pour être sûr ».

## FAQ

### Quand passer au micromètre ?
Quand la tolérance devient serrée par rapport à la précision du pied à coulisse ; une règle d’atelier courante est un instrument environ dix fois plus précis que la tolérance (à valider selon vos exigences qualité).

### Pourquoi mes mesures changent selon l’opérateur ?
Force de mesure, position sur les becs et lecture : standardisez la méthode et privilégiez les instruments à force constante.

## À valider en atelier (Michaël)

- Règle de choix d’instrument utilisée chez nous.
- Fréquence d’étalonnage des instruments.

## Sources

- [Mitutoyo — Quick Guide to Precision Measuring Instruments (PDF)](https://www2.mitutoyo.co.jp/eng/support/service/catalog/08/E11003.pdf) : principe d’Abbe, sources d’erreur du pied à coulisse, exemple de basculement. Consulté le 26 novembre 2026.
- [Mitutoyo — Calipers, quick guide (PDF)](https://www2.mitutoyo.co.jp/eng/products/menu/QuickGuide_Calipers.pdf) : résolution et précision, force de mesure.

=== en
A part is only good if you can **prove it by measurement**. Calipers are handy, but they are not the instrument for every tolerance. This guide sums up the basic rules, based on Mitutoyo’s guide.

## Choosing the instrument

| Instrument | Strengths | Limits |
|---|---|---|
| **Caliper** | Versatile: outside, inside, depth | Does not follow Abbe’s principle; sensitive to force and jaw tilt |
| **Micrometer** | Scale in line with the measurement (Abbe’s principle), ratchet for force | One range per instrument |
| **Dial indicator** | Deviation, runout, alignment | Relative measurement |
| **Go / no-go gauges** | Fast, no interpretation in production | No numeric value |

> [!NOTE] **Resolution ≠ accuracy.** A 0.01 mm display does not guarantee a measurement right to 0.01 mm; it depends on the instrument and how it is used.

## Abbe’s principle

“Maximum accuracy is obtained when the scale and the measurement axes are common.” A micrometer follows this principle; a caliper does not. If the moving jaw tilts (too much force, worn guide), the error grows with the distance between the scale and the contact point.

Mitutoyo’s example: a tilt of 0.01 mm over 50 mm, with 40 mm jaws, gives an error of **0.008 mm** at the jaw tips.

## Caliper error sources

1. **Measuring force**: no constant-force device; measure with a light, even force.
2. **Jaw tips**: measure as close to the beam as possible, not with the tips.
3. **Parallax** (vernier): read straight on.
4. **Temperature**: difference between instrument and part; hot parts straight off the machine.
5. **Small bores**: inside-jaw thickness; insert the jaws as deep as possible.

## First-article inspection

- [ ] Instruments calibrated and zeroed
- [ ] Part and instrument at the same temperature
- [ ] Critical sizes measured with the right instrument (micrometer, gauge)
- [ ] Results recorded with drawing number and revision
- [ ] Wear offsets adjusted before the run

## Common mistakes

- Accepting a ±0.01 mm tolerance with a caliper.
- Measuring a hot part and finding it out of tolerance once cool.
- Squeezing the caliper hard “to be sure”.

## FAQ

### When should I switch to a micrometer?
When the tolerance gets tight relative to the caliper’s accuracy; a common shop rule is an instrument about ten times more accurate than the tolerance (validate against your quality requirements).

### Why do my readings change with the operator?
Measuring force, position on the jaws and reading: standardize the method and favour constant-force instruments.

## For Michaël to review

- Instrument selection rule we use.
- Instrument calibration frequency.

## Sources

- [Mitutoyo — Quick Guide to Precision Measuring Instruments (PDF)](https://www2.mitutoyo.co.jp/eng/support/service/catalog/08/E11003.pdf): Abbe’s principle, caliper error sources, tilt example. Consulted November 26, 2026.
- [Mitutoyo — Calipers, quick guide (PDF)](https://www2.mitutoyo.co.jp/eng/products/menu/QuickGuide_Calipers.pdf): resolution and accuracy, measuring force.
