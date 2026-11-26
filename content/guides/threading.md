---
id: threading
hub: fundamentals
order: 41
nav: Taraudage et filetage à la fraise | Tapping and thread milling
kicker: Fondamentaux · filetage | Fundamentals · threading
level: intermediaire
schema: HowTo
tags: tapping, taraudage, rigid tapping, taraudage rigide, g84, g74, thread milling, filetage à la fraise, fraise à fileter, form tap, taraud à refouler, pitch, pas, tpi, blind hole, trou borgne
related: canned-cycles, cnc-mill, feeds-speeds, haas
fr_slug: taraudage-filetage-fraise
en_slug: tapping-thread-milling
fr_title: Taraudage ou filetage à la fraise : choisir la méthode et programmer sans casser
en_title: Tapping or thread milling: picking the method and programming without breakage
fr_desc: Quand tarauder et quand fileter à la fraise, la règle avance = pas × tr/min du taraudage rigide, un exemple G84, et les précautions pour les trous borgnes et les pièces chères.
en_desc: When to tap and when to thread mill, the rigid tapping rule feed = pitch × RPM, a G84 example, and precautions for blind holes and expensive parts.
---
=== fr
Deux méthodes dominent pour les filets intérieurs sur un centre d’usinage : le **taraudage** (rapide, économique, surtout pour les petits filets) et le **filetage à la fraise** (plus sûr et plus flexible). Le bon choix dépend de la pièce, de la matière et de la quantité.

## Comparer les méthodes

| Critère | Taraudage | Filetage à la fraise |
|---|---|---|
| Vitesse | Très rapide | Plus lent (interpolation hélicoïdale) |
| Outils | Un taraud par dimension | Une fraise couvre plusieurs diamètres de même pas |
| Bris d’outil | Taraud cassé souvent difficile à retirer | La fraise se retire toujours de la pièce |
| Copeaux | Dépend de la matière et du taraud | Coupe interrompue, bon fractionnement |
| Fond de trou borgne | Filets incomplets sur l’entrée du taraud | Filets complets près du fond |
| Ajustement | Fixé par le taraud | Réglable par la compensation de rayon |
| Machine | Toute machine, taraudage rigide ou porte-taraud | Interpolation X, Y, Z simultanée |

**Règle simple** : beaucoup de trous de même taille → taraudage. Pièce chère, matière difficile, paroi mince, filet près du fond ou grand diamètre → filetage à la fraise.

## Taraudage rigide : avance = pas × vitesse

En taraudage rigide, l’avance et la vitesse de broche sont synchronisées :

- **Métrique** : avance (mm/min) = pas (mm) × tr/min. M8 × 1,25 à 500 tr/min → 625 mm/min.
- **Pouces** : avance (po/min) = (1 ÷ filets par pouce) × tr/min. 7/16-14 à 500 tr/min → 35,7143 po/min.

```gcode
T18 M06 (TARAUD 7/16-14)
G90 G54 G00 X0.625 Y0.625
S500
G43 H18 Z1. M08
G84 G99 Z-0.65 R0.1 F35.7143
X-0.625 Y-0.625
G80 G00 Z1. M09
```

Sur Haas, `G84` démarre la broche lui-même ; `G74` taraude à gauche. Voir [[canned-cycles]].

## Liste de vérification

- [ ] Diamètre de perçage adapté au type de taraud (à couper ou à refouler, voir la fiche du fabricant)
- [ ] Profondeur de perçage plus grande que la profondeur filetée (trou borgne)
- [ ] Avance = pas × tr/min (taraudage rigide)
- [ ] Lubrification adaptée à la matière
- [ ] Jauge tampon entre / n’entre pas sur la première pièce

## Erreurs fréquentes

- Arrondir l’avance de taraudage : écrivez toutes les décimales nécessaires.
- Percer trop court dans un trou borgne : le taraud touche le fond et casse.
- Utiliser le diamètre de perçage d’un taraud à couper pour un taraud à refouler.
- Tarauder une pièce de grande valeur en dernière opération sans plan B.

## FAQ

### Le filetage à la fraise est-il toujours plus lent ?
Généralement oui pour les petits filets, mais il évite les arrêts pour taraud cassé et réduit le nombre d’outils au magasin.

