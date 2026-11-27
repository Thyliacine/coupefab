---
id: hypertherm-edge-phoenix
hub: software
group: control
order: 66
mono: Hy
nav: Hypertherm EDGE / Phoenix | Hypertherm EDGE / Phoenix
kicker: Logiciel · commande plasma | Software · plasma control
level: intermediaire
schema: HowTo
tags: hypertherm, edge connect, edge pro, microedge pro, phoenix, cutpro wizard, soft opcon, cut chart, arcglide, sensor thc, prónest, true hole, bevel
related: pronest, cut-charts, plasma-cutting, thc-hunting
fr_slug: hypertherm-edge-connect-phoenix
en_slug: hypertherm-edge-connect-phoenix
fr_title: Commandes Hypertherm EDGE Connect et Phoenix : prise en main pour l’opérateur
en_title: Hypertherm EDGE Connect and Phoenix controls: an operator’s first steps
fr_desc: EDGE Connect, EDGE Pro, MicroEDGE Pro et le logiciel Phoenix : charger une pièce, imbriquer, CutPro Wizard, processus et chartes de coupe, contrôle de hauteur, True Hole, et où trouver la bonne documentation.
en_desc: EDGE Connect, EDGE Pro, MicroEDGE Pro and Phoenix software: loading a part, nesting, CutPro Wizard, cut processes and charts, height control, True Hole, and where to find the right documentation.
codes: edge
---
=== fr
Sur beaucoup de tables plasma industrielles (et certaines tables oxycoupage et jet d’eau), la commande est une **Hypertherm** : les anciennes **EDGE Pro / MicroEDGE Pro / EDGE Pro Ti** et la plateforme actuelle **EDGE Connect**. Toutes tournent le logiciel **Phoenix**. Selon Hypertherm, EDGE Connect communique en EtherCAT avec le mouvement et la coupe, tourne sous Windows 10 Enterprise et se décline en EDGE Connect (CNC embarquée) et EDGE Connect TC (avec écran tactile et console matérielle).

## Ce que l’opérateur fait dans Phoenix

| Tâche | Où | À retenir |
|---|---|---|
| Charger une pièce | Écran principal : bibliothèque de formes, fichier, téléchargement depuis l’hôte, import DXF | Les programmes de ProNest arrivent prêts à couper ; voir [[pronest]] |
| Disposer les pièces | Répétition (droite, décalée, imbriquée), alignement (*Align Wizard*), imbrication manuelle ou automatique | L’imbrication automatique dépend des options installées |
| Couper | **CutPro Wizard** (assistant pas à pas) ou mode manuel | Hypertherm le présente comme la façon la plus rapide pour un nouvel opérateur |
| Processus et chartes | Écrans Process et Cut Chart | Chartes d’usine ou personnalisées, appelées par le programme ou par l’assistant |
| Pause / reprise | Pause, retour sur le trajet, reprise après perte d’arc | Voir la procédure exacte de votre version |
| Mouvement manuel | *Soft OpCon* (console logicielle) ou console matérielle | Prise d’origine (*Home axes*) au démarrage |

## Démarche type pour une tôle

1. Mise sous tension et **prise d’origine** des axes.
2. Charger la tôle, vérifier son équerrage ; utiliser l’**Align Wizard** si la tôle est de travers.
3. Charger le programme (ou le nid) ; vérifier l’aperçu.
4. Lancer le **CutPro Wizard** : choix du processus, de la matière, de l’épaisseur et du courant selon les chartes ; l’assistant indique les **consommables** à installer.
5. Vérifier les consommables, le gaz et la hauteur ; lancer.
6. Surveiller le premier perçage et la première pièce.

## Contrôle de hauteur et qualité de trou

- Le contrôle de hauteur (ArcGlide, Sensor THC ou intégré, selon l’installation) suit la **tension d’arc** des chartes ; voir [[thc-hunting]].
- **True Hole** (selon système plasma et options) améliore les trous sur l’acier doux en combinant consommables, chartes et mouvement ; il exige les conditions décrites par Hypertherm (matière, diamètre, épaisseur).
- La documentation Phoenix comprend des sections « problèmes de qualité » et « conseils biseau » : à lire avant d’appeler le service.

## Liste de vérification de quart

- [ ] Axes référencés (*Home*)
- [ ] Consommables conformes à ce que l’assistant demande
- [ ] Pression de gaz et débit (test de gaz)
- [ ] Tôle alignée, programme vérifié en aperçu
- [ ] Sauvegarde des chartes personnalisées à jour

## Erreurs fréquentes

| Erreur | Correctif |
|---|---|
| Modifier une charte d’usine sans la renommer | Créer une charte personnalisée et la sauvegarder |
| Consommables différents de ceux du processus choisi | Suivre l’indication du CutPro Wizard |
| Tôle non alignée, pièces hors tôle | Align Wizard avant la coupe |
| Oublier de sauvegarder les réglages machine | Exporter les fichiers de configuration selon le manuel |

## FAQ

### Où trouver le bon manuel ?
Chez Hypertherm (bibliothèque documentaire), en choisissant votre CNC (EDGE Connect, EDGE Pro…) et la version de Phoenix ; les manuels d’installation contiennent aussi une section d’utilisation de Phoenix et de la Soft OpCon.

