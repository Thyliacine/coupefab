---
id: fusion-plasma-posts
hub: software
group: cam
order: 36
mono: Fp
nav: Fusion plasma : posts par table | Fusion plasma: posts per table
kicker: Logiciel · FAO plasma | Software · plasma CAM
level: intermediaire
schema: HowTo
tags: fusion, fusion 360, plasma, post processor, langmuir, crossfire, firecontrol, torchmate, hypertherm, sheetcam, thc, ihs, kerf, cutting tool, local post
related: fusion-cam, post-processors, firecontrol, torchmate-avid
fr_slug: fusion-plasma-post-par-table
en_slug: fusion-plasma-posts-per-table
fr_title: Fusion pour le plasma : choisir et installer le bon post selon votre table
en_title: Fusion for plasma: choosing and installing the right post for your table
fr_desc: Langmuir CrossFire (FireControl), Torchmate, Hypertherm, LinuxCNC, Mach : où trouver le post plasma de Fusion, comment l’importer en post local, quelles propriétés régler (IHS, THC, hauteurs) et comment tester sans risque.
en_desc: Langmuir CrossFire (FireControl), Torchmate, Hypertherm, LinuxCNC, Mach: where to find Fusion’s plasma post, how to import it as a local post, which properties to set (IHS, THC, heights) and how to test safely.
---
=== fr
Dans Fusion, le parcours de découpe (2D Profile en mode *cutting*) est le même pour toutes les tables plasma. **C’est le post-processeur qui fait la différence** : codes d’allumage de la torche, gestion de la hauteur (IHS, THC), extension du fichier, commentaires acceptés par la commande. Un mauvais post donne au mieux une erreur à l’ouverture, au pire une torche qui plonge.

## D’où vient le post ?

| Table / commande | Source du post | Remarques |
|---|---|---|
| Langmuir CrossFire, CrossFire PRO / XR (FireControl) | Page *Downloads* de Langmuir (post Fusion pour FireControl) | Une version avec axe Z et une sans ; **sans Z, mettre IHS et THC à « No »** selon Langmuir. Les firmwares récents exigent les posts récents |
| Torchmate | Bibliothèque de posts Fusion (*Torchmate 3.0 Mill/Plasma*) ou post fourni par Torchmate selon la commande | Selon le logiciel de commande, des posts modifiés (codes M d’allumage, extension) circulent sur les forums Autodesk : à valider avec Torchmate |
| Hypertherm (commandes Phoenix / EDGE) | Bibliothèque Fusion (*Hypertherm Jet*) | Les commandes Phoenix lisent aussi les programmes produits par ProNest ; voir [[hypertherm-edge-phoenix]] |
| LinuxCNC / QtPlasmaC | Posts génériques ou communautaires | QtPlasmaC gère hauteurs et matériaux dans la commande ; voir [[linuxcnc]] |
| Mach3/Mach4 (avec THC) | Posts du fabricant de la table | Voir [[mach]] |

La **bibliothèque de posts** se trouve dans l’espace Fabrication : *Gérer > Bibliothèque de post*, dossier Fusion ; les posts téléchargés s’importent dans le dossier **Local**.

## Installer un post local (exemple FireControl)

1. Télécharger le fichier `.cps` sur le site du fabricant de la table.
2. Dans Fusion : *Post Process* → bouton « … » à côté du champ Post → **Local** → **Import** → choisir le fichier.
3. Choisir un **dossier de sortie** dédié (ex. un dossier « Programmes plasma » sur le bureau).
4. Régler les **propriétés du post** : unités, hauteurs de perçage et de coupe, délai, IHS, THC (selon le post).
5. Dans les réglages du parcours, laisser les hauteurs de Fusion (dégagement, retrait, dessus) **aux valeurs demandées par le fabricant** : chez Langmuir, les vraies hauteurs sont données dans le post, et « garder la buse en bas » doit rester décoché si la machine a un Z motorisé.

