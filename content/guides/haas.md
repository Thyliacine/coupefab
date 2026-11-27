---
id: haas
hub: software
group: control
order: 52
mono: Ha
nav: Commande Haas | Haas control
kicker: Commande machine · Haas | Machine control · Haas
level: intermediaire
schema: HowTo
tags: haas, ngc, next generation control, g154, g110, g187, g103, g47, setting 15, work offsets, tool length, vmc, st lathe, haas post
related: fanuc, work-offsets, gcode, cnc-mill
fr_slug: commande-haas-cnc
en_slug: haas-cnc-control
fr_title: Commande Haas : origines G54/G154, longueurs d’outil, G187 et réglages qui piègent
en_title: Haas CNC control: G54/G154 offsets, tool lengths, G187 and the settings that catch people out
fr_desc: Le dialecte Haas (proche de Fanuc) pour fraiseuses : origines G54–G59, G110–G129 et G154 P1–P99, G43 et le réglage 15, précision de contournage G187, gravure G47, démarche de première pièce.
en_desc: The Haas dialect (close to Fanuc) for mills: G54–G59, G110–G129 and G154 P1–P99 offsets, G43 and Setting 15, G187 contouring accuracy, G47 engraving and a first-part routine.
codes: haas
---
=== fr
Les centres d’usinage et tours **Haas** sont omniprésents dans les ateliers québécois, des écoles aux sous-traitants. Leur commande parle un dialecte **de type Fanuc**, avec des codes et des **réglages (Settings)** propres à Haas. La documentation publique de Haas (manuels en ligne, cahier de programmation) est l’une des plus complètes du marché : servez-vous-en.

## Ce qui est propre à Haas

