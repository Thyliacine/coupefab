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
| `prices/page.py` | Rendu FR/EN : recherche rapide, onglets (Comparer, Calculateur, Tendances, Nuances & calibres, Méthode & sources), cartes « meilleure offre », pastilles qualité-prix vs médiane, boutons d’achat, schema.org `Dataset`. |
| `js/prix.js`, `css/prix.css` | JS natif (onglets avec hash d’URL, filtres, tri, cartes mobiles, calculateur, graphique) et styles propres à la page (préfixe `.px`, ne touche pas au CSS global). |
| `data/prices/latest.json` | Toutes les lignes du dernier relevé + statut par fournisseur + taux BdC. |
| `data/prices/history/AAAA-MM.csv` | Journal daté : chaque prix vu pour la première fois et chaque changement de prix/stock. |
| `data/prices/index.csv` | Indice quotidien : médiane CAD/lb par famille et forme (courbe de tendance). |
| `prix/donnees-toles.json`, `prix/donnees.json`, `prix/coupefab-prix-metaux.csv` | Données publiques générées par `build.py` : tôle/plaque seulement (chargé d’abord, ~220 Ko), toutes les formes (chargé à la demande), CSV. |

### Rafraîchir (routine quotidienne)

```bash
# dépendances (une fois) : python3 -m venv /workspace/coupefab-venv-tools && /workspace/coupefab-venv-tools/bin/pip install requests beautifulsoup4 lxml
scripts/refresh.sh                      # QUOTIDIEN : tôle et plaque, tous les fournisseurs (~6-8 min, Metals Depot est le plus lent)
scripts/refresh.sh --weekly             # HEBDOMADAIRE : ajoute barres, tubes et tuyaux (collections Metals 'R' Us, ~+1 min, plus lourd)
scripts/refresh.sh --only metalsrus     # un ou plusieurs fournisseurs; les autres sont repris de latest.json
```

`refresh.sh` relève les prix, régénère **tout** le site (`build.py`), fait un commit local des seuls fichiers de prix et écrit `/tmp/coupefab-deploy/create_deployment.json` + `uploads.json` (tout le site, pour ne pas écraser les autres pages).
Déploiement : `create_deployment` du connecteur Vercel (équipe `micro-bot` = `team_51rPr828F5cibUCQd4qzdhyb`, projet `coupefab`) en passant le **contenu** de `create_deployment.json` comme objet d’arguments (pas une référence `$file:` en chaîne); si Vercel répond `missing_files`, `upload_file` (`xVercelDigest`=SHA, `contentLength`=taille, `requestBody`=`$file:<b64_path>`) pour les fichiers modifiés listés dans `uploads.json` (au minimum `prix/*`, `en/sheet-prices/index.html`, `js/prix.js`, `css/prix.css`, `sitemap.xml`), puis relancer.
Puis pousser les fichiers modifiés sur GitHub (`Thyliacine/coupefab`).
Vérifier ensuite : `curl -s https://coupefab.vercel.app/prix/ | grep -o 'Mis à jour[^<]*'`.

En quotidien, les lignes barre/tube/tuyau sont reprises du dernier relevé hebdomadaire avec leur propre date.
Millennium Alloys (C.-B.) et National Salvage (Alb.) sont des repères canadiens masqués par défaut (filtre « Achetable au Québec ») et jamais « meilleur prix ».

Pastilles : pour chaque spécification (famille + sous-classe + épaisseur; $/pi² pour tôle/plaque, $/pi ou $/lb pour barres/tubes, jamais mélangés), médiane du meilleur prix unitaire de chaque fournisseur achetable au Québec; ≥ 2 fournisseurs requis. « Meilleur prix » = le plus bas; « Bon prix » ≤ −10 %; « Dans la moyenne » ±10 %; « Cher » ≥ +10 % (`TIER_PCT` dans `page.py`). Repères, ruptures et valeurs « à vérifier » affichent l’écart sans pastille de classement.
Boutons : « Acheter » (fournisseur qui livre au Québec) ou « Voir chez … » (cueillette, repères) mènent à la fiche produit (`buy_url`; pour Metals Depot, l’ancre `#id` de la ligne produit sur la page catégorie); « Demander un prix » mène à la page contact/soumission (`QUOTE_URL` dans `page.py`). Aucun paramètre d’affiliation.

### Licence des données

Les données compilées (`data/prices/`, `prix/donnees.json`, `prix/coupefab-prix-metaux.csv`) sont publiées sous
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — réutilisation libre en citant CoupeFab. Les prix restent ceux des fournisseurs cités.

Un fournisseur en échec garde ses lignes de la veille, marquées « [relevé précédent] », et son erreur est inscrite dans `latest.json` → `status`.
