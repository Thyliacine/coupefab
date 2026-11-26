---
id: siemens-sinumerik
hub: software
group: control
order: 54
mono: Si
nav: Commande Siemens Sinumerik | Siemens Sinumerik control
kicker: Commande machine · Siemens | Machine control · Siemens
level: intermediaire
schema: HowTo
tags: siemens, sinumerik, 828d, 840d sl, one, g54, g505, g599, g500, trans, atrans, cycle800, g291, g290, iso dialect, frames, shopmill, shopturn
related: fanuc, work-offsets, five-axis, gcode
fr_slug: commande-siemens-sinumerik
en_slug: siemens-sinumerik-control
fr_title: Siemens Sinumerik (828D, 840D sl, ONE) : frames, origines G54–G599 et mode ISO
en_title: Siemens Sinumerik (828D, 840D sl, ONE): frames, G54–G599 offsets and ISO mode
fr_desc: Ce qui change sur une commande Sinumerik : origines G54–G57 et G505–G599, G500, frames programmables TRANS/ATRANS, cycles comme CYCLE800, et le passage au dialecte ISO avec G291/G290.
en_desc: What changes on a Sinumerik control: G54–G57 and G505–G599 offsets, G500, programmable frames TRANS/ATRANS, cycles such as CYCLE800, and switching to ISO dialect with G291/G290.
---
=== fr
Les commandes **Siemens Sinumerik** (828D, 840D sl et la génération ONE) équipent beaucoup de centres d’usinage européens, de tours et de machines 5 axes. Elles peuvent lire du code de type ISO (Fanuc), mais leur langage natif repose sur des **frames** et des **cycles** propres à Siemens. Bien comprendre cette différence évite la plupart des surprises.

## Les deux modes de programmation

| Mode | Activation | Usage |
|---|---|---|
| **Mode Siemens** (natif) | par défaut, ou `G290` | Frames, cycles Siemens (`CYCLE800`, etc.), syntaxe complète |
| **Dialecte ISO** (option) | `G291` | Programmes de type Fanuc existants |

`G290` et `G291` s’écrivent **seuls dans leur bloc**. Les cycles Siemens comme `CYCLE800` (plan incliné) ne fonctionnent qu’en mode Siemens.

> [!NOTE] Le dialecte ISO est une option installée ou non selon la machine. Vérifiez avant de choisir un post ISO.

## Origines pièce : différent de Fanuc

| Code | Sinumerik (mode Siemens) |
|---|---|
| `G54`–`G57` | 1re à 4e origine réglable |
| `G505`–`G599` | 5e à 99e origine réglable |
| `G500` | Désactive l’origine réglable courante (avec le frame zéro par défaut) |
| `G53` | Supprime l’origine réglable et programmable pour le bloc seulement |
| `G58`, `G59` | **Décalages programmables axiaux**, pas des origines réglables comme sur Fanuc |

> [!WARN] Un programme Fanuc qui appelle `G58` ou `G59` comme 5e ou 6e origine ne fera pas la même chose en mode Siemens. Repostez avec un post Sinumerik ou remappez vers `G505`/`G506` après vérification.

## Frames programmables

Les **frames** décalent, tournent, mettent à l’échelle ou miroitent le système de coordonnées dans le programme :

- `TRANS X.. Y.. Z..` : décalage absolu (remplace les frames programmables précédents).
- `ATRANS X.. Y.. Z..` : décalage additif (s’ajoute au frame actif).
- `ROT`/`AROT`, `SCALE`/`ASCALE`, `MIRROR`/`AMIRROR` : rotation, échelle, miroir.

## Exemple d’en-tête (mode Siemens)

```gcode
; SUPPORT OP10
N10 T="FRAISE_D12"
N20 M6
N30 S2000 M3 M8
N40 G90 G64 G54 G17 G0 X-72 Y-72
N50 G0 Z2
N60 G1 Z-10 F3000
...
N900 M30
```

Les commentaires commencent par `;`. Sur une machine avec gestion d’outils, l’outil est appelé par **nom** (`T="..."`) ; sinon par numéro, avec le tranchant `D1`.

## Liste de vérification

- [ ] Version (828D, 840D sl, ONE) et options connues : dialecte ISO, gestion d’outils, 5 axes
- [ ] Post écrit pour le mode visé (Siemens ou ISO), pas un post Fanuc générique
- [ ] Origines : `G505`+ plutôt que `G58/G59` pour des origines supplémentaires
- [ ] Mode de contournage (`G64`, `G642`) et tolérances validés en finition
- [ ] Simulation à l’écran avant la première pièce

## Erreurs fréquentes

- Envoyer un programme Fanuc avec `G58`/`G59` en croyant appeler des origines.
- Mélanger cycles Siemens et code ISO sans repasser en `G290`.
- Oublier qu’un `TRANS` remplace les frames programmables actifs alors qu’un `ATRANS` s’y ajoute.
- Appeler un outil par numéro sur une machine configurée pour des noms d’outils.

## FAQ

### ShopMill et ShopTurn, c’est quoi ?
Des interfaces de programmation conversationnelle (à l’atelier) proposées sur les commandes Sinumerik. Elles produisent des programmes en séquences de travail plutôt qu’en G-code écrit à la main.

### Puis-je utiliser mes posts Fanuc ?
Seulement si le dialecte ISO est installé et que vous n’avez pas besoin des cycles Siemens. Pour le 5 axes et les plans inclinés, un post Sinumerik natif est préférable.

