---
id: kerf
hub: fundamentals
order: 20
nav: Kerf et qualité de coupe | Kerf and cut quality
kicker: Fondamentaux · plasma | Fundamentals · plasma
level: debutant
schema: HowTo
tags: kerf, plasma, cut chart, hypertherm, quality, compensation
related: lead-ins-pierce, plasma-troubleshooting, sheetcam, plasma-cutting
prices: no
fr_slug: kerf-qualite-coupe
en_slug: kerf-and-cut-quality
fr_title: Kerf et qualité de coupe : lire une charte, mesurer, compenser
en_title: Kerf and cut quality: read a chart, measure, compensate
fr_desc: Ce qu’est le kerf, comment lire une charte de coupe de fabricant sans mélanger les manuels, et comment mesurer puis compenser le kerf réel de votre table.
en_desc: What kerf is, how to read a manufacturer cut chart without mixing manuals, and how to measure and compensate your table’s real kerf.
---
=== fr
Le **kerf** est la largeur de matière enlevée par le jet (plasma, laser, jet d’eau) ou par l’outil. Si le parcours ne le compense pas, les contours extérieurs sortent trop petits et les trous trop grands — d’environ un kerf au diamètre. La qualité de coupe (scories, biseau, fini) dépend de la vitesse, de la hauteur, de l’usure des consommables et de l’état de la table.

## Lire une charte de coupe

Hypertherm, dans ses chartes et dans « How to use the cut charts », présente les valeurs comme un **point de départ**. On y trouve typiquement :

| Colonne | Ce qu’elle veut dire |
|---|---|
| Épaisseur | Épaisseur de la tôle pour cette ligne |
| Hauteur de coupe (cut height) | Distance torche-tôle pendant la coupe |
| Hauteur et délai de perçage | Hauteur et temps d’attente au perçage |
| Meilleure qualité (best quality) | Vitesse et tension pour l’angle et le fini |
| Production | Plus rapide, pas forcément le meilleur fini |
| Kerf | Largeur de saignée de référence |

La tension d’arc monte à mesure que les consommables s’usent ; certaines commandes ajustent la hauteur automatiquement (THC). Hypertherm précise aussi que les largeurs de kerf publiées sont **de référence**, mesurées aux réglages « best quality », et que l’installation et la composition de la matière changent le résultat réel.

> [!WARN] **Ne mélangez pas les manuels.** Deux documents officiels pour la même famille de source peuvent donner des kerfs différents, parce que la torche, le jeu de consommables ou la révision du manuel diffèrent. Prenez la charte de *votre* source, *votre* torche et *vos* consommables.

## Un exemple cité — une charte, une configuration

Le tableau reprend les kerfs publiés dans la charte officielle [Mild steel — 125 A — air](https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/vkl1065237733940.html) du manuel de la torche de rattrapage Powermax125 (acier doux, air, 125 A, consommables blindés). Ce n’est **pas** une table universelle.

| Épaisseur | Kerf (best quality, selon cette charte) |
|---|--:|
| 6 mm (1/4 po) | 1,0 mm (0,040 po) |
| 10 mm (≈ 3/8 po) | 1,1 mm (0,042 po à 3/8 po) |
| 12 mm (1/2 po) | 1,3 mm (0,051 po) |
| 25 mm (1 po) | 2,6 mm (0,105 po) |
| 40 mm (≈ 1-1/2 po) | 3,2 mm (0,122 po à 1-1/2 po) |

À titre d’avertissement : le manuel d’opération Powermax125 808080 publie un tableau distinct de « compensation estimée de largeur de kerf » pour une configuration « 125 A shielded », par exemple 2,2 mm à 6 mm — un autre chiffre, dans un autre contexte documentaire.

## Mesurer le kerf réel de votre table

1. **Dessinez un coupon** : un carré de 50 mm (ou 2 po) avec un trou de 25 mm (1 po) au centre.
2. **Coupez-le sans compensation** (parcours sur la ligne), avec les réglages de la charte pour cette épaisseur.
3. **Mesurez au pied à coulisse** la largeur du carré et le diamètre du trou, sur la face supérieure.
4. **Calculez** : kerf ≈ (cote dessinée − cote mesurée du carré), ou (diamètre mesuré du trou − diamètre dessiné). Les deux doivent concorder à peu près.
5. **Saisissez ce kerf** dans l’outil du FAO (SheetCam : Tools → kerf width), puis recoupez le coupon **avec** compensation.
6. **Notez la valeur** avec l’épaisseur, l’ampérage, les consommables et la date. Refaites l’essai quand les consommables, l’air ou la nuance changent.

> [!TIP] Mesurez en haut et en bas de la coupe : l’écart vous donne le biseau. Un kerf plus large en haut qu’en bas indique souvent une torche trop haute ou une vitesse trop lente — voir [Dépannage plasma](/guides/depannage-plasma-scories-biseau/).

## Kerf et compensation dans le FAO ou la commande

Deux façons de compenser : le **FAO** décale le parcours d’un demi-kerf (le plus courant en plasma), ou la **commande** le fait avec G41/G42 et une valeur d’outil. N’activez jamais les deux en même temps. Voir [Référence G-code](/guides/reference-g-code-m-code/).

## Erreurs fréquentes

- Utiliser un kerf « standard » trouvé en ligne au lieu de la charte de votre torche.
- Mesurer un coupon coupé avec compensation pour calculer le kerf (on mesure alors l’erreur, pas le kerf).
- Garder la même valeur après un changement de consommables ou d’ampérage.
- Compenser dans le FAO **et** dans la commande.

