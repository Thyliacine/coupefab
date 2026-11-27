---
id: sheet-gauges
hub: materials
order: 5
nav: Calibres de tôle (jauges) | Sheet metal gauges
kicker: Matériaux · référence | Materials · reference
level: debutant
schema: Article
prices: yes
tags: gauge, calibre, jauge, sheet metal, manufacturers standard gauge, galvanized, stainless, aluminum, brown and sharpe, thickness, 10ga, 11ga, 14ga, 16ga, 18ga
related: materials-grades, mild-steel, stainless-steel, aluminum
fr_slug: calibres-tole-jauges
en_slug: sheet-metal-gauge-chart
fr_title: Calibres de tôle (jauges) : tableau acier, galvanisé, inox et aluminium en pouces et en mm
en_title: Sheet metal gauge chart: steel, galvanized, stainless and aluminum in inches and mm
fr_desc: Le même calibre n’a pas la même épaisseur selon la matière : 16 ga = 0,0598 po en acier, 0,0635 po en galvanisé, 0,0625 po en inox et 0,0508 po en aluminium. Tableau complet, pièges et conseils pour commander.
en_desc: The same gauge isn’t the same thickness across materials: 16 ga = 0.0598 in steel, 0.0635 in galvanized, 0.0625 in stainless and 0.0508 in aluminum. Full chart, pitfalls and ordering tips.
---
=== fr
Le **calibre** (*gauge*, « jauge ») est une vieille convention : plus le numéro est **grand**, plus la tôle est **mince**. Surtout, **chaque famille de matière a sa propre table**. C’est la première source d’erreur de commande et de soumission. Ce tableau est celui qu’utilise notre [[prix]] pour convertir les calibres publiés par les fournisseurs.

## Tableau des calibres courants

| Calibre | Acier au carbone (Manufacturers’ Standard Gauge) | Acier galvanisé | Inox | Aluminium (Brown & Sharpe) |
|---|---|---|---|---|
| 7 | 0,1793 po · 4,55 mm | — | 0,1875 po · 4,76 mm | 0,1443 po · 3,67 mm |
| 8 | 0,1644 po · 4,18 mm | 0,1681 po · 4,27 mm | 0,1719 po · 4,37 mm | 0,1285 po · 3,26 mm |
| 10 | 0,1345 po · 3,42 mm | 0,1382 po · 3,51 mm | 0,1406 po · 3,57 mm | 0,1019 po · 2,59 mm |
| 11 | 0,1196 po · 3,04 mm | 0,1233 po · 3,13 mm | 0,1250 po · 3,18 mm | 0,0907 po · 2,30 mm |
| 12 | 0,1046 po · 2,66 mm | 0,1084 po · 2,75 mm | 0,1094 po · 2,78 mm | 0,0808 po · 2,05 mm |
| 13 | 0,0897 po · 2,28 mm | 0,0934 po · 2,37 mm | 0,0938 po · 2,38 mm | 0,0720 po · 1,83 mm |
| 14 | 0,0747 po · 1,90 mm | 0,0785 po · 1,99 mm | 0,0781 po · 1,98 mm | 0,0641 po · 1,63 mm |
| 16 | 0,0598 po · 1,52 mm | 0,0635 po · 1,61 mm | 0,0625 po · 1,59 mm | 0,0508 po · 1,29 mm |
| 18 | 0,0478 po · 1,21 mm | 0,0516 po · 1,31 mm | 0,0500 po · 1,27 mm | 0,0403 po · 1,02 mm |
| 20 | 0,0359 po · 0,91 mm | 0,0396 po · 1,01 mm | 0,0375 po · 0,95 mm | 0,0320 po · 0,81 mm |
| 22 | 0,0299 po · 0,76 mm | 0,0336 po · 0,85 mm | 0,0313 po · 0,80 mm | 0,0253 po · 0,64 mm |
| 24 | 0,0239 po · 0,61 mm | 0,0276 po · 0,70 mm | 0,0250 po · 0,64 mm | 0,0201 po · 0,51 mm |
| 26 | 0,0179 po · 0,45 mm | 0,0217 po · 0,55 mm | 0,0188 po · 0,48 mm | 0,0159 po · 0,40 mm |

