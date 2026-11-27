# CoupeFab

Site francophone d’abord (avec version anglaise) pour les ateliers de découpe plasma et de fabrication métallique au Québec : guides CAD/CAM, digest d’occasions, suivi des prix de tôles publiés.

Live : https://coupefab.ca  (ancien hôte : https://coupefab.vercel.app)

Admin (protégé par mot de passe, noindex) : https://coupefab.ca/admin/ — boîte de réception des formulaires et des courriels info@. Rien n’est transféré vers Gmail.

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
| `prices/page.py` | Rendu FR/EN : recherche rapide, onglets (Comparer, Calculateur, Tendances, Alliages & épaisseurs, Méthode & sources), cartes « meilleure offre », étiquettes de prix vs médiane (tableau groupé par produit), boutons d’achat, schema.org `Dataset`. |
| `js/prix.js`, `css/prix.css` | JS natif (onglets avec hash d’URL, filtres, tri, cartes mobiles, calculateur, graphique) et styles propres à la page (préfixe `.px`, ne touche pas au CSS global). |
| `data/prices/latest.json` | Statut par fournisseur + taux BdC + liste des fichiers de lignes (`rows_files`, `n_rows`). |
| `data/prices/latest-rows/part-NN.jsonl` | Toutes les lignes du dernier relevé, une par ligne, ≤ 4 Mo par fichier (limite de 8 Mo du connecteur GitHub). Lecture/écriture : `prices/store.py`. |
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

`refresh.sh` relève les prix **et** les occasions (`python -m used.fetch_listings`), régénère **tout** le site (`build.py`), fait un commit local des fichiers de prix et d’occasions, et prépare le déploiement via `scripts/deploy_manifest.py`.
Déploiement (méthode **site.tgz**) : le manifeste empacte le site construit dans `/tmp/coupefab-deploy/site.tgz` et écrit un `create_deployment` de trois fichiers (`src/site.tgz`, `src/vercel.json` issu de `scripts/vercel-deploy.json`, `src/api/subscribe.js`). Le `vercel.json` de déploiement lance `mkdir -p public && tar xzf site.tgz -C public` (`rootDirectory` = `src`). Appeler `upload_file` pour tout SHA nouveau (`xVercelDigest`, `contentLength`, `requestBody`=`$file:<b64_path>`, équipe `micro-bot` = `team_51rPr828F5cibUCQd4qzdhyb`, projet `coupefab`), puis `create_deployment` avec le contenu de `requestBody.json`. Ne pas renvoyer les ~200 pages une par une : les déploiements récents ne conservent que le tarball.
Puis pousser les fichiers modifiés sur GitHub (`Thyliacine/coupefab`).
Vérifier ensuite : `curl -s https://coupefab.ca/prix/ | grep -o 'Mis à jour[^<]*'`.

En quotidien, les lignes barre/tube/tuyau sont reprises du dernier relevé hebdomadaire avec leur propre date.
Sources relevées (19) : Metals ’R’ Us, Metals Depot (USD → CAD), United Stainless (indicatif), Mercier 40 (surplus), Princess Auto, Millennium Alloys et National Salvage (repères), et depuis le balayage du 26 nov. 2026 : Aluminox (Montréal), Forces Inc (Blainville), Valmont Metal (Montréal), Acier Terrebonne, WeMachine & Fabricate, Smith Metal Shop, OptiKutz, Canadian Laser Supply, Coop Recyborg (Montréal, tableau public au pied), Aircraft Spruce Canada (Brantford; prix CAD sur les pages catalogue — le PDF imprime « --- »), Cobalt Industrial (Barrie/Calgary; quincaillerie H. Paulin), Metal Pros (Ottawa; catalogue public GET de quote.metalpros.com, au pied ou au pi² — chutes et lots aléatoires non ajoutés). `prices/fetch_more.py` contient les lecteurs génériques (Shopify `products.json`, API WooCommerce Store) : une ligne par section, la plus grande longueur ou le plus grand format offert. Quotidien : tôles/plaques et petites boutiques Shopify; hebdomadaire (`--weekly`) : barres/tubes/tuyaux/cornières de Metals ’R’ Us, Metals Depot (39 catégories, une requête de prix par produit) Acier Terrebonne et Coop Recyborg (`WEEKLY` dans `fetch_prices.py`).

Balayage des sources : `data/sources/discovery-log.csv` (5 passes : recherche web FR/EN par nuance et forme; répertoires, régions et places de marché; liens/concurrents, forums, vendeurs américains; catalogues et listes de prix PDF, y compris la réponse de McMaster-Carr; recherche de catalogues/sources publiques pour tous les fournisseurs encore sans prix). Colonnes : passe, requête, URL, prix publics O/N, livre au QC, robots OK, statut (`added`, `blocked`, `quote-only`, `irrelevant`, `pending`). Les fournisseurs « sur demande » trouvés sont ajoutés (ajout seulement) à `/workspace/coupefab-supplier-contacts.csv` avec la note « from price sweep ».

