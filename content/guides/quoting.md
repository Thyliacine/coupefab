---
id: quoting
hub: shop
order: 20
nav: Soumission de pièces coupées | Quoting cut parts
kicker: Atelier · prix de revient | Shop · costing
level: intermediaire
schema: HowTo
prices: yes
tags: quoting, quote, costing, cost per part, machine hourly rate, cut length, pierce count, nesting utilization, material cost, setup, deburring, margin, laser, plasma
related: nesting, shop-rates-quebec, deburring, sheet-gauges
fr_slug: soumission-pieces-coupees
en_slug: quoting-cut-parts
fr_title: Soumissionner des pièces coupées au laser ou au plasma : méthode de calcul complète
en_title: Quoting laser and plasma cut parts: a complete costing method
fr_desc: Matière avec taux d’utilisation réel, temps de coupe (longueur + perçages), taux horaire machine, consommables, mise en course, ébavurage, pliage et marge : la méthode pas à pas avec une feuille de calcul type, sans chiffres inventés.
en_desc: Material with real nesting utilization, cut time (length + pierces), machine hourly rate, consumables, setup, deburring, bending and margin: the step-by-step method with a template worksheet, no made-up numbers.
---
=== fr
Un prix de pièce coupée n’est pas « le poids de la pièce fois le prix de l’acier ». Il additionne la **matière réellement consommée**, le **temps machine**, les **opérations secondaires** et la **mise en course**, puis une **marge**. Les logiciels de soumission spécialisés utilisent la même logique ; la voici à la main.

## La formule de base

**Coût par pièce = matière + temps de coupe × taux machine + consommables + (mise en course ÷ quantité) + secondaires**

| Bloc | Comment le calculer | D’où vient la donnée |
|---|---|---|
| Matière | Surface de la pièce ÷ **taux d’utilisation** de l’imbrication × épaisseur × densité × prix au poids | Imbrication réelle (voir [[nesting]]) ; densité et prix publiés dans le [[prix]] |
| Temps de coupe | Longueur de coupe ÷ vitesse **+** nombre de perçages × temps de perçage **+** déplacements rapides | Charte de coupe (voir [[cut-charts]]) ou estimation de la FAO |
| Taux machine | $/h incluant amortissement, énergie, gaz, entretien, opérateur, frais généraux | Vos propres chiffres (voir [[shop-rates-quebec]]) |
| Consommables | Coût par perçage ou par heure d’arc (plasma), buses et fenêtres (laser) | Vos relevés d’usure |
| Mise en course | Programmation, chargement de la tôle, réglage, première pièce | Temps réel mesuré |
| Secondaires | Ébavurage, pliage, taraudage, soudure, peinture, emballage | Temps standard par opération |

> [!TIP] Une pièce compte **un perçage par contour fermé** (contour extérieur + chaque trou). Une pièce avec 40 petits trous peut coûter plus cher en perçages qu’en longueur de coupe.

## Démarche pas à pas

1. **Lire le dessin** : matière, grade, épaisseur (calibre **et** décimale, voir [[sheet-gauges]]), quantité, tolérances, fini.
2. **Mesurer la géométrie** : longueur totale de coupe et nombre de contours (la FAO ou le logiciel d’imbrication les donne).
3. **Imbriquer** sur le format de tôle réel pour obtenir le taux d’utilisation et le nombre de pièces par tôle.
4. **Chiffrer la matière** : décider si la chute est facturée (souvent oui, en tout ou en partie) ; utiliser un **prix courant** du fournisseur.
5. **Chiffrer le temps** : vitesse de la charte pour l’épaisseur, temps de perçage, marge pour les ralentissements (coins, petits trous).
6. **Ajouter consommables, mise en course, secondaires.**
7. **Appliquer la marge** et vérifier le prix au marché.
8. **Écrire les hypothèses** sur la soumission (matière fournie ou non, tolérances, fini d’arête, délai, validité du prix matière).

## Feuille de calcul type (colonnes)

| Colonne | Exemple de contenu |
|---|---|
| Pièce / révision | P-1024 rév. B |
| Matière, grade, épaisseur | A36, 1/4 po |
| Quantité | 50 |
| Surface pièce | (de la FAO) |
| Taux d’utilisation | (de l’imbrication) |
| Longueur de coupe | (de la FAO) |
| Nombre de perçages | (de la FAO) |
| Temps de coupe calculé | formule |
| Taux machine | votre valeur |
| Coût matière | formule |
| Secondaires | minutes × taux |
| Mise en course répartie | minutes ÷ quantité |
| Prix unitaire, prix total | formule + marge |

## Liste de vérification avant d’envoyer

- [ ] Prix de la matière vérifié **cette semaine** (les prix publiés bougent ; voir le [[prix]])
- [ ] Format de tôle disponible chez le fournisseur
- [ ] Ébavurage et tolérances d’arête compris (voir [[deburring]])
- [ ] Quantité minimale ou frais de mise en course indiqués
- [ ] Validité de la soumission et conditions de transport

## Erreurs fréquentes

| Erreur | Effet |
|---|---|
| Matière au poids net de la pièce | Chute non payée, marge perdue |
| Ignorer les perçages | Pièces très perforées sous-évaluées |
| Utiliser la vitesse maximale de la charte | Temps sous-estimé ; la machine ralentit dans les détails |
| Oublier l’ébavurage | Temps de main-d’œuvre non facturé |
| Prix matière périmé | Perte quand le prix monte entre soumission et achat |

