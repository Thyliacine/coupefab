---
id: mastercam-posts-lathe
hub: software
group: cam
order: 31
mono: Mc
nav: Mastercam post et tour | Mastercam posts and lathe
kicker: Logiciel · FAO | Software · CAM
level: avance
schema: Article
tags: mastercam, post processor, machine definition, control definition, pst, lathe, turning, groove, thread, nci
related: mastercam-2d, post-processors, cnc-lathe, gcode
fr_slug: mastercam-post-tour
en_slug: mastercam-posts-and-lathe
fr_title: Mastercam : définition machine, post-processeur et premiers pas en tournage
en_title: Mastercam: machine definition, post processor and first steps in turning
fr_desc: Comment Mastercam relie définition machine, définition de commande et post-processeur, quoi demander à votre revendeur, et la démarche de base en tournage : brut, mandrin, ébauche, finition, gorge, filetage.
en_desc: How Mastercam links machine definition, control definition and post processor, what to ask your reseller, and the basic turning workflow: stock, chuck, roughing, finishing, grooving, threading.
---
=== fr
Dans Mastercam, le G-code ne sort pas « du parcours » : il passe par une chaîne de trois éléments. Comprendre cette chaîne évite la majorité des surprises au premier programme.

## La chaîne de post-traitement

| Élément | Rôle |
|---|---|
| **Définition machine** | Axes, courses, composants (tourelle, broche, contre-pointe) |
| **Définition de commande** | Comportement de la commande : arcs, compensation, cycles, formats |
| **Post-processeur** | Traduit le fichier intermédiaire (NCI) en G-code pour votre commande |

Le parcours produit un **NCI** (données intermédiaires neutres) ; le post le transforme en programme. Changer de machine, c’est changer la définition machine du groupe.

> [!WARN] Les posts Mastercam sont habituellement fournis et maintenus par le **revendeur**. Demandez un post pour votre modèle et votre commande exacts (par exemple Haas, Fanuc 0i-TF, Okuma), et faites-le valider sur une première pièce simple. Voir [Post-processeurs](/guides/post-processeurs/).

## Quoi demander au revendeur

- [ ] Modèle de machine, commande et options (sous-programmes, cycles fixes, axe C, outils motorisés)
- [ ] Format attendu de l’entête (nom du programme, commentaires, outils)
- [ ] Cycles fixes de perçage et de tournage pris en charge (G71, G76…)
- [ ] Gestion de la vitesse de coupe constante (G96) et de la limite de régime (G50 ou G92 selon la commande)
- [ ] Un programme de test fourni avec le post

## Démarche de tournage

1. Groupe de machine **Lathe** avec la bonne définition.
2. **Propriétés du brut** : diamètre, longueur, face ; **mandrin** et mors ; contre-pointe si besoin.
3. Géométrie : demi-profil dans le plan de tournage (axe Z le long de la pièce, X au diamètre ou au rayon selon la configuration).
4. Opérations dans l’ordre habituel : **dressage** (Face), **ébauche** (Rough ou Dynamic Rough), **finition** (Finish), **gorge** (Groove), **filetage** (Thread), **tronçonnage** (Cutoff).
5. Vérifier en simulation, puis post-traiter.

## Points de vigilance au tour

| Point | Pourquoi |
|---|---|
| Diamètre ou rayon en X | Une erreur double les cotes |
| Limite de régime avec G96 | Sans limite, la broche accélère dangereusement près du centre |
| Rayon de bec d’outil | Compensation (G41/G42) ou parcours compensé, pas les deux |
| Dégagement en fin de gorge | Éviter de frotter en sortie |

Voir aussi [Tour CNC](/guides/tour-cnc/) pour les bases.

## FAQ

### Puis-je modifier un post moi-même ?
Techniquement oui (fichiers .pst), mais un post modifié sans contrôle peut produire un programme dangereux. Gardez l’original, versionnez vos changements et testez à vide.

## À valider en atelier (Michaël)

- Le post et la commande de vos machines ; exemple de programme validé.

## Sources

- [Mastercam — Post processors](https://www.mastercam.com/support/post-processors/), consulté le 26 novembre 2026.
- [Mastercam — Lathe](https://www.mastercam.com/solutions/products/lathe/).
- [Mastercam — Dynamic Motion (tournage dynamique)](https://www.mastercam.com/solutions/products/dynamic-motion/).
=== en
In Mastercam, G-code does not come “from the toolpath”: it goes through a chain of three elements. Understanding that chain avoids most first-program surprises.

## The posting chain

| Element | Role |
|---|---|
| **Machine definition** | Axes, travel, components (turret, spindle, tailstock) |
| **Control definition** | Control behaviour: arcs, compensation, cycles, formats |
| **Post processor** | Translates the intermediate file (NCI) into G-code for your control |

The toolpath produces an **NCI** (neutral intermediate data); the post turns it into a program. Changing machines means changing the group’s machine definition.

> [!WARN] Mastercam posts are usually supplied and maintained by the **reseller**. Ask for a post for your exact model and control (for example Haas, Fanuc 0i-TF, Okuma), and prove it on a simple first part. See [Post processors](/en/guides/post-processors/).

## What to ask your reseller

- [ ] Machine model, control and options (subprograms, canned cycles, C axis, live tooling)
- [ ] Expected header format (program name, comments, tools)
- [ ] Supported drilling and turning canned cycles (G71, G76…)
- [ ] Handling of constant surface speed (G96) and spindle speed limit (G50 or G92 depending on control)
- [ ] A test program supplied with the post

## Turning workflow

1. **Lathe** machine group with the right definition.
2. **Stock properties**: diameter, length, face; **chuck** and jaws; tailstock if needed.
3. Geometry: half-profile in the turning plane (Z along the part, X on diameter or radius depending on setup).
4. Operations in the usual order: **Face**, **roughing** (Rough or Dynamic Rough), **Finish**, **Groove**, **Thread**, **Cutoff**.
5. Verify in simulation, then post.

## Watch-outs on the lathe

| Point | Why |
|---|---|
| Diameter or radius in X | A mistake doubles dimensions |
| Speed limit with G96 | Without a limit, the spindle speeds up dangerously near centre |
| Tool nose radius | Compensation (G41/G42) or compensated path, not both |
| Clearance at the end of a groove | Avoid rubbing on exit |

See also [CNC lathe](/en/guides/cnc-lathe/) for the basics.

## FAQ

### Can I edit a post myself?
Technically yes (.pst files), but an uncontrolled post edit can produce a dangerous program. Keep the original, version your changes and dry-run.

## For Michaël to review

- Post and control for your machines; a proven example program.

## Sources

- [Mastercam — Post processors](https://www.mastercam.com/support/post-processors/), consulted November 26, 2026.
- [Mastercam — Lathe](https://www.mastercam.com/solutions/products/lathe/).
- [Mastercam — Dynamic Motion (dynamic turning)](https://www.mastercam.com/solutions/products/dynamic-motion/).
