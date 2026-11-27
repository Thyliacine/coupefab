---
id: alarm-crash-response
hub: troubleshooting
order: 1
nav: Alarme ou collision : premiers gestes | Alarm or crash: first steps
kicker: Dépannage · sur le plancher | Troubleshooting · on the floor
level: debutant
schema: HowTo
tags: alarme, alarm, collision, crash, e-stop, arrêt d’urgence, reset, haas, siemens, fanuc, safe run, historique des alarmes, alarm history, cadenassage, lockout, codes d’erreur, error codes
related: milling-troubleshooting, lockout-cadenassage, work-offsets, probing
fr_slug: alarme-collision-premiers-gestes
en_slug: alarm-crash-first-steps
fr_title: Alarme ou collision sur une machine CNC : les premiers gestes, dans l’ordre
en_title: Alarm or crash on a CNC machine: the first steps, in order
fr_desc: Quoi faire quand une alarme s’affiche ou qu’un outil frappe : sécuriser, noter le code exact, lire l’historique, chercher la cause avant le RESET, vérifier la machine avant de relancer. Avec les consignes publiques de Haas et Siemens.
en_desc: What to do when an alarm appears or a tool hits: make safe, write down the exact code, read the history, find the cause before RESET, check the machine before restarting. With Haas and Siemens public guidance.
---
=== fr
Une alarme n’est pas un bouton à faire disparaître : c’est la commande qui vous dit **ce qu’elle a vu**. Le réflexe « RESET et on relance » efface l’indice le plus utile et, après une collision, peut relancer une machine désalignée. Ce guide donne un ordre simple à suivre, que l’alarme soit un simple message ou qu’un outil vienne de frapper la pièce.

> [!TIP] Pour la signification d’un code précis, utilisez la [recherche de codes d’erreur](/codes-erreur/) : plus de 400 codes tirés des manuels officiels (Haas, Siemens, FANUC, Hypertherm, ESAB, Lincoln, Grbl…), avec la source sous chaque tableau.

## Les 5 premières minutes

1. **Mettre en sécurité.** Si quelque chose bouge encore ou risque de bouger, **arrêt d’urgence**. Personne ne met les mains dans la zone de travail tant que la machine n’est pas arrêtée et, pour tout travail dans la zone dangereuse, cadenassée (voir [[lockout-cadenassage]]).
2. **Ne pas appuyer sur RESET tout de suite.** Prenez une photo de l’écran : numéro **et** texte de l’alarme, ligne de programme, position des axes, outil actif.
3. **Noter le contexte** : programme, numéro d’outil, origine (G54…), ce qui venait d’être changé (outil, correcteur, programme, matière).
4. **Lire l’historique.** Sur Haas, la touche **[ALARMS]** ouvre les onglets *Active Alarm*, *Alarm History* (avec recherche) et *Alarm Viewer* ; l’onglet *Key History* montre les 2000 dernières touches, très utile pour comprendre « ce qu’on a fait juste avant ».
5. **Chercher la signification** du code dans le manuel de la commande ou dans la [recherche de codes](/codes-erreur/), puis **corriger la cause**. Seulement ensuite : acquitter.

> [!WARN] Une personne coincée dans la machine : arrêt d’urgence immédiat. Haas précise que si la personne est pincée ou entraînée, il faut couper l’alimentation ; les axes peuvent alors être déplacés par une force externe pour la dégager.

## Lire l’alarme : ce qu’elle demande pour s’effacer

Les commandes classent les alarmes selon la façon de les effacer. Siemens le documente clairement dans son manuel d’alarmes SINUMERIK (critères d’effacement) :