## Le parcours plasma dans Fusion, en bref

- **Outil de coupe** : type plasma, avec **kerf** et avance tirés de la charte (voir [[cut-charts]]).
- **2D Profile** en mode découpe : côté de compensation (extérieur pour une pièce, intérieur pour un trou).
- **Entrées/sorties** : en dehors de la pièce, perçage dans la chute (voir [[lead-ins-pierce]]).
- **Ordre** : trous intérieurs avant le contour extérieur.
- **Compensation** : « dans l’ordinateur » (Fusion applique le kerf) dans la plupart des cas de petites tables.

## Tester sans risque

- [ ] Ouvrir le fichier dans la commande et vérifier l’aperçu (pas d’erreur, bonne échelle)
- [ ] Simulation à vide, torche **éteinte** ou levée selon la procédure de la machine
- [ ] Vérifier la séquence de hauteur au premier perçage (IHS, perçage, descente)
- [ ] Coupe d’une pièce test sur une chute
- [ ] Noter version du post et du firmware dans votre fiche machine

## Erreurs fréquentes

| Erreur | Effet | Correctif |
|---|---|---|
| Post générique de fraisage au lieu du post plasma | Codes de broche au lieu d’allumage, Z erronés | Post de la table, catégorie *cutting* |
| Vieux post avec firmware récent | Programme refusé ou converti | Télécharger le post courant (Langmuir le précise) |
| IHS/THC actifs sur une table sans Z | Erreurs ou mouvements inattendus | Désactiver dans les propriétés du post |
| Kerf compté deux fois (Fusion + commande) | Pièces trop petites | Compensation à un seul endroit |
| Mauvaise extension de fichier | La commande ne voit pas le fichier | Régler l’extension dans le post ou renommer selon le fabricant |

## FAQ

### Fusion gratuit suffit-il pour le plasma ?
La licence personnelle a des limites qui changent dans le temps (voir [[fusion-cam]]) ; vérifiez la politique actuelle d’Autodesk avant de bâtir votre flux dessus.

### SheetCam ou Fusion pour le plasma ?
Fusion est pratique si vous dessinez déjà dedans ; SheetCam est plus direct pour les DXF, l’imbrication simple et les tables de matériaux. Voir [[sheetcam]].

## À valider en atelier (Michaël)

- La table et le post que vous utilisez réellement avec Fusion, et leurs propriétés.
- Les pièges vus chez des clients (extensions, hauteurs).

## Sources