### Puis-je fileter à l’extérieur avec une fraise à fileter ?
Oui, en interpolation autour d’un tenon, ce qu’un taraud ne peut pas faire.

## À valider en atelier (Michaël)

- Méthode privilégiée chez nous selon la matière (inox, aluminium, acier).
- Marques de tarauds et de fraises à fileter utilisées.

## Sources

- [Sandvik Coromant — Threading](https://www.sandvik.coromant.com/en-us/knowledge/threading) : avantages du taraudage et du filetage à la fraise. Consulté le 26 novembre 2026.
- [Sandvik Coromant — What is thread milling?](https://www.sandvik.coromant.com/en-us/knowledge/threading/thread-milling) : cas où le filetage à la fraise s’impose.
- [Haas — Mill Programming Workbook (PDF)](https://haascnc.com/content/dam/haascnc/en/service/reference/programming-workbooks/mill---programming-workbook.pdf) : G84, règle 1/TPI × tr/min, exemple 7/16-14.

=== en
Two methods dominate internal threads on a machining center: **tapping** (fast, economical, especially for small threads) and **thread milling** (safer and more flexible). The right choice depends on the part, the material and the quantity.

## Comparing the methods

| Criterion | Tapping | Thread milling |
|---|---|---|
| Speed | Very fast | Slower (helical interpolation) |
| Tools | One tap per size | One mill covers several diameters of the same pitch |
| Tool breakage | A broken tap is often hard to remove | The mill always comes out of the part |
| Chips | Depends on material and tap | Interrupted cut, good chip breaking |
| Blind-hole bottom | Incomplete threads on the tap’s lead | Full threads near the bottom |
| Fit | Set by the tap | Adjustable through radius compensation |
| Machine | Any machine, rigid tapping or tap holder | Simultaneous X, Y, Z interpolation |

**Simple rule**: many holes of the same size → tap. Expensive part, difficult material, thin wall, thread near the bottom or large diameter → thread mill.

## Rigid tapping: feed = pitch × speed

In rigid tapping, feed and spindle speed are synchronized:

- **Metric**: feed (mm/min) = pitch (mm) × RPM. M8 × 1.25 at 500 RPM → 625 mm/min.
- **Inch**: feed (in/min) = (1 ÷ threads per inch) × RPM. 7/16-14 at 500 RPM → 35.7143 in/min.

```gcode
T18 M06 (7/16-14 TAP)
G90 G54 G00 X0.625 Y0.625
S500
G43 H18 Z1. M08
G84 G99 Z-0.65 R0.1 F35.7143
X-0.625 Y-0.625
G80 G00 Z1. M09
```

On Haas, `G84` starts the spindle itself; `G74` taps left-hand. See [[canned-cycles]].

## Checklist

- [ ] Drill size suited to the tap type (cutting or forming, see the maker’s data)
- [ ] Drill depth deeper than thread depth (blind hole)
- [ ] Feed = pitch × RPM (rigid tapping)
- [ ] Lubrication suited to the material
- [ ] Go / no-go plug gauge on the first part

## Common mistakes

- Rounding the tapping feed: write all the decimals needed.
- Drilling too short in a blind hole: the tap bottoms out and breaks.
- Using a cutting tap’s drill size for a forming tap.
- Tapping a high-value part as the last operation with no plan B.

## FAQ

### Is thread milling always slower?
Usually for small threads, but it avoids broken-tap stoppages and frees magazine pockets.

### Can I cut external threads with a thread mill?
Yes, by interpolating around a boss, which a tap cannot do.

## For Michaël to review

- Preferred method here by material (stainless, aluminum, steel).
- Tap and thread-mill brands we use.

## Sources

- [Sandvik Coromant — Threading](https://www.sandvik.coromant.com/en-us/knowledge/threading): advantages of tapping and thread milling. Consulted November 26, 2026.
- [Sandvik Coromant — What is thread milling?](https://www.sandvik.coromant.com/en-us/knowledge/threading/thread-milling): when thread milling is the right choice.
- [Haas — Mill Programming Workbook (PDF)](https://haascnc.com/content/dam/haascnc/en/service/reference/programming-workbooks/mill---programming-workbook.pdf): G84, 1/TPI × RPM rule, 7/16-14 example.
