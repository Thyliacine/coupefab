---
id: edm
hub: process
order: 45
nav: Électroérosion (fil et enfonçage) | EDM (wire and sinker)
kicker: Procédé · usinage non conventionnel | Process · non-conventional machining
level: intermediaire
schema: Article
tags: edm, wire edm, sinker edm, ram edm, electroerosion, fil, enfoncage, dielectric, deionized water, graphite electrode, recast layer, white layer, skim cut, taper, hardened steel, carbide
related: tolerances, five-axis, ph-17-4, inconel
fr_slug: electroerosion-fil-enfoncage
en_slug: edm-wire-sinker
fr_title: Électroérosion (EDM) à fil et par enfonçage : principe, usages et limites
en_title: EDM, wire and sinker: how it works, what it’s for and its limits
fr_desc: L’électroérosion enlève la matière par étincelles, sans effort de coupe : fil pour les profils débouchants et les dépouilles, enfonçage pour les cavités borgnes. Matières, couche refondue, passes de finition et quand la choisir.
en_desc: EDM removes material with sparks, with no cutting force: wire for through profiles and tapers, sinker for blind cavities. Materials, recast layer, skim passes and when to choose it.
---
=== fr
L’électroérosion (*EDM, Electrical Discharge Machining*) enlève la matière par une succession d’**étincelles** entre une électrode et la pièce, dans un liquide **diélectrique**. Pas de contact, pas d’effort de coupe : la dureté de la matière n’a presque pas d’importance, seule sa **conductivité** compte.

## Fil ou enfonçage ?

| Critère | EDM à fil | EDM par enfonçage (*sinker / ram*) |
|---|---|---|
| Électrode | Fil fin dévidé en continu (souvent laiton) | Électrode usinée à la forme (graphite ou cuivre) |
| Diélectrique | Eau déminéralisée en général | Huile diélectrique en général |
| Formes | Profils **débouchants**, dépouilles (*taper*), poinçons et matrices | Cavités **borgnes**, nervures fines, formes 3D, angles vifs intérieurs |
| Départ | Trou de départ (ou bord de pièce) | Surface de la pièce |
| Usages | Matrices de découpe, engrenages, pièces en carbure, fentes fines | Moules, empreintes, détails impossibles à fraiser |

## Points forts

- Matières **trempées**, carbure, superalliages (voir [[inconel]]) usinées après traitement thermique.
- Pas de bavure ni d’effort : pièces minces ou fragiles.
- Angles intérieurs très vifs (limités par le diamètre du fil ou la forme de l’électrode).
- Excellente précision et répétabilité avec passes de finition.

## Limites

- **Lent** comparé au fraisage.
- Matière **conductrice** seulement.
- **Couche refondue** (*recast / white layer*) : métal refondu et resolidifié en surface, dur, parfois fissuré et contraint. Les passes de finition à basse énergie (*skim cuts*) la réduisent ; certaines spécifications exigent sa limitation ou son retrait.
- Électrodes d’enfonçage à fabriquer (coût, usure).

## Démarche type (fil)

1. Concevoir la pièce en tenant compte du **trou de départ** et des points d’attache (pour que la chute ne tombe pas).
2. Programmer le contour (FAO fil : ESPRIT, Mastercam Wire, etc.) avec **décalage** de fil et nombre de passes.
3. Brider la pièce à plat, aligner.
4. Ébauche puis **passes de finition** selon la tolérance et le fini.
5. Retirer les attaches et finir.

## Liste de vérification pour sous-traiter de l’EDM

- [ ] Matière et état (trempé ?) indiqués
- [ ] Tolérances et fini de surface réalistes pour le procédé
- [ ] Exigence sur la couche refondue si critique
- [ ] Trou de départ prévu ou à percer par le sous-traitant
- [ ] Modèle 3D ou DXF propre (voir [[dxf-best-practices]])

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Demander de l’EDM pour ce qu’une fraise fait | Coût et délai inutiles |
| Oublier la couche refondue sur une pièce en fatigue | Amorce de fissure |
| Pas de trou de départ prévu | Opération supplémentaire |
| Spécifier un angle intérieur plus vif que le fil | Impossible à fil ; enfonçage nécessaire |

