---
id: lockout-cadenassage
hub: shop
order: 2
nav: Cadenassage (CNESST) | Lockout (CNESST)
kicker: Atelier · sécurité | Shop · safety
level: debutant
schema: HowTo
tags: cadenassage, lockout, tagout, loto, cnesst, rsst, 188.2, 188.3, 188.6, contrôle des énergies, energy control, csa z460, maintenance, déblocage, plasma, laser, presse plieuse, press brake
related: safety, alarm-crash-response, preventive-maintenance, press-brake
fr_slug: cadenassage-machines-cnc
en_slug: lockout-cnc-machines-quebec
fr_title: Cadenassage des machines CNC au Québec : ce que le RSST demande, en clair
en_title: Locking out CNC machines in Quebec: what the RSST requires, in plain words
fr_desc: Quand cadenasser une fraiseuse, un tour, une table plasma, un laser ou une presse plieuse, qui pose son cadenas, ce que doit contenir la fiche de cadenassage et les énergies qu’on oublie (air, hydraulique, gravité). D’après le guide de la CNESST.
en_desc: When to lock out a mill, lathe, plasma table, laser or press brake, who puts on a lock, what the lockout sheet must contain and the energies people forget (air, hydraulics, gravity). Based on the CNESST guide.
---
=== fr
Au Québec, le **cadenassage** est obligatoire en vertu du **Règlement sur la santé et la sécurité du travail (RSST)** avant tout travail dans la **zone dangereuse** d’une machine. Ce guide explique, en mots simples, ce que cela veut dire pour une fraiseuse, un tour, une table plasma, un laser ou une presse plieuse. Il ne remplace ni le règlement ni le programme de cadenassage de votre employeur.

> [!WARN] Le bouton d’arrêt d’urgence et la porte fermée **ne sont pas** du cadenassage. L’arrêt d’urgence arrête la machine ; il n’empêche pas quelqu’un d’autre de la remettre en marche, ni l’air, l’hydraulique ou la gravité de faire bouger une pièce.

## Quand faut-il cadenasser ?

L’article **188.2 du RSST**, tel que présenté par la CNESST, vise tout travail dans la zone dangereuse d’une machine, « notamment de montage, d’installation, d’ajustement, d’inspection, de décoinçage, de réglage, de mise hors d’usage, d’entretien, de désassemblage, de nettoyage, de maintenance, de remise à neuf, de réparation, de modification ou de déblocage ». Le cadenassage, ou à défaut une autre méthode qui assure une **sécurité équivalente**, doit alors être appliqué.

Exemples concrets en atelier :

| Machine | Situations typiques qui demandent le contrôle des énergies |
|---|---|
| Fraiseuse, tour | Débloquer le changeur d’outil ou le convoyeur à copeaux en entrant dans la zone, changer un essuie-glace de vis, nettoyer le bac sous la table |
| Table plasma | Vider ou nettoyer le bac à eau ou les lattes, intervenir sur le portique ou la torche au-delà du simple changement de consommables prévu par le fabricant |
| Laser fibre | Intervenir sur la tête de coupe, les lattes, le changeur de table |
| Presse plieuse | Changer ou ajuster des outils, intervenir sous le coulisseau (gravité et hydraulique) |

Le règlement prévoit deux exceptions (art. 188.2) : une machine qui dispose d’un **mode de commande spécifique** conforme à l’article 189.1 (un mode de réglage conçu pour travailler dans la zone en sécurité), et une machine à **source d’énergie unique** dont la fiche est **à portée de main et sous le contrôle exclusif** de la personne, sans énergie résiduelle (l’exemple de la CNESST : une scie à onglets).

## Chacun son cadenas

L’article **188.3** est simple : le cadenassage doit être fait par **chacune des personnes** ayant accès à la zone dangereuse, avec **son propre cadenas à cléage unique** (une seule clé l’ouvre). Deux personnes dans la machine = deux cadenas, souvent sur une boîte de cadenassage.

## Ce que la fiche de cadenassage doit contenir

L’employeur doit avoir une procédure par machine (art. 188.5). Selon l’article **188.6**, elle comprend :

1. l’identification de la machine ;
2. la personne responsable de la méthode de contrôle des énergies ;
3. l’identification et la localisation de tout dispositif de commande et de **toute source d’énergie** ;
4. l’identification et la localisation de **chaque point de coupure** ;
5. le type et la quantité de matériel requis (cadenas, moraillons, dispositifs pour vannes…) ;
6. les **étapes** pour contrôler les énergies ;
7. au besoin, la continuité lors d’un changement de personnel (transfert du matériel) ;
8. au besoin, les particularités : **énergie résiduelle ou emmagasinée** à libérer, EPI requis, autres mesures.

## Les énergies qu’on oublie sur des machines CNC

