---
id: shop-rates-quebec
hub: shop
order: 22
nav: Taux horaire d’atelier (Québec) | Shop hourly rates (Quebec)
kicker: Atelier · prix de revient | Shop · costing
level: intermediaire
schema: HowTo
tags: shop rate, hourly rate, machine rate, burden rate, overhead, quebec, salaire machiniste, cnp 72100, guichet-emplois, depreciation, utilization, billable hours
related: quoting, careers-quebec, buying-cnc-canada, tool-life
fr_slug: taux-horaire-atelier-quebec
en_slug: shop-hourly-rate-quebec
fr_title: Calculer son taux horaire d’atelier au Québec (machine + main-d’œuvre), avec des sources honnêtes
en_title: Calculating your shop hourly rate in Quebec (machine + labour), with honest sourcing
fr_desc: Méthode pour bâtir un taux horaire machine et main-d’œuvre : salaires publiés par Guichet-Emplois (CNP 72100), charges sociales, amortissement, énergie, entretien, frais généraux et heures réellement facturables. Pourquoi aucun « taux du marché » publié n’est fiable.
en_desc: A method to build a machine and labour hourly rate: wages published by Job Bank (NOC 72100), payroll burden, depreciation, power, maintenance, overhead and truly billable hours. Why no published “market rate” is reliable.
---
=== fr
« Quel est le taux horaire normal d’un atelier d’usinage ou de découpe au Québec ? » Réponse honnête : **il n’existe pas de source publique fiable** des taux facturés par les ateliers québécois. Les chiffres qui circulent viennent de sondages privés, de forums ou d’autres marchés. Ce qui est public et fiable, ce sont les **salaires** ; le reste, vous devez le calculer avec **vos** coûts. Voici la méthode.

## Ce que disent les données publiques (salaires)

Guichet-Emplois (gouvernement du Canada) publie les salaires de la profession **CNP 72100 – Machinistes et vérificateurs d’usinage et d’outillage**. Pour la province de Québec, la page mise à jour le 18 novembre 2026 indique (période de référence 2024-2025, Enquête sur la population active de Statistique Canada) :

| Niveau | Salaire horaire |
|---|---|
| Bas | 23,00 $ |
| **Médian** | **31,41 $** |
| Haut | 40,00 $ |

Les valeurs régionales varient (par exemple 30,93 $ en Capitale-Nationale, 29,78 $ à Montréal, 31,81 $ en Montérégie, selon la même page). Ce sont des **salaires**, pas des taux facturés : il faut y ajouter charges, machine et frais généraux.

## La méthode en 5 blocs

| Bloc | Contenu | Comment l’estimer |
|---|---|---|
| 1. Main-d’œuvre chargée | Salaire + charges de l’employeur (RRQ, AE, RQAP, FSS, CNESST, CNT) + avantages + vacances/fériés | Salaire × (1 + taux de charges réel de votre paie) |
| 2. Machine | Amortissement (prix ÷ durée d’utilisation prévue) ou paiements de financement, intérêts | Prix réel, durée réaliste |
| 3. Exploitation | Électricité, gaz (plasma/laser/oxycoupage), air comprimé, entretien, consommables non facturés | Factures des 12 derniers mois |
| 4. Frais généraux | Loyer, assurances, logiciels (FAO, licences), administration, vente, véhicules | Budget annuel réparti sur les machines |
| 5. Heures facturables | Heures payées × **taux d’utilisation réel** (pas 100 %) | Feuilles de temps : heures réellement facturées |

**Taux horaire (coût) = (main-d’œuvre chargée annuelle + coûts machine annuels + exploitation + part des frais généraux) ÷ heures facturables annuelles**

Puis : **taux facturé = taux coût + marge** visée.

## Exemple de feuille (sans chiffres inventés)

