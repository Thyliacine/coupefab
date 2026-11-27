# CoupeFab — admin guide: revenue features

Four ways to earn money are built and ready. **All are off.** With every switch off, the public site is exactly what it was before. Nothing is linked, nothing is indexed, and nobody is charged or contacted.

## 0. Web admin (production): `https://coupefab.ca/admin/`

Password-protected inbox and settings. `noindex`, not linked from the public nav or sitemap.

- **Inbox** — quote requests, newsletter/contact forms, supplier submissions, and inbound email to `info@coupefab.ca` (once MX is in place). Status new / read / archived, search, CSV export, attachments, and replies (Send only; no auto-reply).
- **Storage** — Vercel Blob store `coupefab-inbox` (private, Hobby free tier). Forms write here directly. FormSubmit is no longer used.
- **Login** — `ADMIN_PASSWORD` env var, session cookie (`cf_admin`, 12 h, HttpOnly, Secure, SameSite=Lax), 5 attempts / 15 minutes / IP.
- **Reply / inbound email** — Resend free tier. Set `RESEND_API_KEY`, `RESEND_WEBHOOK_SECRET`, and optionally `RESEND_FROM` (default `CoupeFab <info@coupefab.ca>`). Webhook URL: `https://coupefab.ca/api/inbound-email`. Add the MX / SPF / DKIM records Resend shows for each domain (none are on the domains today). Do not point mail at a personal Gmail inbox.
- **Switches / partner / sponsors / affiliates** — also in this admin, saved to Blob. The public site still reads the repo JSON until a rebuild and deploy. Use « Télécharger le JSON » if you want the files for a local build. Featured suppliers stay read-only (paid hook only).

The local page `python3 scripts/admin.py` (127.0.0.1 only) still edits the repo files directly.


## 1. The switches: `config/monetization.json`

| Switch | What turns on |
|---|---|
| `featured_suppliers` | An “En vedette / Featured” block, marked **Commandité / Sponsored**, at the top of `/fournisseurs/`, `/prix/`, `/pieces/` and `/outillage/` (and the EN pages). Only suppliers with an active paid subscription appear. |
| `affiliate_links` | A “Où acheter / Where to buy” box on parts and tooling pages, for slots that have a URL. Links are `rel="sponsored nofollow"` with a disclosure line. The footer, home page and disclosure page then say affiliate links exist. |
| `digest_sponsor` | One “Commandité” box in the price newsletter (`scripts/digest.py`). |
| `quote_requests` | Publishes `/soumission/` and `/en/quote/`, adds a footer link, and adds a “Demander une soumission” box on suppliers, parts and tooling. |
| `advertise_page` | Publishes `/annoncer/` and `/en/advertise/`. **Prices still say “à déterminer (TBD)”**, so set them first in `revenue/pages.py`. |

While a page’s switch is off, the page is still built so you can look at it (`/soumission/`, `/annoncer/`). It shows a yellow “Aperçu interne” note and is `noindex`. It is left out of `sitemap.xml` and linked from nowhere.

To change a switch, edit the file by hand or use the local admin (below). Then run `python3 build.py`, check, commit, push and deploy.

## 2. The local admin: `python3 scripts/admin.py`

Open http://127.0.0.1:8765/. It only runs on your own computer and is never deployed. You can:

- **Switches**: turn the five features on or off.
- **Partner**: choose which shops get the unpaid “Partenaire” label (`content/shops.json`). None are marked as partners today. Any future partner must be named on the Divulgation page.
- **Newsletter sponsors**: name, logo, two lines FR/EN, https link, dates and “payé” (`config/sponsors.json`, schema in `config/sponsors.schema.json`). Only one sponsor shows per issue: the first one that is paid and whose dates include today.
- **Affiliate links**: merchant, labels and URL for each slot (`config/affiliate-links.json`). Leave the URL empty until you have joined the program yourself. An empty URL is never shown.
- **Featured suppliers (read only)**: who is featured, their subscription status and dates. **There is no manual picker. Featured means paid.**

