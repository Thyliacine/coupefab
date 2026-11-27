---
id: press-brake
hub: process
order: 7
nav: Presse plieuse | Press brake
kicker: Procédé · formage | Process · forming
level: intermediaire
schema: HowTo
tags: press brake, bending, air bending, v-die, tonnage, inside radius, springback, sheet metal
related: bend-allowance, solidworks-sheet-metal, tolerances, materials-grades
prices: yes
fr_slug: presse-plieuse
en_slug: press-brake-bending
fr_title: Presse plieuse : choisir le V, calculer le tonnage, prévoir le rayon
en_title: Press brake: choose the V-die, compute tonnage, predict the radius
fr_desc: Pliage en l’air, règle des 8 fois l’épaisseur, règle des 20 % pour le rayon intérieur, formule de tonnage par pied, retour élastique et séquence de pliage — avec les formules de Steve Benson (The Fabricator).
en_desc: Air bending, the 8× thickness rule, the 20 percent rule for inside radius, tonnage per foot formula, springback and bend sequence — with Steve Benson’s formulas (The Fabricator).
---
=== fr
La presse plieuse forme la tôle entre un poinçon et une matrice en V. En **pliage en l’air** (le plus courant), l’angle dépend de la profondeur de pénétration du poinçon et le rayon intérieur dépend surtout de l’**ouverture du V**. Bien choisir le V, c’est donc choisir le rayon, le tonnage et la stabilité de l’angle.

## Trois règles et une formule

Steve Benson, ancien président du Precision Sheet Metal Technology Council de la FMA, les résume dans *The Fabricator* :

| Règle | Énoncé | Limite |
|---|---|---|
| Règle des 8× | Ouverture du V ≈ 8 × épaisseur (base : acier laminé à froid 60 000 psi) ; donne un rayon intérieur proche de l’épaisseur | Le facteur peut varier de 6× à 12× selon l’épaisseur ; ne tient pas compte de la matière |
| Règle des 20 % | Rayon intérieur ≈ % de l’ouverture du V : **15–17 %** acier laminé à froid, **20–22 %** inox 304, **9–11 %** aluminium 5052-H32 | Décrit le rayon obtenu, ne choisit pas le V (ignore retour élastique et tonnage) |
| Pli « vif » | Pour l’acier doux, le pli devient vif quand le rayon intérieur descend vers environ **63 %** de l’épaisseur : le poinçon marque la tôle | En dessous, il faut frapper ou mater, pas plier en l’air |

**Tonnage par pied de pli** (acier 60 000 psi = facteur 1) :

tonnes/pi = [ (575 × T²) / V ] × facteur matière

avec T et V en pouces. Le facteur matière = résistance à la traction ÷ 60 000 psi (par exemple 85 000 psi → 1,4). Multipliez par la longueur de pli en pieds et comparez à la capacité de la presse **et** de l’outillage.

## Démarche pas à pas

1. **Vérifier le rayon demandé** : il doit être supérieur au rayon de pli vif, sinon il est physiquement impossible en l’air.
2. **Choisir l’ouverture du V** : point de départ 8 × T, puis ajuster pour approcher le rayon voulu avec la règle des 20 %.
3. **Calculer le tonnage** avec la formule et la longueur de pli ; vérifier presse et outils.
4. **Calculer le rayon réel** avec le V disponible (règle des 20 %, valeur médiane).
5. **Calculer la déduction de pli** avec ce rayon — voir [Pliage : K-factor](/guides/pliage-k-factor/).
6. **Vérifier l’aile minimale** : l’aile doit reposer sur les deux épaules du V pendant tout le pli.
7. **Planifier la séquence** pour éviter les collisions avec le poinçon et le bâti.
8. **Pli d’essai**, mesure de l’angle et des ailes, correction.

### Exemple de calcul (d’après l’article de Benson)
Inox 304, T = 0,075 po, V = 0,551 po, traction 85 000 psi (facteur 1,4) :
tonnage = [(575 × 0,075²) / 0,551] × 1,4 ≈ 8,2 tonnes par pied ; rayon intérieur ≈ 0,551 × 21 % ≈ 0,116 po.

## Retour élastique

Après le pli, la tôle se relâche un peu. Il augmente avec la résistance de la matière et le rapport rayon/épaisseur. On compense en pliant au-delà de l’angle (commande CNC avec correction d’angle, ou essais).

## Sécurité

Le point de pincement entre poinçon et matrice est l’un des plus dangereux de l’atelier. Protecteurs, rideaux lumineux ou dispositifs de protection conformes, pédale protégée, formation. Au Québec, voir les exigences de la CNESST sur les protecteurs de machines (RSST). Voir [Sécurité](/guides/securite-cnc-cnesst/).

## Erreurs fréquentes

- Plier avec un V trop étroit pour « faire un petit rayon » : surcharge de l’outil ou de la presse.
- Rayon dans la CAO différent du rayon réel : déplié faux.
- Aile trop courte qui tombe dans le V.
- Plier perpendiculairement au laminage sans vérifier le rayon minimal (fissures, surtout aluminium traité).

## Liste de vérification

- [ ] Rayon demandé supérieur au rayon de pli vif
- [ ] Ouverture du V choisie (départ 8 × T, ajustée avec la règle des 20 %)
- [ ] Tonnage calculé pour la longueur de pli, comparé à la presse **et** à l’outillage
- [ ] Déduction de pli calculée avec le rayon réel
- [ ] Aile minimale respectée (repose sur les deux épaules du V)
- [ ] Séquence de pliage vérifiée pour éviter les collisions
- [ ] Sens de laminage vérifié pour les petits rayons (aluminium traité)
- [ ] Protecteurs, rideaux lumineux et pédale protégée en place ; cadenassage pour changer l’outillage (voir [[lockout-cadenassage]])
- [ ] Pli d’essai mesuré (angle et ailes) avant la série

