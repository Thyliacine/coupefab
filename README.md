# CoupeFab

Site francophone d’abord (avec version anglaise) pour les ateliers de découpe plasma et de fabrication métallique au Québec : guides CAD/CAM, digest d’occasions, suivi des prix de tôles publiés.

Live (Vercel) : https://coupefab.vercel.app

## Contenu

Les six pages d’angle sont des **brouillons** (`brouillon — à réviser par Michaël`) jusqu’à validation technique :

1. Débuter avec SheetCam en français
2. De BricsCAD à un DXF propre
3. Kerf et qualité de coupe
4. Consommables plasma et achats au Canada
5. Évaluer une table plasma usagée au Québec (liste de vérification + digest n° 1)

Aucun paramètre de coupe ni prix n’est inventé. Aucun lien d’affiliation pour le moment.

## Développement

Site statique généré par `build.py`, plus une fonction Vercel `api/subscribe.js`.

```bash
python3 build.py
```

Ouvrir `index.html` ou servir le dossier :

```bash
python3 -m http.server 8080
```

La fonction `/api/subscribe` ne tourne pas dans ce serveur local simple ; utiliser `vercel dev` une fois le projet lié, ou tester après déploiement.

## Infolettre (CASL)

Le formulaire (case de consentement non précochée) envoie un POST JSON à `/api/subscribe`.

Pour une conservation durable, définir dans le projet Vercel (Production + Preview) :

- `NEWSLETTER_INBOX` — une adresse Gmail d’exploitation. Les inscriptions passent par [FormSubmit](https://formsubmit.co). **Confirmez le premier courriel** que FormSubmit envoie à cette boîte.
- et/ou `NEWSLETTER_WEBHOOK_URL` — un script Google Apps Script (ou équivalent) qui ajoute une ligne dans une feuille.

Sans ces variables, l’inscription est acceptée mais n’est consignée que dans le journal éphémère de la fonction (`/tmp` sur Vercel). Configurez au moins `NEWSLETTER_INBOX` avant de pousser l’infolettre.

Les premiers numéros sont prévus pour un envoi manuel depuis Gmail.

## Domaines (plus tard)

`coupefab.ca` et `coupefab.com` sont achetés à part (Porkbun). Ne rien acheter depuis ce dépôt.

Quand les domaines sont actifs, les ajouter dans Vercel : Project → Settings → Domains. Deux approches, au choix :

1. **Enregistrements chez Porkbun** (Vercel affiche les valeurs exactes à coller) :
   - apex (`coupefab.ca` / `coupefab.com`) : enregistrement **A** vers l’IPv4 indiqué par Vercel (souvent `76.76.21.21` — confirmer dans le tableau de bord)
   - `www` : **CNAME** vers `cname.vercel-dns.com` (ou la cible CNAME affichée par Vercel)
2. **Serveurs de noms Vercel** chez Porkbun : `ns1.vercel-dns.com` et `ns2.vercel-dns.com` — Vercel crée alors les enregistrements tout seul.

Faire de `coupefab.ca` le domaine canonique, puis rediriger `www` et `.com` vers celui-ci (ou l’inverse, une fois le choix tranché). Mettre ensuite à jour la constante `SITE` dans `build.py` et régénérer le site pour les URL canoniques, le plan du site et les `hreflang`.

## Licence

Contenu et code : tous droits réservés, CoupeFab / Michaël Brassard, sauf mention contraire des sources citées (Hypertherm, SheetCam, BricsCAD, annonces de tiers, etc.).


## Prix des tôles et des métaux (`/prix/`, `/en/sheet-prices/`)

Comparateur généré à partir de prix **publiés en ligne** — jamais de prix inventé. Chaque ligne garde son URL source et l’heure du relevé.

| Fichier | Rôle |
| --- | --- |
| `prices/fetch_prices.py` | Robot poli (`CoupeFabPrixBot`, robots.txt + Crawl-delay, aucune connexion, aucun contournement anti-robot). Écrit les données normalisées. |
| `prices/normalize.py` | Familles/nuances (catalogue d’atelier), calibres → po/mm, densités, détection forme (tôle, plaque, barre, tube, tuyau). |
| `prices/page.py` | Rendu FR/EN : comparateur filtrable, meilleur prix par spécification, calculateur (kerf + imbrication), indice/tendance, tableau des calibres, schema.org `Dataset`. |
| `js/prix.js` | Tri, filtres, calculateur et graphique (JS natif). |
| `data/prices/latest.json` | Toutes les lignes du dernier relevé + statut par fournisseur + taux BdC. |
| `data/prices/history/AAAA-MM.csv` | Journal daté : chaque prix vu pour la première fois et chaque changement de prix/stock. |
| `data/prices/index.csv` | Indice quotidien : médiane CAD/lb par famille et forme (courbe de tendance). |
| `prix/donnees.json`, `prix/coupefab-prix-metaux.csv` | Données publiques servies par le site (générées par `build.py`). |

### Rafraîchir (routine quotidienne)

```bash
# dépendances (une fois) : python3 -m venv /workspace/coupefab-venv-tools && /workspace/coupefab-venv-tools/bin/pip install requests beautifulsoup4 lxml
scripts/refresh.sh                      # tous les fournisseurs (~6-8 min, Metals Depot est le plus lent)
scripts/refresh.sh --only metalsrus     # un ou plusieurs fournisseurs; les autres sont repris de latest.json
```

`refresh.sh` relève les prix, régénère le site (`build.py`), fait un commit local et écrit `/tmp/coupefab-deploy.json`.
Déploiement : appel `create_deployment` du connecteur Vercel (équipe `micro-bot`, projet `coupefab`) avec le contenu de ce fichier
(chaque fichier y est référencé en `$file:/chemin`). Puis pousser les fichiers modifiés sur GitHub (`Thyliacine/coupefab`).
Vérifier ensuite : `curl -s https://coupefab.vercel.app/prix/ | grep -o 'Mis à jour[^<]*'`.

Un fournisseur en échec garde ses lignes de la veille, marquées « [relevé précédent] », et son erreur est inscrite dans `latest.json` → `status`.
