---
id: plasma-cutting
hub: process
order: 1
nav: Plasma CNC | CNC plasma
kicker: Procédé · découpe thermique | Process · thermal cutting
level: debutant
schema: Article
tags: plasma, cnc, thc, air plasma, high definition, hypertherm, table, water table, downdraft
related: kerf, lead-ins-pierce, sheetcam, plasma-troubleshooting
prices: yes
fr_slug: decoupe-plasma-cnc
en_slug: cnc-plasma-cutting
fr_title: Découpe plasma CNC : comment ça marche et comment bien démarrer
en_title: CNC plasma cutting: how it works and how to start right
fr_desc: Principe de l’arc plasma, plasma à l’air ou haute définition, contrôle de hauteur (THC), table à eau ou aspirante, chaîne logicielle et réglages : la vue d’ensemble pour choisir et réussir ses premières coupes.
en_desc: How the plasma arc works, air versus high-definition plasma, torch height control (THC), water or downdraft table, software chain and settings: the overview to choose well and nail your first cuts.
---
=== fr
La découpe plasma fait fondre le métal avec un arc électrique concentré dans un gaz ionisé, puis chasse le métal fondu par le jet. Elle coupe tous les métaux conducteurs (acier, inox, aluminium) rapidement, pour un coût machine bien plus bas qu’un laser. Son point faible : la saignée plus large et un léger biseau.

## La chaîne complète

| Maillon | Rôle | Guides |
|---|---|---|
| DAO | Dessiner la pièce, exporter un DXF propre | [DXF](/guides/dxf-bonnes-pratiques/), [BricsCAD](/guides/bricscad-dxf/) |
| FAO | Kerf, entrées, ordre, imbrication, post | [SheetCam](/guides/debuter-sheetcam/), [Fusion](/guides/fusion-fao-debuter/), [ProNest](/guides/pronest-imbrication/) |
| Commande | Exécuter le G-code, gérer IHS et THC | [LinuxCNC](/guides/linuxcnc-qtplasmac/), [Mach](/guides/mach3-mach4/), [FireControl](/guides/firecontrol-langmuir/) |
| Source plasma | Courant, gaz, consommables | [Consommables](/guides/consommables-plasma-canada/) |
| Table | Mécanique, support de tôle, captation des fumées | [Acheter une CNC](/guides/acheter-cnc-canada/) |

## Air ou haute définition ?

| | Plasma à l’air (type Powermax) | Haute définition / précision (type XPR) |
|---|---|---|
| Gaz | Air comprimé | Oxygène, azote, mélanges selon la matière |
| Qualité | Bonne en tôle mince et moyenne | Biseau réduit, meilleurs trous |
| Coût | Machine et consommables abordables | Investissement industriel |
| Atelier type | Petits ateliers, fabrication générale | Production, pièces de précision |

## Les réglages qui comptent

- **Courant (ampérage)** et **jeu de consommables** assortis : choisis dans la charte selon l’épaisseur.
- **Vitesse** : trop lente = scories en bas et saignée large ; trop rapide = arc qui traîne, scories difficiles, biseau.
- **Hauteur de coupe**, maintenue par le **THC** (contrôle de hauteur par la tension d’arc).
- **Hauteur et délai de perçage**, et **IHS** (palpage initial de la tôle).
- **Air** propre et sec, à la pression du manuel.

Tout part de la **charte de coupe** du fabricant : voir [Kerf et qualité de coupe](/guides/kerf-qualite-coupe/) et [Entrées et perçage](/guides/entrees-sorties-percage-plasma/).

## Le THC en deux phrases

La tension de l’arc est proportionnelle à sa longueur : si la torche s’approche de la tôle, la tension baisse. Le THC remonte ou descend l’axe Z pour garder la tension visée (Langmuir décrit précisément ce principe pour son LS-THC). Il doit être **verrouillé** dans les coins et les petits trous, où la vitesse chute.

## Table à eau ou table aspirante

| | Table à eau | Table aspirante (downdraft) |
|---|---|---|
| Fumées | Une partie piégée par l’eau | Captées par un dépoussiéreur |
| Déformation | Refroidit la tôle | Pas de refroidissement |
| Entretien | Vidange, boues, gel l’hiver dans un local non chauffé | Filtres, risque de poussières combustibles (aluminium) |

> [!WARN] Couper de l’aluminium au-dessus d’une table à eau peut produire de l’hydrogène qui s’accumule sous la tôle : les fabricants de sources et de tables publient des mises en garde (agitation de l’eau, évacuation). Lisez celles de votre équipement.

## Premières coupes : la méthode

1. Choisir une épaisseur courante (par exemple de l’acier doux de 3 à 6 mm).
2. Prendre la ligne exacte de la charte : courant, consommables, vitesse, hauteurs, délai.
3. Couper un coupon de mesure (carré + trou) — méthode dans le guide [Kerf](/guides/kerf-qualite-coupe/).
4. Régler le kerf dans le FAO, recouper.
5. Ajuster la vitesse par petits pas en lisant les scories — voir [Dépannage plasma](/guides/depannage-plasma-scories-biseau/).
6. Noter les réglages qui marchent dans la bibliothèque d’outils du FAO.

## FAQ