- **Électrique** : sectionneur principal de la machine. Attention à l’armoire : certains circuits (éclairage, prises, variateurs chargés) peuvent rester sous tension ; suivez le manuel du fabricant.
- **Pneumatique** : l’air du changeur d’outil, du serrage de broche, des vérins. Fermer et **purger** la conduite.
- **Hydraulique** : presse plieuse, mandrin hydraulique, serrage de palette. La pression peut rester dans les accumulateurs.
- **Gravité** : coulisseau de presse plieuse, axe Z ou tête qui peut descendre, pièce lourde sur un montage.
- **Thermique et chimique** : pièce chaude, liquide de coupe, gaz de coupe laser (oxygène, azote) dans les conduites.

> [!NOTE] La CNESST précise que ses exigences s’inspirent de la norme **CSA Z460** (*Maîtrise des énergies dangereuses : cadenassage et autres méthodes*). Pour la construction, c’est le Code de sécurité pour les travaux de construction qui s’applique.

## Liste de vérification

- [ ] Fiche de cadenassage de la machine disponible sur place
- [ ] Personnes touchées prévenues
- [ ] Machine arrêtée normalement (cycle terminé, broche arrêtée)
- [ ] Chaque source d’énergie coupée au point de coupure indiqué
- [ ] Mon propre cadenas posé (et celui de chaque intervenant)
- [ ] Énergies résiduelles libérées : air purgé, pression hydraulique à zéro, axes et coulisseau bloqués mécaniquement
- [ ] **Vérification** : tentative de démarrage, la machine ne réagit pas ; remettre le sélecteur à l’arrêt
- [ ] À la fin : outils retirés, protecteurs remis, personnes à l’écart, cadenas retirés par leurs propriétaires

## Erreurs fréquentes

| Erreur | Pourquoi c’est dangereux |
|---|---|
| Se fier à l’arrêt d’urgence | Quelqu’un peut réarmer et redémarrer |
| Un seul cadenas pour l’équipe | Le premier qui part enlève la protection des autres |
| Couper l’électricité sans purger l’air | Un vérin ou le changeur d’outil bouge encore |
| Ne pas tester le démarrage | Mauvais sectionneur coupé, machine encore alimentée |
| Ignorer la gravité | Coulisseau ou axe Z qui descend |

## FAQ

### Je change seulement les consommables plasma. Faut-il cadenasser ?

Suivez le manuel du fabricant et la fiche de l’atelier. Hypertherm, par exemple, demande de mettre la source hors tension ou de placer le commutateur de verrouillage de la torche en position verrouillée avant de changer une cartouche. Si vous entrez dans la zone dangereuse de la table (portique, bac), le cadenassage s’applique.

### Le cadenas « de l’atelier » suffit-il ?

Non. L’article 188.3 demande que chaque personne qui a accès à la zone dangereuse pose son propre cadenas à cléage unique.

### Où trouver le texte exact ?

Dans le RSST (sous-section sur le cadenassage, art. 188.1 et suivants) sur Légis Québec, et dans le guide de la CNESST cité ci-dessous.

## À valider en atelier (Michaël)

- Nos fiches de cadenassage existantes (par machine).
- Fournisseur de cadenas et de boîtes de cadenassage.

## Sources