### Combien d’origines réglables ?
Jusqu’à 99 : `G54`–`G57` puis `G505`–`G599`, selon la configuration de la machine.

## À valider en atelier (Michaël)

- Option dialecte ISO présente ou non sur nos machines Siemens.
- Gestion d’outils par nom ou par numéro.
- Post FAO utilisé et cycles Siemens autorisés.

## Sources

- [Siemens — SINUMERIK 840D sl / 828D, Programming Manual Fundamentals (PDF)](https://cache.industry.siemens.com/dl/files/800/109760800/att_962405/v1/840Dsl_828D_fundamentals_progr_man_0818_en-US.pdf) : origines G54–G57 et G505–G599, G500, G53, G58/G59, TRANS/ATRANS, exemple de programme. Consulté le 26 novembre 2026.
- [Siemens — SINUMERIK ONE / 840D sl / 828D, ISO dialects (PDF)](https://cache.industry.siemens.com/dl/files/254/109801254/att_1077768/v1/ONE_840Dsl_828D_iso_dialects_fct_man_0721_en-US.pdf) : G290/G291, CYCLE800 en mode Siemens seulement.

=== en
**Siemens Sinumerik** controls (828D, 840D sl and the ONE generation) run many European machining centers, lathes and 5-axis machines. They can read ISO (Fanuc-style) code, but their native language is built on **frames** and Siemens **cycles**. Understanding that difference avoids most surprises.

## The two programming modes

| Mode | How to activate | Use |
|---|---|---|
| **Siemens mode** (native) | default, or `G290` | Frames, Siemens cycles (`CYCLE800`, etc.), full syntax |
| **ISO dialect** (option) | `G291` | Existing Fanuc-style programs |

`G290` and `G291` go **alone in their block**. Siemens cycles such as `CYCLE800` (tilted plane) only work in Siemens mode.

> [!NOTE] The ISO dialect is an option that may or may not be installed. Check before choosing an ISO post.

## Work offsets: not like Fanuc

| Code | Sinumerik (Siemens mode) |
|---|---|
| `G54`–`G57` | 1st to 4th settable zero offset |
| `G505`–`G599` | 5th to 99th settable zero offset |
| `G500` | Deactivates the current settable offset (with the default zero frame) |
| `G53` | Suppresses settable and programmable offsets for that block only |
| `G58`, `G59` | **Axial programmable offsets**, not settable offsets as on Fanuc |

> [!WARN] A Fanuc program that calls `G58` or `G59` as the 5th or 6th offset will not do the same thing in Siemens mode. Re-post with a Sinumerik post, or remap to `G505`/`G506` after checking.

## Programmable frames

**Frames** shift, rotate, scale or mirror the coordinate system inside the program:

- `TRANS X.. Y.. Z..`: absolute shift (replaces earlier programmable frames).
- `ATRANS X.. Y.. Z..`: additive shift (added to the active frame).
- `ROT`/`AROT`, `SCALE`/`ASCALE`, `MIRROR`/`AMIRROR`: rotation, scaling, mirroring.

## Header example (Siemens mode)

```gcode
; BRACKET OP10
N10 T="ENDMILL_D12"
N20 M6
N30 S2000 M3 M8
N40 G90 G64 G54 G17 G0 X-72 Y-72
N50 G0 Z2
N60 G1 Z-10 F3000
...
N900 M30
```

Comments start with `;`. On a machine with tool management, tools are called by **name** (`T="..."`); otherwise by number, with cutting edge `D1`.

## Checklist

- [ ] Version (828D, 840D sl, ONE) and options known: ISO dialect, tool management, 5-axis
- [ ] Post written for the target mode (Siemens or ISO), not a generic Fanuc post
- [ ] Offsets: `G505`+ rather than `G58/G59` for extra offsets
- [ ] Contouring mode (`G64`, `G642`) and tolerances validated for finishing
- [ ] On-screen simulation before the first part

## Common mistakes

- Sending a Fanuc program with `G58`/`G59` believing they call work offsets.
- Mixing Siemens cycles and ISO code without switching back to `G290`.
- Forgetting that `TRANS` replaces active programmable frames while `ATRANS` adds to them.
- Calling a tool by number on a machine set up for tool names.

## FAQ

### What are ShopMill and ShopTurn?
Shop-floor conversational programming interfaces offered on Sinumerik controls. They build programs as work steps rather than hand-written G-code.

### Can I use my Fanuc posts?
Only if the ISO dialect is installed and you don’t need Siemens cycles. For 5-axis and tilted planes, a native Sinumerik post is better.

### How many settable offsets?
Up to 99: `G54`–`G57` then `G505`–`G599`, depending on machine configuration.

## For Michaël to review

- Whether the ISO dialect option is on our Siemens machines.
- Tool management by name or number.
- CAM post used and which Siemens cycles are allowed.

## Sources

- [Siemens — SINUMERIK 840D sl / 828D, Programming Manual Fundamentals (PDF)](https://cache.industry.siemens.com/dl/files/800/109760800/att_962405/v1/840Dsl_828D_fundamentals_progr_man_0818_en-US.pdf): offsets G54–G57 and G505–G599, G500, G53, G58/G59, TRANS/ATRANS, program example. Consulted November 26, 2026.
- [Siemens — SINUMERIK ONE / 840D sl / 828D, ISO dialects (PDF)](https://cache.industry.siemens.com/dl/files/254/109801254/att_1077768/v1/ONE_840Dsl_828D_iso_dialects_fct_man_0721_en-US.pdf): G290/G291, CYCLE800 in Siemens mode only.