## FAQ

### Faut-il facturer la chute ?
C’est une décision commerciale ; beaucoup d’ateliers facturent la tôle entière pour les petites séries et un pourcentage d’utilisation pour les grandes. Écrivez-le dans la soumission.

### Comment obtenir mon taux horaire ?
En divisant tous les coûts annuels de la machine et de son opérateur par les heures réellement facturables ; voir [[shop-rates-quebec]].

## À valider en atelier (Michaël)

- Votre structure de soumission réelle (logiciel ou feuille Excel).
- Vos règles pour la chute et la mise en course minimale.

## Sources

- [Quotation Factory — How to quote a laser cutting job](https://www.quotationfactory.com/en/blog/how-to-quote-a-laser-cutting-job), consulté le 26 novembre 2026.
- [Quotometry — How to price laser cutting: cut length, pierces, material and sheet use](https://quotometry.com/learn/laser-cutting-cost/), consulté le 26 novembre 2026.
- [Hypertherm — Powermax cut charts (vitesses de référence)](https://xnet.hypertherm.com/Xnet/library/download/?file=HYP254756), consulté le 26 novembre 2026.
=== en
A cut part price isn’t “part weight times the price of steel”. It adds up the **material actually consumed**, **machine time**, **secondary operations** and **setup**, then a **margin**. Specialized quoting software uses the same logic; here it is by hand.

## The basic formula

**Cost per part = material + cut time × machine rate + consumables + (setup ÷ quantity) + secondaries**

| Block | How to calculate it | Where the data comes from |
|---|---|---|
| Material | Part area ÷ nesting **utilization** × thickness × density × price per weight | Real nest (see [[nesting]]); density and published prices in the [[prix]] |
| Cut time | Cut length ÷ speed **+** pierce count × pierce time **+** rapid moves | Cut chart (see [[cut-charts]]) or CAM estimate |
| Machine rate | $/h including depreciation, power, gas, maintenance, operator, overhead | Your own figures (see [[shop-rates-quebec]]) |
| Consumables | Cost per pierce or per arc-hour (plasma), nozzles and windows (laser) | Your wear records |
| Setup | Programming, loading the sheet, adjustment, first article | Measured actual time |
| Secondaries | Deburring, bending, tapping, welding, paint, packing | Standard time per operation |

> [!TIP] A part has **one pierce per closed contour** (outer profile + each hole). A part with 40 small holes can cost more in pierces than in cut length.

## Step by step

1. **Read the drawing**: material, grade, thickness (gauge **and** decimal, see [[sheet-gauges]]), quantity, tolerances, finish.
2. **Measure the geometry**: total cut length and contour count (CAM or nesting software provides them).
3. **Nest** on the real sheet size to get utilization and parts per sheet.
4. **Price material**: decide whether scrap is billed (often yes, fully or partly); use a **current** supplier price.
5. **Price time**: chart speed for the thickness, pierce time, allowance for slowdowns (corners, small holes).
6. **Add consumables, setup, secondaries.**
7. **Apply margin** and sanity-check against the market.
8. **Write assumptions** on the quote (material supplied or not, tolerances, edge finish, lead time, material price validity).

## Template worksheet (columns)

| Column | Example content |
|---|---|
| Part / revision | P-1024 rev. B |
| Material, grade, thickness | A36, 1/4 in |
| Quantity | 50 |
| Part area | (from CAM) |
| Utilization | (from nest) |
| Cut length | (from CAM) |
| Pierce count | (from CAM) |
| Calculated cut time | formula |
| Machine rate | your value |
| Material cost | formula |
| Secondaries | minutes × rate |
| Setup per part | minutes ÷ quantity |
| Unit price, total price | formula + margin |

## Checklist before sending

- [ ] Material price checked **this week** (published prices move; see the [[prix]])
- [ ] Sheet size available from the supplier
- [ ] Deburring and edge requirements included (see [[deburring]])
- [ ] Minimum quantity or setup charge stated
- [ ] Quote validity and shipping terms

## Common mistakes

| Mistake | Effect |
|---|---|
| Material at net part weight | Scrap unpaid, margin lost |
| Ignoring pierces | Heavily perforated parts underpriced |
| Using the chart’s maximum speed | Time underestimated; the machine slows in details |
| Forgetting deburring | Unbilled labour |
| Stale material price | Loss when price rises between quote and purchase |

## FAQ

### Should scrap be billed?
It’s a business decision; many shops bill the full sheet for small runs and a utilization percentage for large ones. Put it in the quote.

### How do I get my hourly rate?
Divide all annual costs of the machine and its operator by truly billable hours; see [[shop-rates-quebec]].

## For Michaël to review

- Your actual quoting structure (software or Excel sheet).
- Your rules for scrap and minimum setup.

## Sources

- [Quotation Factory — How to quote a laser cutting job](https://www.quotationfactory.com/en/blog/how-to-quote-a-laser-cutting-job), consulted November 26, 2026.
- [Quotometry — How to price laser cutting: cut length, pierces, material and sheet use](https://quotometry.com/learn/laser-cutting-cost/), consulted November 26, 2026.
- [Hypertherm — Powermax cut charts (reference speeds)](https://xnet.hypertherm.com/Xnet/library/download/?file=HYP254756), consulted November 26, 2026.
