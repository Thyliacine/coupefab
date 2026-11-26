---
id: fusion-cam
hub: software
group: cam
order: 20
mono: F
nav: Fusion (FAO) | Fusion CAM
kicker: Logiciel · FAO | Software · CAM
level: debutant
schema: HowTo
tags: fusion, fusion 360, autodesk, cam, manufacture, adaptive, plasma, laser, waterjet, post processor, personal use
related: post-processors, feeds-speeds, work-offsets, sheetcam
fr_slug: fusion-fao-debuter
en_slug: fusion-cam-getting-started
fr_title: Débuter en FAO avec Autodesk Fusion : fraisage 2D, découpe plasma et post-traitement
en_title: Getting started with Autodesk Fusion CAM: 2D milling, plasma cutting and posting
fr_desc: Configuration (setup), opérations 2D, Adaptive, profil de découpe plasma ou laser, simulation et post-processeur dans l’espace Fabrication de Fusion, plus les limites réelles de la licence Usage personnel.
en_desc: Setup, 2D operations, Adaptive, plasma or laser profiling, simulation and post processing in Fusion’s Manufacture workspace, plus the real limits of the Personal Use licence.
---
=== fr
Autodesk Fusion réunit CAO et FAO dans un même fichier : la pièce modélisée est usinée dans l’espace **Fabrication** (Manufacture), et toute modification du modèle se propage aux parcours après régénération. C’est souvent le premier logiciel de FAO d’un petit atelier.

## Licences : ce que la version Usage personnel ne fait pas

| Fonction | Usage personnel | Commercial |
|---|---|---|
| Fraisage 2 / 2,5 / 3 axes, tournage, profilage plasma, laser, jet d’eau | Oui | Oui |
| Déplacements rapides (G0) | **Sortis à la vitesse d’avance de coupe** | Oui |
| Changement d’outil automatique (un seul outil par fichier posté) | Non | Oui |
| Palpage, 3+2, multiaxe | Non | Selon l’extension |
| Documents modifiables actifs | 10 | Illimité |
| Usage | Non commercial, revenus sous 1 000 $ US/an | Commercial |

> [!WARN] Autodesk précise que la licence Usage personnel est réservée à un usage non commercial. Un atelier qui facture des pièces a besoin d’un abonnement commercial. Le statut « Basic Access » se comporte comme l’Usage personnel.

## Démarche de fraisage 2D

1. Ouvrir l’espace **Fabrication**, onglet Fraisage.
2. Créer une **configuration** (Setup) : orientation du SCU de travail (WCS), origine (coin ou centre du brut, voir [Décalages d’origine](/guides/decalages-origine-g54/)), type et taille du brut.
3. Choisir ou créer les outils dans la **bibliothèque d’outils** ; renseigner diamètre, longueur de sortie, nombre de dents et vitesses.
4. Ajouter les opérations : **Surfaçage**, **2D Adaptive** (évidement à engagement constant), **2D Contour**, **Perçage**.
5. Régler dans chaque opération : hauteurs (dégagement, retrait, haut, bas), passes, surépaisseur, entrées et sorties.
6. **Simuler** avec le brut ; vérifier collisions et matière restante.
7. **Post-traiter** : choisir le post de la machine, la sortie et le programme ; relire l’entête du G-code.

## Découpe plasma, laser et jet d’eau

Fusion traite ces procédés comme du profilage 2D :

- Outil de type plasma, laser ou jet d’eau, avec **largeur de saignée** (kerf), hauteurs de perçage et de coupe, délai de perçage.
- Opération **Profil 2D** de découpe : sélection des contours, côté de compensation, entrées et sorties, mode de compensation (dans l’ordinateur ou dans la commande).
- Pour les tables Langmuir, utilisez les posts publiés par le fabricant afin que le contrôle de hauteur fonctionne — voir [FireControl](/guides/firecontrol-langmuir/).

> [!TIP] La compensation « dans l’ordinateur » décale le parcours de la moitié du kerf ; « dans la commande » sort G41/G42 et laisse la machine compenser. Ne cumulez pas les deux. Voir [Kerf](/guides/kerf-qualite-coupe/).

## Post-processeurs

La **bibliothèque de post-processeurs** d’Autodesk propose des posts génériques et par fabricant (Haas, Fanuc, Mach, LinuxCNC, grbl, plasma…). Un post modifié se met dans un dossier personnel pour survivre aux mises à jour. Voir [Post-processeurs](/guides/post-processeurs/).

## Erreurs fréquentes

| Erreur | Correctif |
|---|---|
| Origine du WCS différente de celle réglée sur la machine | Documenter l’origine dans la feuille de configuration |
| Hauteurs référencées au modèle au lieu du brut | Revoir les hauteurs « Haut » et « Bas » |
| Rapides lents en Usage personnel pris pour un bogue | C’est une limite de licence |
| Post générique sur une commande spécifique | Prendre le post du fabricant, tester à vide |

