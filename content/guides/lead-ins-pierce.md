---
id: lead-ins-pierce
hub: fundamentals
order: 21
nav: Entrées, sorties et perçage | Lead-ins and pierce
kicker: Fondamentaux · plasma | Fundamentals · plasma
level: intermediaire
schema: HowTo
tags: plasma, lead-in, lead-out, pierce height, pierce delay, ihs, thc, holes, laser, waterjet
related: kerf, plasma-cutting, sheetcam, plasma-troubleshooting
fr_slug: entrees-sorties-percage-plasma
en_slug: lead-ins-pierce-height
fr_title: Entrées, sorties, hauteur et délai de perçage en découpe plasma
en_title: Lead-ins, lead-outs, pierce height and pierce delay in plasma cutting
fr_desc: Où placer l’entrée, quelle forme lui donner, pourquoi percer plus haut que la hauteur de coupe, comment régler le délai, et les trous propres — avec les valeurs qui viennent de votre charte.
en_desc: Where to place the lead-in, what shape to give it, why pierce higher than cut height, how to set the delay, and clean holes — with the values that come from your chart.
---
=== fr
Le perçage est le moment le plus dur pour les consommables : le métal en fusion est projeté vers la torche avant que l’arc ne traverse. L’entrée (lead-in) emmène ensuite l’arc stabilisé jusqu’au contour, et la sortie (lead-out) le termine sans marquer la pièce. Bien réglés, ils font la différence entre une pièce propre et une pièce à meuler.

## Les réglages et d’où ils viennent

| Réglage | Rôle | Source de la valeur |
|---|---|---|
| Hauteur de perçage | Protéger la torche des projections | Charte de coupe de votre source (souvent exprimée par rapport à la hauteur de coupe) |
| Délai de perçage | Laisser l’arc traverser avant de bouger | Charte de coupe, selon l’épaisseur |
| Hauteur de coupe | Distance pendant la coupe | Charte de coupe |
| Tension d’arc (THC) | Maintien de la hauteur | Charte ; mode automatique selon la commande |
| Longueur d’entrée | Arc stable avant le contour | Essais ; dépend de l’épaisseur et du perçage |

> [!WARN] Ne copiez pas une hauteur ou un délai « universel » trouvé sur un forum. Les chartes Hypertherm, par exemple, donnent ces valeurs par épaisseur, ampérage, gaz et jeu de consommables — c’est la seule base honnête.

## Où placer l’entrée

1. **Côté chute.** Pour un contour extérieur, l’entrée part de la chute ; pour un trou, elle part de l’intérieur du trou (qui tombera).
2. **Loin des arêtes fonctionnelles.** Évitez une face d’appui, un trou de précision ou un bord visible ; le point d’entrée laisse presque toujours une marque.
3. **Dans un coin si possible.** Sur un contour extérieur, entrer près d’un angle cache la marque.
4. **Assez loin du contour.** Le cratère de perçage doit être entièrement dans la chute.
5. **Ordre de coupe.** Petits éléments intérieurs d’abord, contour extérieur en dernier, pour que la pièce ne bouge pas avant la fin.

## Forme de l’entrée et de la sortie

| Forme | Usage typique |
|---|---|
| Droite perpendiculaire | Simple, contours extérieurs |
| Arc tangent | Trous et contours où l’on veut éviter une encoche |
| Droite + arc | Compromis courant en FAO plasma |
| Sortie courte ou nulle, surcoupe faible | Éviter l’entaille au point de fermeture |

Une **surcoupe** (overcut) trop longue entaille la pièce ; trop courte, elle laisse une languette. Réglez-la à l’essai, par petits pas.

## Sens de coupe

Le jet plasma tourne : un côté de la saignée est plus droit que l’autre. Avec un anneau de turbulence standard (rotation horaire), le côté droit dans le sens d’avance est en général le meilleur : on coupe les contours extérieurs **dans le sens horaire** et les trous **dans le sens antihoraire**. Vérifiez la recommandation de votre manuel : certains consommables tournent à l’inverse.

## Trous propres

- Les petits trous plasma ont un biseau et une conicité plus marqués. Les fabricants publient des recommandations (diamètre minimal par rapport à l’épaisseur, vitesse réduite, désactivation du THC dans le trou) ; Hypertherm commercialise par exemple sa technologie True Hole sur certains systèmes haut de gamme.
- Désactivez ou verrouillez le **THC** sur les petits trous et dans les coins (fonction « anti-plongée » de la commande) : la vitesse baisse, la tension monte, la torche plongerait.
- Pour un trou fonctionnel précis : percer ou aléser après, ou passer au laser.

## Perçage des tôles épaisses

Au-delà de la capacité de perçage indiquée par le fabricant, on perce « en mouvement » (moving pierce) ou on démarre depuis le bord (edge start). La capacité de perçage est **inférieure** à la capacité de coupe annoncée : lisez bien les deux chiffres dans la fiche de la source.

## Erreurs fréquentes

| Symptôme | Cause probable |
|---|---|
| Buse et bouclier usés vite, projections collées | Hauteur de perçage trop basse ou délai trop court |
| Pas de traversée, arc qui s’éteint | Délai trop court pour l’épaisseur |
| Cratère qui mord la pièce | Entrée trop courte ou mal placée |
| Encoche au point de fermeture | Surcoupe trop longue, sortie mal orientée |
| Torche qui plonge dans les trous | THC actif à basse vitesse |

