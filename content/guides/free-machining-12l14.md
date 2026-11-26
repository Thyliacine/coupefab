---
id: free-machining-12l14
hub: materials
order: 14
nav: 12L14 et 1215 (décolletage) | 12L14 and 1215 (free-machining)
kicker: Matériaux · aciers de décolletage | Materials · free-machining steels
level: intermediaire
schema: Article
prices: yes
tags: 12l14, 1215, 1117, 1144, free machining, leaded steel, resulfurized, screw machine, swiss, machinability, weldability, lead, chip control
related: steel-1018-hr-cr, swiss-turn-mill, feeds-speeds, cnc-lathe
fr_slug: acier-decolletage-12l14-1215
en_slug: free-machining-steel-12l14-1215
fr_title: Aciers de décolletage 12L14 et 1215 : usinabilité, limites et quand les éviter
en_title: Free-machining steels 12L14 and 1215: machinability, limits and when to avoid them
fr_desc: Pourquoi le 12L14 (au plomb) et le 1215 (resulfuré) s’usinent beaucoup plus vite que le 1018, et pourquoi il ne faut pas les souder ni les utiliser n’importe où. Comparatif et choix.
en_desc: Why 12L14 (leaded) and 1215 (resulfurized) machine much faster than 1018, and why you shouldn’t weld them or use them everywhere. Comparison and selection.
---
=== fr
Les aciers de **décolletage** sont conçus pour l’usinage en série (tours automatiques, décolleteuses de type suisse) : leurs additions (soufre, phosphore, **plomb** pour le 12L14) fragmentent le copeau, réduisent les efforts et améliorent le fini. En échange, ils perdent en soudabilité et en ductilité.

## Comparatif

| Critère | 12L14 | 1215 | 1018 (référence) |
|---|---|---|---|
| Additions | Soufre + **plomb** | Soufre + phosphore (sans plomb) | — |
| Usinabilité (B1112 = 100, tableaux de distributeurs) | ~160–180 % | ~135 % | ~70–78 % |
| Contrôle du copeau | Excellent | Très bon | Copeaux longs |
| Soudabilité | **À éviter** (porosités, fissuration, fumées de plomb) | Médiocre | Bonne |
| Cémentation | Possible mais moins prévisible | Possible, limitée | Classique |
| Usages | Pièces décolletées non critiques : raccords, axes, douilles | Idem quand le plomb est exclu | Pièces générales, soudées |

## Quand les choisir

- Grandes séries de pièces tournées où le temps de cycle domine le prix.
- Pièces non soudées, non soumises à des chocs ou à de la fatigue sévère.
- **1215** quand une exigence (client, environnement) interdit le plomb.

## Quand les éviter

- Toute pièce **soudée** ou brasée.
- Pièces de sécurité, chocs, fatigue : préférez un acier allié traité (voir [[alloy-4140-4340]]) ou le 1144 selon la spécification.
- Contact alimentaire ou eau potable avec plomb : vérifier les exigences applicables.

> [!WARN] Usiner ou chauffer du 12L14 libère du plomb dans les copeaux et les fumées : hygiène, ventilation et gestion des copeaux selon les règles de santé et sécurité (voir [[safety]]).

## Usinage en pratique

- Vitesses et avances plus élevées qu’en 1018, selon les fiches des fabricants d’outils (voir [[feeds-speeds]]).
- Très bon fini de surface en tournage ; idéal en décolletage de type suisse (voir [[swiss-turn-mill]]).
- Le plomb n’empêche pas l’usure d’outil : surveillez la durée de vie (voir [[tool-life]]).

## Liste de vérification

- [ ] La pièce ne sera ni soudée ni brasée
- [ ] Aucune exigence « sans plomb » (sinon 1215)
- [ ] Sollicitations compatibles (pas de chocs ni fatigue critiques)
- [ ] Certificat matière si traçabilité exigée
- [ ] Comparer les prix publiés dans le [[prix]]

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Souder un support en 12L14 | Soudure poreuse et fissurée |
| Remplacer du 1018 par du 12L14 sans avis du concepteur | Ductilité et résistance aux chocs réduites |
| Mélanger les barres au stock | Pièce soudée par erreur en 12L14 ; identifier les bouts de barre |

