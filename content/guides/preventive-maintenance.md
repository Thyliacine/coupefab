---
id: preventive-maintenance
hub: shop
order: 45
nav: Entretien préventif | Preventive maintenance
kicker: Atelier · entretien | Shop · maintenance
level: debutant
schema: HowTo
tags: entretien, maintenance, preventive maintenance, calendrier, schedule, haas, vmc, lubrification, lubrication, liquide de coupe, coolant, filtre à air, air filter, powermax, hypertherm, laser, lentille, cover glass, vitre de protection, raytools
related: lockout-cadenassage, coolant, consumables, laser-troubleshooting
fr_slug: entretien-preventif-cnc-plasma-laser
en_slug: preventive-maintenance-cnc-plasma-laser
fr_title: Entretien préventif : calendrier pour centre d’usinage, plasma et laser fibre
en_title: Preventive maintenance: a schedule for machining centres, plasma and fiber laser
fr_desc: Quoi vérifier chaque jour, chaque semaine, chaque mois, aux six mois et chaque année sur un centre d’usinage Haas, une source plasma Powermax et une tête laser fibre, d’après les calendriers publiés par les fabricants.
en_desc: What to check daily, weekly, monthly, every six months and yearly on a Haas machining centre, a Powermax plasma system and a fiber laser head, based on the makers’ published schedules.
---
=== fr
La plupart des alarmes « mystérieuses » viennent d’un entretien sauté : réservoir de lubrification vide, filtre d’armoire bouché, air humide dans la source plasma, vitre de protection sale sur la tête laser. Ce guide reprend les **calendriers publiés par les fabricants** et les regroupe par fréquence. Le manuel de **votre** machine a toujours le dernier mot.

> [!WARN] Avant tout entretien dans la zone dangereuse d’une machine : cadenassage ou méthode équivalente (voir [[lockout-cadenassage]]).

## Centre d’usinage (Haas VMC)

Haas publie un calendrier d’entretien pour ses centres d’usinage verticaux (document RD0080). En voici l’essentiel, regroupé par fréquence :

| Fréquence | Point d’entretien (Haas) |
|---|---|
| Chaque jour | Inspecter les vitres de l’enceinte (dommages) ; vérifier le fonctionnement du verrouillage de porte |
| Chaque semaine | Enlever les copeaux du changeur d’outil ; vérifier le niveau et la **concentration** du liquide de coupe (registre) ; vérifier la pression du régulateur d’air de la broche |
| Chaque mois | Niveau du réservoir de lubrification des axes ; niveau du réservoir de lubrification de broche ; nettoyer les évents et filtres d’air du variateur (armoire électrique) ; inspecter et lubrifier les soufflets/capots de glissières ; pression de l’équilibreur (contrepoids) ; niveau d’huile de la boîte de vitesses |
| Aux six mois | Test de lubrification des axes et de la broche ; inspecter les boyaux (fissures) ; vider et nettoyer complètement le bac et remplacer le liquide de coupe ; nettoyer le filtre du liquide de coupe ; vérifier piles et étalonnage du palpeur |
| Chaque année | Graisser les cames du changeur d’outil (SMTC) ; remplacer l’huile de la boîte de vitesses ; nettoyer l’électrovanne de purge d’air ; mesurer la force de la barre de tirage (*drawbar*) |
| Au besoin | Nettoyer et lubrifier le cône de broche ; graisser les tirettes (*pull studs*) ; nettoyer le tamis du liquide de coupe |

> [!TIP] Une alarme de lubrification ou de basse pression d’air sur Haas pointe souvent vers un point de cette liste. Cherchez le numéro dans la [recherche de codes d’erreur](/codes-erreur/?b=haas).

Les autres fabricants (Fanuc-based, Doosan, Okuma, Mazak…) publient des calendriers semblables dans le manuel d’entretien de la machine : utilisez-les, les intervalles diffèrent.

## Source plasma (Hypertherm Powermax SYNC)

Le manuel de l’opérateur des Powermax65/85/105 SYNC (810470) donne ces tâches régulières :

| Fréquence | Point d’entretien (Hypertherm) |
|---|---|
| À chaque utilisation | Lire les voyants de la source et corriger tout défaut (voir les codes) ; examiner la cartouche : bien installée, usure |
| À chaque changement de cartouche ou chaque semaine (le plus fréquent des deux) | Tester le **commutateur de verrouillage de la torche** : verrouillé, la torche ne doit pas s’allumer ; déverrouillé, elle doit s’allumer (torche machine : commande START/STOP depuis la CNC) |
| Aux trois mois | Examiner le cordon et la fiche d’alimentation ; les étiquettes ; la gâchette (torche manuelle) ; le corps de torche (fissures, fils exposés) ; le faisceau de torche |
| Régulièrement | Bol et élément du **filtre à air** : sans huile ni saleté, joint torique en bon état ; remplacer l’élément quand il est sale, surtout en milieu poussiéreux, chaud ou humide |