| Critère d’effacement (Siemens) | Ce que ça veut dire sur le plancher |
|---|---|
| Effacement automatique | L’alarme disparaît d’elle-même quand la cause est réglée (porte fermée, pression revenue). |
| Touche d’effacement ou départ cycle | Message ou avertissement : on lit, on corrige, on efface. |
| RESET puis relancer le programme | Le programme a été interrompu : repartir du bon endroit, pas du milieu d’un mouvement. |
| Mettre la commande hors tension puis sous tension | Défaut plus profond (configuration, entraînement) : noter le code avant de couper. |

Sur les entraînements Siemens (SINAMICS), le manuel distingue **défaut** (*fault* : réaction de l’entraînement, inscrit dans le tampon de défauts, à acquitter après correction) et **alarme** (*alarm* : avertissement qui s’efface seul quand la cause disparaît). Haas, de son côté, place souvent le numéro d’axe devant l’alarme sur la NGC (ex. 1.108 = alarme 108 sur l’axe X).

## Après une collision

Une collision, même lente, peut déplacer un mors, fausser un porte-outil, marquer la broche ou décaler une origine. Avant de relancer en production :

1. **Dégager doucement.** Haas recommande, pour un outil coincé dans la matière : portes fermées, [RESET] pour effacer les alarmes, puis déplacer l’axe en manivelle pour dégager outil et pièce. Pour le changeur d’outil : [RECOVER] et suivre l’écran.
2. **Inspecter l’outil et le porte-outil** : arête, faux-rond au comparateur sur le porte-outil, cône propre.
3. **Vérifier le montage** : étau ou montage déplacé ? Re-palper ou re-mesurer l’origine (voir [[work-offsets]] et [[probing]]).
4. **Vérifier la machine** : bruit anormal de broche, jeu, alarme de servo qui revient. Si la broche ou un axe a pris un choc important, faites vérifier avant de reprendre des tolérances serrées.
5. **Trouver la cause** : Haas cite comme causes fréquentes de collision un **correcteur d’outil** erroné, une **origine** erronée et le **mauvais outil** dans la broche.
6. **Relancer prudemment** : avance et rapide réduits, bloc par bloc sur la zone en cause.

> [!NOTE] **Safe Run (Haas)** : sur les machines et versions logicielles prises en charge, ce mode réduit la vitesse, rend la commande plus sensible à l’erreur de position et recule l’axe dès qu’une collision est détectée. Haas précise qu’il ne détecte les collisions qu’en manivelle et en rapide (G00), pas en avance de travail, et qu’il sert au premier essai d’un programme, pas à la production.

## Erreurs fréquentes

| Erreur | Conséquence |
|---|---|
| RESET avant de noter le code | Diagnostic à l’aveugle, appel au service plus long |
| Relancer au milieu du programme sans vérifier la position | Deuxième collision |
| Changer un correcteur « pour voir » | La vraie cause (mauvais outil, mauvaise origine) reste |
| Ignorer une alarme qui revient | Petite cause qui devient une panne (lubrification, filtre, air) |
| Mettre les mains dans la zone sans cadenasser | Risque grave ; obligation légale au Québec (RSST) |

## Liste de vérification

- [ ] Machine arrêtée, zone sécurisée (cadenassage si intervention dans la zone dangereuse)
- [ ] Photo de l’écran : numéro, texte, ligne, outil, origine
- [ ] Historique des alarmes consulté
- [ ] Signification trouvée dans le manuel ou la [recherche de codes](/codes-erreur/)
- [ ] Cause corrigée avant d’acquitter
- [ ] Après collision : outil, porte-outil, montage et origine vérifiés
- [ ] Relance en avance réduite, bloc par bloc sur la zone en cause
- [ ] Événement noté dans le cahier de la machine

## FAQ

### Est-ce grave de redémarrer la commande pour effacer une alarme ?

Parfois c’est le critère prévu (Siemens : « POWER ON »). Mais notez toujours le code avant : certaines informations disparaissent et le service vous demandera le numéro exact.

### L’alarme revient à chaque fois. Que faire ?