## Liste de vérification avant le premier usinage

- [ ] Brut et origine identiques au montage réel
- [ ] Outils mesurés, numéros d’outil cohérents avec la machine
- [ ] Simulation sans collision
- [ ] Bon post, unités vérifiées (G20/G21)
- [ ] Premier passage en l’air ou avec un Z décalé

## FAQ

### Fusion peut-il imbriquer des pièces de tôle ?
Fusion propose une fonction d’imbrication (Arrange) et une extension d’imbrication avancée selon l’abonnement. Pour un atelier plasma, comparez avec la solution intégrée à SheetCam — voir [Imbrication](/guides/imbrication/).

## À valider en atelier (Michaël)

- Post utilisé sur votre table et réglages de hauteur éprouvés.

## Sources

- [Autodesk — Fusion for personal use: limitations](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Fusion-360-Free-License-Changes.html), consulté le 26 novembre 2026.
- [Autodesk — Fusion post library](https://cam.autodesk.com/hsmposts).
- [Autodesk Fusion — Aide en ligne](https://help.autodesk.com/view/fusion360/ENU/).
=== en
Autodesk Fusion combines CAD and CAM in one file: the modelled part is machined in the **Manufacture** workspace, and any model change flows into the toolpaths after regeneration. It is often a small shop’s first CAM software.

## Licences: what Personal Use does not do

| Feature | Personal Use | Commercial |
|---|---|---|
| 2 / 2.5 / 3-axis milling, turning, plasma, laser and waterjet profiling | Yes | Yes |
| Rapid moves (G0) | **Output at the cutting feed** | Yes |
| Automatic tool change (one tool per posted file) | No | Yes |
| Probing, 3+2, multi-axis | No | Per extension |
| Active editable documents | 10 | Unlimited |
| Use | Non-commercial, revenue under US$1,000/yr | Commercial |

> [!WARN] Autodesk states the Personal Use licence is for non-commercial use only. A shop that bills for parts needs a commercial subscription. “Basic Access” status behaves like Personal Use.

## 2D milling workflow

1. Open the **Manufacture** workspace, Milling tab.
2. Create a **Setup**: work coordinate system (WCS) orientation, origin (stock corner or centre, see [Work offsets](/en/guides/work-offsets-g54/)), stock type and size.
3. Pick or create tools in the **tool library**; enter diameter, stick-out, flute count and speeds.
4. Add operations: **Face**, **2D Adaptive** (constant-engagement clearing), **2D Contour**, **Drill**.
5. Set in each operation: heights (clearance, retract, top, bottom), passes, stock to leave, leads.
6. **Simulate** with stock; check collisions and remaining material.
7. **Post process**: pick the machine’s post, output and program number; read the G-code header.

## Plasma, laser and waterjet cutting

Fusion treats these processes as 2D profiling:

- Plasma, laser or waterjet tool type, with **kerf width**, pierce and cut heights, pierce delay.
- Cutting **2D Profile** operation: contour selection, compensation side, leads, compensation mode (in computer or in control).
- For Langmuir tables, use the maker’s published posts so torch height control works — see [FireControl](/en/guides/firecontrol-langmuir/).

> [!TIP] “In computer” compensation offsets the path by half the kerf; “in control” outputs G41/G42 and lets the machine compensate. Never stack both. See [Kerf](/en/guides/kerf-and-cut-quality/).

## Post processors

Autodesk’s **post library** offers generic and maker-specific posts (Haas, Fanuc, Mach, LinuxCNC, grbl, plasma…). Keep a modified post in a personal folder so it survives updates. See [Post processors](/en/guides/post-processors/).

## Common mistakes

| Mistake | Fix |
|---|---|
| WCS origin differs from the one set on the machine | Document the origin on the setup sheet |
| Heights referenced to the model instead of stock | Review “Top” and “Bottom” heights |
| Slow rapids in Personal Use mistaken for a bug | It is a licence limit |
| Generic post on a specific control | Use the maker’s post, dry-run |

## Checklist before the first cut

- [ ] Stock and origin identical to the real setup
- [ ] Tools measured, tool numbers consistent with the machine
- [ ] Simulation collision-free
- [ ] Right post, units checked (G20/G21)
- [ ] First pass in the air or with a raised Z

## FAQ

### Can Fusion nest sheet-metal parts?
Fusion offers an Arrange function and an advanced nesting extension depending on subscription. For a plasma shop, compare with SheetCam’s built-in nesting — see [Nesting](/en/guides/nesting/).

## For Michaël to review

- Post used on your table and proven height settings.

## Sources

- [Autodesk — Fusion for personal use: limitations](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Fusion-360-Free-License-Changes.html), consulted November 26, 2026.
- [Autodesk — Fusion post library](https://cam.autodesk.com/hsmposts).
- [Autodesk Fusion — Online help](https://help.autodesk.com/view/fusion360/ENU/).