Hypertherm insiste sur un **air propre et sec** : l’huile, l’eau et la saleté endommagent les composants internes et réduisent la qualité de coupe et la durée des consommables. Une matière jaune dans le bol indique souvent de l’huile dans la conduite d’air.

> [!WARN] Gants isolants pour changer les cartouches (chaudes, et risque de choc si la source est sous tension et la torche non verrouillée). Torches à allumage instantané : source hors tension **ou** commutateur en position verrouillée avant le changement.

## Tête laser fibre (exemple Raytools BM110)

Le manuel de la tête Raytools BM110 recommande :

| Fréquence | Point d’entretien (Raytools) |
|---|---|
| Chaque semaine | Nettoyer la **vitre de protection** (*cover glass*) |
| Aux 2 à 3 mois | Nettoyer les lentilles de collimation et de focalisation |

Outils indiqués par Raytools : gants ou doigtiers antipoussière, coton-tige en polyester, éthanol absolu, poire à air (air comprimé pur). Le manuel signale aussi que les impuretés du gaz de coupe (hydrocarbures, vapeur d’eau) peuvent endommager la lentille et faire varier la puissance. Sur un laser de production, on inspecte la vitre bien plus souvent (souvent à chaque quart) : c’est une pratique d’atelier, pas une exigence du manuel.

## Mettre en place un registre simple

1. **Une fiche par machine**, affichée près de la commande : tâche, fréquence, initiales, date.
2. **Lier aux alarmes** : quand une alarme revient, noter la date dans la même fiche ; on voit vite si c’est un entretien en retard.
3. **Stock minimal** : filtres, huile de lubrification, cartouches ou consommables, vitres de protection.
4. **Réviser** les intervalles après six mois selon l’usage réel (matériaux poussiéreux, deux quarts, etc.).

## Liste de vérification

- [ ] Calendrier du fabricant téléchargé pour chaque machine
- [ ] Fiche d’entretien affichée et tenue à jour
- [ ] Niveaux de lubrification vérifiés chaque mois (ou selon le manuel)
- [ ] Concentration du liquide de coupe mesurée chaque semaine
- [ ] Filtre d’air de la source plasma inspecté
- [ ] Vitre de protection laser nettoyée selon le manuel
- [ ] Pièces d’usure en stock

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| Remplir le réservoir de lubrification sans chercher pourquoi il se vide vite | Fuite ou boyau fissuré non trouvé |
| Ignorer la concentration du liquide de coupe | Corrosion, odeur, mauvaise durée d’outil (voir [[coolant]]) |
| Air comprimé non filtré vers la source plasma | Consommables usés vite, défauts de pression |
| Nettoyer une lentille avec un chiffon ordinaire | Rayures, lentille à remplacer |

## FAQ

### Les intervalles Haas s’appliquent-ils à ma machine d’une autre marque ?

Non, prenez-les comme exemple de ce qu’il faut surveiller. Les intervalles et les produits (huile, graisse) viennent du manuel de votre machine.

### Faut-il un logiciel de GMAO ?

Pas pour commencer. Une fiche papier ou un tableur bien tenu suffit ; l’important est la régularité.

## À valider en atelier (Michaël)

- Les intervalles que nous suivons réellement par machine.
- Les produits (huiles, graisses, filtres) utilisés chez nous.

## Sources

