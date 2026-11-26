---
id: inconel
hub: materials
order: 50
nav: Inconel 625 et 718 | Inconel 625 and 718
kicker: Matériaux · superalliages de nickel | Materials · nickel superalloys
level: avance
schema: Article
prices: yes
tags: inconel, 625, 718, nickel alloy, superalloy, hrsa, work hardening, aging, solution annealed, ceramic inserts, carbide, waterjet, laser, machining
related: ph-17-4, stainless-steel, tool-life, waterjet
fr_slug: inconel-625-718-usinage
en_slug: inconel-625-718-machining
fr_title: Inconel 625 et 718 : propriétés d’usage, usinage et découpe des superalliages de nickel
en_title: Inconel 625 and 718: what they’re for, machining and cutting nickel superalloys
fr_desc: Pourquoi l’Inconel est si difficile à usiner (écrouissage, chaleur, abrasion), différences entre 625 et 718 (durcissable par vieillissement), stratégie d’outils carbure et céramique, et découpe jet d’eau, laser ou plasma.
en_desc: Why Inconel is so hard to machine (work hardening, heat, abrasion), differences between 625 and 718 (age-hardenable), carbide and ceramic tooling strategy, and waterjet, laser or plasma cutting.
---
=== fr
« Inconel » est une marque (Special Metals) devenue nom commun pour les **superalliages à base de nickel**. Ils gardent leur résistance à haute température et résistent à la corrosion — exactement ce qui les rend difficiles à usiner : la chaleur reste dans l’outil, la matière **s’écrouit** et elle est abrasive.

## 625 vs 718

| Critère | Alliage 625 (UNS N06625) | Alliage 718 (UNS N07718) |
|---|---|---|
| Durcissement | Par solution solide (pas de vieillissement) | **Durcissable par vieillissement** (précipitation) |
| Points forts | Corrosion, soudabilité, fatigue | Très haute résistance mécanique jusqu’à haute température |
| Usages typiques | Chimie, marin, revêtements, soufflets | Aéronautique (disques, arbres, fixations), pétrole et gaz |
| Usinage | Difficile | Difficile ; encore plus après vieillissement |

## Stratégie d’usinage

- **718** : ébaucher et semi-finir à l’état **mis en solution**, vieillir, puis finir légèrement (Machining Doctor et les guides d’outilleurs recommandent d’éviter d’enlever beaucoup de matière à l’état vieilli).
- **Outils** : carbure revêtu, affûté, à coupe positive pour la finition et le 625 ; **céramiques** (rondes, entrée progressive) seulement pour l’ébauche en coupe continue sur machine rigide, selon le guide Sandvik Coromant des superalliages (HRSA).
- **Épaisseur de copeau minimale** : ne jamais « caresser » la matière ; une avance trop faible écrouit la surface et détruit l’outil suivant.
- **Pas d’arrêt en matière**, pas de reprise dans la couche écrouie.
- **Arrosage** abondant, haute pression si possible ; montage très rigide.
- Vitesses : nettement plus basses que pour l’inox, suivre la fiche de l’outil (voir [[feeds-speeds]]) et surveiller l’usure (voir [[tool-life]]).

## Découpe de tôle et de plaque

| Procédé | Remarques |
|---|---|
| Jet d’eau | Le plus sûr pour la qualité : aucune zone affectée thermiquement ; voir [[waterjet]] |
| Laser fibre | Courant en mince à l’azote selon la machine et la recette |
| Plasma | Possible (chartes « inox/alliages » selon la source), zone thermique et bord à reprendre |
| Scie / disque abrasif | Lent, usure élevée |

## Liste de vérification

- [ ] Alliage et état exacts (625 recuit ; 718 mis en solution ou vieilli, spécification AMS)
- [ ] Certificat matière et traçabilité (souvent exigés en aéronautique)
- [ ] Outils dédiés, neufs ou en bon état ; stratégie validée sur un essai
- [ ] Surépaisseur pour la finition après vieillissement (718)
- [ ] Prix vérifié : le nickel est cher et volatil (voir le [[prix]])

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Vitesses d’inox | Outil détruit en quelques secondes |
| Avance trop faible « pour être prudent » | Écrouissage, usure accélérée |
| Céramique en coupe interrompue | Écaillage de la plaquette |
| Ébaucher le 718 déjà vieilli | Temps de cycle et coût d’outils multipliés |

## FAQ

### L’Inconel est-il magnétique ?
Les alliages 625 et 718 sont essentiellement non magnétiques à température ambiante.

### Peut-on remplacer l’Inconel par de l’inox 316 ?
Pas sans avis du concepteur : à haute température ou en milieu très corrosif, le 316 n’offre pas les mêmes propriétés.