## FAQ

### Le kerf change-t-il avec l’usure ?
Oui. La tension d’arc et le jet changent avec l’usure de la buse et de l’électrode ; la largeur de saignée suit. Remesurez périodiquement.

### Le kerf est-il le même pour les trous et les contours ?
La largeur du jet est la même, mais les petits trous plasma ont souvent un fini et un biseau différents. Les fabricants publient des recommandations pour les trous ; suivez celles de votre système.

## À valider en atelier (Michaël)

- Les sources et torches les plus courantes chez les ateliers visés, pour citer les bonnes chartes.
- Votre méthode réelle de mesure du kerf et de mise à jour dans SheetCam.
- Toute formulation trop générale sur les scories ou le biseau.

## Sources

- [Hypertherm — Mild steel, 125 A, air (torche de rattrapage Powermax125)](https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/vkl1065237733940.html), consulté le 26 novembre 2026.
- [Hypertherm — How to use the cut charts](https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/bzv0315406918125.html).
- Manuel d’opération Powermax125 808080 (tableau de compensation estimée de kerf, contexte distinct).
=== en
**Kerf** is the width of material removed by the jet (plasma, laser, waterjet) or the tool. If the toolpath does not compensate for it, outside profiles come out small and holes come out large — by about one kerf on the diameter. Cut quality (dross, bevel, finish) depends on speed, height, consumable wear and the state of the table.

## Reading a cut chart

Hypertherm, in its charts and in “How to use the cut charts,” presents the values as a **starting point**. You typically get:

| Column | Meaning |
|---|---|
| Thickness | Plate thickness for this row |
| Cut height | Torch-to-plate distance while cutting |
| Pierce height and delay | Height and dwell time at pierce |
| Best quality | Speed and voltage for angle and finish |
| Production | Faster, not necessarily the best finish |
| Kerf | Reference kerf width |

Arc voltage rises as consumables wear; some controls adjust height automatically (THC). Hypertherm also states published kerf widths are **for reference**, taken at Best Quality settings, and that installation and material composition change the real result.

> [!WARN] **Do not mix manuals.** Two official documents for the same source family can list different kerfs, because the torch, consumable set or manual revision differs. Use the chart for *your* source, *your* torch and *your* consumables.

## A cited example — one chart, one setup

The table copies kerfs published in the official [Mild steel — 125 A — air](https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/vkl1065237733940.html) chart from the Powermax125 retrofit-torch manual (mild steel, air, 125 A, shielded consumables). It is **not** a universal table.

| Thickness | Kerf (best quality, per this chart) |
|---|--:|
| 6 mm (1/4 in) | 1.0 mm (0.040 in) |
| 10 mm (≈ 3/8 in) | 1.1 mm (0.042 in at 3/8 in) |
| 12 mm (1/2 in) | 1.3 mm (0.051 in) |
| 25 mm (1 in) | 2.6 mm (0.105 in) |
| 40 mm (≈ 1-1/2 in) | 3.2 mm (0.122 in at 1-1/2 in) |

As a warning: Powermax125 Operator Manual 808080 publishes a separate “estimated kerf-width compensation” table for a “125 A shielded” setup, for example 2.2 mm at 6 mm — a different number in a different documentary context.

## Measuring your table’s real kerf

1. **Draw a coupon**: a 50 mm (or 2 in) square with a 25 mm (1 in) hole in the middle.
2. **Cut it without compensation** (path on the line), with the chart settings for that thickness.
3. **Measure with calipers** the square width and hole diameter, on the top face.
4. **Calculate**: kerf ≈ (drawn size − measured square size), or (measured hole − drawn hole). Both should roughly agree.
5. **Enter that kerf** in the CAM tool (SheetCam: Tools → kerf width), then recut the coupon **with** compensation.
6. **Record the value** with thickness, amperage, consumables and date. Redo the test when consumables, air or grade change.

> [!TIP] Measure top and bottom of the cut: the difference is your bevel. A kerf wider at the top than the bottom often means torch too high or speed too slow — see [Plasma troubleshooting](/en/guides/plasma-troubleshooting-dross-bevel/).

## Kerf compensation in CAM or in the control

Two ways to compensate: the **CAM** offsets the path by half a kerf (most common in plasma), or the **control** does it with G41/G42 and a tool value. Never enable both. See [G-code reference](/en/guides/g-code-m-code-reference/).

## Common mistakes

- Using a “standard” kerf found online instead of your torch’s chart.
- Measuring a coupon cut with compensation to compute kerf (you then measure the error, not the kerf).
- Keeping the same value after changing consumables or amperage.
- Compensating in CAM **and** in the control.

## FAQ

### Does kerf change with wear?
Yes. Arc voltage and jet shape change as nozzle and electrode wear; kerf width follows. Re-measure periodically.

### Is kerf the same for holes and outsides?
The jet width is the same, but small plasma holes often have a different finish and bevel. Manufacturers publish hole-cutting guidance; follow your system’s.

## For Michaël to review

- Which sources and torches are most common among the target shops, so we cite the right charts.
- Your real method for measuring kerf and updating SheetCam.
- Any wording on dross or bevel that is too sweeping.

## Sources

- [Hypertherm — Mild steel, 125 A, air (Powermax125 retrofit torch)](https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/vkl1065237733940.html), consulted November 26, 2026.
- [Hypertherm — How to use the cut charts](https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/bzv0315406918125.html).
- Powermax125 Operator Manual 808080 (estimated kerf-width compensation table, distinct context).
