---
id: nesting
hub: fundamentals
order: 22
nav: Imbrication | Nesting
kicker: Fondamentaux · tôlerie | Fundamentals · sheet metal
level: intermediaire
schema: HowTo
tags: nesting, plasma, laser, waterjet, sheetcam, pronest, yield, remnant, common line
related: sheetcam, pronest, kerf, materials-grades
prices: yes
fr_slug: imbrication
en_slug: nesting
fr_title: Imbrication : placer plus de pièces par tôle sans risquer la coupe
en_title: Nesting: more parts per sheet without risking the cut
fr_desc: Espacement, marge de bord, rotation, chutes réutilisables, coupe en ligne commune et ordre de coupe : la méthode pour mieux utiliser chaque tôle, en SheetCam, ProNest ou autre.
en_desc: Spacing, edge margin, rotation, reusable remnants, common-line cutting and cut order: the method to use every sheet better, in SheetCam, ProNest or another CAM.
---
=== fr
L’imbrication (nesting) place les pièces sur la tôle pour minimiser la chute. Chaque point de rendement compte : la matière est souvent le premier coût d’une pièce découpée. Mais une imbrication trop serrée fait bouger les pièces, surchauffe la tôle et ruine la qualité. Voici la méthode.

## Les paramètres qui comptent

| Paramètre | Pourquoi | Comment le fixer |
|---|---|---|
| Espacement entre pièces | Laisser passer entrées, kerf et chaleur | Au moins l’espace nécessaire aux entrées ; plus en tôle épaisse |
| Marge de bord | Bord de tôle rarement droit, souvent abîmé | Mesurer vos tôles ; prévoir pinces ou butées |
| Rotation permise | Mieux remplir | Respecter le sens de laminage si la pièce est pliée ou visible |
| Pièces dans les trous | Utiliser l’intérieur des grandes découpes | Activer si le FAO le permet, en vérifiant l’ordre |
| Ordre de coupe | Pièce qui bouge, accumulation de chaleur | Intérieurs d’abord, répartir la chaleur sur la tôle |

## Démarche pas à pas

1. **Préparer les pièces** avec leurs opérations complètes (kerf, entrées) : SheetCam v8, par exemple, imbrique à partir des parcours existants.
2. **Définir la tôle réelle** : dimensions mesurées, marge de bord, zones abîmées.
3. **Définir les quantités** et les priorités (pièces urgentes d’abord).
4. **Choisir les rotations** : libres, par 90°, ou bloquées (sens de grain, brossage).
5. **Lancer l’imbrication automatique**, comparer les variantes (rendement, longueur des rapides).
6. **Corriger à la main** : déplacer une pièce isolée, ajouter des petites pièces dans les vides.
7. **Vérifier l’ordre** de coupe et la répartition de la chaleur.
8. **Enregistrer la chute** réutilisable (dimensions, nuance, épaisseur) pour le prochain travail.

## Rendement : comment le calculer honnêtement

Rendement = surface des pièces ÷ surface de tôle consommée. Si une chute rectangulaire est vraiment réutilisée, on la retire de la surface consommée ; sinon, elle compte comme perte. Croisez avec le prix de la tôle : le [comparateur de prix](/prix/) donne le $/pi² publié par épaisseur et nuance.

## Coupe en ligne commune

Deux pièces rectangulaires peuvent partager une coupe : un seul passage sépare les deux. Gain de temps et de matière, mais :

- le kerf doit être exactement compensé, sinon les deux pièces sont fausses ;
- la qualité des deux côtés de la saignée n’est pas identique en plasma (un côté plus biseauté) ;
- les pièces peuvent basculer en fin de coupe.

ProNest et les FAO laser de production gèrent la ligne commune ; en plasma léger, testez avant d’en faire une habitude.

## Pièces qui basculent

Petites pièces sur une table à lattes : elles tombent ou basculent et accrochent la torche. Solutions : micro-attaches (tabs), ordre de coupe, regrouper les petites pièces au-dessus de lattes, ou laisser un pont de matière.

## Erreurs fréquentes

- Imbriquer sans les entrées : les entrées débordent dans la pièce voisine.
- Espacement trop serré en tôle épaisse : chaleur, déformation, scories.
- Rotation libre sur des pièces brossées ou pliées dans le sens du laminage.
- Oublier les zones de pinces ou de butées.

## Liste de vérification

- [ ] Opérations complètes avant imbrication
- [ ] Dimensions et marge de la tôle réelle
- [ ] Rotations compatibles avec grain et pliage
- [ ] Ordre de coupe : intérieurs d’abord, chaleur répartie
- [ ] Chute réutilisable enregistrée