| Élément | Haas | Remarque |
|---|---|---|
| Origines standard | `G54`–`G59` | Comme Fanuc |
| Origines supplémentaires | `G110`–`G129` puis `G154 P1`–`P99` | `G154` ajoute 99 origines (versions logicielles récentes) |
| Longueur d’outil | `G43 H..` | Le **réglage 15** impose `H` = numéro d’outil (alarme sinon) |
| Précision en grande vitesse | `G187` avec `E` | `E` de 0,0001 à 0,25 ; le réglage 85 fixe la valeur par défaut |
| Anticipation de blocs | `G103 P..` | Limite le nombre de blocs lus d’avance |
| Gravure de texte | `G47` | Texte et numéros de série (variable macro #599) |

> [!NOTE] Les réglages (Settings) modifient le comportement de la machine : unités, sécurité des portes, avance rapide pendant la vérification, etc. Notez ceux qui diffèrent de l’état d’usine avant d’accuser le programme.

## Démarche de première pièce (fraiseuse)

1. **Choisir le post Haas** dans la FAO (Fusion, Mastercam et les autres FAO courantes proposent des posts Haas ; prenez celui qui correspond à la machine et à sa version).
2. **Mesurer les outils** (sonde ou palpeur) et vérifier que chaque `T` a sa longueur `H` correspondante.
3. **Régler l’origine** en mode manivelle (*Handle Jog*) à l’écran des décalages, ou avec le palpeur.
4. **Charger et vérifier** : graphique, puis marche bloc à bloc avec avance et rapide réduits.
5. **Ajuster** l’usure d’outil (pas la géométrie) pour corriger une cote.

```gcode
%
O00010 (SUPPORT OP10)
G00 G17 G20 G40 G49 G80 G90
T1 M06
G00 G90 G54 X-1.5 Y2.5
S2500 M03
G43 Z1. H01 M08
G187 E0.001 (precision de contournage)
...
G187 (retour a la valeur par defaut)
G28 G91 Z0.
M30
%
```

## Liste de vérification

- [ ] Version logicielle connue (certaines fonctions comme `G154` dépendent de la version)
- [ ] Réglage 15 activé si l’atelier impose `H` = `T`
- [ ] Unités du programme = unités de la machine (réglage)
- [ ] Origine appelée par le programme = origine réglée (`G54`, `G110`, `G154 Pn`)
- [ ] `G187` remis par défaut après une finition fine

## Erreurs fréquentes

- Programmer `G154 P5` mais régler l’origine dans `G54` : la pièce est coupée « dans le vide » ou dans l’étau.
- Laisser un `G187 E` très serré pendant l’ébauche : temps de cycle inutilement long.
- Copier un programme Fanuc qui utilise `G54.1 P..` : Haas utilise `G154 P..`. Repostez plutôt que de corriger à la main.
- Oublier de vérifier les M-codes d’options (arrosage par le centre, convoyeur) propres à la machine.

## FAQ

### Haas et Fanuc, c’est la même chose ?
Non. La base G-code est très proche, mais les origines étendues, plusieurs cycles et tous les réglages sont propres à Haas. Utilisez un post Haas.

### Où trouver la liste officielle des codes ?
Dans le manuel de l’opérateur en ligne de Haas (sections G-codes, M-codes et réglages) et dans le cahier de programmation fraiseuse (PDF).

### Combien d’origines puis-je utiliser ?
Six standard, vingt de plus avec `G110`–`G129`, puis 99 avec `G154 P1`–`P99` sur les versions qui l’offrent.

## À valider en atelier (Michaël)

- Versions logicielles et réglages non standard des Haas de l’atelier.
- Valeurs `G187 E` utilisées en finition selon la matière.
- Post Haas retenu pour chaque FAO.

## Sources

- [Haas — Mill Programming Workbook (PDF)](https://haascnc.com/content/dam/haascnc/en/service/reference/programming-workbooks/mill---programming-workbook.pdf) : origines G54–G59, G110–G129, G154 P1–99 ; réglage 15 ; `E` avec G187 ; G103 ; G47. Consulté le 26 novembre 2026.
- [Haas — Manuel de l’opérateur fraiseuse : G-codes](https://haascnc.com/service/online-operator-s-manuals/mill-operator-s-manual/mill---g-codes.html).

=== en
**Haas** machining centers and lathes are everywhere in Quebec shops, from schools to job shops. The control speaks a **Fanuc-style** dialect with codes and **Settings** of its own. Haas’s public documentation (online manuals, programming workbook) is among the most complete on the market: use it.

## What is specific to Haas

| Item | Haas | Note |
|---|---|---|
| Standard offsets | `G54`–`G59` | Same as Fanuc |
| Extra offsets | `G110`–`G129` then `G154 P1`–`P99` | `G154` adds 99 offsets (recent software versions) |
| Tool length | `G43 H..` | **Setting 15** enforces `H` = tool number (alarm otherwise) |
| High-speed accuracy | `G187` with `E` | `E` from 0.0001 to 0.25; Setting 85 sets the default |
| Block look-ahead | `G103 P..` | Limits how many blocks are read ahead |
| Text engraving | `G47` | Text and serial numbers (macro variable #599) |

> [!NOTE] Settings change how the machine behaves: units, door safety, rapid override in graphics, and more. Write down the ones that differ from factory before blaming the program.

## First-part routine (mill)

1. **Pick the Haas post** in CAM (Fusion, Mastercam and the other common CAM packages offer Haas posts; take the one matching the machine and its version).
2. **Measure tools** (setter or probe) and check each `T` has its matching `H` length.
3. **Set the work offset** in *Handle Jog* on the offset page, or with the probe.
4. **Load and verify**: graphics, then single block with reduced feed and rapid.
5. **Adjust** tool wear (not geometry) to correct a size.

```gcode
%
O00010 (BRACKET OP10)
G00 G17 G20 G40 G49 G80 G90
T1 M06
G00 G90 G54 X-1.5 Y2.5
S2500 M03
G43 Z1. H01 M08
G187 E0.001 (contouring accuracy)
...
G187 (back to default)
G28 G91 Z0.
M30
%
```

## Checklist

- [ ] Software version known (some features like `G154` depend on it)
- [ ] Setting 15 on if the shop enforces `H` = `T`
- [ ] Program units = machine units (setting)
- [ ] Offset called by the program = offset set (`G54`, `G110`, `G154 Pn`)
- [ ] `G187` reset to default after a fine finish

## Common mistakes

- Programming `G154 P5` but setting the zero in `G54`: the part is cut in the air, or in the vise.
- Leaving a very tight `G187 E` during roughing: needlessly long cycle time.
- Copying a Fanuc program that uses `G54.1 P..`: Haas uses `G154 P..`. Re-post instead of hand-fixing.
- Forgetting to check machine-specific option M-codes (through-spindle coolant, chip conveyor).

## FAQ

### Are Haas and Fanuc the same?
No. The G-code base is very close, but extended offsets, several cycles and all Settings are Haas-specific. Use a Haas post.

### Where is the official code list?
In Haas’s online operator’s manual (G-codes, M-codes and Settings sections) and the mill programming workbook (PDF).

### How many work offsets can I use?
Six standard, twenty more with `G110`–`G129`, then 99 with `G154 P1`–`P99` on versions that offer it.

## For Michaël to review

- Software versions and non-standard settings on the shop’s Haas machines.
- `G187 E` values used for finishing per material.
- Haas post chosen for each CAM package.

## Sources

- [Haas — Mill Programming Workbook (PDF)](https://haascnc.com/content/dam/haascnc/en/service/reference/programming-workbooks/mill---programming-workbook.pdf): offsets G54–G59, G110–G129, G154 P1–99; Setting 15; `E` with G187; G103; G47. Consulted November 26, 2026.
- [Haas — Mill operator’s manual: G-codes](https://haascnc.com/service/online-operator-s-manuals/mill-operator-s-manual/mill---g-codes.html).
