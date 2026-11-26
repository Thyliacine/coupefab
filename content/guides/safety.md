---
id: safety
hub: shop
order: 1
nav: Sécurité et CNESST | Safety and CNESST
kicker: Atelier · sécurité | Shop · safety
level: debutant
schema: Article
tags: safety, ppe, fumes, ventilation, cnesst, rsst, plasma, laser, noise, uv, hexavalent chromium, combustible dust
related: plasma-cutting, fiber-laser, press-brake, buying-cnc-canada
fr_slug: securite-cnc-cnesst
en_slug: cnc-shop-safety
fr_title: Sécurité en atelier CNC : EPI, fumées, bruit, rayonnement et repères CNESST
en_title: CNC shop safety: PPE, fumes, noise, radiation and CNESST pointers
fr_desc: Les risques propres à la découpe plasma et laser, au routage et au pliage, l’équipement de protection adapté, la captation des fumées à la source et les références CNESST et RSST au Québec.
en_desc: The hazards specific to plasma and laser cutting, routing and bending, the right protective equipment, capturing fumes at the source, and CNESST and RSST references in Quebec.
---
=== fr
Ce guide n’est pas un programme de prévention : c’est un aide-mémoire pour repérer les risques des procédés CNC courants et savoir où chercher les exigences officielles. Au Québec, la référence est la **CNESST** et le **Règlement sur la santé et la sécurité du travail (RSST)**. Les manuels de sécurité des fabricants (sources plasma, lasers, presses) complètent ces obligations.

## Les risques par procédé

| Procédé | Risques principaux |
|---|---|
| Plasma | Fumées métalliques, rayonnement UV de l’arc, bruit, chocs électriques, brûlures, incendie ; hydrogène possible avec l’aluminium sur table à eau |
| Laser | Faisceau classe 4 (yeux, peau), fumées, incendie |
| Routeur | Poussières fines (bois, MDF), projection de pièces, bruit, incendie de poussières |
| Fraiseuse / tour | Happement (vêtements, cheveux), projections de copeaux, fluides de coupe |
| Presse plieuse | Écrasement au point de pincement, chute de pièces |
| Jet d’eau | Jet haute pression, bruit, boues |

## Fumées : capter à la source

La CNESST rappelle que la ventilation locale par extraction doit capter les fumées **au plus près du point d’émission**, que le travailleur ne doit pas se trouver entre la source et l’aspiration, et que l’air extrait doit être rejeté loin des prises d’air neuf. Pour le coupage et le soudage, le RSST exige une ventilation locale aux postes fixes qui produisent des fumées.

> [!WARN] Découper ou souder de l’**inox** produit des fumées contenant du chrome, notamment du chrome hexavalent, dont l’exposition est réglementée. Les tôles **galvanisées** dégagent des fumées de zinc. Les revêtements (peinture, huile) ajoutent leurs propres contaminants : nettoyez avant de couper quand c’est possible.

## Équipement de protection individuelle

| Risque | EPI typique | Référence |
|---|---|---|
| Arc plasma (UV) | Lunettes ou visière à teinte adaptée au courant | CSA W117.2 (sécurité en soudage et coupage) ; manuel de la source |
| Laser (entretien faisceau ouvert) | Lunettes spécifiques à la longueur d’onde et à la puissance | IEC 60825-1, ANSI Z136.1 |
| Bruit | Protecteurs auditifs selon l’exposition mesurée | RSST |
| Projections, copeaux | Lunettes de sécurité, écran facial | CSA Z94.3 |
| Brûlures | Vêtements ignifuges, gants de cuir | — |
| Fumées résiduelles | Protection respiratoire si l’exposition dépasse les valeurs, après la ventilation | RSST, programme de protection respiratoire |

L’EPI vient **après** les mesures à la source (enceinte, captation, protecteurs) : c’est la dernière barrière.

## Poussières combustibles

Les poussières fines d’aluminium (tables aspirantes plasma) et de bois (routeur) peuvent brûler ou exploser dans un dépoussiéreur. Ne mélangez pas des poussières incompatibles dans un même collecteur, videz régulièrement, et suivez les consignes du fabricant du dépoussiéreur.

## Protecteurs de machines

Le RSST impose que les zones dangereuses des machines soient rendues inaccessibles (protecteurs, dispositifs de protection) et encadre les interventions de maintenance par le **cadenassage**. Une presse plieuse, une fraiseuse ou une table CNC n’y échappent pas.

## Liste de vérification d’un poste de découpe

- [ ] Captation des fumées à la source, en marche pendant la coupe
- [ ] EPI adapté au procédé (teinte, longueur d’onde, ouïe, yeux)
- [ ] Extincteur adapté à proximité, zone dégagée des combustibles
- [ ] Arrêt d’urgence accessible et testé
- [ ] Cadenassage connu pour l’entretien (électricité, air, eau)
- [ ] Fiches de données de sécurité des fluides et des matières disponibles