## FAQ

### L’imbrication automatique fait-elle mieux qu’un humain ?
Sur des dizaines de pièces différentes, en général oui. Sur quelques pièces simples, un placement manuel réfléchi fait aussi bien. Le meilleur résultat combine les deux.

### Faut-il un logiciel dédié ?
Pour un atelier plasma léger, l’imbrication de SheetCam suffit souvent. Pour la production multi-tôles, avec inventaire de chutes, rapports de coût et ligne commune, des logiciels comme ProNest sont conçus pour ça.

## À valider en atelier (Michaël)

- L’espacement et la marge de bord que vous utilisez par épaisseur.
- Votre gestion des chutes (étiquetage, rangement).

## Sources

- [SheetCam LLC — Support Manuals (Auto Nesting Quick Start)](https://sheetcamshop.myshopify.com/pages/support), consulté le 26 novembre 2026.
- [Hypertherm — ProNest nesting software comparison](https://www.hypertherm.com/solutions/about-our-products/pronest-nesting-software/nesting-software-comparison/).
=== en
Nesting places parts on the sheet to minimize scrap. Every point of yield counts: material is often the largest cost of a cut part. But nesting too tight makes parts move, overheats the sheet and ruins quality. Here is the method.

## The parameters that matter

| Parameter | Why | How to set it |
|---|---|---|
| Part spacing | Room for leads, kerf and heat | At least the room the leads need; more on thick plate |
| Edge margin | Sheet edges are rarely straight, often damaged | Measure your sheets; allow for clamps or stops |
| Allowed rotation | Better fill | Respect rolling direction if the part is bent or visible |
| Parts in holes | Use the inside of large cutouts | Enable if the CAM allows, checking order |
| Cut order | Moving parts, heat build-up | Insides first, spread heat across the sheet |

## Step by step

1. **Prepare parts** with complete operations (kerf, leads): SheetCam v8, for example, nests from existing toolpaths.
2. **Define the real sheet**: measured size, edge margin, damaged zones.
3. **Set quantities** and priorities (urgent parts first).
4. **Choose rotations**: free, by 90°, or locked (grain, brushed finish).
5. **Run auto-nesting**, compare variants (yield, rapid length).
6. **Fix by hand**: move an isolated part, drop small parts into gaps.
7. **Check cut order** and heat distribution.
8. **Record the reusable remnant** (size, grade, thickness) for the next job.

## Yield: computing it honestly

Yield = part area ÷ sheet area consumed. If a rectangular remnant is really reused, subtract it from the consumed area; otherwise it counts as loss. Combine with the sheet price: the [price tool](/en/sheet-prices/) gives the published $/sq ft by thickness and grade.

## Common-line cutting

Two rectangular parts can share a cut: one pass separates both. It saves time and material, but:

- kerf must be compensated exactly, or both parts are wrong;
- plasma cut quality differs between the two sides of the kerf (one side more beveled);
- parts can tip at the end of the cut.

ProNest and production laser CAM handle common line; on light plasma, test before making it a habit.

## Tipping parts

Small parts on a slat table drop or tip and catch the torch. Fixes: micro-tabs, cut order, grouping small parts over slats, or leaving a material bridge.

## Common mistakes

- Nesting without leads: leads spill into the neighbouring part.
- Spacing too tight on thick plate: heat, distortion, dross.
- Free rotation on brushed parts or parts bent along the rolling direction.
- Forgetting clamp or stop zones.

## Checklist

- [ ] Complete operations before nesting
- [ ] Real sheet size and margin
- [ ] Rotations compatible with grain and bending
- [ ] Cut order: insides first, heat spread
- [ ] Reusable remnant recorded

## FAQ

### Does auto-nesting beat a human?
On dozens of different parts, usually yes. On a few simple parts, thoughtful manual placement does as well. The best result combines both.

### Do I need dedicated software?
For a light plasma shop, SheetCam nesting is often enough. For multi-sheet production with remnant inventory, cost reports and common line, software like ProNest is built for it.

## For Michaël to review

- The spacing and edge margin you use by thickness.
- How you manage remnants (labelling, storage).

## Sources

- [SheetCam LLC — Support Manuals (Auto Nesting Quick Start)](https://sheetcamshop.myshopify.com/pages/support), consulted November 26, 2026.
- [Hypertherm — ProNest nesting software comparison](https://www.hypertherm.com/solutions/about-our-products/pronest-nesting-software/nesting-software-comparison/).