Appariement : `normalize.section_key()` ramène chaque section publiée à une clé canonique (rond Ø, plat ép × larg, carré, hex, tube rond DE × paroi, tube carré/rect côtés × paroi, tuyau NPS + cédule, cornière aile × aile × ép; calibre de tube → paroi; tolérance ±4,5 % sur la paroi, fractions au 1/64). `grade_group()` regroupe les nuances comparables : acier doux (A36/44W/HR, HSS A500), acier étiré à froid (CR/1018/1020), galvanisé, inox 304/304L, inox 316/316L, aluminium 6061/6063 (profilés). Tôles : épaisseur ramenée au calibre ou à la fraction la plus proche (±7 %). Chaque ligne affiche le nombre de fournisseurs de sa spécification; une spécification à un seul fournisseur propose jusqu’à 3 « specs proches comparables » (même famille, groupe, forme et unité).

Mercier 40 et Coop Recyborg sont classés « Surplus / indicatif » (`SURPLUS` dans `page.py`) : affiché, mais exclu de la médiane et du « Meilleur prix ».

Millennium Alloys (C.-B.) et National Salvage (Alb.) sont des repères canadiens masqués par défaut (filtre « Achetable au Québec ») et jamais « meilleur prix ».

Étiquettes de prix : pour chaque spécification (famille + sous-classe + épaisseur; $/pi² pour tôle/plaque, $/pi ou $/lb pour barres/tubes, jamais mélangés), médiane du meilleur prix unitaire de chaque fournisseur achetable au Québec; ≥ 2 fournisseurs requis. « Meilleur prix » = le plus bas; « Bon prix » ≤ −10 %; « Dans la moyenne » ±10 %; « Cher » ≥ +10 % (`TIER_PCT` dans `page.py`). Repères, ruptures et valeurs « à vérifier » affichent l’écart sans étiquette de classement.
Boutons : « Acheter » (fournisseur qui livre au Québec) ou « Voir chez … » (cueillette, repères) mènent à la fiche produit (`buy_url`; pour Metals Depot, l’ancre `#id` de la ligne produit sur la page catégorie); « Demander un prix » mène à la page contact/soumission (`QUOTE_URL` dans `page.py`). Aucun paramètre d’affiliation.

### Licence des données

Les données compilées (`data/prices/`, `prix/donnees.json`, `prix/coupefab-prix-metaux.csv`) sont publiées sous
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — réutilisation libre en citant CoupeFab. Les prix restent ceux des fournisseurs cités.

Un fournisseur en échec garde ses lignes de la veille, marquées « [relevé précédent] », et son erreur est inscrite dans `latest.json` → `status`.



## Occasions (`used/`)

Comparateur d’équipements CNC et de fabrication usagés : `/occasions/` et `/en/used-equipment/`.

| Fichier | Rôle |
| --- | --- |
| `used/fetch_listings.py` | Robot poli (`CoupeFabOccasionsBot`, robots.txt + Crawl-delay, aucune connexion, aucun contournement anti-robot). Agrège les annonces publiques et le journal des sources. |
| `used/score.py` | Pastilles Super aubaine / Bonne affaire / Prix du marché / Cher : médiane usagée (±10 %, super à −20 %) et écart vs un prix neuf **documenté** (jamais inventé). |
| `used/page.py` | Rendu FR/EN : onglets de catégories, filtres (région depuis Berthierville, prix, année, source, aubaines), cartes, méthodologie. |
| `js/occasions.js`, `css/occasions.css` | Filtres, tri et onglets (préfixe `.oc`). |
| `data/used/listings.json` | Annonces du dernier relevé + taux + table MSRP + statut des sources. |
| `data/used/discovery.csv` | Journal append-only des sources candidates (`added`, `blocked`, `quote-only`, `pending`) et la raison. |
| `data/used/msrp.json` | Prix neufs officiels (URL + date). |
| `data/used/history/AAAA-MM.csv` | Journal daté : première vue et chaque changement de prix ou de statut. |
| `occasions/donnees.json` | Données publiques servies avec la page. |

`scripts/refresh.sh` appelle aussi `used/fetch_listings.py` avant `build.py`. Pour un relevé d’occasions seul : `/workspace/coupefab-venv-tools/bin/python -m used.fetch_listings` puis `python3 -c "from used.page import write_pages; write_pages()"`. Les annonces absentes 14 jours sont marquées périmées ; « vendu » seulement si le vendeur l’indique. Les prix ALX de l’API WooCommerce ne sont pas publiés : les fiches publiques disent « Demander le prix ».

## Design et bibliothèque de guides (`sitekit/`, `content/guides/`)

