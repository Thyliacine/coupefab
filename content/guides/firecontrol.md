---
id: firecontrol
hub: software
group: control
order: 30
mono: Fi
nav: FireControl (Langmuir) | FireControl (Langmuir)
kicker: Logiciel · commande plasma | Software · plasma control
level: debutant
schema: HowTo
tags: firecontrol, langmuir, crossfire, crossfire pro, xr, thc, smart voltage, torch speed cutoff, h0, h1, plasma
related: plasma-cutting, fusion-cam, sheetcam, plasma-troubleshooting
fr_slug: firecontrol-langmuir
en_slug: firecontrol-langmuir
fr_title: FireControl (Langmuir) : charger, ajuster et couper sur CrossFire, PRO et XR
en_title: FireControl (Langmuir): load, adjust and cut on CrossFire, PRO and XR
fr_desc: Le logiciel de commande gratuit des tables Langmuir : chargement du G-code, mise à l’échelle, essai à blanc, reprise de coupe, délai de perçage, et contrôle de hauteur (THC) avec SMART Voltage et coupure par vitesse.
en_desc: The free control software for Langmuir tables: loading G-code, scaling, dry run, run-from-here, pierce delay, and torch height control (THC) with SMART Voltage and speed cutoff.
---
=== fr
**FireControl** est le logiciel de commande **gratuit** des tables plasma Langmuir Systems (CrossFire, CrossFire PRO, CrossFire XR). Il reçoit le G-code produit par la FAO et pilote la table et la torche.

## Ce qu’il permet

| Fonction | Usage |
|---|---|
| Charger un G-code, mettre à l’échelle, pivoter | Ajuster sans repasser par la FAO |
| **Essai à blanc** (dry run) | Vérifier le parcours sans arc |
| **Reprendre d’ici** (run from here) | Repartir après une perte d’arc |
| Forcer le **délai de perçage** | Ajuster sans reposter |
| Imbrication manuelle simple | Dupliquer une pièce sur la tôle |
| Contrôle de hauteur (avec module THC) | Garder une distance constante pendant la coupe |

## Contrôle de hauteur (THC)

- **SMART Voltage** : la tension de consigne est échantillonnée au début de chaque coupe plutôt que fixée à la main.
- **Torch Speed Cutoff** : le THC est désactivé quand la vitesse tombe sous un seuil (coins, petits trous) pour éviter les plongées.
- Codes **H0 / H1** dans le G-code pour désactiver ou réactiver le THC sur une partie du parcours.
- Plage de tension de 0 à 300 V.

> [!WARN] Le THC ne fonctionne qu’avec les **post-processeurs Langmuir** pour Fusion et SheetCam, qui insèrent les bons codes. Un post générique produira un programme sans contrôle de hauteur.

## Démarche de coupe

1. Dans la FAO, utiliser le post Langmuir ([Fusion](/guides/fusion-fao-debuter/) ou [SheetCam](/guides/debuter-sheetcam/)) et les paramètres du tableau de coupe de votre source.
2. Ouvrir le fichier dans FireControl ; vérifier dimensions et position.
3. Placer l’origine (coin de la tôle) ; vérifier que la pièce tient dans la zone.
4. **Essai à blanc** à hauteur sûre.
5. Couper ; observer l’arc et la tension.
6. En cas de perte d’arc : corriger la cause (consommables, masse), puis **reprendre d’ici**.

## Erreurs fréquentes

| Erreur | Correctif |
|---|---|
| THC inactif | Post Langmuir, module THC branché, réglages THC activés |
| Plongée dans les coins | Régler Torch Speed Cutoff |
| Pièces décalées | Origine mal placée, ou tôle qui a bougé |
| Mauvais fini | Voir [Dépannage plasma](/guides/depannage-plasma-scories-biseau/) |

## FAQ

### FireControl fonctionne-t-il avec d’autres tables ?
Il est conçu pour les tables Langmuir et leur électronique.

## À valider en atelier (Michaël)

- Retour d’utilisateurs CrossFire sur les réglages THC.

## Sources

- [Langmuir Systems — FireControl](https://www.langmuirsystems.com/firecontrol), consulté le 26 novembre 2026.
- [Langmuir Systems — Documentation et posts](https://www.langmuirsystems.com/software).
=== en
**FireControl** is the **free** control software for Langmuir Systems plasma tables (CrossFire, CrossFire PRO, CrossFire XR). It takes the G-code from CAM and drives the table and torch.

## What it does

| Feature | Use |
|---|---|
| Load G-code, scale, rotate | Adjust without going back to CAM |
| **Dry run** | Check the path with no arc |
| **Run from here** | Restart after an arc loss |
| Override **pierce delay** | Adjust without reposting |
| Simple manual nesting | Duplicate a part on the sheet |
| Height control (with THC module) | Keep a constant standoff while cutting |

## Torch height control (THC)

- **SMART Voltage**: the target voltage is sampled at the start of each cut rather than set by hand.
- **Torch Speed Cutoff**: THC is disabled when speed drops below a threshold (corners, small holes) to avoid diving.
- **H0 / H1** codes in G-code to disable or re-enable THC on part of a path.
- Voltage range 0 to 300 V.

> [!WARN] THC only works with **Langmuir’s post processors** for Fusion and SheetCam, which insert the right codes. A generic post produces a program without height control.

## Cutting workflow

1. In CAM, use the Langmuir post ([Fusion](/en/guides/fusion-cam-getting-started/) or [SheetCam](/en/guides/getting-started-sheetcam/)) and your source’s cut chart parameters.
2. Open the file in FireControl; check size and position.
3. Set the origin (sheet corner); check the part fits the area.
4. **Dry run** at a safe height.
5. Cut; watch the arc and voltage.
6. On arc loss: fix the cause (consumables, ground), then **run from here**.

## Common mistakes

| Mistake | Fix |
|---|---|
| THC inactive | Langmuir post, THC module connected, THC settings enabled |
| Diving in corners | Set Torch Speed Cutoff |
| Parts offset | Origin misplaced, or sheet moved |
| Poor finish | See [Plasma troubleshooting](/en/guides/plasma-troubleshooting-dross-bevel/) |

## FAQ

### Does FireControl work with other tables?
It is designed for Langmuir tables and their electronics.

## For Michaël to review

- Feedback from CrossFire users on THC settings.

## Sources

- [Langmuir Systems — FireControl](https://www.langmuirsystems.com/firecontrol), consulted November 26, 2026.
- [Langmuir Systems — Documentation and posts](https://www.langmuirsystems.com/software).