Valeurs nominales. Les conversions en mm sont arrondies au centième.

## À retenir

- **Galvanisé** : épaisseur de l’acier plus le revêtement de zinc, d’où des valeurs légèrement supérieures à l’acier noir.
- **Aluminium** : table Brown & Sharpe (la même que les fils AWG) ; beaucoup de fournisseurs vendent plutôt l’aluminium en **décimales** (0,040, 0,063, 0,080, 0,125 po).
- **Tolérance** : l’épaisseur réelle varie autour de la valeur nominale selon la norme du produit (ASTM A1008/A1011 pour l’acier, etc.) ; pour une pièce critique, mesurez au micromètre.
- **Au-delà d’environ 3/16 po**, on parle de **plaque** et on commande en fraction ou en décimale, plus en calibre.

## Commander sans se tromper

- [ ] Toujours écrire **calibre + décimale** sur le bon de commande (« 14 ga (0,0747 po) A1011 »)
- [ ] Préciser la matière et le grade (laminé à chaud décapé, laminé à froid, galvanisé G90, 304 2B…)
- [ ] Vérifier l’épaisseur à la réception (micromètre ou pied à coulisse)
- [ ] Utiliser la **même épaisseur réelle** dans la FAO (K-factor, kerf) — voir [[bend-allowance]]

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Appliquer la table acier à l’aluminium | 14 ga alu commandé à 0,0747 po au lieu de 0,0641 po |
| Confondre calibre de tôle et calibre de fil | Épaisseurs différentes |
| Calcul de poids avec la mauvaise épaisseur | Soumission fausse ; utilisez le calculateur du [[prix]] |
| Pliage calculé sur l’épaisseur nominale d’une tôle hors tolérance | Cotes pliées hors tolérance |

## FAQ

### Pourquoi le 11 ga inox fait-il 1/8 po ?
La table inox est basée sur des fractions rondes pour certains calibres (11 ga = 0,1250 po), alors que la table acier au carbone dérive historiquement du poids au pied carré.

### Comment comparer des prix publiés en calibres différents ?
Ramenez tout au **prix par livre** ou par pied carré à épaisseur réelle : c’est ce que fait le [[prix]].

## À valider en atelier (Michaël)

- Les calibres que vous stockez réellement et vos épaisseurs mesurées à la réception.

## Sources