- `sitekit/` (Python, sans dépendance) : gabarit commun (`layout.py` — en-tête avec méga-menu, recherche, sélecteur FR/EN, pied de page), rendu Markdown maison (`md.py`), taxonomie et chaînes FR/EN (`taxonomy.py`), pages guides / pôles / index (`guides.py`) et accueil (`home.py`). `build.py` l’appelle via `sitekit.extend_pages()` et `sitekit.write_assets()` ; les anciennes chaînes HOME/GUIDES de `build.py` ne servent plus.
- `content/guides/*.md` : un fichier par guide, en-tête (id, hub, group, slugs, titres, description, related, tags…) puis sections `=== fr` et `=== en`. Encadrés `> [!NOTE|TIP|WARN|SHOP]`, listes `- [ ]`, tableaux, `## FAQ` (schema FAQPage), `## Sources`, `## À valider en atelier (Michaël)` / `## For Michaël to review`.
- Pôles : logiciels/software, procedes/processes, fondamentaux/fundamentals, depannage/troubleshooting, atelier/shop. Index de recherche client : `/guides/recherche.json`, `/en/guides/search.json`.
- Styles : `css/site.css` (système de design) par-dessus `css/style.css` ; JS : `js/site.js`.
- Tous les guides sont marqués « Brouillon » jusqu’à la révision de Michaël. Aucun chiffre sans source.

Ajouter un guide : créer `content/guides/<id>.md`, lancer `python3 build.py`, vérifier les liens internes.

## Répertoire des fournisseurs (`/fournisseurs/`, `/en/suppliers/`)

`python -m suppliers.directory [contacts.csv]` régénère `data/suppliers/directory.json` à partir des fournisseurs du comparateur (`data/prices/latest.json`) et du fichier de contacts privé (hors dépôt, par défaut `/workspace/coupefab-supplier-contacts.csv`). Seuls des faits publics sortent du script : nom, villes, province, site web, catégories déduites, langue de service, prix publics oui/non. Aucun nom de personne, courriel ni téléphone.

`suppliers/page.py` rend les deux pages (cartes statiques + filtres `js/fournisseurs.js`, défaut « Toutes »). Le formulaire « Ajoutez vos prix » poste vers `api/supplier-submit.js` : **vérification manuelle obligatoire, rien n’est publié automatiquement**. Stockage : `SUPPLIER_WEBHOOK_URL` (ou `NEWSLETTER_WEBHOOK_URL`) et/ou `SUPPLIER_INBOX` (ou `NEWSLETTER_INBOX`, relais FormSubmit avec pièce jointe). Sans l’une de ces variables, la fonction répond 503 (le fournisseur est invité à réessayer, rien n’est perdu en silence). Le badge « Prix vérifiés » s’active en mettant `"verified": true` sur la fiche après vérification.

## Logo

Marque « Tôle tranchée » (une plaque tranchée par une saignée orange, les deux pièces qui se séparent; option B retenue par Michaël) : `favicon.svg`, `sitekit/layout.py` (`brand_svg`), icônes et images sociales encodées dans `assets/bin/` (`og-fr/en`, `icon-192/512`, `apple-touch-icon`). Source des options et aperçus : `assets/logo/`.

## Calculateur de liquide de coupe (`/outils/calculateur-liquide-de-coupe/`, `/en/tools/coolant-calculator/`)

- `data/coolant-machines.json` : capacité du réservoir d’arrosage (L et gal US) par machine, avec marque, modèle, type et URL source (fiche du fabricant, brochure, manuel, revendeur). **Jamais de capacité inventée** : une machine sans capacité sourcée n’est pas listée (l’utilisateur entre la sienne). Les lignes `dealer_listing: true` viennent d’annonces de revendeurs d’occasion (« à vérifier sur la plaque »). Généré par `/workspace/cf-coolant/build_db.py` (lignes web sourcées : `/workspace/cf-coolant/web_rows.py`), qui retire toute ligne sans capacité. Publié aussi en `outils/machines-liquide-de-coupe.json` (CC BY 4.0).
- `coolant/page.py` rend les deux pages (tableau statique indexable des machines documentées à la main + `outils/calculateur-liquide-de-coupe/machines.json`, chargé par la page : sélecteur et tableau complet). `js/liquide-math.js` contient tout le calcul (remplissage neuf, appoint/correction avec ou sans vidange, Brix × facteur), `js/liquide.js` l’interface, `css/liquide.css` les styles (préfixe `.lq`, par-dessus `outillage.css`).
- Sélecteur de machine : combobox maison (pas de `<datalist>`) — un champ, panneau de résultats juste dessous à la même largeur, groupé par marque (en-têtes collants), modèle + type + capacité, correspondances surlignées, flèches / Entrée / Échap, clic à l’extérieur ferme, bouton effacer, liste pleine largeur à grandes cibles sur mobile. ARIA combobox/listbox (`aria-activedescendant`).
- Lignes `source` = `machinetoolindex.com/machines/…` : capacité lue sur la fiche MachineToolIndex (propriété « Coolant Capacity »), avec `official` = lien du fabricant cité par la fiche. Collecte respectant robots.txt (délai de 2 s, pas de `/api/`). Si une fiche contredit une source déjà présente de plus de 10 %, la ligne existante est gardée et la valeur MTI ajoutée en note.
- Tests : `node tests/test_liquide_math.js`.
- Ajouter une machine : une entrée dans `data/coolant-machines.json` (`brand`, `model`, `type` ∈ vmc/hmc/5ax/lathe/millturn/vtl/boring/router/swiss/grinder, `liters`, `us_gal`, `source`, `source_label`, `checked`), puis `python3 build.py`.
