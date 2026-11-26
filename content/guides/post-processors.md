---
id: post-processors
hub: fundamentals
order: 2
nav: Post-processeurs | Post processors
kicker: Fondamentaux · FAO | Fundamentals · CAM
level: intermediaire
schema: HowTo
tags: post processor, cam, fusion, mastercam, sheetcam, g-code
related: gcode, fusion-cam, mastercam-posts-lathe, sheetcam
fr_slug: post-processeurs
en_slug: post-processors
fr_title: Post-processeurs : choisir, tester et modifier sans casser la machine
en_title: Post processors: choose, test and edit without crashing the machine
fr_desc: Ce que fait un post-processeur, où trouver le bon pour votre commande (Fusion, Mastercam, SheetCam…), comment le valider à blanc et quelles modifications sont sûres.
en_desc: What a post processor does, where to find the right one for your control (Fusion, Mastercam, SheetCam…), how to dry-run it and which edits are safe.
---
=== fr
Le FAO calcule des trajectoires dans un format neutre. Le **post-processeur** (ou « post ») les traduit dans le dialecte exact de **votre** commande : en-tête, unités, format des arcs, changements d’outil, codes de torche ou de broche, fin de programme. Un bon parcours avec un mauvais post donne un mauvais programme.

## Ce que le post décide

| Élément | Exemple de différence entre commandes |
|---|---|
| Arcs | `I J` incrémentaux ou absolus, `R`, ou arcs découpés en segments |
| Changement d’outil | `T1 M6`, `M6 T1`, ou pause manuelle |
| Compensation | Sortie de `G41/G42` ou trajectoire déjà décalée |
| Plasma | Codes torche, IHS, THC (`M3/M5`, `M62/M63`, `H0/H1`…) |
| Format | Nombre de décimales, numéros de ligne, `%`, commentaires `( )` ou `;` |
| Sécurité | Ligne d’initialisation, retours `G28`/`G53` |

## Où trouver le bon post

- **Fusion** : bibliothèque officielle de posts d’Autodesk, consultable en ligne et depuis le dialogue *Post Process* ; les posts sont des fichiers `.cps` (JavaScript).
- **Mastercam** : le post est livré avec une *machine definition* et une *control definition* ; on l’obtient d’ordinaire auprès du revendeur Mastercam (fichiers `.pst`/`.psb`, langage MP).
- **SheetCam** : posts en Lua dans la bibliothèque du logiciel ; les fabricants de tables fournissent souvent le leur.
- **Fabricant de la machine** : toujours la première source. Langmuir, par exemple, publie ses posts Fusion et SheetCam pour FireControl, et précise qu’un programme généré sans eux n’active pas le THC.

## Valider un post neuf, pas à pas

1. **Programme de test court** : un carré, un cercle, un trou, deux outils si la machine a un changeur.
2. **Lire le code** : en-tête, unités (`G20/G21`), mode `G90`, format des arcs, appel du bon décalage, codes broche ou torche.
3. **Simuler** dans un visualiseur (CAMotics, NC Viewer, ou l’aperçu de la commande).
4. **Essai à blanc** : outil relevé bien au-dessus de la pièce (décalage Z temporairement remonté) ou, en plasma, mode *dry run* sans arc.
5. **Réduction d’avance et main sur l’arrêt d’urgence** pour la première vraie coupe.
6. **Archiver** le post validé avec sa date et la version du FAO.

## Modifications sûres… et moins sûres

| Généralement sûr | À confier au fournisseur ou au revendeur |
|---|---|
| Texte d’en-tête et commentaires | Logique de changement d’outil |
| Nombre de décimales | Gestion des axes rotatifs |
| Ligne d’initialisation | Cycles fixes, macros, palpage |
| Propriétés exposées par le post (Fusion) | Codes THC / IHS plasma |

> [!TIP] Dans Fusion, beaucoup de réglages sont des **propriétés** du post modifiables dans le dialogue de post-traitement : changez-les là avant de toucher au fichier `.cps`.

## Erreurs fréquentes

- Utiliser un post « générique Fanuc » sur une commande qui n’est pas de type Fanuc.
- Post plasma sans les codes THC du fabricant : la torche ne suit pas la tôle.
- Modifier un post sans garder l’original ni noter la modification.
- Post à jour mais FAO plus récent ou plus ancien : vérifiez la compatibilité.

## FAQ

### Mon programme vient de Fusion pour usage personnel et les rapides sont lents. Le post est-il en cause ?
Non. Autodesk documente que Fusion pour usage personnel réduit les rapides à l’avance de coupe et retire les changements d’outil automatiques. Voir [Fusion : débuter en FAO](/guides/fusion-fao-debuter/).