## FAQ

### Comment reconnaître du 12L14 dans le stock ?
Pas à l’œil : identifiez les barres (code couleur en bout, étiquette, certificat). Un essai de soudure n’est pas une méthode.

### Le 1215 est-il aussi rapide que le 12L14 ?
Un peu moins selon les tableaux publiés, mais il évite le plomb.

## À valider en atelier (Michaël)

- Vos règles de stockage et d’identification des barres de décolletage.

## Sources

- [Metals Service Center Institute — Machinability ratings](https://www.msci.org/topic/machinability-ratings/), consulté le 26 novembre 2026.
- [Charter Steel — Technical reference guide (PDF)](https://www.chartersteel.com/documents/technical-pocket-book-guide-digital.pdf), consulté le 26 novembre 2026.
- [MatGrade — AISI 12L14: machinability and 12L14 vs 1215](https://www.matgrade.com/materials/aisi-12l14/), consulté le 26 novembre 2026.
=== en
**Free-machining** steels are designed for production machining (automatic lathes, Swiss-type machines): their additions (sulfur, phosphorus, **lead** for 12L14) break up the chip, lower cutting forces and improve finish. In exchange they lose weldability and ductility.

## Comparison

| Criterion | 12L14 | 1215 | 1018 (reference) |
|---|---|---|---|
| Additions | Sulfur + **lead** | Sulfur + phosphorus (lead-free) | — |
| Machinability (B1112 = 100, distributor tables) | ~160–180% | ~135% | ~70–78% |
| Chip control | Excellent | Very good | Long chips |
| Weldability | **Avoid** (porosity, cracking, lead fumes) | Poor | Good |
| Case hardening | Possible but less predictable | Possible, limited | Classic |
| Uses | Non-critical screw-machine parts: fittings, pins, bushings | Same when lead is excluded | General and welded parts |

## When to choose them

- Large runs of turned parts where cycle time drives price.
- Parts that aren’t welded and don’t see severe impact or fatigue.
- **1215** when a requirement (customer, environment) excludes lead.

## When to avoid them

- Any **welded** or brazed part.
- Safety, impact or fatigue parts: prefer a heat-treated alloy steel (see [[alloy-4140-4340]]) or 1144 per the specification.
- Food contact or potable water with lead: check applicable requirements.

> [!WARN] Machining or heating 12L14 releases lead into chips and fumes: hygiene, ventilation and chip handling per health and safety rules (see [[safety]]).

## Machining in practice

- Higher speeds and feeds than 1018, per tool makers’ data (see [[feeds-speeds]]).
- Very good surface finish in turning; ideal for Swiss-type work (see [[swiss-turn-mill]]).
- Lead doesn’t stop tool wear: track tool life (see [[tool-life]]).

## Checklist

- [ ] The part won’t be welded or brazed
- [ ] No “lead-free” requirement (otherwise 1215)
- [ ] Loading compatible (no critical impact or fatigue)
- [ ] Material certificate if traceability is required
- [ ] Compare published prices in the [[prix]]

## Common mistakes

| Mistake | Consequence |
|---|---|
| Welding a 12L14 bracket | Porous, cracked weld |
| Swapping 1018 for 12L14 without asking the designer | Reduced ductility and impact resistance |
| Mixed bars in stock | A 12L14 part welded by mistake; mark bar ends |

## FAQ

### How do I recognize 12L14 in stock?
Not by eye: identify bars (end colour code, tag, certificate). A test weld isn’t a method.

### Is 1215 as fast as 12L14?
A little slower per published tables, but it avoids lead.

## For Michaël to review

- Your storage and identification rules for free-machining bar.

## Sources

- [Metals Service Center Institute — Machinability ratings](https://www.msci.org/topic/machinability-ratings/), consulted November 26, 2026.
- [Charter Steel — Technical reference guide (PDF)](https://www.chartersteel.com/documents/technical-pocket-book-guide-digital.pdf), consulted November 26, 2026.
- [MatGrade — AISI 12L14: machinability and 12L14 vs 1215](https://www.matgrade.com/materials/aisi-12l14/), consulted November 26, 2026.
