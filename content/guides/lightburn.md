---
id: lightburn
hub: software
group: cam
order: 70
mono: LB
nav: LightBurn | LightBurn
kicker: Logiciel · laser | Software · laser
level: debutant
schema: HowTo
tags: lightburn, laser, diode, co2, fiber, galvo, ruida, grbl, material test, cut settings, layers
related: fiber-laser, kerf, safety, dxf-best-practices
fr_slug: lightburn-laser
en_slug: lightburn-laser
fr_title: LightBurn : configurer sa machine laser, ses calques et ses paramètres de coupe
en_title: LightBurn: set up your laser, layers and cut settings
fr_desc: Core ou Pro selon le contrôleur (GCode, DSP Ruida, galvo), ajout de la machine, calques par couleur, vitesse et puissance, grille de test de matériau et compensation du kerf.
en_desc: Core or Pro depending on the controller (GCode, Ruida DSP, galvo), adding the machine, colour layers, speed and power, material test grid and kerf offset.
---
=== fr
**LightBurn** est le logiciel de préparation et de pilotage le plus répandu pour les lasers à diode, CO₂ et fibre galvo de petite et moyenne puissance. Il dessine, organise les calques et envoie directement le travail à la machine.

## Quelle licence

| Licence | Contrôleurs | Prix indicatif (USD, au 26 novembre 2026) |
|---|---|---|
| **Core** | Contrôleurs à base de G-code (grbl, Smoothieware, Marlin…) | 99 $ |
| **Pro** | G-code **+ DSP** (Ruida, Trocen, TopWisdom…) **+ galvo** | 199 $ |

La licence est perpétuelle avec **un an de mises à jour** ; ensuite, renouvellement optionnel. Un essai gratuit permet de vérifier la compatibilité avant d’acheter.

## Démarche

1. **Ajouter la machine** : détection automatique ou choix manuel du contrôleur ; zone de travail ; origine.
2. Importer ou dessiner (SVG, DXF, AI, PDF, images).
3. Assigner chaque objet à un **calque de couleur** ; un calque = un mode (ligne, remplissage, image, découpe) et ses paramètres.
4. Régler **vitesse**, **puissance** (min/max), nombre de passes, air assist, décalage Z.
5. **Prévisualiser** (temps estimé, ordre de coupe).
6. **Cadrer** (Frame) pour vérifier la position sur le matériau, puis lancer.

## Trouver les bons paramètres

> [!TIP] Utilisez l’outil **Test de matériau** (Material Test) : il grave une grille vitesse × puissance sur une chute. Notez le meilleur couple dans la **bibliothèque de matériaux** pour ne pas recommencer.

- **Kerf** : mesurez une pièce test et entrez le décalage de kerf dans le calque pour obtenir la cote — voir [Kerf](/guides/kerf-qualite-coupe/).
- **Ordre de coupe** : intérieurs avant extérieurs, pour que la pièce ne tombe pas avant la fin.

> [!WARN] Les lasers de classe 4 exigent des lunettes adaptées à la longueur d’onde, une extraction des fumées et une surveillance constante (risque d’incendie). Certains matériaux (PVC, vinyle) dégagent des gaz corrosifs et toxiques. Voir [Sécurité](/guides/securite-cnc-cnesst/).

## FAQ

### LightBurn pilote-t-il une découpeuse laser fibre industrielle ?
Non, en général : les machines industrielles de découpe de tôle ont leur propre commande et leur logiciel d’imbrication. LightBurn vise les machines de bureau, CO₂ à contrôleur DSP et galvos de marquage. Voir [Laser fibre](/guides/laser-fibre/).

## À valider en atelier (Michaël)

- Vos paramètres testés si vous avez un laser.

## Sources

- [LightBurn — Boutique et licences](https://lightburnsoftware.com/collections/frontpage), consulté le 26 novembre 2026.
- [LightBurn — Documentation](https://docs.lightburnsoftware.com/).
- [LightBurn — Material Test](https://docs.lightburnsoftware.com/latest/Reference/MaterialTest/).
=== en
**LightBurn** is the most widely used layout and control software for small and mid-power diode, CO₂ and fiber galvo lasers. It draws, organizes layers and sends the job straight to the machine.

## Which licence

| Licence | Controllers | Indicative price (USD, as of November 26, 2026) |
|---|---|---|
| **Core** | G-code based controllers (grbl, Smoothieware, Marlin…) | $99 |
| **Pro** | G-code **+ DSP** (Ruida, Trocen, TopWisdom…) **+ galvo** | $199 |

The licence is perpetual with **one year of updates**; renewal is optional afterwards. A free trial lets you confirm compatibility before buying.

## Workflow

1. **Add the machine**: auto-detect or pick the controller; work area; origin.
2. Import or draw (SVG, DXF, AI, PDF, images).
3. Assign each object to a **colour layer**; one layer = one mode (line, fill, image, cut) and its settings.
4. Set **speed**, **power** (min/max), passes, air assist, Z offset.
5. **Preview** (estimated time, cut order).
6. **Frame** to check position on the material, then start.

## Finding the right settings

> [!TIP] Use the **Material Test** tool: it engraves a speed × power grid on scrap. Save the best pair in the **material library** so you never redo it.

- **Kerf**: measure a test part and enter the kerf offset on the layer to hit size — see [Kerf](/en/guides/kerf-and-cut-quality/).
- **Cut order**: inside before outside, so the part doesn’t drop before the end.

> [!WARN] Class 4 lasers require wavelength-specific eyewear, fume extraction and constant supervision (fire risk). Some materials (PVC, vinyl) release corrosive, toxic gases. See [Safety](/en/guides/cnc-shop-safety/).

## FAQ

### Does LightBurn drive an industrial fiber laser cutter?
Generally no: industrial sheet cutting machines have their own control and nesting software. LightBurn targets desktop machines, CO₂ with DSP controllers and marking galvos. See [Fiber laser](/en/guides/fiber-laser-cutting/).

## For Michaël to review

- Your tested settings if you run a laser.

## Sources

- [LightBurn — Store and licences](https://lightburnsoftware.com/collections/frontpage), consulted November 26, 2026.
- [LightBurn — Documentation](https://docs.lightburnsoftware.com/).
- [LightBurn — Material Test](https://docs.lightburnsoftware.com/latest/Reference/MaterialTest/).