## À valider en atelier (Michaël)

- Vos expériences d’usinage d’Inconel (outils, vitesses, durée de vie) et vos fournisseurs.

## Sources

- [Sandvik Coromant — Heat resistant super alloys, application guide (PDF)](https://cdn.sandvik.coromant.com/files/sitecollectiondocuments/downloads/global/technical%20guides/en-gb/c-2920-034.pdf), consulté le 26 novembre 2026.
- [Machining Doctor — Machining Inconel: turning, milling and drilling guide](https://www.machiningdoctor.com/machining-materials/machining-inconel/), consulté le 26 novembre 2026.
- [American Machinist — Rx for high-nickel anxiety](https://www.americanmachinist.com/machining-cutting/article/21895460/rx-for-high-nickel-anxiety), consulté le 26 novembre 2026.
- [Special Metals — Inconel alloy 718 (fiche technique)](https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-718.pdf), consulté le 26 novembre 2026.
=== en
“Inconel” is a brand (Special Metals) that became the common name for **nickel-based superalloys**. They keep their strength at high temperature and resist corrosion — exactly what makes them hard to machine: heat stays in the tool, the material **work-hardens** and it’s abrasive.

## 625 vs 718

| Criterion | Alloy 625 (UNS N06625) | Alloy 718 (UNS N07718) |
|---|---|---|
| Hardening | Solid-solution strengthened (no aging) | **Age-hardenable** (precipitation) |
| Strengths | Corrosion, weldability, fatigue | Very high strength up to high temperature |
| Typical uses | Chemical, marine, cladding, bellows | Aerospace (discs, shafts, fasteners), oil and gas |
| Machining | Difficult | Difficult; even more so after aging |

## Machining strategy

- **718**: rough and semi-finish in the **solution-annealed** condition, age, then finish lightly (Machining Doctor and tooling guides recommend avoiding heavy stock removal in the aged condition).
- **Tools**: sharp, positive coated carbide for finishing and for 625; **ceramics** (round, gradual entry) only for roughing in continuous cuts on a rigid machine, per Sandvik Coromant’s heat-resistant superalloy (HRSA) guide.
- **Minimum chip thickness**: never “stroke” the material; too light a feed work-hardens the surface and ruins the next tool.
- **No dwelling** in the cut, no re-cutting the work-hardened layer.
- **Coolant** in volume, high pressure if possible; very rigid setup.
- Speeds: well below stainless; follow the tool’s data (see [[feeds-speeds]]) and track wear (see [[tool-life]]).

## Cutting sheet and plate

| Process | Notes |
|---|---|
| Waterjet | Safest for quality: no heat-affected zone; see [[waterjet]] |
| Fiber laser | Common on thin material with nitrogen, depending on machine and recipe |
| Plasma | Possible (“stainless/alloy” charts depending on the source), heat zone and edge to clean up |
| Saw / abrasive disc | Slow, high wear |

## Checklist

- [ ] Exact alloy and condition (625 annealed; 718 solution-treated or aged, AMS spec)
- [ ] Material certificate and traceability (often required in aerospace)
- [ ] Dedicated tools, new or in good condition; strategy proven on a test
- [ ] Allowance for finishing after aging (718)
- [ ] Price checked: nickel is expensive and volatile (see the [[prix]])

## Common mistakes

| Mistake | Consequence |
|---|---|
| Stainless speeds | Tool destroyed in seconds |
| Feed too light “to be safe” | Work hardening, accelerated wear |
| Ceramics in interrupted cuts | Insert chipping |
| Roughing 718 that’s already aged | Cycle time and tooling cost multiplied |

## FAQ

### Is Inconel magnetic?
Alloys 625 and 718 are essentially non-magnetic at room temperature.

### Can Inconel be replaced with 316 stainless?
Not without the designer’s approval: at high temperature or in very corrosive environments, 316 doesn’t offer the same properties.

## For Michaël to review

- Your Inconel machining experience (tools, speeds, tool life) and suppliers.

## Sources

- [Sandvik Coromant — Heat resistant super alloys, application guide (PDF)](https://cdn.sandvik.coromant.com/files/sitecollectiondocuments/downloads/global/technical%20guides/en-gb/c-2920-034.pdf), consulted November 26, 2026.
- [Machining Doctor — Machining Inconel: turning, milling and drilling guide](https://www.machiningdoctor.com/machining-materials/machining-inconel/), consulted November 26, 2026.
- [American Machinist — Rx for high-nickel anxiety](https://www.americanmachinist.com/machining-cutting/article/21895460/rx-for-high-nickel-anxiety), consulted November 26, 2026.
- [Special Metals — Inconel alloy 718 (data sheet)](https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-718.pdf), consulted November 26, 2026.
