---
id: reading-drawings-gdt
hub: fundamentals
order: 32
nav: Lire un dessin et le GD&T | Reading drawings and GD&T
kicker: Fondamentaux · dessin technique | Fundamentals · drawings
level: intermediaire
schema: Article
tags: dessin technique, engineering drawing, gd&t, gps, asme y14.5, iso 1101, iso 8015, datum, référence, cadre de tolérance, feature control frame, position, planéité, flatness, perpendicularité, profil, faux-rond, runout, mmc, lmc, cote encadrée, basic dimension, cartouche, title block, projection
related: tolerances, measuring-inspection, fixturing, quoting
fr_slug: lire-un-dessin-gdt
en_slug: reading-drawings-gdt
fr_title: Lire un dessin technique et le GD&T : cartouche, références, cadres de tolérance
en_title: Reading an engineering drawing and GD&T: title block, datums, feature control frames
fr_desc: Ce qu’il faut lire avant de programmer ou de soumissionner : cartouche, projection, tolérances générales, références (datums), cadre de tolérance, position avec MMC, différences ASME Y14.5 et ISO. En mots simples, avec exemples chiffrés.
en_desc: What to read before programming or quoting: title block, projection, general tolerances, datums, feature control frames, position at MMC, ASME Y14.5 vs ISO differences. In plain words, with worked numbers.
---
=== fr
Un dessin est un contrat : il dit ce que la pièce doit **faire**, pas comment la fabriquer. Bien le lire évite deux pertes d’argent classiques : la soumission trop basse (une tolérance ou un traitement oublié) et la pièce refusée (une référence mal comprise). Ce guide complète [[tolerances]] : ici, on apprend à **lire** ce qui est écrit, y compris le GD&T (cotation et tolérancement géométriques).

> [!NOTE] Deux familles de normes : en Amérique du Nord, surtout **ASME Y14.5** (édition 2018 en vigueur) ; en Europe et chez beaucoup de donneurs d’ordre internationaux, le système **ISO GPS** (ISO 1101 pour les symboles, ISO 8015 pour les principes). Les symboles se ressemblent, mais certaines règles par défaut diffèrent : vérifiez la norme indiquée dans le cartouche.

## Le cartouche d’abord

Avant la moindre cote, lisez le cartouche (*title block*) :

| Champ | Pourquoi c’est important |
|---|---|
| Norme (ASME Y14.5-2018, ISO 8015…) | Change les règles par défaut (voir plus bas) |
| Unités (po ou mm) | Erreur classique en soumission et en programmation |
| Tolérance générale | S’applique à toute cote sans tolérance propre (ex. ±0,005 po, ISO 2768-m) |
| Matière, grade et état | Ex. 6061-T6, 304L, A36 ; influence prix et procédé |
| Fini, traitement, peinture | Coût et sous-traitance à prévoir |
| Révision | Fabriquer à la mauvaise révision = pièce refusée |
| Projection | 3ᵉ angle (habituel en Amérique du Nord) ou 1ᵉʳ angle (habituel en Europe) : le symbole est dans le cartouche |

> [!WARN] « Ne pas mesurer sur le dessin » : une cote absente se demande au client, elle ne se mesure pas à la règle sur le papier ou le PDF.

## Les références (datums)

Une **référence** (lettre dans un carré : A, B, C) est une surface ou un axe réel de la pièce qui sert de point de départ. L’ordre compte :

1. **Référence primaire** : la pièce s’y appuie d’abord (pour un plan, au moins 3 points de contact).
2. **Secondaire** : ensuite (2 points).
3. **Tertiaire** : enfin (1 point).

C’est le principe 3-2-1 qu’on retrouve au montage (voir [[fixturing]]) : si possible, **montez la pièce sur ses références** et prenez l’origine dessus. On évite ainsi d’empiler les erreurs.

## Le cadre de tolérance

Un cadre de tolérance (*feature control frame*) se lit de gauche à droite :

| Case | Exemple | Lecture |
|---|---|---|
| Symbole | ⌖ (position) | Quel contrôle |
| Tolérance | ⌀0,1 Ⓜ | Zone cylindrique de 0,1 mm de diamètre, au maximum de matière |
| Références | A B C | Mesurée par rapport à A, puis B, puis C |