## FAQ

### L’EDM peut-il couper le verre ou le plastique ?
Non : il faut une matière conductrice.

### Pourquoi l’EDM à fil est-il si précis ?
Pas d’effort de coupe ni d’usure d’outil significative (le fil est neuf en permanence), et des passes de finition successives.

## À valider en atelier (Michaël)

- Vos sous-traitants EDM et les pièces que vous leur confiez.

## Sources

- [Makino — EDM: when milling just won’t cut it](https://www.makino.com/en-us/machine-technology/machining-process/edm), consulté le 26 novembre 2026.
- [Makino — Wire EDM tutorial](https://www.makino.com/resources/content-library/article/archive/edm-wire-tutorial/198), consulté le 26 novembre 2026.
- [SME — Electrical Discharge Machining study guide (PDF)](https://www.sme.org/globalassets/sme.org/media/training-guides/dv03pub14_study_guide.pdf), consulté le 26 novembre 2026.
=== en
EDM (Electrical Discharge Machining) removes material with a series of **sparks** between an electrode and the part, in a **dielectric** fluid. No contact, no cutting force: material hardness barely matters, only **conductivity** does.

## Wire or sinker?

| Criterion | Wire EDM | Sinker (ram) EDM |
|---|---|---|
| Electrode | Thin, continuously fed wire (often brass) | Electrode machined to shape (graphite or copper) |
| Dielectric | Usually deionized water | Usually dielectric oil |
| Shapes | **Through** profiles, tapers, punches and dies | **Blind** cavities, fine ribs, 3D forms, sharp inside corners |
| Start | Start hole (or part edge) | Part surface |
| Uses | Blanking dies, gears, carbide parts, fine slots | Molds, cavities, details impossible to mill |

## Strengths

- **Hardened** materials, carbide, superalloys (see [[inconel]]) machined after heat treatment.
- No burr, no force: thin or fragile parts.
- Very sharp inside corners (limited by wire diameter or electrode shape).
- Excellent precision and repeatability with skim passes.

## Limits

- **Slow** compared with milling.
- **Conductive** materials only.
- **Recast layer** (white layer): remelted and resolidified metal at the surface, hard, sometimes cracked and stressed. Low-energy skim cuts reduce it; some specifications require it be limited or removed.
- Sinker electrodes must be made (cost, wear).

## Typical workflow (wire)

1. Design the part around the **start hole** and tabs (so the slug doesn’t drop).
2. Program the contour (wire CAM: ESPRIT, Mastercam Wire, etc.) with wire **offset** and number of passes.
3. Clamp the part flat, align.
4. Rough cut then **skim passes** per tolerance and finish.
5. Remove tabs and finish.

## Checklist for subcontracting EDM

- [ ] Material and condition (hardened?) stated
- [ ] Tolerances and surface finish realistic for the process
- [ ] Recast layer requirement if critical
- [ ] Start hole provided or to be drilled by the subcontractor
- [ ] Clean 3D model or DXF (see [[dxf-best-practices]])

## Common mistakes

| Mistake | Consequence |
|---|---|
| Asking for EDM where an end mill would do | Needless cost and lead time |
| Forgetting the recast layer on a fatigue part | Crack initiation |
| No start hole planned | Extra operation |
| Specifying an inside corner sharper than the wire | Impossible on wire; sinker needed |

## FAQ

### Can EDM cut glass or plastic?
No: the material must be conductive.

### Why is wire EDM so precise?
No cutting force or significant tool wear (the wire is always fresh), plus successive skim passes.

## For Michaël to review

- Your EDM subcontractors and the parts you send them.

## Sources

- [Makino — EDM: when milling just won’t cut it](https://www.makino.com/en-us/machine-technology/machining-process/edm), consulted November 26, 2026.
- [Makino — Wire EDM tutorial](https://www.makino.com/resources/content-library/article/archive/edm-wire-tutorial/198), consulted November 26, 2026.
- [SME — Electrical Discharge Machining study guide (PDF)](https://www.sme.org/globalassets/sme.org/media/training-guides/dv03pub14_study_guide.pdf), consulted November 26, 2026.