C’est un signal, pas un caprice : la cause n’est pas réglée. Notez quand elle revient (au démarrage, en usinage lourd, au changement d’outil) ; ce contexte oriente le technicien.

### Où trouver la liste complète des alarmes de ma machine ?

Dans le manuel de l’opérateur ou le manuel de diagnostic de la commande, et sur la commande elle-même (Haas : onglet *Alarm Viewer*). La [recherche de codes CoupeFab](/codes-erreur/) regroupe les codes publiés publiquement.

## À valider en atelier (Michaël)

- Procédure maison après collision (qui vérifie, quand appeler le service).
- Cahier de la machine utilisé chez nous.

## Sources

- [Haas — Mill Operator’s Manual, NGC (96-8210, PDF)](https://haascnc.com/content/dam/haascnc/en/service/manual/operator/english---mill-ngc---operator%27s-manual---2025.pdf) : écran Alarms and Messages, Safe Run, récupération après blocage. Consulté le 26 novembre 2026.
- [Siemens — SINUMERIK 828D Alarms, Diagnostics Manual 04/2026](https://cache.industry.siemens.com/dl/files/127/110002127/att_1364390/v1/828D_alarms_diagnostics_man_0426_en-US.pdf) : structure des alarmes, critères d’effacement, défauts et alarmes SINAMICS. Consulté le 26 novembre 2026.
- [CNESST — Cadenassage et autres méthodes de contrôle des énergies (guide, PDF)](https://www.upa.qc.ca/fileadmin/01_UPA_provincial/Prod_SST/Documentation/Cadenassage_controle-energies.pdf). Consulté le 26 novembre 2026.

=== en
An alarm is not a button to make go away: it is the control telling you **what it saw**. The “RESET and restart” reflex wipes out the most useful clue and, after a crash, may restart a misaligned machine. This guide gives a simple order to follow, whether the alarm is a plain message or a tool just hit the part.

> [!TIP] For the meaning of a specific code, use the [error code lookup](/en/error-codes/): more than 400 codes taken from official manuals (Haas, Siemens, FANUC, Hypertherm, ESAB, Lincoln, Grbl…), with the source under each table.

## The first 5 minutes

1. **Make it safe.** If anything is still moving or could move, hit **emergency stop**. Nobody puts hands in the work area until the machine is stopped and, for any work in the danger zone, locked out (see [[lockout-cadenassage]]).
2. **Don’t press RESET yet.** Take a photo of the screen: alarm number **and** text, program line, axis positions, active tool.
3. **Write down the context**: program, tool number, work offset (G54…), what was just changed (tool, offset, program, material).
4. **Read the history.** On Haas, the **[ALARMS]** key opens the *Active Alarm*, *Alarm History* (searchable) and *Alarm Viewer* tabs; the *Key History* tab shows the last 2000 keystrokes, very handy to see “what we did just before”.
5. **Look up the code** in the control manual or the [code lookup](/en/error-codes/), then **fix the cause**. Only then: clear it.

> [!WARN] Someone trapped in the machine: emergency stop immediately. Haas states that if the person is pinched or entangled, power must be turned off; the axes can then be moved by external force to free them.

## Reading the alarm: what it needs to clear

Controls group alarms by how they clear. Siemens documents this clearly in its SINUMERIK alarm manual (cancel criteria):

| Cancel criterion (Siemens) | What it means on the floor |
|---|---|
| Self-clearing | The alarm goes away once the cause is gone (door closed, pressure back). |
| Clear key or cycle start | Message or warning: read it, fix it, clear it. |
| RESET then restart the program | The program was interrupted: restart from the right place, not mid-move. |
| Switch the control off and on | Deeper fault (configuration, drive): write the code down before powering off. |

On Siemens drives (SINAMICS), the manual separates a **fault** (drive response, logged in the fault buffer, acknowledged after the fix) from an **alarm** (a warning that clears itself when the cause disappears). Haas, for its part, often prefixes the axis number on NGC alarms (e.g. 1.108 = alarm 108 on X).

## After a crash

A crash, even a slow one, can shift a jaw, bend a tool holder, mark the spindle or move a work offset. Before going back into production:

1. **Back out gently.** For a tool stuck in material, Haas says: doors closed, [RESET] to clear alarms, then handle-jog the axis to free tool and part. For the tool changer: [RECOVER] and follow the screen.
2. **Inspect tool and holder**: cutting edge, runout on the holder with an indicator, clean taper.
3. **Check the setup**: did the vise or fixture move? Re-probe or re-measure the offset (see [[work-offsets]] and [[probing]]).
4. **Check the machine**: unusual spindle noise, play, servo alarm coming back. If the spindle or an axis took a hard hit, have it checked before holding tight tolerances again.
5. **Find the cause**: Haas lists common crash causes as a wrong **tool offset**, a wrong **work offset** and the **wrong tool** in the spindle.
6. **Restart carefully**: reduced feed and rapid, single block through the problem area.

> [!NOTE] **Safe Run (Haas)**: on supported machines and software, this mode slows motion, makes the control more sensitive to position error and backs the axis off as soon as a crash is detected. Haas notes that it only detects crashes in handle jog and rapid (G00), not in feed moves, and that it is meant for first runs of a program, not production.

## Common mistakes

| Mistake | Consequence |
|---|---|
| RESET before writing the code down | Blind diagnosis, longer service call |
| Restarting mid-program without checking position | A second crash |
| Changing an offset “to see” | The real cause (wrong tool, wrong offset) remains |
| Ignoring an alarm that keeps coming back | A small cause turns into a breakdown (lube, filter, air) |
| Reaching into the zone without lockout | Serious hazard; a legal requirement in Quebec (RSST) |

## Checklist

- [ ] Machine stopped, area safe (lockout for any work in the danger zone)
- [ ] Photo of the screen: number, text, line, tool, offset
- [ ] Alarm history checked
- [ ] Meaning found in the manual or the [code lookup](/en/error-codes/)
- [ ] Cause fixed before clearing
- [ ] After a crash: tool, holder, setup and offset checked
- [ ] Restart at reduced feed, single block through the problem area
- [ ] Event logged in the machine logbook

## FAQ

### Is it bad to power-cycle the control to clear an alarm?

Sometimes that is the intended criterion (Siemens: “POWER ON”). But always write the code down first: some information is lost and service will ask for the exact number.

### The alarm keeps coming back. What now?

It is a signal, not a whim: the cause is not fixed. Note when it returns (at start-up, in heavy cuts, at tool change); that context guides the technician.

### Where is the full alarm list for my machine?

In the control’s operator or diagnostics manual, and on the control itself (Haas: *Alarm Viewer* tab). The [CoupeFab code lookup](/en/error-codes/) gathers publicly published codes.

## For Michaël to review

- Our in-house procedure after a crash (who checks, when to call service).
- The machine logbook we use.

## Sources

- [Haas — Mill Operator’s Manual, NGC (96-8210, PDF)](https://haascnc.com/content/dam/haascnc/en/service/manual/operator/english---mill-ngc---operator%27s-manual---2025.pdf): Alarms and Messages display, Safe Run, recovering from a jam. Consulted November 26, 2026.
- [Siemens — SINUMERIK 828D Alarms, Diagnostics Manual 04/2026](https://cache.industry.siemens.com/dl/files/127/110002127/att_1364390/v1/828D_alarms_diagnostics_man_0426_en-US.pdf): alarm structure, cancel criteria, SINAMICS faults and alarms. Consulted November 26, 2026.
- [CNESST — Lockout and other energy control methods (guide, PDF, French)](https://www.upa.qc.ca/fileadmin/01_UPA_provincial/Prod_SST/Documentation/Cadenassage_controle-energies.pdf). Consulted November 26, 2026.
