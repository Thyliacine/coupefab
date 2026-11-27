"""Home pages (FR / EN)."""
from .taxonomy import T, PATHS
from .layout import esc
from news.page import home_section as hot_news


def home(lang, form_newsletter, prix_meta=None):
    fr = lang == "fr"
    t, p = T[lang], PATHS[lang]
    arrow = "\u2192"
    links = [
        (p["prices"], t["prices_nav"],
         "Comparer les prix publiés, en $ CA par pi² et par lb." if fr else "Compare published prices in CAD per sq ft and per lb.",
         t["prices_cta_b"]),
        (p["suppliers"], "Fournisseurs" if fr else "Suppliers",
         "Répertoire québécois et canadien, avec prix lorsqu’ils sont publics." if fr else "Quebec and Canadian directory, with prices when they are public.",
         "Voir le répertoire" if fr else "Open the directory"),
        (p["used"], t["used"],
         "Machines et équipements d’occasion au Québec et au Canada." if fr else "Used machines and equipment in Quebec and Canada.",
         "Voir les annonces" if fr else "Browse listings"),
        (p["tools"], t["tools"],
         "Calculateur de liquide de coupe et autres outils d’atelier." if fr else "Coolant calculator and other shop-floor tools.",
         t.get("all_tools", "Tous les outils" if fr else "All tools")),
    ]
    tiles = "".join(
        f'<a href="{href}"><strong>{title}</strong><span>{desc}</span><span class="more">{cta} {arrow}</span></a>'
        for href, title, desc, cta in links
    )
    return f"""
<section class="hero2">
  <div class="hero2-inner">
    <p class="kicker kicker-light">{'CNC · plasma · laser · usinage · tôlerie' if fr else 'CNC · plasma · laser · machining · sheet metal'}</p>
    <h1>{'Couper, plier et usiner juste, du premier coup.' if fr else 'Cut, bend and machine it right the first time.'}</h1>
    <p class="hero2-lede">{'Guides d’atelier sourcés, prix des tôles comparés et nouvelles de l’industrie, en français d’abord.' if fr else 'Sourced shop-floor guides, compared sheet prices and industry news, French-first.'}</p>
    <button class="hero-search" type="button" data-search-open>
      <svg viewBox="0 0 24 24" aria-hidden="true" class="ico"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 20l-3.6-3.6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      <span>{esc(t['search_ph'])}</span><kbd>/</kbd>
    </button>
  </div>
</section>
<div class="page page-home">
<section class="home-quick" aria-label="{'Accès rapide' if fr else 'Quick links'}">
  {tiles}
</section>
{hot_news(lang)}
<section class="price-feature">
  <div class="price-feature-txt">
    <p class="kicker">{'Prix des tôles' if fr else 'Sheet prices'}</p>
    <h2>{'Le bon prix, et le mauvais, d’un coup d’œil.' if fr else 'Spot a good price, and a bad one, at a glance.'}</h2>
    <p>{'Acier, inox et aluminium en tôle, plaque, barre et tube. Les prix publiés sont convertis en $ CA, le meilleur prix par spécification est mis en évidence, et chaque ligne renvoie à sa source.' if fr else 'Steel, stainless and aluminum in sheet, plate, bar and tube. Published prices are converted to CAD, the best price for each spec is highlighted, and every row links to its source.'}</p>
    <div class="actions"><a class="btn btn-lg" href="{p['prices']}">{t['prices_cta_b']}</a></div>
  </div>
  <div class="price-feature-art" aria-hidden="true">
    <div class="pf-row pf-best"><span>A36 · 1/4"</span><b>{'meilleur' if fr else 'best'}</b></div>
    <div class="pf-row"><span>5052-H32 · 0.125"</span><i></i></div>
    <div class="pf-row pf-high"><span>304 2B · 16 ga</span><b>{'élevé' if fr else 'high'}</b></div>
    <div class="pf-row"><span>6061-T6 · 3/8"</span><i></i></div>
  </div>
</section>
<section class="home-news" id="infolettre">
  <p class="kicker">{t['news']}</p>
  <h2>{t['news_t']}</h2>
  <p>{t['news_d']}</p>
  <div class="stack">{form_newsletter(lang)}</div>
</section>
</div>
"""