## 3. Featured = paid (payment hook)

`data/revenue/featured.json` is written only by `revenue/featured.py → apply_subscription_event()`.

The flow, once you decide to sell spots:

1. Create a product and price in Stripe yourself, plus a Payment Link or Checkout page. **Nothing was created in Stripe.** Put `supplier_id`, `tier` (`standard` or `plus`) and `categories` (e.g. `suppliers,prices`) in the Checkout or Subscription **metadata**.
2. In Stripe → Developers → Webhooks, point an endpoint at `https://coupefab.ca/api/stripe-webhook` with these events: `checkout.session.completed`, `customer.subscription.created`, `customer.subscription.updated` and `customer.subscription.deleted`.
3. In Vercel → Settings → Environment Variables, set:
   - `STRIPE_WEBHOOK_SECRET` (whsec_…)
   - `FEATURED_WEBHOOK_URL`: where events are stored, for example a Google Apps Script that writes to a Sheet.

   Until both are set, the endpoint answers 503.
4. Apply each stored event with `python3 -m revenue.featured event.json` (or from the daily refresh). Add a `profile` object (name, url, logo, blurb_fr, blurb_en) the first time. Rebuild and deploy.

A spot shows only when all of these hold: the switch is on, the status is `active` or `trialing`, and today (Toronto time) is within start..end. If a subscription is cancelled or a payment fails, the spot goes away at the next build.

## 4. Quote requests: `/soumission/` → `api/quote-request.js`

- **Fields:** process, material, thickness, quantity, drawing link or description, region, date needed, name, company, email, phone, and a **Loi 25 consent checkbox** (required; its version is stored with each request).
- **Spam protection:** a hidden honeypot field, a minimum of 3 seconds to fill in, and 5 requests per hour per IP (`QUOTE_RATE_MAX`, `QUOTE_RATE_WINDOW_S`).
- **Where requests go** (set at least one in Vercel):
  - `QUOTE_WEBHOOK_URL` (JSON), or
  - `QUOTE_INBOX=info@coupefab.ca` (FormSubmit; it sends one confirmation email the first time).

  Both fall back to `NEWSLETTER_WEBHOOK_URL` and `NEWSLETTER_INBOX`. Until one is set, the form answers 503 with a clear message.
- **Routing:** each request includes `matched_shops`, the shops that do that process in that region. They come from `data/revenue/lead-routing.json` and `api/_lead-routing.js`, which `python3 -m revenue.routing` regenerates from `content/shops.json`. **Nothing is sent to shops automatically.** You read the request and decide.

## 5. Price newsletter: `python3 scripts/digest.py`

This writes `digest-preview/digest-DATE.{fr,en}.{html,txt}`, which is ignored by git and never deployed. It contains the lowest sheet price per pound by metal and a link to the price tool. The sponsor box is added only when `digest_sponsor` is on and a paid sponsor is in its date range. The script sends nothing; paste the result into your mail tool.

## 6. Previewing everything on (demo)

`config/demo/` has every switch on and **fictitious** example.com data. Build it in a scratch copy only:

```bash
cp -r . /tmp/cf-demo && cd /tmp/cf-demo && COUPEFAB_REVENUE_DIR=config/demo python3 build.py
```

Never deploy a demo build.

## 7. Before switching anything on

- Set real prices on `/annoncer/` (now TBD) and reread the draft paragraphs that get added to `/divulgation/`.
- `quote_requests`: set `QUOTE_INBOX` or `QUOTE_WEBHOOK_URL` first, and reread the consent text against the privacy page.
- `affiliate_links`: join the program yourself, then paste the URL.
- `featured_suppliers`: see section 3.

## Note : noms de classes

Ne jamais préfixer les classes ou id de l’admin par `ad-` (ni `ad`, `ads`, `advert`…) : les listes des bloqueurs de pub (EasyList, Liste FR) masquent `.ad-top`, `.ad-panel`, `.ad-btn`, `.ad-tabs`, `.ad-detail`, ce qui donnait une page blanche après connexion. Le préfixe est `cfa-`.