- [Allied Titanium — Standard Sheet Metal Gauges (PDF)](https://www.alliedtitanium.com/technical/gauges/Standard_Sheet_Metal_Gauges.pdf), consulté le 26 novembre 2026.
- [Continental Steel — Gauge and weight chart (PDF)](https://www.continentalsteel.com/wp-content/uploads/continental-steel-gauge-and-weight-chart-tabloid-1.pdf), consulté le 26 novembre 2026.
- [Noramark — Sheet metal gauge thickness chart](https://www.noramark.com/resources/charts/sheet-metal-gauge-chart/), consulté le 26 novembre 2026.
=== en
**Gauge** is an old convention: the **bigger** the number, the **thinner** the sheet. Most importantly, **each material family has its own table**. That is the number one source of ordering and quoting errors. This is the table our [[prix]] uses to convert gauges published by suppliers.

## Common gauge chart

| Gauge | Carbon steel (Manufacturers’ Standard Gauge) | Galvanized steel | Stainless | Aluminum (Brown & Sharpe) |
|---|---|---|---|---|
| 7 | 0.1793 in · 4.55 mm | — | 0.1875 in · 4.76 mm | 0.1443 in · 3.67 mm |
| 8 | 0.1644 in · 4.18 mm | 0.1681 in · 4.27 mm | 0.1719 in · 4.37 mm | 0.1285 in · 3.26 mm |
| 10 | 0.1345 in · 3.42 mm | 0.1382 in · 3.51 mm | 0.1406 in · 3.57 mm | 0.1019 in · 2.59 mm |
| 11 | 0.1196 in · 3.04 mm | 0.1233 in · 3.13 mm | 0.1250 in · 3.18 mm | 0.0907 in · 2.30 mm |
| 12 | 0.1046 in · 2.66 mm | 0.1084 in · 2.75 mm | 0.1094 in · 2.78 mm | 0.0808 in · 2.05 mm |
| 13 | 0.0897 in · 2.28 mm | 0.0934 in · 2.37 mm | 0.0938 in · 2.38 mm | 0.0720 in · 1.83 mm |
| 14 | 0.0747 in · 1.90 mm | 0.0785 in · 1.99 mm | 0.0781 in · 1.98 mm | 0.0641 in · 1.63 mm |
| 16 | 0.0598 in · 1.52 mm | 0.0635 in · 1.61 mm | 0.0625 in · 1.59 mm | 0.0508 in · 1.29 mm |
| 18 | 0.0478 in · 1.21 mm | 0.0516 in · 1.31 mm | 0.0500 in · 1.27 mm | 0.0403 in · 1.02 mm |
| 20 | 0.0359 in · 0.91 mm | 0.0396 in · 1.01 mm | 0.0375 in · 0.95 mm | 0.0320 in · 0.81 mm |
| 22 | 0.0299 in · 0.76 mm | 0.0336 in · 0.85 mm | 0.0313 in · 0.80 mm | 0.0253 in · 0.64 mm |
| 24 | 0.0239 in · 0.61 mm | 0.0276 in · 0.70 mm | 0.0250 in · 0.64 mm | 0.0201 in · 0.51 mm |
| 26 | 0.0179 in · 0.45 mm | 0.0217 in · 0.55 mm | 0.0188 in · 0.48 mm | 0.0159 in · 0.40 mm |

Nominal values. Millimetre conversions rounded to two decimals.

## Remember

- **Galvanized**: steel thickness plus the zinc coating, hence values slightly above black steel.
- **Aluminum**: Brown & Sharpe table (the same as AWG wire); many suppliers sell aluminum in **decimals** instead (0.040, 0.063, 0.080, 0.125 in).
- **Tolerance**: actual thickness varies around nominal per the product standard (ASTM A1008/A1011 for steel, etc.); for a critical part, measure with a micrometer.
- **Beyond about 3/16 in**, it’s **plate** and is ordered by fraction or decimal, not gauge.

## Ordering without mistakes

- [ ] Always write **gauge + decimal** on the PO (“14 ga (0.0747 in) A1011”)
- [ ] Specify material and grade (hot-rolled pickled, cold-rolled, G90 galvanized, 304 2B…)
- [ ] Check thickness on receipt (micrometer or caliper)
- [ ] Use the **same actual thickness** in CAM (K-factor, kerf) — see [[bend-allowance]]

## Common mistakes

| Mistake | Consequence |
|---|---|
| Using the steel table for aluminum | 14 ga aluminum ordered at 0.0747 in instead of 0.0641 in |
| Confusing sheet gauge with wire gauge | Different thicknesses |
| Weight calculated from the wrong thickness | Wrong quote; use the calculator in the [[prix]] |
| Bends calculated on nominal thickness of an off-tolerance sheet | Bent dimensions out of tolerance |

## FAQ

### Why is 11 ga stainless exactly 1/8 in?
The stainless table uses round fractions for some gauges (11 ga = 0.1250 in), while the carbon steel table historically derives from weight per square foot.

### How do I compare prices published in different gauges?
Bring everything back to **price per pound** or per square foot at actual thickness: that’s what the [[prix]] does.

## For Michaël to review

- The gauges you actually stock and your measured thicknesses on receipt.

## Sources

- [Allied Titanium — Standard Sheet Metal Gauges (PDF)](https://www.alliedtitanium.com/technical/gauges/Standard_Sheet_Metal_Gauges.pdf), consulted November 26, 2026.
- [Continental Steel — Gauge and weight chart (PDF)](https://www.continentalsteel.com/wp-content/uploads/continental-steel-gauge-and-weight-chart-tabloid-1.pdf), consulted November 26, 2026.
- [Noramark — Sheet metal gauge thickness chart](https://www.noramark.com/resources/charts/sheet-metal-gauge-chart/), consulted November 26, 2026.