### Quelle épaisseur peut-on couper ?
Les fabricants distinguent capacité de **perçage**, capacité de **coupe de production** et capacité de **séparation** (coupe lente, qualité médiocre). Pour une table CNC, regardez la capacité de perçage et de production, pas la séparation.

### Le plasma remplace-t-il un laser ?
Pour beaucoup de pièces de structure et de fabrication générale, oui. Pour des petits trous précis, des détails fins et des bords sans biseau, le laser fibre fait mieux. Voir [Laser fibre](/guides/laser-fibre/).

## À valider en atelier (Michaël)

- Les sources et tables les plus courantes chez vos clients et collègues.
- Vos réglages de démarrage favoris pour une première coupe.

## Sources

- [LinuxCNC — Plasma Cutting Primer](https://linuxcnc.org/docs/stable/html/plasma/plasma-cnc-primer.html), consulté le 26 novembre 2026.
- [Langmuir Systems — THC guide](https://www.langmuirsystems.com/pages/thc-guide).
- [Hypertherm — How to use the cut charts](https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/bzv0315406918125.html).
=== en
Plasma cutting melts metal with an electric arc constricted in an ionized gas, then blows the molten metal out with the jet. It cuts every conductive metal (steel, stainless, aluminum) quickly, for a machine cost far below a laser. Its weak points: a wider kerf and a slight bevel.

## The full chain

| Link | Job | Guides |
|---|---|---|
| CAD | Draw the part, export a clean DXF | [DXF](/en/guides/dxf-best-practices/), [BricsCAD](/en/guides/bricscad-to-clean-dxf/) |
| CAM | Kerf, leads, order, nesting, post | [SheetCam](/en/guides/getting-started-sheetcam/), [Fusion](/en/guides/fusion-cam-getting-started/), [ProNest](/en/guides/pronest-nesting/) |
| Control | Run the G-code, handle IHS and THC | [LinuxCNC](/en/guides/linuxcnc-qtplasmac/), [Mach](/en/guides/mach3-mach4/), [FireControl](/en/guides/firecontrol-langmuir/) |
| Power source | Current, gas, consumables | [Consumables](/en/guides/plasma-consumables-canada/) |
| Table | Mechanics, sheet support, fume capture | [Buying a CNC](/en/guides/buying-cnc-canada/) |

## Air or high definition?

| | Air plasma (Powermax type) | High definition / precision (XPR type) |
|---|---|---|
| Gas | Compressed air | Oxygen, nitrogen, mixes by material |
| Quality | Good on thin and medium plate | Reduced bevel, better holes |
| Cost | Affordable machine and consumables | Industrial investment |
| Typical shop | Small shops, general fabrication | Production, precision parts |

## The settings that matter

- **Current (amperage)** and a matching **consumable set**: picked from the chart by thickness.
- **Speed**: too slow = bottom dross and wide kerf; too fast = trailing arc, hard dross, bevel.
- **Cut height**, held by **THC** (torch height control by arc voltage).
- **Pierce height and delay**, and **IHS** (initial height sensing).
- Clean, dry **air** at the manual’s pressure.

Everything starts from the maker’s **cut chart**: see [Kerf and cut quality](/en/guides/kerf-and-cut-quality/) and [Lead-ins and pierce](/en/guides/lead-ins-pierce-height/).

## THC in two sentences

Arc voltage is proportional to arc length: when the torch gets closer to the plate, voltage drops. THC raises or lowers Z to hold the target voltage (Langmuir describes this principle precisely for its LS-THC). It must be **locked** in corners and small holes, where speed drops.

## Water table or downdraft table

| | Water table | Downdraft table |
|---|---|---|
| Fumes | Partly trapped by water | Captured by a dust collector |
| Distortion | Cools the plate | No cooling |
| Upkeep | Draining, sludge, freezing in an unheated building | Filters, combustible dust risk (aluminum) |

> [!WARN] Cutting aluminum over a water table can produce hydrogen that collects under the plate: power source and table makers publish warnings (water agitation, venting). Read your equipment’s.

## First cuts: the method

1. Pick a common thickness (for example 3–6 mm mild steel).
2. Use the exact chart row: current, consumables, speed, heights, delay.
3. Cut a measuring coupon (square + hole) — method in the [Kerf](/en/guides/kerf-and-cut-quality/) guide.
4. Set kerf in CAM, recut.
5. Tune speed in small steps by reading the dross — see [Plasma troubleshooting](/en/guides/plasma-troubleshooting-dross-bevel/).
6. Save the settings that work in the CAM tool library.

## FAQ

### How thick can it cut?
Makers distinguish **pierce** capacity, **production cut** capacity and **severance** capacity (slow, poor-quality cut). For a CNC table, look at pierce and production capacity, not severance.

### Does plasma replace a laser?
For many structural and general fabrication parts, yes. For small precise holes, fine detail and bevel-free edges, fiber laser does better. See [Fiber laser](/en/guides/fiber-laser-cutting/).

## For Michaël to review

- The sources and tables most common among your customers and peers.
- Your favourite starting settings for a first cut.

## Sources

- [LinuxCNC — Plasma Cutting Primer](https://linuxcnc.org/docs/stable/html/plasma/plasma-cnc-primer.html), consulted November 26, 2026.
- [Langmuir Systems — THC guide](https://www.langmuirsystems.com/pages/thc-guide).
- [Hypertherm — How to use the cut charts](https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/bzv0315406918125.html).