## FAQ

### Faut-il une entrée pour le marquage ?
Non : le marquage se fait à faible courant, sans perçage traversant. Utilisez l’opération de marquage du FAO.

### Délai plus long = plus sûr ?
Pas forcément : un délai trop long élargit le cratère et use la buse. Suivez la charte, puis ajustez à l’essai.

## À valider en atelier (Michaël)

- Vos longueurs d’entrée types selon l’épaisseur sur vos tables.
- Le sens de coupe recommandé pour vos consommables.

## Sources

- [Hypertherm — How to use the cut charts](https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/bzv0315406918125.html), consulté le 26 novembre 2026.
- [Hypertherm — Mild steel, 125 A, air (exemple de charte avec hauteur et délai de perçage)](https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/vkl1065237733940.html).
- [LinuxCNC — Plasma Cutting Primer](https://linuxcnc.org/docs/stable/html/plasma/plasma-cnc-primer.html).
- [Langmuir Systems — THC guide (Torch Speed Cutoff, SMART Voltage)](https://www.langmuirsystems.com/pages/thc-guide).
=== en
Piercing is the hardest moment for consumables: molten metal is blown back toward the torch before the arc breaks through. The lead-in then carries the stabilized arc to the contour, and the lead-out ends it without marking the part. Set well, they make the difference between a clean part and a part to grind.

## The settings and where they come from

| Setting | Job | Source of the value |
|---|---|---|
| Pierce height | Protect the torch from spatter | Your source’s cut chart (often expressed relative to cut height) |
| Pierce delay | Let the arc break through before moving | Cut chart, by thickness |
| Cut height | Distance while cutting | Cut chart |
| Arc voltage (THC) | Height control | Chart; automatic mode depends on the control |
| Lead-in length | Stable arc before the contour | Testing; depends on thickness and pierce |

> [!WARN] Do not copy a “universal” height or delay from a forum. Hypertherm charts, for example, give these values by thickness, amperage, gas and consumable set — the only honest baseline.

## Where to place the lead-in

1. **Scrap side.** For an outside profile, the lead-in starts in the scrap; for a hole, it starts inside the hole (which will drop).
2. **Away from functional edges.** Avoid a datum face, a precision hole or a visible edge; the entry point almost always leaves a mark.
3. **Into a corner when possible.** On an outside profile, entering near a corner hides the mark.
4. **Far enough from the contour.** The pierce crater must sit entirely in the scrap.
5. **Cut order.** Small inside features first, outside profile last, so the part does not move before the end.

## Lead-in and lead-out shapes

| Shape | Typical use |
|---|---|
| Straight perpendicular | Simple, outside profiles |
| Tangent arc | Holes and profiles where you want to avoid a nick |
| Line + arc | Common compromise in plasma CAM |
| Short or no lead-out, small overcut | Avoid a gouge at the closing point |

Too long an **overcut** gouges the part; too short leaves a tab. Tune it by testing in small steps.

## Cut direction

The plasma jet swirls: one side of the kerf is squarer than the other. With a standard swirl ring (clockwise), the right side in the direction of travel is usually the good side: cut outside profiles **clockwise** and holes **counter-clockwise**. Check your manual: some consumables swirl the other way.

## Clean holes

- Small plasma holes show more bevel and taper. Manufacturers publish guidance (minimum diameter relative to thickness, reduced speed, THC off in the hole); Hypertherm, for example, markets True Hole technology on some high-end systems.
- Disable or lock the **THC** on small holes and in corners (the control’s anti-dive function): speed drops, voltage rises, the torch would dive.
- For a precise functional hole: drill or ream afterward, or go to laser.

## Piercing thick plate

Beyond the maker’s stated pierce capacity, use a moving pierce or an edge start. Pierce capacity is **lower** than the advertised cut capacity: read both numbers on the source’s spec sheet.

## Common mistakes

| Symptom | Likely cause |
|---|---|
| Nozzle and shield wear fast, stuck spatter | Pierce height too low or delay too short |
| No break-through, arc goes out | Delay too short for the thickness |
| Crater bites into the part | Lead-in too short or badly placed |
| Nick at the closing point | Overcut too long, lead-out badly oriented |
| Torch dives in holes | THC active at low speed |

## FAQ

### Do I need a lead-in for marking?
No: marking runs at low current without a through pierce. Use the CAM marking operation.

### Longer delay = safer?
Not necessarily: too long a delay widens the crater and wears the nozzle. Follow the chart, then tune by testing.

## For Michaël to review

- Your typical lead-in lengths by thickness on your tables.
- The recommended cut direction for your consumables.

## Sources

- [Hypertherm — How to use the cut charts](https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/bzv0315406918125.html), consulted November 26, 2026.
- [Hypertherm — Mild steel, 125 A, air (example chart with pierce height and delay)](https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/vkl1065237733940.html).
- [LinuxCNC — Plasma Cutting Primer](https://linuxcnc.org/docs/stable/html/plasma/plasma-cnc-primer.html).
- [Langmuir Systems — THC guide (Torch Speed Cutoff, SMART Voltage)](https://www.langmuirsystems.com/pages/thc-guide).
