---
id: oxyfuel
hub: process
order: 25
nav: Oxycoupage | Oxyfuel cutting
kicker: Procédé · coupe thermique | Process · thermal cutting
level: debutant
schema: HowTo
tags: oxyfuel, oxy-acetylene, oxy-propane, cutting torch, preheat, tip, drag lines, slag, thick plate, flashback arrestor, victor, esab
related: plasma-cutting, safety, weld-prep, kerf
fr_slug: oxycoupage
en_slug: oxyfuel-cutting
fr_title: Oxycoupage : principe, réglage de la flamme, qualité de coupe et sécurité
en_title: Oxyfuel cutting: how it works, flame setup, cut quality and safety
fr_desc: Quand l’oxycoupage bat le plasma (acier au carbone épais), choix de la buse selon l’épaisseur, réglage de la flamme de préchauffage, lecture des stries et des scories, et règles de sécurité des gaz.
en_desc: When oxyfuel beats plasma (thick carbon steel), choosing the tip by thickness, setting the preheat flame, reading drag lines and slag, and gas safety rules.
---
=== fr
L’oxycoupage ne « fond » pas l’acier : la flamme de **préchauffage** (acétylène, propane, gaz naturel ou autre gaz combustible, avec oxygène) porte l’acier à sa température d’inflammation, puis un jet d’**oxygène pur** l’oxyde et chasse l’oxyde fondu. C’est pourquoi le procédé marche très bien sur l’**acier au carbone et faiblement allié**, mais pas sur l’inox ni l’aluminium, dont les oxydes protègent le métal.

## Oxycoupage ou plasma ?

| Critère | Oxycoupage | Plasma |
|---|---|---|
| Matières | Acier au carbone et faiblement allié | Tout métal conducteur (acier, inox, alu…) |
| Épaisseur | Très à l’aise en forte épaisseur | Avantagé en mince et moyen |
| Vitesse en mince | Lente | Rapide |
| Investissement | Faible (chalumeau, gaz) | Plus élevé (source, consommables) |
| Plusieurs torches à la fois | Courant sur les grandes tables | Possible mais coûteux |
| Zone affectée thermiquement | Plus large | Plus étroite |

## Équipement

- Bouteilles ou réseau d’**oxygène** et de **gaz combustible**, détendeurs adaptés à chaque gaz.
- **Clapets antiretour et dispositifs anti-retour de flamme** (*flashback arrestors*) selon les exigences du fabricant.
- Chalumeau coupeur ou torche machine, **buses** (*tips*) choisies selon l’épaisseur et le gaz combustible.
- Allumeur à friction (jamais de briquet), lunettes ou visière à teinte adaptée, gants, vêtements ignifuges.

## Démarche (coupe manuelle ou machine)

1. Choisir la **buse** pour l’épaisseur dans la charte du fabricant (Victor, ESAB, Harris…) ; elle donne aussi pressions, vitesse et kerf.
2. Régler les **pressions** de la charte aux détendeurs, gaz qui circulent.
3. Allumer le combustible, ajouter l’oxygène de préchauffage jusqu’à une **flamme neutre** : cônes intérieurs nets et brillants. ESAB recommande le cône intérieur le plus court et le plus vif.
4. Ouvrir l’oxygène de coupe et retoucher le préchauffage (les cônes changent quand le jet s’ouvre).
5. Chauffer le départ (bord de tôle de préférence) jusqu’au rouge cerise, puis ouvrir le jet de coupe et avancer.
6. Garder la torche **perpendiculaire** et à **hauteur constante** ; en machine, préchauffage fort pour percer puis préchauffage réduit pour avancer.

## Lire la coupe

| Observation | Cause probable | Correctif |
|---|---|---|
| Stries presque verticales, bord net | Réglage correct | — |
| Stries très inclinées vers l’arrière, coupe qui se perd | Trop vite ou pas assez d’oxygène de coupe | Ralentir, vérifier pression et buse |
| Arête supérieure arrondie, beaucoup de scories | Trop lent ou préchauffage trop fort | Accélérer, réduire le préchauffage |
| Gouges irrégulières | Buse sale ou abîmée, vitesse irrégulière | Nettoyer ou changer la buse |
| Scories adhérentes | Hauteur ou vitesse inadéquate | Ajuster selon la charte |

## Sécurité : non négociable

- [ ] Bouteilles attachées debout, chapeaux en place pendant le transport
- [ ] Détendeurs et boyaux en bon état, test de fuite à l’eau savonneuse
- [ ] Antiretours en place ; jamais d’huile ni de graisse sur l’équipement d’oxygène
- [ ] Zone dégagée de combustibles, extincteur à portée, permis de travail à chaud si requis
- [ ] Ventilation et protection contre les fumées (voir [[safety]])

> [!WARN] Un retour de flamme (*flashback*) se produit quand la flamme remonte dans le chalumeau. Fermez immédiatement les robinets selon la séquence du fabricant et faites inspecter l’équipement avant de le réutiliser.

## FAQ

### Acétylène ou propane ?
L’acétylène donne une flamme plus chaude et concentrée (préchauffage rapide, perçage rapide) ; le propane est souvent moins cher pour les longues coupes en épaisseur, avec des buses spécifiques. Suivez la charte de la buse pour le gaz choisi.

### Peut-on oxycouper l’inox ?
Pas avec un chalumeau standard : utilisez le plasma, le laser ou le jet d’eau. Voir [[plasma-cutting]].