## FAQ

### Une table à eau dispense-t-elle de la ventilation ?
Non. Elle réduit une partie des fumées, mais la CNESST et les fabricants recommandent quand même une captation adaptée. Évaluez l’exposition réelle.

## À valider en atelier (Michaël)

- Les pratiques de votre atelier (captation, EPI) qui pourraient servir d’exemple.

## Sources

- [CNESST — Ventilation des lieux de travail](https://www.cnesst.gouv.qc.ca/fr/prevention-securite/identifier-corriger-risques/liste-informations-prevention/ventilation-lieux-travail), consulté le 26 novembre 2026.
- [Règlement sur la santé et la sécurité du travail (RSST), LégisQuébec](https://www.legisquebec.gouv.qc.ca/fr/document/rc/S-2.1,%20r.%2013).
- [CSA W117.2:25 — Safety in welding, cutting and allied processes](https://www.csagroup.org/store/product/CSA_W117.2:25/).
- [Hypertherm — manuels de sécurité des sources plasma](https://www.hypertherm.com/).
=== en
This guide is not a prevention program: it is a reminder to spot the hazards of common CNC processes and know where the official requirements live. In Quebec, the reference is **CNESST** and the **Regulation respecting occupational health and safety (RSST)**. Manufacturers’ safety manuals (plasma sources, lasers, presses) complement these obligations.

## Hazards by process

| Process | Main hazards |
|---|---|
| Plasma | Metal fumes, arc UV radiation, noise, electric shock, burns, fire; possible hydrogen with aluminum over a water table |
| Laser | Class 4 beam (eyes, skin), fumes, fire |
| Router | Fine dust (wood, MDF), thrown parts, noise, dust fires |
| Mill / lathe | Entanglement (clothing, hair), flying chips, cutting fluids |
| Press brake | Crushing at the pinch point, falling parts |
| Waterjet | High-pressure jet, noise, sludge |

## Fumes: capture at the source

CNESST stresses that local exhaust ventilation must capture fumes **as close as possible to the emission point**, that the worker must not stand between the source and the hood, and that exhaust air must be discharged away from fresh-air intakes. For cutting and welding, the RSST requires local exhaust at fixed stations that produce fumes.

> [!WARN] Cutting or welding **stainless** produces fumes containing chromium, including hexavalent chromium, whose exposure is regulated. **Galvanized** sheet gives off zinc fumes. Coatings (paint, oil) add their own contaminants: clean before cutting when possible.

## Personal protective equipment

| Hazard | Typical PPE | Reference |
|---|---|---|
| Plasma arc (UV) | Glasses or face shield with a shade suited to the current | CSA W117.2 (safety in welding and cutting); source manual |
| Laser (open-beam service) | Eyewear specific to wavelength and power | IEC 60825-1, ANSI Z136.1 |
| Noise | Hearing protection per measured exposure | RSST |
| Spatter, chips | Safety glasses, face shield | CSA Z94.3 |
| Burns | Flame-resistant clothing, leather gloves | — |
| Residual fumes | Respirator if exposure exceeds limits, after ventilation | RSST, respiratory protection program |

PPE comes **after** source controls (enclosure, capture, guards): it is the last barrier.

## Combustible dust

Fine aluminum dust (plasma downdraft tables) and wood dust (routers) can burn or explode in a dust collector. Do not mix incompatible dusts in one collector, empty regularly, and follow the collector maker’s instructions.

## Machine guarding

The RSST requires machine danger zones to be made inaccessible (guards, safeguarding devices) and governs maintenance work through **lockout**. Press brakes, mills and CNC tables are no exception.

## Cutting station checklist

- [ ] Source fume capture running during cutting
- [ ] PPE suited to the process (shade, wavelength, hearing, eyes)
- [ ] Suitable extinguisher nearby, area clear of combustibles
- [ ] Emergency stop reachable and tested
- [ ] Lockout known for maintenance (electricity, air, water)
- [ ] Safety data sheets for fluids and materials available

## FAQ

### Does a water table remove the need for ventilation?
No. It cuts part of the fumes, but CNESST and manufacturers still recommend suitable capture. Assess actual exposure.

## For Michaël to review

- Your shop’s practices (capture, PPE) that could serve as an example.

## Sources

- [CNESST — Workplace ventilation (French)](https://www.cnesst.gouv.qc.ca/fr/prevention-securite/identifier-corriger-risques/liste-informations-prevention/ventilation-lieux-travail), consulted November 26, 2026.
- [Regulation respecting occupational health and safety (RSST), LégisQuébec](https://www.legisquebec.gouv.qc.ca/en/document/cr/S-2.1,%20r.%2013).
- [CSA W117.2:25 — Safety in welding, cutting and allied processes](https://www.csagroup.org/store/product/CSA_W117.2:25/).
- [Hypertherm — plasma source safety manuals](https://www.hypertherm.com/).