- [CNESST — Cadenassage et autres méthodes de contrôle des énergies : guide d’information sur les dispositions réglementaires (2023, PDF)](https://www.upa.qc.ca/fileadmin/01_UPA_provincial/Prod_SST/Documentation/Cadenassage_controle-energies.pdf) : articles 188.2, 188.3, 188.5 et 188.6 reproduits et commentés. Copie diffusée par l’UPA ; consultée le 26 novembre 2026.
- [Légis Québec — Règlement sur la santé et la sécurité du travail (S-2.1, r. 13)](https://www.legisquebec.gouv.qc.ca/fr/document/rc/S-2.1,%20r.%2013). Consulté le 26 novembre 2026.
- [CNESST — Cadenassage : ressources disponibles au Centre d’information (septembre 2024, PDF)](https://www.centredoc.cnesst.gouv.qc.ca/pdf/Biblioselect/Cadenassage.pdf) : contexte réglementaire, lien avec CSA Z460. Consulté le 26 novembre 2026.
- [Hypertherm — Powermax65/85/105 SYNC Operator Manual (810470)](https://xnet.hypertherm.com/Xnet/library/download/?file=HYP254734) : consignes avant le changement de cartouche. Consulté le 26 novembre 2026.

=== en
In Quebec, **lockout** (*cadenassage*) is mandatory under the **Regulation respecting occupational health and safety (RSST)** before any work in the **danger zone** of a machine. This guide explains, in plain words, what that means for a mill, lathe, plasma table, laser or press brake. It replaces neither the regulation nor your employer’s lockout program.

> [!WARN] The emergency stop button and a closed door are **not** lockout. E-stop stops the machine; it does not stop someone else from restarting it, nor air, hydraulics or gravity from moving a part.

## When must you lock out?

**Section 188.2 of the RSST**, as presented by the CNESST, covers any work in the danger zone of a machine, “including assembly, installation, adjustment, inspection, unjamming, setting, decommissioning, servicing, dismantling, cleaning, maintenance, refurbishing, repair, modification or unblocking”. Lockout, or failing that another method ensuring **equivalent safety**, must then be applied.

Concrete shop examples:

| Machine | Typical situations that call for energy control |
|---|---|
| Mill, lathe | Clearing the tool changer or chip conveyor by reaching into the zone, replacing a way wiper, cleaning the pan under the table |
| Plasma table | Draining or cleaning the water table or slats, working on the gantry or torch beyond the consumable change the maker describes |
| Fiber laser | Working on the cutting head, slats, pallet changer |
| Press brake | Changing or adjusting tooling, working under the ram (gravity and hydraulics) |

The regulation has two exceptions (s. 188.2): a machine with a **specific control mode** meeting section 189.1 (a setting mode designed for safe work in the zone), and a **single-energy-source** machine whose plug is **within reach and under the exclusive control** of the person, with no residual energy (the CNESST’s example: a mitre saw).

## Everyone gets their own lock

**Section 188.3** is simple: lockout must be done by **each person** with access to the danger zone, using **their own single-key lock**. Two people in the machine = two locks, often on a group lockbox.

## What the lockout sheet must contain

The employer must have a procedure for each machine (s. 188.5). Under **section 188.6**, it includes:

1. identification of the machine;
2. the person responsible for the energy control method;
3. identification and location of every control device and **every energy source**;
4. identification and location of **every cut-off point**;
5. type and quantity of equipment needed (locks, hasps, valve devices…);
6. the **steps** to control the energies;
7. where needed, continuity during a shift change (handing over equipment);
8. where needed, specifics: **residual or stored energy** to release, required PPE, other measures.

## Energies people forget on CNC machines

- **Electrical**: the machine’s main disconnect. Careful with the cabinet: some circuits (lighting, outlets, charged drives) may stay live; follow the maker’s manual.
- **Pneumatic**: air for the tool changer, spindle clamp, cylinders. Shut off and **bleed** the line.
- **Hydraulic**: press brake, hydraulic chuck, pallet clamping. Pressure can remain in accumulators.
- **Gravity**: press brake ram, a Z axis or head that can drop, a heavy part on a fixture.
- **Thermal and chemical**: hot parts, coolant, laser assist gas (oxygen, nitrogen) in the lines.

> [!NOTE] The CNESST notes that its requirements draw on **CSA Z460** (*Control of hazardous energy: lockout and other methods*). Construction sites fall under the Safety Code for the construction industry instead.

## Checklist

- [ ] Machine lockout sheet available on site
- [ ] Affected people told
- [ ] Machine stopped normally (cycle finished, spindle stopped)
- [ ] Every energy source cut at the listed cut-off point
- [ ] My own lock on (and one for each person working)
- [ ] Residual energy released: air bled, hydraulic pressure at zero, axes and ram blocked mechanically
- [ ] **Verify**: try to start, the machine does not respond; return the selector to off
- [ ] When done: tools out, guards back, people clear, locks removed by their owners

## Common mistakes

| Mistake | Why it is dangerous |
|---|---|
| Relying on e-stop | Someone can reset and restart |
| One lock for the whole crew | The first one to leave removes everyone’s protection |
| Cutting power without bleeding air | A cylinder or the tool changer still moves |
| Not testing start-up | Wrong disconnect opened, machine still live |
| Ignoring gravity | Ram or Z axis comes down |

## FAQ

### I’m only changing plasma consumables. Do I need to lock out?

Follow the maker’s manual and your shop’s sheet. Hypertherm, for example, requires turning the power supply off or putting the torch-lock switch in the locked position before changing a cartridge. If you go into the table’s danger zone (gantry, water pan), lockout applies.

### Is the “shop lock” enough?

No. Section 188.3 requires each person with access to the danger zone to apply their own single-key lock.

### Where is the exact wording?

In the RSST (lockout subdivision, s. 188.1 and following) on Légis Québec, and in the CNESST guide cited below.

## For Michaël to review

- Our existing lockout sheets (per machine).
- Supplier for locks and lockboxes.

## Sources

- [CNESST — Cadenassage et autres méthodes de contrôle des énergies: guide to the regulatory provisions (2023, PDF, French)](https://www.upa.qc.ca/fileadmin/01_UPA_provincial/Prod_SST/Documentation/Cadenassage_controle-energies.pdf): sections 188.2, 188.3, 188.5 and 188.6 quoted and explained. Copy distributed by the UPA; consulted November 26, 2026.
- [Légis Québec — Regulation respecting occupational health and safety (S-2.1, r. 13)](https://www.legisquebec.gouv.qc.ca/en/document/cr/S-2.1,%20r.%2013). Consulted November 26, 2026.
- [CNESST — Lockout: resources at the information centre (September 2024, PDF, French)](https://www.centredoc.cnesst.gouv.qc.ca/pdf/Biblioselect/Cadenassage.pdf): regulatory background, link to CSA Z460. Consulted November 26, 2026.
- [Hypertherm — Powermax65/85/105 SYNC Operator Manual (810470)](https://xnet.hypertherm.com/Xnet/library/download/?file=HYP254734): instructions before changing a cartridge. Consulted November 26, 2026.
