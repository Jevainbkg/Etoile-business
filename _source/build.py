#!/usr/bin/env python3
"""Génère les pages HTML statiques d'Etoile Business (FR + EN) dans ../site/.
Optionnel : le site fonctionne sans ce script. Il sert à mettre à jour les
coordonnées partout d'un coup depuis donnees.json."""
import json, html, os, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "site")
D = json.load(open(os.path.join(HERE, "donnees.json"), encoding="utf-8"))
TODAY = datetime.date.today().isoformat()

def t(s):
    """Affiche une valeur ; les [À REMPLACER] sont surlignés."""
    e = html.escape(s)
    return f'<span class="todo">{e}</span>' if s.startswith("[") else e

def plain(s):
    return html.escape(s)

ICON = {
 "transfer": '<path d="M4 8h14M14 4l4 4-4 4M20 16H6M10 12l-4 4 4 4"/>',
 "exchange": '<circle cx="9" cy="9" r="5.5"/><circle cx="15" cy="15" r="5.5"/><path d="M9 6.5v5M15 12.5v5"/>',
 "credit": '<rect x="3" y="6" width="18" height="12" rx="1"/><path d="M3 10h18M7 14.5h4"/>',
 "subscription": '<rect x="4" y="5" width="16" height="15" rx="1"/><path d="M4 9h16M8 3v4M16 3v4M8 13h3M8 16h6"/>',
 "parcel": '<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5 12 12l9-4.5M12 12v9"/>',
}
def icon(name, cls="card__icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICON[name]}</svg>'
WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 20Zm4.4-6c-.2-.1-1.4-.7-1.7-.8s-.4-.1-.5.1-.6.8-.8 1-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.6.3 2.7 2.7 0 0 0-.8 2 4.7 4.7 0 0 0 1 2.5 10.7 10.7 0 0 0 4.1 3.6c1.5.7 2.1.7 2.9.6a2.4 2.4 0 0 0 1.6-1.1 2 2 0 0 0 .1-1.1c0-.1-.2-.2-.4-.3Z"/></svg>'
PHONE_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>'

PAGES = {  # clé : (fichier FR, fichier EN)
 "home": ("index.html", "en/index.html"),
 "services": ("services.html", "en/services.html"),
 "about": ("a-propos.html", "en/about.html"),
 "contact": ("contact.html", "en/contact.html"),
 "legal": ("mentions-legales.html", "en/legal-notice.html"),
 "privacy": ("confidentialite.html", "en/privacy.html"),
}
NAV = ["home", "services", "about", "contact"]
L = {
 "fr": {"lang": "fr", "locale": "fr_FR", "skip": "Aller au contenu", "menu": "Menu", "navlabel": "Navigation principale",
        "nav": {"home": "Accueil", "services": "Services", "about": "À propos", "contact": "Agences & contact", "legal": "Mentions légales", "privacy": "Confidentialité"},
        "wa": "Écrire sur WhatsApp", "call": "Appeler", "switch": ("EN", "English version", "en"),
        "home_aria": "Etoile Business, accueil", "footer_tag": "Messagerie financière : transfert de fonds, change, paiement de crédit et d'abonnements.",
        "f_contact": "Contact", "f_pages": "Pages", "f_info": "Informations", "rights": "Tous droits réservés.",
        "brands": "Les marques citées appartiennent à leurs propriétaires respectifs.", "hours": D["horaires_fr"], "wa_float": "Écrire à Etoile Business sur WhatsApp"},
 "en": {"lang": "en", "locale": "en_US", "skip": "Skip to content", "menu": "Menu", "navlabel": "Main navigation",
        "nav": {"home": "Home", "services": "Services", "about": "About", "contact": "Locations & contact", "legal": "Legal notice", "privacy": "Privacy"},
        "wa": "Message us on WhatsApp", "call": "Call", "switch": ("FR", "Version française", "fr"),
        "home_aria": "Etoile Business, home", "footer_tag": "Money services: transfers, currency exchange, loan and subscription payments.",
        "f_contact": "Contact", "f_pages": "Pages", "f_info": "Information", "rights": "All rights reserved.",
        "brands": "Brand names belong to their respective owners.", "hours": D["horaires_en"], "wa_float": "Message Etoile Business on WhatsApp"},
}
VILLE = D["ville"]
WA = f"https://wa.me/{D['whatsapp_lien']}"
TEL = f"tel:{D['telephone_lien']}"
NETS = D["reseaux"]

def rel(lang):
    return "../" if lang == "en" else ""

def href(lang, key, cur_lang=None):
    """Lien vers la page key dans la langue lang, depuis une page de langue cur_lang."""
    cur_lang = cur_lang or lang
    f = PAGES[key][0 if lang == "fr" else 1]
    if cur_lang == "en":
        return f[3:] if lang == "en" else "../" + f
    return f

def head(lang, key, title, desc, extra=""):
    p = rel(lang); dom = D["domaine"].rstrip("/")
    url_fr = f"{dom}/{PAGES[key][0]}".replace("/index.html", "/")
    url_en = f"{dom}/{PAGES[key][1]}".replace("/index.html", "/")
    canon = url_fr if lang == "fr" else url_en
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{plain(title)}</title>
  <meta name="description" content="{plain(desc)}">
  <link rel="canonical" href="{canon}">
  <link rel="alternate" hreflang="fr" href="{url_fr}">
  <link rel="alternate" hreflang="en" href="{url_en}">
  <link rel="alternate" hreflang="x-default" href="{url_fr}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Etoile Business">
  <meta property="og:locale" content="{L[lang]['locale']}">
  <meta property="og:title" content="{plain(title)}">
  <meta property="og:description" content="{plain(desc)}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{dom}/img/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#14130f">
  <link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
  <link rel="preload" href="{p}fonts/jost-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{p}fonts/jost-500.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{p}css/tokens.css">
  <link rel="stylesheet" href="{p}css/base.css">
  <link rel="stylesheet" href="{p}css/components.css">
{extra}  <script src="{p}js/main.js" defer></script>
</head>"""

def header(lang, key):
    l = L[lang]; p = rel(lang)
    items = "\n".join(
        f'          <li><a class="nav__link" href="{href(lang,k)}"{" aria-current=\"page\"" if k==key else ""}>{l["nav"][k]}</a></li>' for k in NAV)
    s_label, s_title, s_lang = l["switch"]
    return f"""<body>
  <a class="skip-link" href="#contenu">{l['skip']}</a>
  <header class="header">
    <div class="container header__inner">
      <a class="header__logo" href="{href(lang,'home')}" aria-label="{l['home_aria']}"><img src="{p}img/logo.svg" alt="" width="132" height="51"></a>
      <div class="header__tools">
        <nav class="nav" aria-label="{l['navlabel']}">
          <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="nav-list">{l['menu']}</button>
          <ul class="nav__list" id="nav-list">
{items}
            <li><a class="btn btn--primary nav__cta" href="{WA}">{WA_ICON}{l['wa']}</a></li>
          </ul>
        </nav>
        <a class="lang" href="{href(s_lang, key, lang)}" hreflang="{s_lang}" lang="{s_lang}" title="{s_title}"><span aria-hidden="true">{s_label}</span><span class="visually-hidden">{s_title}</span></a>
      </div>
    </div>
  </header>
"""

def footer(lang):
    l = L[lang]; p = rel(lang)
    pages = "".join(f'<li><a href="{href(lang,k)}">{l["nav"][k]}</a></li>' for k in NAV)
    info = "".join(f'<li><a href="{href(lang,k)}">{l["nav"][k]}</a></li>' for k in ("legal", "privacy"))
    return f"""
  <footer class="footer inverse">
    <div class="container">
      <div class="footer__grid">
        <div>
          <a class="footer__logo" href="{href(lang,'home')}" aria-label="{l['home_aria']}"><img loading="lazy" src="{p}img/logo-blanc.svg" alt="" width="150" height="58"></a>
          <p style="margin-top:var(--space-3)">{l['footer_tag']}</p>
        </div>
        <div><h2>{l['f_contact']}</h2><ul>
          <li><a href="{WA}">WhatsApp</a></li>
          <li><a href="{TEL}">{t(D['telephone_affiche'])}</a></li>
          <li><a href="mailto:{D['email_lien']}">{t(D['email'])}</a></li>
          <li>{t(l['hours'])}</li></ul></div>
        <div><h2>{l['f_pages']}</h2><ul>{pages}</ul></div>
        <div><h2>{l['f_info']}</h2><ul>{info}</ul></div>
      </div>
      <div class="footer__bottom">
        <p>© <span data-year>{datetime.date.today().year}</span> Etoile Business. {l['rights']}</p>
        <p>{l['brands']}</p>
      </div>
    </div>
    <a class="wa-float" href="{WA}" aria-label="{l['wa_float']}">{WA_ICON}</a>
  </footer>
</body>
</html>
"""

def ctas(lang, second=None):
    l = L[lang]
    s = second or f'<a class="btn btn--ghost" href="{TEL}">{PHONE_ICON}{l["call"]}</a>'
    return f'<div class="actions"><a class="btn btn--primary" href="{WA}">{WA_ICON}{l["wa"]}</a>{s}</div>'

def final_cta(lang, title, text):
    l = L[lang]
    return f"""
    <section class="section inverse" aria-labelledby="cta-titre">
      <div class="container reveal">
        <p class="eyebrow">Etoile Business</p>
        <h2 id="cta-titre">{title}</h2>
        <p class="lead">{text}</p>
        <div class="actions"><a class="btn btn--gold" href="{WA}">{WA_ICON}{l['wa']}</a><a class="btn btn--ghost" href="{TEL}">{PHONE_ICON}{l['call']}</a></div>
      </div>
    </section>"""

def page_hero(lang, eyebrow, h1, lead, extra=""):
    p = rel(lang)
    return f"""
    <section class="hero hero--page inverse">
      <img class="hero__star" src="{p}img/etoile-or.svg" alt="" width="340" height="340">
      <div class="container">
        <div class="hero__frame">
          <p class="eyebrow">{eyebrow}</p>
          <h1>{h1}</h1>
          <p class="lead">{lead}</p>{extra}
        </div>
      </div>
    </section>"""

# ---------------------------------------------------------------- contenus
SERV = {
 "fr": [
  ("transfer", "transfert", "Transfert de fonds", "Envoyez ou recevez de l'argent, en RDC et à l'international, via le réseau qui vous convient."),
  ("exchange", "change", "Change", "Changez vos devises au guichet, au taux du jour affiché en agence."),
  ("credit", "credit", "Paiement de crédit", "Réglez vos échéances de crédit sans faire la queue à la banque."),
  ("subscription", "abonnements", "Paiement d'abonnements", "Payez vos abonnements au même endroit que vos autres opérations."),
 ],
 "en": [
  ("transfer", "transfer", "Money transfer", "Send or receive money, in the DRC and abroad, through the network that suits you."),
  ("exchange", "exchange", "Currency exchange", "Exchange currencies at the counter, at the daily rate posted in our branch."),
  ("credit", "loans", "Loan payments", "Pay your loan instalments without queuing at the bank."),
  ("subscription", "subscriptions", "Subscription payments", "Pay your subscriptions in the same place as your other transactions."),
 ]}
SOON = {"fr": ("parcel", "colis", "Envoi de colis à l'étranger", "Bientôt", "Un nouveau service arrive. Demandez-nous d'être prévenu."),
        "en": ("parcel", "parcels", "Parcel shipping abroad", "Coming soon", "A new service is on its way. Ask us to let you know.")}

def home(lang):
    fr = lang == "fr"; l = L[lang]; p = rel(lang)
    title = f"Etoile Business — Transfert d'argent et change à {VILLE}" if fr else f"Etoile Business — Money transfer & exchange in {VILLE}"
    desc = ("Envoyez et recevez de l'argent avec MoneyGram, Ria, M-Pesa ou Airtel Money. Change, paiement de crédit et d'abonnements dans nos agences."
            if fr else "Send and receive money with MoneyGram, Ria, M-Pesa or Airtel Money. Currency exchange, loan and subscription payments in our branches.")
    ld = {"@context": "https://schema.org", "@type": "FinancialService", "name": "Etoile Business",
          "url": D["domaine"].rstrip("/") + ("/" if fr else "/en/"), "logo": D["domaine"].rstrip("/") + "/img/logo.svg",
          "image": D["domaine"].rstrip("/") + "/img/og-image.png",
          "description": desc, "telephone": D["telephone_lien"], "email": D["email_lien"],
          "address": {"@type": "PostalAddress", "addressLocality": VILLE, "addressCountry": D["pays_code"]},
          "areaServed": D["pays_code"], "knowsLanguage": ["fr", "en"]}
    extra = f'  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    out = head(lang, "home", title, desc, extra) + header(lang, "home")
    cards = "".join(f"""
          <article class="card">{icon(i)}<h3 class="card__title">{n}</h3><p>{d}</p></article>""" for i, a, n, d in SERV[lang])
    si, sa, sn, sb, sd = SOON[lang]
    cards += f"""
          <article class="card card--soon">{icon(si)}<h3 class="card__title">{sn}<span class="badge">{sb}</span></h3><p>{sd}</p></article>"""
    nets = "".join(f"<li>{plain(n)}</li>" for n in NETS)
    ag = D["agences"][0]
    if fr:
        hero_ey = f"Messagerie financière à {t(VILLE)}"; h1 = "Envoyez et recevez votre argent, simplement."
        lead = "Transfert de fonds, change, paiement de crédit et d'abonnements : Etoile Business vous accueille en agence et vous répond sur WhatsApp."
        sec = "Voir nos agences"; trust = "Partenaire des réseaux " + ", ".join(NETS[:-1]) + " et " + NETS[-1] + "."
        s_ey, s_h2, more = "Services", "Nos services", "Voir tous les services"
        n_ey, n_h2, n_p = "Réseaux", "Des réseaux que vous connaissez", "Nous travaillons avec les principaux réseaux de transfert et de mobile money."
        st_ey, st_h2 = "Comment ça marche", "En agence, en 3 étapes"
        steps = [("Préparez votre pièce d'identité", "Et, pour un retrait, la référence du transfert donnée par l'expéditeur."),
                 ("Passez au guichet", "Un agent s'occupe de votre opération et vous indique les frais avant de valider."),
                 ("Repartez avec votre reçu", "Gardez-le jusqu'à la confirmation de l'opération.")]
        a_ey, a_h2, itin = "Agences", "Venez nous voir", "Itinéraire"
        c_h2, c_p = "Une question avant de vous déplacer ?", "Écrivez-nous sur WhatsApp : nous vous disons quel service choisir et quoi apporter."
        hours_lbl, addr_lbl = "Horaires", "Adresse"
    else:
        hero_ey = f"Money services in {t(VILLE)}"; h1 = "Send and receive money, simply."
        lead = "Money transfers, currency exchange, loan and subscription payments: Etoile Business welcomes you in branch and answers you on WhatsApp."
        sec = "See our locations"; trust = "Partner of " + ", ".join(NETS[:-1]) + " and " + NETS[-1] + "."
        s_ey, s_h2, more = "Services", "Our services", "See all services"
        n_ey, n_h2, n_p = "Networks", "Networks you already know", "We work with the leading money transfer and mobile money networks."
        st_ey, st_h2 = "How it works", "In branch, in 3 steps"
        steps = [("Bring your ID", "And, to collect money, the transfer reference given by the sender."),
                 ("Come to the counter", "An agent handles your transaction and tells you the fees before confirming."),
                 ("Leave with your receipt", "Keep it until the transaction is confirmed.")]
        a_ey, a_h2, itin = "Locations", "Come and see us", "Directions"
        c_h2, c_p = "A question before you come?", "Message us on WhatsApp: we will tell you which service to choose and what to bring."
        hours_lbl, addr_lbl = "Opening hours", "Address"
    st = "".join(f"<li><div><h3>{a}</h3><p>{b}</p></div></li>" for a, b in steps)
    out += f"""
  <main id="contenu">
    <section class="hero inverse">
      <img class="hero__star" src="{p}img/etoile-or.svg" alt="" width="340" height="340">
      <div class="container">
        <div class="hero__frame">
          <p class="eyebrow">{hero_ey}</p>
          <h1>{h1}</h1>
          <p class="lead">{lead}</p>
          <div class="actions"><a class="btn btn--gold" href="{WA}">{WA_ICON}{l['wa']}</a><a class="btn btn--ghost" href="{href(lang,'contact')}">{sec}</a></div>
          <p class="hero__trust">{trust}</p>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="services-titre">
      <div class="container">
        <p class="eyebrow">{s_ey}</p>
        <h2 id="services-titre">{s_h2}</h2>
        <div class="grid grid--3 reveal" style="margin-top:var(--space-5)">{cards}
        </div>
        <a class="more" href="{href(lang,'services')}">{more} →</a>
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="reseaux-titre">
      <div class="container grid grid--split reveal">
        <div><p class="eyebrow">{n_ey}</p><h2 id="reseaux-titre">{n_h2}</h2></div>
        <div><p class="lead">{n_p}</p><ul class="networks">{nets}</ul></div>
      </div>
    </section>

    <section class="section" aria-labelledby="etapes-titre">
      <div class="container grid grid--split reveal">
        <div><p class="eyebrow">{st_ey}</p><h2 id="etapes-titre">{st_h2}</h2></div>
        <ol class="steps">{st}</ol>
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="agences-titre">
      <div class="container grid grid--split reveal">
        <div><p class="eyebrow">{a_ey}</p><h2 id="agences-titre">{a_h2}</h2></div>
        <address class="agency">
          <h3>{t(ag['nom'])}</h3>
          <dl><dt>{addr_lbl}</dt><dd>{t(ag['adresse'])}, {t(VILLE)}</dd><dt>{hours_lbl}</dt><dd>{t(l['hours'])}</dd></dl>
          <div class="actions"><a class="btn btn--ghost" href="{href(lang,'contact')}">{sec}</a><a class="btn btn--ghost" href="{ag['itineraire']}">{itin}</a></div>
        </address>
      </div>
    </section>
{final_cta(lang, c_h2, c_p)}
  </main>
"""
    return out + footer(lang)

def services(lang):
    fr = lang == "fr"; l = L[lang]
    title = "Services : transfert, change, paiements | Etoile Business" if fr else "Services: transfers, exchange, payments | Etoile Business"
    desc = (f"Transfert de fonds MoneyGram, Ria, M-Pesa, Airtel Money, change, paiement de crédit et d'abonnements à {VILLE}. Ce qu'il faut apporter."
            if fr else f"Money transfers with MoneyGram, Ria, M-Pesa, Airtel Money, currency exchange, loan and subscription payments in {VILLE}. What to bring.")
    nets = ", ".join(NETS)
    if fr:
        blocks = [
         ("transfer", "transfert", "Transfert de fonds", "Envoyez de l'argent à vos proches ou recevez un transfert, en RDC comme à l'étranger.",
          [f"<strong>Réseaux disponibles :</strong> {nets}.", "<strong>Pour envoyer :</strong> votre pièce d'identité, le nom complet du bénéficiaire et son pays.",
           "<strong>Pour recevoir :</strong> votre pièce d'identité et la référence du transfert donnée par l'expéditeur.",
           "Les frais dépendent du réseau, du montant et du pays : demandez-les en agence ou sur WhatsApp."]),
         ("exchange", "change", "Change de devises", "Changez vos devises directement au guichet. Le taux du jour est affiché en agence.",
          [f"<strong>Devises acceptées :</strong> {t('[À REMPLACER : devises]')}"]),
         ("credit", "credit", "Paiement de crédit", "Réglez vos échéances de crédit chez nous, sans vous déplacer à la banque.",
          [f"<strong>Organismes concernés :</strong> {t('[À REMPLACER : organismes]')}", "<strong>À apporter :</strong> votre référence de crédit et le montant de l'échéance."]),
         ("subscription", "abonnements", "Paiement d'abonnements", "Payez vos abonnements en même temps que vos autres opérations.",
          [f"<strong>Abonnements acceptés :</strong> {t('[À REMPLACER : TV, internet, eau, électricité…]')}"]),
        ]
        soon = ("parcel", "colis", "Envoi de colis à l'étranger", "Bientôt", "Nous préparons un service d'envoi de colis vers l'étranger. Écrivez-nous pour être prévenu de son ouverture.", "Être prévenu sur WhatsApp")
        intro = "Toutes vos opérations d'argent au même guichet. Choisissez un service pour savoir comment il fonctionne et quoi apporter."
        faq_t = "Questions fréquentes"
        faq = [("Quels documents dois-je apporter ?", "Une pièce d'identité valide, et pour un retrait la référence du transfert."),
               ("Combien coûte un transfert ?", "Les frais dépendent du réseau, du montant et du pays de destination. Demandez-nous un montant exact sur WhatsApp avant de venir."),
               ("En combien de temps l'argent arrive-t-il ?", "Cela dépend du réseau choisi. " + t("[À REMPLACER : délais réels par réseau]")),
               ("Puis-je recevoir de l'argent sur mon téléphone ?", "Oui, via M-Pesa ou Airtel Money."),
               ("Quels sont vos horaires ?", t(l["hours"]))]
        c_h2, c_p = "Un doute sur votre opération ?", "Écrivez-nous avant de vous déplacer : nous vous répondons pendant les heures d'ouverture."
        toc_label = "Sommaire des services"
    else:
        blocks = [
         ("transfer", "transfer", "Money transfer", "Send money to your family or receive a transfer, in the DRC or abroad.",
          [f"<strong>Available networks:</strong> {nets}.", "<strong>To send:</strong> your ID, the recipient's full name and country.",
           "<strong>To receive:</strong> your ID and the transfer reference given by the sender.",
           "Fees depend on the network, the amount and the country: ask us in branch or on WhatsApp."]),
         ("exchange", "exchange", "Currency exchange", "Exchange currencies at the counter. The daily rate is posted in our branch.",
          [f"<strong>Accepted currencies:</strong> {t('[TO REPLACE: currencies]')}"]),
         ("credit", "loans", "Loan payments", "Pay your loan instalments with us, without going to the bank.",
          [f"<strong>Lenders covered:</strong> {t('[TO REPLACE: lenders]')}", "<strong>What to bring:</strong> your loan reference and the instalment amount."]),
         ("subscription", "subscriptions", "Subscription payments", "Pay your subscriptions together with your other transactions.",
          [f"<strong>Accepted subscriptions:</strong> {t('[TO REPLACE: TV, internet, water, electricity…]')}"]),
        ]
        soon = ("parcel", "parcels", "Parcel shipping abroad", "Coming soon", "We are preparing a parcel shipping service to other countries. Message us to be told when it opens.", "Get notified on WhatsApp")
        intro = "All your money transactions at one counter. Choose a service to see how it works and what to bring."
        faq_t = "Frequently asked questions"
        faq = [("What documents should I bring?", "A valid ID, and to collect money, the transfer reference."),
               ("How much does a transfer cost?", "Fees depend on the network, the amount and the destination country. Ask us for an exact amount on WhatsApp before you come."),
               ("How long does the money take to arrive?", "It depends on the network. " + t("[TO REPLACE: actual times per network]")),
               ("Can I receive money on my phone?", "Yes, through M-Pesa or Airtel Money."),
               ("What are your opening hours?", t(l["hours"]))]
        c_h2, c_p = "Not sure about your transaction?", "Message us before you come: we reply during opening hours."
        toc_label = "Services list"
    allb = blocks + [(soon[0], soon[1], soon[2], None, None)]
    toc = "".join(f'<li><a href="#{a}">{n}</a></li>' for i, a, n, *_ in allb) + f'<li><a href="#faq">{faq_t}</a></li>'
    body = ""
    for i, a, n, d, items in blocks:
        lis = "".join(f"<li>{x}</li>" for x in items)
        body += f"""
        <article class="service reveal" id="{a}">
          <div class="service__head">{icon(i, '')}<h2>{n}</h2></div>
          <div><p class="lead">{d}</p><ul>{lis}</ul><a class="btn btn--primary" href="{WA}">{WA_ICON}{l['wa']}</a></div>
        </article>"""
    i, a, n, b, d, cta = soon
    body += f"""
        <article class="service reveal" id="{a}">
          <div class="service__head">{icon(i, '')}<h2>{n}<span class="badge">{b}</span></h2></div>
          <div><p class="lead">{d}</p><a class="btn btn--ghost" href="{WA}">{WA_ICON}{cta}</a></div>
        </article>"""
    faqs = "".join(f"<details><summary>{q}</summary><p>{r}</p></details>" for q, r in faq)
    out = head(lang, "services", title, desc) + header(lang, "services")
    out += f"""
  <main id="contenu">{page_hero(lang, 'Etoile Business', 'Nos services' if fr else 'Our services', intro, f'<nav aria-label="{toc_label}"><ul class="toc">{toc}</ul></nav>')}
    <section class="section">
      <div class="container">{body}
      </div>
    </section>
    <section class="section section--alt" aria-labelledby="faq">
      <div class="container grid grid--split reveal">
        <div><p class="eyebrow">FAQ</p><h2 id="faq">{faq_t}</h2></div>
        <div class="faq">{faqs}</div>
      </div>
    </section>
{final_cta(lang, c_h2, c_p)}
  </main>
"""
    return out + footer(lang)

def about(lang):
    fr = lang == "fr"; l = L[lang]
    if fr:
        title = f"À propos d'Etoile Business, messagerie financière à {VILLE}"
        desc = f"Etoile Business est une messagerie financière à {VILLE} : transfert de fonds, change et paiements, avec un accueil simple et sérieux."
        h1 = "Etoile Business, votre messagerie financière de proximité"
        lead = f"Nous aidons les particuliers et les commerçants de {t(VILLE)} à envoyer, recevoir, changer et payer leur argent. Nos agents vous accueillent au guichet et vous répondent sur WhatsApp."
        story_h, story = "Notre histoire", t("[À REMPLACER : année de création, fondateur, nombre d'agences, si le client souhaite les donner]")
        eng_h = "Nos engagements"
        eng = [("Sécurité", "Chaque opération est enregistrée et vous recevez un reçu."),
               ("Clarté", "Nous vous donnons les frais avant l'opération."),
               ("Proximité", "Une équipe joignable en agence et sur WhatsApp.")]
        cadre_h = "Un cadre sérieux"
        cadre = "Etoile Business opère en partenariat avec des réseaux de transfert reconnus. " + t("[À REMPLACER : statut juridique, RCCM, agrément de la Banque centrale du Congo si applicable]")
        c_h2, c_p = "Passez nous voir", "Nos agents vous accueillent et répondent à vos questions."
    else:
        title = f"About Etoile Business, money services in {VILLE}"
        desc = f"Etoile Business is a money services provider in {VILLE}: transfers, currency exchange and payments, with simple and reliable service."
        h1 = "Etoile Business, your local money services provider"
        lead = f"We help individuals and traders in {t(VILLE)} send, receive, exchange and pay their money. Our agents welcome you at the counter and answer you on WhatsApp."
        story_h, story = "Our story", t("[TO REPLACE: founding year, founder, number of branches, if the client wishes to share them]")
        eng_h = "Our commitments"
        eng = [("Security", "Every transaction is recorded and you get a receipt."),
               ("Clarity", "We tell you the fees before the transaction."),
               ("Close to you", "A team you can reach in branch and on WhatsApp.")]
        cadre_h = "A reliable framework"
        cadre = "Etoile Business works in partnership with recognised money transfer networks. " + t("[TO REPLACE: legal status, RCCM, Central Bank of Congo authorisation if applicable]")
        c_h2, c_p = "Come and see us", "Our agents will welcome you and answer your questions."
    cards = "".join(f'<article class="card"><h3 class="card__title">{a}</h3><p>{b}</p></article>' for a, b in eng)
    out = head(lang, "about", title, desc) + header(lang, "about")
    out += f"""
  <main id="contenu">{page_hero(lang, l['nav']['about'], h1, lead)}
    <section class="section" aria-labelledby="histoire">
      <div class="container grid grid--split reveal">
        <div><h2 id="histoire">{story_h}</h2></div>
        <div><p class="lead">{story}</p></div>
      </div>
    </section>
    <section class="section section--alt" aria-labelledby="engagements">
      <div class="container reveal">
        <h2 id="engagements">{eng_h}</h2>
        <div class="grid grid--3" style="margin-top:var(--space-5)">{cards}</div>
      </div>
    </section>
    <section class="section" aria-labelledby="cadre">
      <div class="container grid grid--split reveal">
        <div><h2 id="cadre">{cadre_h}</h2></div>
        <div><p>{cadre}</p></div>
      </div>
    </section>
{final_cta(lang, c_h2, c_p)}
  </main>
"""
    return out + footer(lang)

def contact(lang):
    fr = lang == "fr"; l = L[lang]
    if fr:
        title = f"Nos agences et contact | Etoile Business {VILLE}"
        desc = f"Adresse, horaires et contacts des agences Etoile Business à {VILLE}. Écrivez-nous sur WhatsApp ou appelez-nous."
        h1, lead = "Nos agences et contact", "Le plus rapide : écrivez-nous sur WhatsApp. Nous répondons pendant les heures d'ouverture."
        ag_h, addr_lbl, hours_lbl, itin = "Nos agences", "Adresse", "Horaires", "Itinéraire"
        f_h = "Nous écrire"
        lbl = {"nom": "Nom", "tel": "Téléphone ou WhatsApp", "message": "Message", "hp": "Ne pas remplir ce champ", "send": "Envoyer",
               "tel_hint": "Nous vous rappelons ou vous écrivons sur ce numéro."}
        privacy = f'Vos données servent uniquement à vous répondre. Voir la <a href="{href(lang,"privacy")}">politique de confidentialité</a>.'
        msgs = {"required": "Ce champ est obligatoire.", "phone": "Saisissez un numéro valide, par exemple +243 81 000 0000.",
                "short": "Votre message est trop court.", "success": "Merci, nous vous répondons rapidement.",
                "error": "L'envoi a échoué. Écrivez-nous sur WhatsApp."}
        warn = "Etoile Business ne vous demandera jamais votre code secret ou un paiement par message."
        mail_lbl = "E-mail"
    else:
        title = f"Our locations & contact | Etoile Business {VILLE}"
        desc = f"Address, opening hours and contact details of Etoile Business branches in {VILLE}. Message us on WhatsApp or call us."
        h1, lead = "Our locations & contact", "The quickest way: message us on WhatsApp. We reply during opening hours."
        ag_h, addr_lbl, hours_lbl, itin = "Our branches", "Address", "Opening hours", "Directions"
        f_h = "Write to us"
        lbl = {"nom": "Name", "tel": "Phone or WhatsApp", "message": "Message", "hp": "Do not fill in this field", "send": "Send",
               "tel_hint": "We will call or message you on this number."}
        privacy = f'Your data is only used to reply to you. See our <a href="{href(lang,"privacy")}">privacy policy</a>.'
        msgs = {"required": "This field is required.", "phone": "Enter a valid number, e.g. +243 81 000 0000.",
                "short": "Your message is too short.", "success": "Thank you, we will get back to you soon.",
                "error": "Sending failed. Please message us on WhatsApp."}
        warn = "Etoile Business will never ask for your PIN or for a payment by message."
        mail_lbl = "Email"
    agencies = "".join(f"""
          <address class="card agency">
            <h3 class="card__title">{t(a['nom'])}</h3>
            <dl><dt>{addr_lbl}</dt><dd>{t(a['adresse'])}, {t(VILLE)}</dd><dt>{hours_lbl}</dt><dd>{t(l['hours'])}</dd></dl>
            <a class="btn btn--ghost" href="{a['itineraire']}">{itin}</a>
          </address>""" for a in D["agences"])
    quick = f'<div class="actions"><a class="btn btn--gold" href="{WA}">{WA_ICON}{l["wa"]}</a><a class="btn btn--ghost" href="{TEL}">{PHONE_ICON}{l["call"]} · {t(D["telephone_affiche"])}</a></div><p class="hero__trust">{mail_lbl} : <a href="mailto:{D["email_lien"]}">{t(D["email"])}</a></p>'
    out = head(lang, "contact", title, desc) + header(lang, "contact")
    out += f"""
  <main id="contenu">{page_hero(lang, 'Etoile Business', h1, lead, quick)}
    <section class="section" aria-labelledby="agences">
      <div class="container reveal">
        <h2 id="agences">{ag_h}</h2>
        <div class="grid grid--2" style="margin-top:var(--space-5)">{agencies}
        </div>
      </div>
    </section>
    <section class="section section--alt" aria-labelledby="ecrire">
      <div class="container grid grid--split">
        <div><h2 id="ecrire">{f_h}</h2><div class="notice"><p>{warn}</p></div></div>
        <form class="form" action="{D['formulaire_action']}" method="post" novalidate data-form data-messages='{html.escape(json.dumps(msgs, ensure_ascii=False), quote=True)}'>
          <div class="form__field"><label class="form__label" for="nom">{lbl['nom']}</label><input class="form__input" id="nom" name="nom" autocomplete="name" required maxlength="100" aria-describedby="nom-error"><p class="form__error" id="nom-error" aria-live="polite"></p></div>
          <div class="form__field"><label class="form__label" for="tel">{lbl['tel']}</label><p class="form__hint" id="tel-hint">{lbl['tel_hint']}</p><input class="form__input" id="tel" name="telephone" type="tel" autocomplete="tel" inputmode="tel" required maxlength="20" aria-describedby="tel-hint tel-error"><p class="form__error" id="tel-error" aria-live="polite"></p></div>
          <div class="form__field"><label class="form__label" for="message">{lbl['message']}</label><textarea class="form__input" id="message" name="message" required maxlength="2000" aria-describedby="message-error"></textarea><p class="form__error" id="message-error" aria-live="polite"></p></div>
          <input type="hidden" name="access_key" value="{plain(D['web3forms_cle'])}">
          <input type="hidden" name="subject" value="{'Nouveau message du site Etoile Business' if fr else 'New message from the Etoile Business website (EN)'}">
          <input type="hidden" name="from_name" value="Site Etoile Business">
          <div class="form__hp" aria-hidden="true"><label for="botcheck">{lbl['hp']}</label><input id="botcheck" name="botcheck" tabindex="-1" autocomplete="off"></div>
          <p class="form__hint">{privacy}</p>
          <div><button class="btn btn--primary" type="submit">{lbl['send']}</button></div>
          <p class="form__status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>
  </main>
"""
    return out + footer(lang)

def legal(lang):
    fr = lang == "fr"; l = L[lang]; R = "[À REMPLACER]" if fr else "[TO REPLACE]"
    if fr:
        title, desc, h1 = "Mentions légales | Etoile Business", "Mentions légales du site Etoile Business : éditeur, hébergeur, propriété intellectuelle.", "Mentions légales"
        secs = [("Éditeur du site", f"Etoile Business — forme juridique : {t(R)}<br>Siège : {t(R)}<br>RCCM : {t(R)} · Id. nat. : {t(R)} · N° impôt : {t(R)}<br>Téléphone : {t(D['telephone_affiche'])} · E-mail : {t(D['email'])}"),
                ("Directeur de la publication", t(R)),
                ("Hébergement", f"Hébergeur : {t(R)} — adresse : {t(R)}"),
                ("Activité réglementée", t("[À REMPLACER : agrément ou autorisation de la Banque centrale du Congo, statut d'agent des réseaux partenaires]")),
                ("Propriété intellectuelle", "Les textes, le logo et les éléments graphiques de ce site appartiennent à Etoile Business. Toute reproduction sans autorisation est interdite. Les noms MoneyGram, Ria, Equity, M-Pesa et Airtel Money sont des marques de leurs propriétaires respectifs et sont cités pour indiquer les services disponibles."),
                ("Crédits", "Polices : Jost et Allura (licence SIL Open Font License).")]
    else:
        title, desc, h1 = "Legal notice | Etoile Business", "Legal notice of the Etoile Business website: publisher, host, intellectual property.", "Legal notice"
        secs = [("Publisher", f"Etoile Business — legal form: {t(R)}<br>Registered office: {t(R)}<br>RCCM: {t(R)} · Nat. ID: {t(R)} · Tax no.: {t(R)}<br>Phone: {t(D['telephone_affiche'])} · Email: {t(D['email'])}"),
                ("Publication director", t(R)),
                ("Hosting", f"Host: {t(R)} — address: {t(R)}"),
                ("Regulated activity", t("[TO REPLACE: Central Bank of Congo authorisation, agent status with partner networks]")),
                ("Intellectual property", "The texts, logo and graphic elements of this website belong to Etoile Business. Any reproduction without permission is prohibited. MoneyGram, Ria, Equity, M-Pesa and Airtel Money are trademarks of their respective owners and are mentioned to indicate the available services."),
                ("Credits", "Fonts: Jost and Allura (SIL Open Font License).")]
    return prose_page(lang, "legal", title, desc, h1, secs)

def privacy(lang):
    fr = lang == "fr"
    if fr:
        title, desc, h1 = "Politique de confidentialité | Etoile Business", "Comment Etoile Business utilise les données envoyées par le formulaire de contact. Aucun cookie ni traceur.", "Politique de confidentialité"
        secs = [("Données collectées", "Uniquement celles que vous saisissez dans le formulaire de contact : nom, numéro de téléphone et message."),
                ("Finalité", "Ces données servent seulement à répondre à votre demande. Elles ne sont ni vendues ni utilisées pour de la publicité."),
                ("Durée de conservation", t("[À REMPLACER : durée, par exemple 12 mois après le dernier échange]")),
                ("Destinataires", "Etoile Business et Web3Forms, le service technique qui transmet le formulaire par e-mail."),
                ("Cookies et traceurs", "Ce site n'utilise aucun cookie de mesure d'audience ni de publicité, et aucun traceur."),
                ("Vos droits", f"Vous pouvez demander à consulter, corriger ou supprimer vos données en écrivant à {t(D['email'])}.")]
    else:
        title, desc, h1 = "Privacy policy | Etoile Business", "How Etoile Business uses the data sent through the contact form. No cookies or trackers.", "Privacy policy"
        secs = [("Data collected", "Only what you enter in the contact form: name, phone number and message."),
                ("Purpose", "This data is only used to reply to your request. It is never sold or used for advertising."),
                ("Retention period", t("[TO REPLACE: period, e.g. 12 months after the last exchange]")),
                ("Recipients", "Etoile Business and Web3Forms, the technical service that delivers the form by email."),
                ("Cookies and trackers", "This website uses no analytics or advertising cookies, and no trackers."),
                ("Your rights", f"You can ask to access, correct or delete your data by writing to {t(D['email'])}.")]
    return prose_page(lang, "privacy", title, desc, h1, secs)

def prose_page(lang, key, title, desc, h1, secs):
    body = "".join(f"<h2>{a}</h2><p>{b}</p>" for a, b in secs)
    out = head(lang, key, title, desc) + header(lang, key)
    upd = ("Dernière mise à jour : " if lang == "fr" else "Last updated: ") + TODAY
    out += f"""
  <main id="contenu">
    <section class="section">
      <div class="container prose">
        <h1>{h1}</h1>
        <p class="muted">{upd}</p>
        {body}
      </div>
    </section>
  </main>
"""
    return out + footer(lang)

def page404():
    l = L["fr"]
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page introuvable | Etoile Business</title>
  <meta name="robots" content="noindex">
  <meta name="description" content="Page introuvable. Page not found.">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/css/tokens.css">
  <link rel="stylesheet" href="/css/base.css">
  <link rel="stylesheet" href="/css/components.css">
</head>
<body>
  <main id="contenu" class="hero inverse" style="min-height:100vh;display:grid;align-items:center">
    <img class="hero__star" src="/img/etoile-or.svg" alt="" width="340" height="340">
    <div class="container">
      <div class="hero__frame">
        <a href="/" aria-label="Etoile Business, accueil"><img src="/img/logo-blanc.svg" alt="" width="150" height="58"></a>
        <h1 style="margin-top:var(--space-5)">Page introuvable <span lang="en" class="muted" style="display:block;font-size:var(--fs-lg)">Page not found</span></h1>
        <p class="lead">Cette page n'existe pas ou a été déplacée. <span lang="en">This page does not exist or has moved.</span></p>
        <div class="actions"><a class="btn btn--gold" href="/">Retour à l'accueil</a><a class="btn btn--ghost" href="/en/" lang="en">English home</a><a class="btn btn--ghost" href="{WA}">{WA_ICON}WhatsApp</a></div>
      </div>
    </div>
  </main>
</body>
</html>
"""

def ext(page):
    """Liens externes : nouvel onglet + rel=noopener."""
    for host in ("https://wa.me/", "https://www.openstreetmap.org/"):
        page = page.replace(f'href="{host}', f'target="_blank" rel="noopener" href="{host}')
    return page.replace('<img src="{0}img/logo-blanc.svg"'.format(""), '<img loading="lazy" src="img/logo-blanc.svg"')

BUILD = {"home": home, "services": services, "about": about, "contact": contact, "legal": legal, "privacy": privacy}
os.makedirs(os.path.join(OUT, "en"), exist_ok=True)
for key, fn in BUILD.items():
    for i, lang in enumerate(("fr", "en")):
        open(os.path.join(OUT, PAGES[key][i]), "w", encoding="utf-8").write(ext(fn(lang)))
open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(ext(page404()))
dom = D["domaine"].rstrip("/")
urls = ""
for key in PAGES:
    fr_u = f"{dom}/{PAGES[key][0]}".replace("/index.html", "/"); en_u = f"{dom}/{PAGES[key][1]}".replace("/index.html", "/")
    for u in (fr_u, en_u):
        urls += f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod>\n    <xhtml:link rel="alternate" hreflang="fr" href="{fr_u}"/>\n    <xhtml:link rel="alternate" hreflang="en" href="{en_u}"/>\n  </url>\n'
open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n')
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {dom}/sitemap.xml\n")
print("OK : 13 pages, sitemap.xml, robots.txt")