Les **cotes encadrées** (*basic dimensions*, « cotes théoriquement exactes » en ISO) donnent la position parfaite ; la tolérance vient du cadre, pas d’un ±.

## Les familles de contrôles

| Famille | Contrôles | Référence ? |
|---|---|---|
| Forme | Rectitude, planéité, circularité, cylindricité | Jamais |
| Orientation | Perpendicularité, parallélisme, inclinaison | Oui |
| Position | Position | Oui |
| Profil | Profil d’une ligne, profil d’une surface | Souvent |
| Battement | Battement circulaire, battement total | Oui (axe) |

L’édition **ASME Y14.5-2018 a supprimé la concentricité et la symétrie** ; on utilise à la place la position, le battement ou le profil. L’ISO 1101 les conserve. Si un dessin ASME récent montre ces symboles, c’est sans doute un dessin ancien ou ISO : demandez.

## Position au maximum de matière : un exemple chiffré

Trou ⌀10,0–10,2 mm, position ⌀0,1 Ⓜ par rapport à A B C.

- Le **maximum de matière** (MMC) d’un trou, c’est le **plus petit** trou : ⌀10,0.
- À ⌀10,0, la tolérance de position est ⌀0,1.
- Plus le trou s’éloigne du MMC, plus on gagne de tolérance (**bonus**) : à ⌀10,2, la tolérance devient ⌀0,1 + 0,2 = **⌀0,3**.

Pour un arbre, c’est l’inverse : le MMC est le **plus gros** diamètre. Le modificateur Ⓛ (minimum de matière) fonctionne de la même façon dans l’autre sens. Sans modificateur, la tolérance est fixe, quelle que soit la taille réelle (RFS).

> [!TIP] En soumission, une position ⌀0,05 sans Ⓜ sur des trous de goujon n’a pas le même coût qu’une position ⌀0,2 Ⓜ sur des trous de passage. Voir [[quoting]].

## ASME et ISO : la règle par défaut qui change tout

- **ASME Y14.5 — Règle nº 1 (enveloppe)** : les limites de taille contrôlent aussi la forme. Au MMC, la pièce doit avoir une forme parfaite. Une pièce dans ses cotes de taille, mais trop arquée pour entrer dans l’enveloppe, est hors tolérance. On peut lever la règle avec le symbole ⓘ (indépendance).
- **ISO 8015 — principe d’indépendance** par défaut : la taille et la forme sont contrôlées séparément. Pour exiger l’enveloppe, le dessin doit porter Ⓔ.

Sur une barre longue, une tôle découpée ou une pièce mince, la différence est réelle : lisez la norme du cartouche.

## État de surface

Le symbole √ avec une valeur donne la rugosité, souvent **Ra** en µm (ISO) ou en µpo (pratique nord-américaine). Repères de conversion : Ra 3,2 µm ≈ 125 µpo ; Ra 1,6 µm ≈ 63 µpo ; Ra 0,8 µm ≈ 32 µpo. Ne le spécifiez que là où il compte.

## Liste de vérification avant de programmer ou de soumissionner

- [ ] Norme, unités et révision lues dans le cartouche
- [ ] Tolérance générale notée
- [ ] Matière, grade, état, fini et traitements notés
- [ ] Projection identifiée (1ᵉʳ ou 3ᵉ angle)
- [ ] Références A/B/C repérées sur la pièce et dans le montage
- [ ] Chaque cadre de tolérance lu : symbole, zone, modificateur, références
- [ ] Tolérances serrées identifiées et méthode de contrôle prévue (voir [[measuring-inspection]])
- [ ] Questions envoyées au client pour toute cote absente ou contradictoire

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Prendre l’origine sur un coin quelconque au lieu des références | Positions hors tolérance même si chaque cote « semble » bonne |
| Ignorer le Ⓜ | Rejet de pièces bonnes, ou contrôle trop coûteux |
| Appliquer la règle ASME sur un dessin ISO (ou l’inverse) | Pièce acceptée ou refusée à tort |
| Mesurer une cote absente sur le PDF | Pièce fausse, responsabilité de l’atelier |

## FAQ