### Puis-je envoyer un programme Fusion ou SheetCam à une commande Phoenix ?
Oui si le post produit un format accepté par Phoenix (EIA/ESSI selon la configuration) ; validez toujours sur une chute. Voir [[fusion-plasma-posts]].

## À valider en atelier (Michaël)

- La version de Phoenix et la configuration de vos commandes.
- Les réglages de l’assistant que vos opérateurs utilisent le plus.

## Sources

- [Hypertherm — EDGE Connect CNC system](https://www.hypertherm.com/hypertherm/edge/edge-connect/), consulté le 26 novembre 2026.
- [Hypertherm — EDGE Connect Installation and Setup Manual 809340 (copie de distributeur, PDF)](https://veracitytechs.com/docs/EDGE%20Connect%20Installation%20and%20Setup%20Manual%20%28IM_809340_R4%29%2009%20Nov%202020.pdf), consulté le 26 novembre 2026.
- [Hypertherm — Phoenix Software V9.76 Operator Manual 806400 (copie de distributeur, PDF)](https://veracitytechs.com/docs/Phoenix%20Software%20Version%209.76.0%20Operator%20Manual%20%28OM_806400_R10%29%2022%20Dec%202014.pdf), consulté le 26 novembre 2026.
=== en
Many industrial plasma tables (and some oxyfuel and waterjet tables) run a **Hypertherm** control: the older **EDGE Pro / MicroEDGE Pro / EDGE Pro Ti** and the current **EDGE Connect** platform. All run **Phoenix** software. Per Hypertherm, EDGE Connect uses EtherCAT for motion and cutting control, runs Windows 10 Enterprise and comes as EDGE Connect (embedded CNC) and EDGE Connect TC (with touchscreen and hardware operator console).

## What the operator does in Phoenix

| Task | Where | Remember |
|---|---|---|
| Load a part | Main screen: shape library, file, download from host, DXF import | ProNest programs arrive ready to cut; see [[pronest]] |
| Arrange parts | Repeat (straight, staggered, nested), alignment (*Align Wizard*), manual or automatic nesting | Automatic nesting depends on installed options |
| Cut | **CutPro Wizard** (step-by-step) or manual mode | Hypertherm presents it as the fastest path for a new operator |
| Processes and charts | Process and Cut Chart screens | Factory or custom charts, called from the program or the wizard |
| Pause / resume | Pause, back up along the path, recover after arc loss | Check the exact procedure for your version |
| Manual motion | *Soft OpCon* (software console) or hardware console | Home axes at startup |

## Typical workflow for a sheet

1. Power up and **home** the axes.
2. Load the plate, check squareness; use the **Align Wizard** if it sits crooked.
3. Load the program (or nest); check the preview.
4. Run the **CutPro Wizard**: process, material, thickness and current per the charts; the wizard shows the **consumables** to install.
5. Check consumables, gas and height; start.
6. Watch the first pierce and the first part.

## Height control and hole quality

- Height control (ArcGlide, Sensor THC or integrated, depending on the install) follows the charts’ **arc voltage**; see [[thc-hunting]].
- **True Hole** (depending on plasma system and options) improves holes in mild steel by combining consumables, charts and motion; it requires the conditions Hypertherm describes (material, diameter, thickness).
- The Phoenix documentation has “cut quality issues” and “bevel cutting tips” sections: read them before calling service.

## Shift checklist

- [ ] Axes homed
- [ ] Consumables match what the wizard asks for
- [ ] Gas pressure and flow (gas test)
- [ ] Plate aligned, program checked in preview
- [ ] Custom chart backup up to date

## Common mistakes

| Mistake | Fix |
|---|---|
| Editing a factory chart without renaming it | Create a custom chart and save it |
| Consumables different from the selected process | Follow the CutPro Wizard prompt |
| Plate not aligned, parts off the sheet | Align Wizard before cutting |
| Not backing up machine settings | Export configuration files per the manual |

## FAQ

### Where do I find the right manual?
From Hypertherm’s documentation library, choosing your CNC (EDGE Connect, EDGE Pro…) and Phoenix version; installation manuals also include a section on operating Phoenix and the Soft OpCon.

### Can I send a Fusion or SheetCam program to a Phoenix control?
Yes if the post outputs a format Phoenix accepts (EIA/ESSI depending on configuration); always validate on a drop. See [[fusion-plasma-posts]].

## For Michaël to review

- The Phoenix version and configuration of your controls.
- The wizard settings your operators use most.

## Sources

- [Hypertherm — EDGE Connect CNC system](https://www.hypertherm.com/hypertherm/edge/edge-connect/), consulted November 26, 2026.
- [Hypertherm — EDGE Connect Installation and Setup Manual 809340 (distributor copy, PDF)](https://veracitytechs.com/docs/EDGE%20Connect%20Installation%20and%20Setup%20Manual%20%28IM_809340_R4%29%2009%20Nov%202020.pdf), consulted November 26, 2026.
- [Hypertherm — Phoenix Software V9.76 Operator Manual 806400 (distributor copy, PDF)](https://veracitytechs.com/docs/Phoenix%20Software%20Version%209.76.0%20Operator%20Manual%20%28OM_806400_R10%29%2022%20Dec%202014.pdf), consulted November 26, 2026.
