---
id: freecad-cam
hub: software
group: cam
order: 50
mono: FC
nav: FreeCAD (CAM) | FreeCAD CAM
kicker: Logiciel libre · FAO | Open source · CAM
level: intermediaire
schema: HowTo
tags: freecad, cam, path, open source, job, profile, pocket, adaptive, post processor, grbl, linuxcnc, sheetmetal addon
related: post-processors, gcode, ugs-grbl, linuxcnc
fr_slug: freecad-cam
en_slug: freecad-cam
fr_title: FreeCAD CAM : la FAO libre et gratuite, de la tâche au G-code
en_title: FreeCAD CAM: free open-source CAM, from job to G-code
fr_desc: L’atelier CAM de FreeCAD 1.0 (anciennement Path) : tâche, outils, opérations Profil, Poche et Adaptive, simulation, choix du post-processeur pour grbl, LinuxCNC ou Mach, et tôlerie avec l’extension SheetMetal.
en_desc: FreeCAD 1.0’s CAM workbench (formerly Path): job, tools, Profile, Pocket and Adaptive operations, simulation, choosing a post processor for grbl, LinuxCNC or Mach, and sheet metal with the SheetMetal add-on.
---
=== fr
FreeCAD est un modeleur 3D paramétrique **libre et gratuit**, sans restriction d’usage commercial. Depuis la version 1.0 (novembre 2024), l’atelier **Path** a été renommé **CAM** et a reçu un nouveau simulateur.

## Démarche

1. Modéliser la pièce (atelier Part Design) ou importer un STEP.
2. Passer à l’atelier **CAM** et créer une **Tâche** (Job) : choisir le modèle, le **brut** et le **post-processeur**.
3. Définir l’origine : elle doit correspondre au zéro réglé sur la machine — voir [Décalages d’origine](/guides/decalages-origine-g54/).
4. Créer les **contrôleurs d’outil** (outil + vitesses + avances) à partir de la bibliothèque.
5. Ajouter les opérations : **Surfaçage**, **Poche**, **Adaptive** (évidement à engagement constant), **Profil** (contour), **Perçage**, **Gravure**.
6. **Simuler**, puis **post-traiter** et inspecter le G-code.

## Choisir le post-processeur

| Commande | Post typique |
|---|---|
| grbl / grblHAL | `grbl` |
| LinuxCNC | `linuxcnc` |
| Mach3 / Mach4 | `mach3_mach4` |
| Commande générique | `centroid`, `fanuc` ou autre selon la liste fournie |

> [!WARN] Un post générique ne connaît pas les particularités de votre machine (changeur d’outil, broche, plasma). Testez à vide et lisez l’entête. Voir [Post-processeurs](/guides/post-processeurs/).

## Tôlerie

L’extension communautaire **SheetMetal** (gestionnaire d’extensions) ajoute brides, déplié et export DXF. Le résultat se traite ensuite comme un DXF ordinaire — voir [DXF : bonnes pratiques](/guides/dxf-bonnes-pratiques/).

## Points faibles à connaître

| Point | Contournement |
|---|---|
| Courbe d’apprentissage, interface dense | Suivre la documentation officielle pas à pas |
| Problème de « nommage topologique » sur modèles modifiés | Amélioré en 1.0 ; garder des esquisses bien contraintes |
| Plasma : pas de gestion native de la hauteur de torche | Utiliser SheetCam ou le post de la commande (ex. [QtPlasmaC](/guides/linuxcnc-qtplasmac/)) |

## FAQ

### FreeCAD peut-il remplacer Fusion ?
Pour du fraisage 2,5 axes et un usage commercial sans abonnement, oui, avec plus d’effort. La FAO 3D avancée et l’ergonomie restent en retrait.

## À valider en atelier (Michaël)

- Un essai complet FreeCAD → votre machine pour confirmer le post.

## Sources

- [FreeCAD — Notes de version 1.0](https://wiki.freecad.org/Release_notes_1.0), consulté le 26 novembre 2026.
- [FreeCAD — CAM Workbench](https://wiki.freecad.org/CAM_Workbench).
- [FreeCAD — SheetMetal Workbench](https://wiki.freecad.org/SheetMetal_Workbench).
=== en
FreeCAD is a **free, open-source** parametric 3D modeller, with no restriction on commercial use. Since version 1.0 (November 2024), the **Path** workbench was renamed **CAM** and got a new simulator.

## Workflow

1. Model the part (Part Design workbench) or import a STEP.
2. Switch to the **CAM** workbench and create a **Job**: pick the model, **stock** and **post processor**.
3. Set the origin: it must match the zero set on the machine — see [Work offsets](/en/guides/work-offsets-g54/).
4. Create **tool controllers** (tool + speeds + feeds) from the library.
5. Add operations: **Face**, **Pocket**, **Adaptive** (constant-engagement clearing), **Profile** (contour), **Drilling**, **Engrave**.
6. **Simulate**, then **post process** and inspect the G-code.

## Choosing the post processor

| Control | Typical post |
|---|---|
| grbl / grblHAL | `grbl` |
| LinuxCNC | `linuxcnc` |
| Mach3 / Mach4 | `mach3_mach4` |
| Generic control | `centroid`, `fanuc` or another from the supplied list |

> [!WARN] A generic post does not know your machine’s specifics (tool changer, spindle, plasma). Dry-run and read the header. See [Post processors](/en/guides/post-processors/).

## Sheet metal

The community **SheetMetal** add-on (Addon Manager) adds flanges, unfolding and DXF export. The result is then handled like any DXF — see [DXF best practices](/en/guides/dxf-best-practices/).

## Weak points to know

| Point | Workaround |
|---|---|
| Learning curve, dense interface | Follow the official documentation step by step |
| “Topological naming” issues on edited models | Improved in 1.0; keep sketches fully constrained |
| Plasma: no native torch height handling | Use SheetCam or the control’s post (e.g., [QtPlasmaC](/en/guides/linuxcnc-qtplasmac/)) |

## FAQ

### Can FreeCAD replace Fusion?
For 2.5-axis milling and commercial use without a subscription, yes, with more effort. Advanced 3D CAM and ergonomics lag behind.

## For Michaël to review

- A full FreeCAD → your machine test to confirm the post.

## Sources

- [FreeCAD — Release notes 1.0](https://wiki.freecad.org/Release_notes_1.0), consulted November 26, 2026.
- [FreeCAD — CAM Workbench](https://wiki.freecad.org/CAM_Workbench).
- [FreeCAD — SheetMetal Workbench](https://wiki.freecad.org/SheetMetal_Workbench).