### Faut-il une machine à mesurer tridimensionnelle (MMT) pour le GD&T ?

Pas toujours. Beaucoup de contrôles se vérifient au marbre, au comparateur et avec des tampons (calibres fonctionnels). La MMT devient utile quand les références et les positions se multiplient.

### Que faire si le dessin et le modèle 3D ne concordent pas ?

Demandez au client lequel fait foi et faites-le écrire. Ne tranchez pas seul.

## À valider en atelier (Michaël)

- Exemples de dessins clients anonymisés à ajouter.
- Nos méthodes de contrôle pour la position et la planéité.

## Sources

- [ASME — Y14.5 Dimensioning and Tolerancing (2018, réaffirmée 2024)](https://www.asme.org/codes-standards/find-codes-standards/y14-5-dimensioning-tolerancing). Consulté le 26 novembre 2026.
- [ISO 1101:2017 — Spécification géométrique des produits (GPS), tolérancement géométrique](https://www.iso.org/standard/66777.html). Consulté le 26 novembre 2026.
- [ISO 8015:2011 — GPS, concepts, principes et règles fondamentaux](https://www.iso.org/standard/55979.html). Consulté le 26 novembre 2026.
- [GD&T Basics — Concentricity: elimination from ASME Y14.5-2018](https://www.gdandtbasics.com/concentricity-and-asme2018/). Consulté le 26 novembre 2026.
- [GD&T Basics — ASME Y14.5 2009 vs 2018](https://www.gdandtbasics.com/asme-2009-vs-2018/). Consulté le 26 novembre 2026.

=== en
A drawing is a contract: it says what the part must **do**, not how to make it. Reading it well avoids two classic money losers: a quote that is too low (a forgotten tolerance or treatment) and a rejected part (a misunderstood datum). This guide complements [[tolerances]]: here, you learn to **read** what is written, including GD&T (geometric dimensioning and tolerancing).

> [!NOTE] Two families of standards: in North America, mostly **ASME Y14.5** (2018 edition current); in Europe and with many international customers, the **ISO GPS** system (ISO 1101 for symbols, ISO 8015 for principles). The symbols look alike, but some default rules differ: check the standard named in the title block.

## Title block first

Before any dimension, read the title block:

| Field | Why it matters |
|---|---|
| Standard (ASME Y14.5-2018, ISO 8015…) | Changes the default rules (see below) |
| Units (in or mm) | Classic quoting and programming mistake |
| General tolerance | Applies to every dimension without its own tolerance (e.g. ±0.005 in, ISO 2768-m) |
| Material, grade and temper | E.g. 6061-T6, 304L, A36; affects price and process |
| Finish, treatment, paint | Cost and outside processing to plan |
| Revision | Making the wrong revision = rejected part |
| Projection | Third angle (usual in North America) or first angle (usual in Europe): the symbol is in the title block |

> [!WARN] “Do not scale drawing”: a missing dimension is asked from the customer, never measured off the paper or PDF.

## Datums

A **datum** (letter in a box: A, B, C) is a real surface or axis on the part used as a starting point. Order matters:

1. **Primary datum**: the part rests on it first (for a plane, at least 3 contact points).
2. **Secondary**: next (2 points).
3. **Tertiary**: last (1 point).

That is the 3-2-1 principle used in fixturing (see [[fixturing]]): when you can, **hold the part on its datums** and set the work offset from them. That way errors don’t stack up.

## The feature control frame

A feature control frame reads left to right:

| Cell | Example | Meaning |
|---|---|---|
| Symbol | ⌖ (position) | Which control |
| Tolerance | ⌀0.1 Ⓜ | Cylindrical zone 0.1 mm in diameter, at maximum material condition |
| Datums | A B C | Measured relative to A, then B, then C |

**Basic dimensions** (boxed; “theoretically exact dimensions” in ISO) give the perfect location; the tolerance comes from the frame, not from a ±.

## Families of controls

| Family | Controls | Datum? |
|---|---|---|
| Form | Straightness, flatness, circularity, cylindricity | Never |
| Orientation | Perpendicularity, parallelism, angularity | Yes |
| Location | Position | Yes |
| Profile | Profile of a line, profile of a surface | Often |
| Runout | Circular runout, total runout | Yes (axis) |

**ASME Y14.5-2018 removed concentricity and symmetry**; position, runout or profile are used instead. ISO 1101 keeps them. If a recent ASME drawing shows those symbols, it is probably an old or ISO drawing: ask.

## Position at MMC: a worked example

Hole ⌀10.0–10.2 mm, position ⌀0.1 Ⓜ relative to A B C.

- A hole’s **maximum material condition** (MMC) is the **smallest** hole: ⌀10.0.
- At ⌀10.0, the position tolerance is ⌀0.1.
- The further the hole departs from MMC, the more tolerance you gain (**bonus**): at ⌀10.2, the tolerance becomes ⌀0.1 + 0.2 = **⌀0.3**.

For a shaft it is the opposite: MMC is the **largest** diameter. The Ⓛ modifier (least material condition) works the same way in reverse. With no modifier, the tolerance is fixed whatever the actual size (RFS).

> [!TIP] When quoting, a ⌀0.05 position with no Ⓜ on dowel holes does not cost the same as a ⌀0.2 Ⓜ position on clearance holes. See [[quoting]].

## ASME vs ISO: the default rule that changes everything

- **ASME Y14.5 — Rule #1 (envelope)**: size limits also control form. At MMC, the part must have perfect form. A part within its size limits but too bowed to fit the envelope is out of tolerance. The rule can be lifted with the ⓘ (independency) symbol.
- **ISO 8015 — independency principle** by default: size and form are controlled separately. To require the envelope, the drawing must show Ⓔ.

On a long bar, a cut sheet part or a thin part, the difference is real: read the standard in the title block.

## Surface finish

The √ symbol with a value gives roughness, usually **Ra** in µm (ISO) or µin (North American practice). Conversion landmarks: Ra 3.2 µm ≈ 125 µin; Ra 1.6 µm ≈ 63 µin; Ra 0.8 µm ≈ 32 µin. Only specify it where it matters.

## Checklist before programming or quoting

- [ ] Standard, units and revision read in the title block
- [ ] General tolerance noted
- [ ] Material, grade, temper, finish and treatments noted
- [ ] Projection identified (first or third angle)
- [ ] Datums A/B/C located on the part and in the fixture
- [ ] Every feature control frame read: symbol, zone, modifier, datums
- [ ] Tight tolerances identified and an inspection method planned (see [[measuring-inspection]])
- [ ] Questions sent to the customer for any missing or conflicting dimension

## Common mistakes

| Mistake | Consequence |
|---|---|
| Setting the offset on any corner instead of the datums | Positions out of tolerance even though each dimension “looks” right |
| Ignoring the Ⓜ | Good parts rejected, or overly costly inspection |
| Applying the ASME rule to an ISO drawing (or vice versa) | Parts wrongly accepted or rejected |
| Scaling a missing dimension off the PDF | Wrong part, shop liability |

## FAQ

### Do you need a CMM for GD&T?

Not always. Many controls can be checked on a surface plate with indicators and functional gauges. A CMM pays off as datums and positions multiply.

### What if the drawing and the 3D model disagree?

Ask the customer which one governs and get it in writing. Don’t decide alone.

## For Michaël to review

- Anonymized customer drawing examples to add.
- Our inspection methods for position and flatness.

## Sources

- [ASME — Y14.5 Dimensioning and Tolerancing (2018, reaffirmed 2024)](https://www.asme.org/codes-standards/find-codes-standards/y14-5-dimensioning-tolerancing). Consulted November 26, 2026.
- [ISO 1101:2017 — Geometrical product specifications (GPS), geometrical tolerancing](https://www.iso.org/standard/66777.html). Consulted November 26, 2026.
- [ISO 8015:2011 — GPS, fundamental concepts, principles and rules](https://www.iso.org/standard/55979.html). Consulted November 26, 2026.
- [GD&T Basics — Concentricity: elimination from ASME Y14.5-2018](https://www.gdandtbasics.com/concentricity-and-asme2018/). Consulted November 26, 2026.
- [GD&T Basics — ASME Y14.5 2009 vs 2018](https://www.gdandtbasics.com/asme-2009-vs-2018/). Consulted November 26, 2026.