| Ligne | Votre valeur |
|---|---|
| Salaire horaire de l’opérateur | (votre paie ; repère public : médiane CNP 72100) |
| Heures payées par an | (convention, horaire) |
| Taux de charges et avantages | (votre comptable) |
| Prix de la machine et durée d’amortissement | (facture, politique comptable) |
| Électricité et gaz par an | (factures Hydro-Québec, fournisseur de gaz) |
| Entretien et consommables par an | (registre) |
| Frais généraux attribués | (budget) |
| Taux d’utilisation | (heures facturées ÷ heures payées) |

> [!TIP] L’erreur la plus coûteuse est de diviser par **toutes** les heures payées. Mise en course, attente de matière, entretien, formation et soumissions ne sont pas facturables : un taux d’utilisation réaliste se mesure, il ne se suppose pas.

## Taux par machine ou taux unique ?

- **Taux par machine** : un laser fibre récent et une petite fraiseuse n’ont pas le même coût ; un taux par machine évite que l’une subventionne l’autre.
- **Taux unique** : plus simple, acceptable si les équipements sont comparables.
- Dans les deux cas, chiffrez séparément les **opérations secondaires** (ébavurage, pliage, soudage) ; voir [[quoting]].

## Liste de vérification annuelle

- [ ] Salaires et charges mis à jour (hausses, nouvelles cotisations)
- [ ] Factures d’énergie et de gaz des 12 derniers mois
- [ ] Taux d’utilisation mesuré sur les feuilles de temps
- [ ] Amortissements et financements à jour
- [ ] Comparaison du taux avec les soumissions gagnées/perdues

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Copier un « taux du marché » trouvé en ligne | Taux sans lien avec vos coûts |
| Oublier les charges sociales | Main-d’œuvre sous-évaluée |
| Utilisation supposée à 100 % | Taux trop bas, marge invisible |
| Même taux pour toutes les machines | Laser sous-facturé, petite machine sur-facturée |

## FAQ

### Où trouver les taux de cotisation à jour ?
Revenu Québec (RRQ, FSS, CNT, RQAP), la CNESST (taux de prime selon l’unité de classification) et l’ARC (AE) publient les taux annuels ; votre comptable les applique à votre paie.

### Les salaires de Guichet-Emplois sont-ils représentatifs de mon atelier ?
Ce sont des données d’enquête par profession et par région : un bon repère, pas un barème. Un programmeur CNC ou un opérateur laser expérimenté peut se situer ailleurs dans la fourchette.

## À valider en atelier (Michaël)

- Votre structure de taux réelle (par machine ou unique) et vos taux d’utilisation mesurés.

## Sources