## À valider en atelier (Michaël)

- Vos buses et gaz habituels pour la plaque épaisse.
- Les règles de permis de travail à chaud chez vos clients.

## Sources

- [ESAB — How does the oxy-fuel cutting process work?](https://esab.com/gb/eur_en/esab-university/blogs/how-does-the-oxy-fuel-cutting-process-work/), consulté le 26 novembre 2026.
- [ESAB — Oxy-fuel torch preheat and its proper adjustment](https://esab.com/us/nam_en/esab-university/blogs/oxy-fuel-torch-preheat-and-its-proper-adjustment/), consulté le 26 novembre 2026.
- [Victor (données reprises par un distributeur) — Oxy-fuel cut charts (PDF)](https://www.americantorchtip.com/wp-content/uploads/2021/03/Oxy-Fuel-Cut-Chart-Victor-1.pdf), consulté le 26 novembre 2026.
- [CNESST — Prévention et sécurité](https://www.cnesst.gouv.qc.ca/fr/prevention-securite), consulté le 26 novembre 2026.
=== en
Oxyfuel cutting doesn’t “melt” steel: the **preheat** flame (acetylene, propane, natural gas or another fuel gas, with oxygen) brings the steel to its ignition temperature, then a jet of **pure oxygen** oxidizes it and blows the molten oxide away. That’s why the process works very well on **carbon and low-alloy steel**, but not on stainless or aluminum, whose oxides protect the metal.

## Oxyfuel or plasma?

| Criterion | Oxyfuel | Plasma |
|---|---|---|
| Materials | Carbon and low-alloy steel | Any conductive metal (steel, stainless, aluminum…) |
| Thickness | Very comfortable in heavy plate | Favoured in thin and medium |
| Speed on thin material | Slow | Fast |
| Investment | Low (torch, gas) | Higher (power source, consumables) |
| Several torches at once | Common on large tables | Possible but costly |
| Heat-affected zone | Wider | Narrower |

## Equipment

- **Oxygen** and **fuel gas** cylinders or supply, regulators matched to each gas.
- **Check valves and flashback arrestors** per the manufacturer’s requirements.
- Cutting torch or machine torch, **tips** chosen by thickness and fuel gas.
- Friction lighter (never a cigarette lighter), goggles or face shield with the right shade, gloves, flame-resistant clothing.

## Workflow (manual or machine)

1. Pick the **tip** for the thickness from the manufacturer’s chart (Victor, ESAB, Harris…); it also gives pressures, speed and kerf.
2. Set chart **pressures** at the regulators with gas flowing.
3. Light the fuel, add preheat oxygen to a **neutral flame**: sharp, bright inner cones. ESAB recommends the shortest, brightest inner cone.
4. Open cutting oxygen and re-trim the preheat (cones change when the jet opens).
5. Heat the start (preferably a plate edge) to cherry red, then open the cutting jet and travel.
6. Keep the torch **square** and at **constant height**; on a machine, high preheat to pierce, then reduced preheat to travel.

## Reading the cut

| Observation | Likely cause | Fix |
|---|---|---|
| Near-vertical drag lines, clean edge | Correct settings | — |
| Drag lines sweeping far back, cut lost | Too fast or not enough cutting oxygen | Slow down, check pressure and tip |
| Rounded top edge, heavy slag | Too slow or preheat too high | Speed up, reduce preheat |
| Irregular gouges | Dirty or damaged tip, uneven speed | Clean or replace the tip |
| Clinging slag | Wrong height or speed | Adjust per the chart |

## Safety: non-negotiable

- [ ] Cylinders secured upright, caps on for transport
- [ ] Regulators and hoses in good condition, soapy-water leak test
- [ ] Check valves fitted; never oil or grease on oxygen equipment
- [ ] Area clear of combustibles, extinguisher at hand, hot-work permit if required
- [ ] Ventilation and fume protection (see [[safety]])

> [!WARN] A flashback happens when the flame travels back into the torch. Close the valves immediately in the manufacturer’s sequence and have the equipment inspected before reuse.

## FAQ

### Acetylene or propane?
Acetylene gives a hotter, more concentrated flame (fast preheat, fast pierce); propane is often cheaper for long cuts in heavy plate, with specific tips. Follow the tip chart for the chosen gas.

### Can you oxyfuel-cut stainless?
Not with a standard torch: use plasma, laser or waterjet. See [[plasma-cutting]].

## For Michaël to review

- Your usual tips and gases for heavy plate.
- Hot-work permit rules at your customers.

## Sources

- [ESAB — How does the oxy-fuel cutting process work?](https://esab.com/gb/eur_en/esab-university/blogs/how-does-the-oxy-fuel-cutting-process-work/), consulted November 26, 2026.
- [ESAB — Oxy-fuel torch preheat and its proper adjustment](https://esab.com/us/nam_en/esab-university/blogs/oxy-fuel-torch-preheat-and-its-proper-adjustment/), consulted November 26, 2026.
- [Victor (data reproduced by a distributor) — Oxy-fuel cut charts (PDF)](https://www.americantorchtip.com/wp-content/uploads/2021/03/Oxy-Fuel-Cut-Chart-Victor-1.pdf), consulted November 26, 2026.
- [CNESST — Prevention and safety (French)](https://www.cnesst.gouv.qc.ca/fr/prevention-securite), consulted November 26, 2026.