- [Haas — VMC Maintenance Schedule (RD0080, rév. C)](https://haascnc.com/service/troubleshooting-and-how-to/reference-documents/vmc-maintenance-schedule.html). Consulté le 26 novembre 2026.
- [Hypertherm — Powermax65/85/105 SYNC Operator Manual (810470), chapitre 7 « Complete Regular Maintenance Tasks »](https://xnet.hypertherm.com/Xnet/library/download/?file=HYP254734). Consulté le 26 novembre 2026.
- [Raytools — BM110 Auto Focus Laser Cutting Head, User Manual (PDF)](https://www.empower.cn/uploads/upload/20250208/User%20Manual-BM110_3.3KW%20Auto%20Focus%20Laser%20Cutting%20Head_2023.11.pdf) : section 5.1 « Cleaning Lens ». Consulté le 26 novembre 2026.

=== en
Most “mystery” alarms come from skipped maintenance: an empty lube tank, a clogged cabinet filter, wet air in the plasma system, a dirty cover glass on the laser head. This guide takes the **schedules the makers publish** and groups them by frequency. **Your** machine’s manual always has the final word.

> [!WARN] Before any maintenance in a machine’s danger zone: lockout or an equivalent method (see [[lockout-cadenassage]]).

## Machining centre (Haas VMC)

Haas publishes a maintenance schedule for its vertical machining centres (document RD0080). Here are the essentials, grouped by frequency:

| Frequency | Maintenance item (Haas) |
|---|---|
| Daily | Inspect enclosure windows for damage; check door interlock operation |
| Weekly | Clean chips from the tool changer; check coolant level and **concentration** (log sheet); check spindle air regulator pressure |
| Monthly | Axis lube reservoir level; spindle lube tank level; clean vector drive air vents/filter (electrical cabinet); inspect and lubricate way covers; counterbalance pressure; gearbox oil level |
| Every six months | Axis and spindle lubrication tests; inspect hoses for cracking; fully clean the coolant tank and replace coolant; clean the coolant filter; check probe batteries and calibration |
| Yearly | Grease tool changer cams (SMTC); replace gearbox oil; clean the air purge solenoid; measure drawbar force |
| As needed | Clean and lubricate the spindle taper; grease pull studs; clean the coolant filter screen |

> [!TIP] A lube or low-air alarm on a Haas often points to an item on this list. Look the number up in the [error code lookup](/en/error-codes/?b=haas).

Other makers (Fanuc-based builders, Doosan, Okuma, Mazak…) publish similar schedules in the machine’s maintenance manual: use those, the intervals differ.

## Plasma system (Hypertherm Powermax SYNC)

The Powermax65/85/105 SYNC operator manual (810470) lists these regular tasks:

| Frequency | Maintenance item (Hypertherm) |
|---|---|
| Every use | Read the power supply LEDs and fix any fault (see the codes); examine the cartridge: correctly installed, wear |
| Every cartridge change or weekly (whichever is more frequent) | Test the **torch-lock switch**: locked, the torch must not fire; unlocked, it must fire (machine torch: START/STOP from the CNC) |
| Every three months | Examine the power cord and plug; labels; trigger (hand torch); torch body (cracks, exposed wires); torch lead |
| Regularly | **Air filter** bowl and element: no oil or dirt, O-ring in good shape; replace the element when dirty, especially in dusty, hot or humid shops |

Hypertherm stresses **clean, dry air**: oil, water and dirt damage internal parts and cut both cut quality and consumable life. Yellow material in the bowl often means oil is getting into the air line.

> [!WARN] Insulated gloves to change cartridges (hot, and a shock risk if the system is on and the torch is not locked). Instant-on torches: power supply off **or** torch-lock switch in the locked position before changing.

## Fiber laser head (example: Raytools BM110)

The Raytools BM110 head manual recommends:

| Frequency | Maintenance item (Raytools) |
|---|---|
| Weekly | Clean the **cover glass** |
| Every 2–3 months | Clean the collimating and focusing lenses |

Tools Raytools lists: dust-proof gloves or finger cots, polyester swab, absolute ethanol, air blower (clean compressed air). The manual also warns that impurities in the assist gas (hydrocarbons, water vapour) can damage the lens and make power fluctuate. On a production laser, people inspect the cover glass far more often (often every shift): that is shop practice, not a manual requirement.

## Set up a simple log

1. **One sheet per machine**, posted by the control: task, frequency, initials, date.
2. **Tie it to alarms**: when an alarm comes back, note the date on the same sheet; you quickly see whether maintenance is overdue.
3. **Minimum stock**: filters, way lube, cartridges or consumables, cover glasses.
4. **Review** the intervals after six months based on real use (dusty materials, two shifts, etc.).

## Checklist

- [ ] Maker’s schedule downloaded for each machine
- [ ] Maintenance sheet posted and kept up to date
- [ ] Lube levels checked monthly (or per the manual)
- [ ] Coolant concentration measured weekly
- [ ] Plasma air filter inspected
- [ ] Laser cover glass cleaned per the manual
- [ ] Wear parts in stock

## Common mistakes

| Mistake | Consequence |
|---|---|
| Topping up way lube without asking why it empties fast | Leak or cracked hose goes unnoticed |
| Ignoring coolant concentration | Rust, smell, poor tool life (see [[coolant]]) |
| Unfiltered shop air to the plasma system | Fast consumable wear, pressure faults |
| Cleaning a lens with an ordinary rag | Scratches, lens to replace |

## FAQ

### Do the Haas intervals apply to my machine from another brand?

No, treat them as an example of what to watch. The intervals and products (oil, grease) come from your machine’s manual.

### Do I need CMMS software?

Not to start. A paper sheet or a well-kept spreadsheet is enough; consistency is what matters.

## For Michaël to review

- The intervals we actually follow per machine.
- The products (oils, greases, filters) we use.

## Sources

- [Haas — VMC Maintenance Schedule (RD0080, rev. C)](https://haascnc.com/service/troubleshooting-and-how-to/reference-documents/vmc-maintenance-schedule.html). Consulted November 26, 2026.
- [Hypertherm — Powermax65/85/105 SYNC Operator Manual (810470), chapter 7 “Complete Regular Maintenance Tasks”](https://xnet.hypertherm.com/Xnet/library/download/?file=HYP254734). Consulted November 26, 2026.
- [Raytools — BM110 Auto Focus Laser Cutting Head, User Manual (PDF)](https://www.empower.cn/uploads/upload/20250208/User%20Manual-BM110_3.3KW%20Auto%20Focus%20Laser%20Cutting%20Head_2023.11.pdf): section 5.1 “Cleaning Lens”. Consulted November 26, 2026.