### Puis-je écrire mon propre post ?
Oui pour Fusion (JavaScript documenté) et SheetCam (Lua documenté). Commencez à partir d’un post proche de votre commande, jamais d’une page blanche.

## À valider en atelier (Michaël)

- Les posts SheetCam et Fusion réellement utilisés sur vos tables.
- Un programme de test type à recommander.

## Sources

- [Autodesk — Fusion post library](https://cam.autodesk.com/hsmposts), consulté le 26 novembre 2026.
- [Langmuir Systems — THC guide (posts FireControl requis)](https://www.langmuirsystems.com/pages/thc-guide).
- [Autodesk — Fusion personal use: rapides et changements d’outil](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Fusion-360-Free-License-Changes.html).
- [SheetCam LLC — Support Manuals](https://sheetcamshop.myshopify.com/pages/support).
=== en
CAM computes toolpaths in a neutral form. The **post processor** (“post”) translates them into the exact dialect of **your** control: header, units, arc format, tool changes, torch or spindle codes, program end. A good toolpath with a bad post is a bad program.

## What the post decides

| Item | Example of differences between controls |
|---|---|
| Arcs | Incremental or absolute `I J`, `R`, or arcs broken into segments |
| Tool change | `T1 M6`, `M6 T1`, or a manual pause |
| Compensation | Output `G41/G42` or an already-offset path |
| Plasma | Torch, IHS, THC codes (`M3/M5`, `M62/M63`, `H0/H1`…) |
| Format | Decimals, line numbers, `%`, comments `( )` or `;` |
| Safety | Start-up line, `G28`/`G53` returns |

## Where to find the right post

- **Fusion**: Autodesk’s official post library, searchable online and from the *Post Process* dialog; posts are `.cps` files (JavaScript).
- **Mastercam**: the post ships with a *machine definition* and a *control definition*; you usually get it from your Mastercam reseller (`.pst`/`.psb` files, MP language).
- **SheetCam**: Lua posts in the software library; table makers often supply their own.
- **Machine maker**: always the first source. Langmuir, for example, publishes its Fusion and SheetCam posts for FireControl and states that a program generated without them will not enable THC.

## Validating a new post, step by step

1. **Short test program**: a square, a circle, a hole, two tools if the machine has a changer.
2. **Read the code**: header, units (`G20/G21`), `G90` mode, arc format, correct work offset, spindle or torch codes.
3. **Simulate** in a viewer (CAMotics, NC Viewer, or the control’s preview).
4. **Dry run**: tool well above the part (Z offset temporarily raised) or, in plasma, *dry run* mode without arc.
5. **Feed override down and hand on the E-stop** for the first real cut.
6. **Archive** the validated post with its date and the CAM version.

## Safe edits… and less safe ones

| Usually safe | Leave to the vendor or reseller |
|---|---|
| Header text and comments | Tool-change logic |
| Number of decimals | Rotary axis handling |
| Start-up line | Canned cycles, macros, probing |
| Properties exposed by the post (Fusion) | Plasma THC / IHS codes |

> [!TIP] In Fusion, many settings are post **properties** you can change in the post dialog: change them there before touching the `.cps` file.

## Common mistakes

- Using a “generic Fanuc” post on a control that is not Fanuc-style.
- Plasma post without the maker’s THC codes: the torch does not follow the plate.
- Editing a post without keeping the original or logging the change.
- Current post but newer or older CAM: check compatibility.

## FAQ

### My program comes from Fusion for personal use and rapids are slow. Is the post to blame?
No. Autodesk documents that Fusion for personal use reduces rapids to the cutting feed and removes automatic tool changes. See [Fusion CAM: getting started](/en/guides/fusion-cam-getting-started/).

### Can I write my own post?
Yes for Fusion (documented JavaScript) and SheetCam (documented Lua). Start from a post close to your control, never from a blank page.

## For Michaël to review

- The SheetCam and Fusion posts actually used on your tables.
- A standard test program to recommend.

## Sources

- [Autodesk — Fusion post library](https://cam.autodesk.com/hsmposts), consulted November 26, 2026.
- [Langmuir Systems — THC guide (FireControl posts required)](https://www.langmuirsystems.com/pages/thc-guide).
- [Autodesk — Fusion personal use: rapids and tool changes](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Fusion-360-Free-License-Changes.html).
- [SheetCam LLC — Support Manuals](https://sheetcamshop.myshopify.com/pages/support).