- [Langmuir Systems — Downloads (post Fusion pour FireControl)](https://www.langmuirsystems.com/pages/downloads), consulté le 26 novembre 2026.
- [Langmuir Systems — Fusion 360 CAD/CAM tutorials (posting for FireControl)](https://www.langmuirsystems.com/pages/software-fusion), consulté le 26 novembre 2026.
- [Autodesk — Post Processor Library reference (Fusion)](https://help.autodesk.com/cloudhelp/ENU/Fusion-CAM/files/MFG-POST-PROCESSOR-LIBRARY-REF.htm), consulté le 26 novembre 2026.
- [Autodesk — Bibliothèque de post-processeurs en ligne](https://cam.autodesk.com/hsmposts), consulté le 26 novembre 2026.
=== en
In Fusion, the cutting toolpath (2D Profile in *cutting* mode) is the same for every plasma table. **The post processor is what differs**: torch on/off codes, height handling (IHS, THC), file extension, comments the control accepts. A wrong post gives, at best, an error when the file opens and, at worst, a torch that dives.

## Where does the post come from?

| Table / control | Post source | Notes |
|---|---|---|
| Langmuir CrossFire, CrossFire PRO / XR (FireControl) | Langmuir *Downloads* page (Fusion post for FireControl) | A Z-axis and a no-Z version; **without Z, set IHS and THC to “No”** per Langmuir. Recent firmware requires recent posts |
| Torchmate | Fusion Post Library (*Torchmate 3.0 Mill/Plasma*) or a post supplied by Torchmate depending on the control | Depending on control software, modified posts (torch M-codes, extension) circulate on Autodesk forums: validate with Torchmate |
| Hypertherm (Phoenix / EDGE controls) | Fusion library (*Hypertherm Jet*) | Phoenix controls also read programs from ProNest; see [[hypertherm-edge-phoenix]] |
| LinuxCNC / QtPlasmaC | Generic or community posts | QtPlasmaC handles heights and materials in the control; see [[linuxcnc]] |
| Mach3/Mach4 (with THC) | Table manufacturer’s posts | See [[mach]] |

The **Post Library** lives in the Manufacture workspace: *Manage > Post Library*, Fusion folder; downloaded posts are imported into the **Local** folder.

## Installing a local post (FireControl example)

1. Download the `.cps` file from the table manufacturer’s site.
2. In Fusion: *Post Process* → the “…” button next to the Post field → **Local** → **Import** → pick the file.
3. Choose a dedicated **output folder** (e.g. a “Plasma programs” folder on the desktop).
4. Set the **post properties**: units, pierce and cut heights, delay, IHS, THC (depending on the post).
5. In the toolpath settings, leave Fusion’s heights (clearance, retract, top) **at the values the manufacturer asks for**: with Langmuir, real heights are entered in the post, and “keep nozzle down” must stay unchecked if the machine has a powered Z.

## The Fusion plasma toolpath, briefly

- **Cutting tool**: plasma type, with **kerf** and feed from the chart (see [[cut-charts]]).
- **2D Profile** in cutting mode: compensation side (outside for a part, inside for a hole).
- **Lead-ins/outs**: off the part, pierce in the scrap (see [[lead-ins-pierce]]).
- **Order**: inner holes before the outer profile.
- **Compensation**: “in computer” (Fusion applies kerf) in most small-table cases.

## Test safely

- [ ] Open the file in the control and check the preview (no error, right scale)
- [ ] Dry run, torch **off** or raised per the machine’s procedure
- [ ] Check the height sequence at the first pierce (IHS, pierce, descent)
- [ ] Cut one test part on a drop
- [ ] Record post and firmware versions in your machine notes

## Common mistakes

| Mistake | Effect | Fix |
|---|---|---|
| Generic milling post instead of the plasma post | Spindle codes instead of torch codes, wrong Z | The table’s post, *cutting* category |
| Old post with recent firmware | Program rejected or converted | Download the current post (Langmuir says so) |
| IHS/THC enabled on a table without Z | Errors or unexpected moves | Disable in post properties |
| Kerf applied twice (Fusion + control) | Parts too small | Compensate in one place only |
| Wrong file extension | The control can’t see the file | Set the extension in the post or rename per the manufacturer |

## FAQ

### Is free Fusion enough for plasma?
The personal licence has limits that change over time (see [[fusion-cam]]); check Autodesk’s current policy before building your workflow on it.

### SheetCam or Fusion for plasma?
Fusion is handy if you already design in it; SheetCam is more direct for DXFs, simple nesting and material tables. See [[sheetcam]].

## For Michaël to review

- The table and post you actually use with Fusion, and their properties.
- Pitfalls seen at customers (extensions, heights).

## Sources

- [Langmuir Systems — Downloads (Fusion post for FireControl)](https://www.langmuirsystems.com/pages/downloads), consulted November 26, 2026.
- [Langmuir Systems — Fusion 360 CAD/CAM tutorials (posting for FireControl)](https://www.langmuirsystems.com/pages/software-fusion), consulted November 26, 2026.
- [Autodesk — Post Processor Library reference (Fusion)](https://help.autodesk.com/cloudhelp/ENU/Fusion-CAM/files/MFG-POST-PROCESSOR-LIBRARY-REF.htm), consulted November 26, 2026.
- [Autodesk — Online post processor library](https://cam.autodesk.com/hsmposts), consulted November 26, 2026.