## FAQ

### Pliage en l’air, frappe ou matage ?
En l’air : un jeu d’outils pour plusieurs angles, peu de tonnage, angle sensible aux variations. Frappe (bottoming) et matage (coining) : angle plus constant, beaucoup plus de tonnage.

## À valider en atelier (Michaël)

- Vos ouvertures de V disponibles et la capacité de vos presses.
- Une séquence de pliage type à illustrer.

## Sources

- [The Fabricator — Six steps for selecting the right die for press brakes (S. Benson)](https://www.thefabricator.com/thefabricator/article/bending/six-steps-for-selecting-the-right-die-for-press-brakes), consulté le 26 novembre 2026.
- [CNESST — Règlement sur la santé et la sécurité du travail (RSST)](https://www.legisquebec.gouv.qc.ca/fr/document/rc/S-2.1,%20r.%2013).
=== en
A press brake forms sheet between a punch and a V-die. In **air bending** (the most common), the angle depends on punch penetration depth and the inside radius depends mostly on the **V opening**. Choosing the V means choosing the radius, the tonnage and angle stability.

## Three rules and a formula

Steve Benson, former chair of the FMA’s Precision Sheet Metal Technology Council, sums them up in *The Fabricator*:

| Rule | Statement | Limit |
|---|---|---|
| 8× rule | V opening ≈ 8 × thickness (based on 60,000 psi cold-rolled steel); gives an inside radius close to thickness | The factor can range 6× to 12× with thickness; ignores material type |
| 20 percent rule | Inside radius ≈ % of V opening: **15–17%** cold-rolled steel, **20–22%** 304 stainless, **9–11%** 5052-H32 aluminum | Describes the resulting radius, does not pick the V (ignores springback and tonnage) |
| Sharp bend | For mild steel, a bend turns sharp when the inside radius drops to about **63%** of thickness: the punch digs into the sheet | Below that you must bottom or coin, not air bend |

**Tonnage per foot of bend** (60,000 psi steel = factor 1):

tons/ft = [ (575 × T²) / V ] × material factor

with T and V in inches. Material factor = tensile strength ÷ 60,000 psi (e.g. 85,000 psi → 1.4). Multiply by bend length in feet and compare with the capacity of the press **and** the tooling.

## Step by step

1. **Check the specified radius**: it must exceed the sharp-bend radius, or it is physically impossible in air bending.
2. **Choose the V opening**: start at 8 × T, then adjust toward the target radius with the 20 percent rule.
3. **Compute tonnage** with the formula and bend length; check press and tooling.
4. **Compute the real radius** with the available V (20 percent rule, median value).
5. **Compute bend deduction** with that radius — see [Bending: K-factor](/en/guides/bend-allowance-k-factor/).
6. **Check minimum flange**: the flange must rest on both die shoulders throughout the bend.
7. **Plan the sequence** to avoid collisions with the punch and frame.
8. **Test bend**, measure angle and flanges, correct.

### Worked example (from Benson’s article)
304 stainless, T = 0.075 in, V = 0.551 in, tensile 85,000 psi (factor 1.4):
tonnage = [(575 × 0.075²) / 0.551] × 1.4 ≈ 8.2 tons per foot; inside radius ≈ 0.551 × 21% ≈ 0.116 in.

## Springback

After bending, the sheet relaxes slightly. It grows with material strength and radius-to-thickness ratio. Compensate by overbending (CNC control with angle correction, or trials).

## Safety

The pinch point between punch and die is one of the most dangerous in the shop. Guards, light curtains or compliant safeguarding devices, guarded foot pedal, training. In Quebec, see CNESST machine-guarding requirements (RSST). See [Safety](/en/guides/cnc-shop-safety/).

## Common mistakes

- Bending in too narrow a V “to get a small radius”: overloaded tooling or press.
- CAD radius different from the real radius: wrong flat.
- Flange too short, falls into the V.
- Bending across the grain without checking minimum radius (cracks, especially heat-treated aluminum).

## Checklist

- [ ] Requested radius larger than the sharp-bend radius
- [ ] V opening chosen (start at 8 × T, adjusted with the 20% rule)
- [ ] Tonnage calculated for the bend length, compared with the press **and** the tooling
- [ ] Bend deduction calculated with the real radius
- [ ] Minimum flange respected (rests on both V shoulders)
- [ ] Bend sequence checked for collisions
- [ ] Grain direction checked for tight radii (heat-treated aluminum)
- [ ] Guards, light curtains and guarded foot pedal in place; lockout to change tooling (see [[lockout-cadenassage]])
- [ ] Test bend measured (angle and flanges) before the run

## FAQ

### Air bending, bottoming or coining?
Air: one tool set for many angles, low tonnage, angle sensitive to variation. Bottoming and coining: more consistent angle, much more tonnage.

## For Michaël to review

- Your available V openings and press capacities.
- A typical bend sequence to illustrate.

## Sources

- [The Fabricator — Six steps for selecting the right die for press brakes (S. Benson)](https://www.thefabricator.com/thefabricator/article/bending/six-steps-for-selecting-the-right-die-for-press-brakes), consulted November 26, 2026.
- [CNESST — Regulation respecting occupational health and safety (RSST)](https://www.legisquebec.gouv.qc.ca/en/document/cr/S-2.1,%20r.%2013).