- [Guichet-Emplois — Salaires, machinistes et vérificateurs d’usinage et d’outillage (CNP 72100), Québec](https://www.guichetemplois.gc.ca/rapportmarche/salaire-profession/16851/QC), consulté le 26 novembre 2026.
- [Gouvernement du Québec — Machinistes et vérificateurs d’usinage et d’outillage (CNP 72100)](https://www.quebec.ca/emploi/informer-metier-profession/explorer-metiers-professions/72100-machinistes-et-verificateurs-verificatrices-dusinage-et-doutillage), consulté le 26 novembre 2026.
- [Revenu Québec — Retenues et cotisations de l’employeur](https://www.revenuquebec.ca/fr/entreprises/retenues-et-cotisations/), consulté le 26 novembre 2026.
=== en
“What’s a normal hourly rate for a machining or cutting shop in Quebec?” Honest answer: **there is no reliable public source** of rates billed by Quebec shops. Figures that circulate come from private surveys, forums or other markets. What is public and reliable is **wages**; the rest you must calculate from **your** costs. Here’s the method.

## What public data says (wages)

Job Bank (Government of Canada) publishes wages for **NOC 72100 – Machinists and machining and tooling inspectors**. For the province of Quebec, the page updated November 18, 2026 shows (reference period 2024-2025, Statistics Canada Labour Force Survey):

| Level | Hourly wage |
|---|---|
| Low | $23.00 |
| **Median** | **$31.41** |
| High | $40.00 |

Regional values vary (for example $30.93 in Capitale-Nationale, $29.78 in Montréal, $31.81 in Montérégie, per the same page). These are **wages**, not billed rates: payroll burden, machine and overhead must be added.

## The 5-block method

| Block | Content | How to estimate it |
|---|---|---|
| 1. Burdened labour | Wage + employer contributions (QPP, EI, QPIP, HSF, CNESST, CNT) + benefits + vacation/holidays | Wage × (1 + your payroll’s real burden rate) |
| 2. Machine | Depreciation (price ÷ expected service life) or financing payments, interest | Real price, realistic life |
| 3. Operating | Electricity, gas (plasma/laser/oxyfuel), compressed air, maintenance, unbilled consumables | Last 12 months of invoices |
| 4. Overhead | Rent, insurance, software (CAM, licences), admin, sales, vehicles | Annual budget allocated to machines |
| 5. Billable hours | Paid hours × **real utilization** (not 100%) | Timesheets: hours actually billed |

**Hourly cost rate = (annual burdened labour + annual machine cost + operating + overhead share) ÷ annual billable hours**

Then: **billed rate = cost rate + target margin**.

## Template worksheet (no made-up numbers)

| Line | Your value |
|---|---|
| Operator hourly wage | (your payroll; public benchmark: NOC 72100 median) |
| Paid hours per year | (agreement, schedule) |
| Burden and benefits rate | (your accountant) |
| Machine price and depreciation period | (invoice, accounting policy) |
| Electricity and gas per year | (Hydro-Québec, gas supplier invoices) |
| Maintenance and consumables per year | (log) |
| Allocated overhead | (budget) |
| Utilization | (hours billed ÷ hours paid) |

> [!TIP] The costliest mistake is dividing by **all** paid hours. Setup, waiting for material, maintenance, training and quoting aren’t billable: realistic utilization is measured, not assumed.

## Per-machine or single rate?

- **Per-machine rate**: a new fiber laser and a small mill don’t cost the same; a per-machine rate stops one subsidizing the other.
- **Single rate**: simpler, acceptable when equipment is comparable.
- Either way, price **secondary operations** separately (deburring, bending, welding); see [[quoting]].

## Annual checklist

- [ ] Wages and burden updated (raises, new contributions)
- [ ] Last 12 months of energy and gas invoices
- [ ] Utilization measured from timesheets
- [ ] Depreciation and financing up to date
- [ ] Rate compared with quotes won/lost

## Common mistakes

| Mistake | Consequence |
|---|---|
| Copying a “market rate” found online | Rate unrelated to your costs |
| Forgetting payroll burden | Labour underpriced |
| Assuming 100% utilization | Rate too low, invisible margin |
| Same rate for every machine | Laser underbilled, small machine overbilled |

## FAQ

### Where are current contribution rates?
Revenu Québec (QPP, HSF, CNT, QPIP), CNESST (premium rate by classification unit) and CRA (EI) publish annual rates; your accountant applies them to your payroll.

### Are Job Bank wages representative of my shop?
They’re survey data by occupation and region: a good benchmark, not a pay scale. An experienced CNC programmer or laser operator can sit elsewhere in the range.

## For Michaël to review

- Your real rate structure (per machine or single) and measured utilization.

## Sources

- [Job Bank — Wages, machinists and machining and tooling inspectors (NOC 72100), Quebec (French page)](https://www.guichetemplois.gc.ca/rapportmarche/salaire-profession/16851/QC), consulted November 26, 2026.
- [Government of Quebec — Machinists and machining and tooling inspectors (NOC 72100) (French)](https://www.quebec.ca/emploi/informer-metier-profession/explorer-metiers-professions/72100-machinistes-et-verificateurs-verificatrices-dusinage-et-doutillage), consulted November 26, 2026.
- [Revenu Québec — Source deductions and employer contributions (French)](https://www.revenuquebec.ca/fr/entreprises/retenues-et-cotisations/), consulted November 26, 2026.
