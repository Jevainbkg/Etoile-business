#!/usr/bin/env python3
"""Génère les pages HTML statiques d'Etoile Business (FR + EN) dans site/.

Le contenu vient de contenu/site.json, contenu/fr.json et contenu/en.json,
modifiables dans l'espace admin (Pages CMS). Vercel lance ce script à chaque
déploiement ; on peut aussi le lancer à la main : python3 _source/build.py
Dans les textes : **gras**, retour à la ligne, et les variables {ville},
{telephone}, {email}, {horaires}, {reseaux}."""
import json, html, os, re, sys, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "site")
class Data(dict):
    """Un champ vidé ou supprimé dans l'admin vaut "" au lieu de faire échouer la génération."""
    def __missing__(self, key):
        return ""

def tolerant(v):
    if isinstance(v, dict):
        return Data({k: tolerant(x) for k, x in v.items()})
    if isinstance(v, list):
        return [tolerant(x) for x in v if x is not None]
    return "" if v is None else v

def load(name):
    return tolerant(json.load(open(os.path.join(ROOT, "contenu", name), encoding="utf-8")))
S = load("site.json")
C = {"fr": load("fr.json"), "en": load("en.json")}
TODAY = datetime.date.today().isoformat()
DOM = S["domaine"].rstrip("/")
WA = f"https://wa.me/{re.sub(r'[^0-9]', '', S['whatsapp'])}"
TEL = f"tel:{re.sub(r'[^0-9+]', '', S['telephone_lien'])}"
TODO_RE = re.compile(r"\[(?:À REMPLACER|TO REPLACE)[^\]]*\]")

def join_list(items, lang):
    items = [i for i in items if i]
    if len(items) < 2:
        return "".join(items)
    return ", ".join(items[:-1]) + (" et " if lang == "fr" else " and ") + items[-1]

def subst(s, lang):
    return (s.replace("{ville}", S["ville"]).replace("{telephone}", S["telephone_affiche"])
             .replace("{email}", S["email"]).replace("{horaires}", S[f"horaires_{lang}"])
             .replace("{reseaux}", join_list(S["reseaux"], lang)))

def plain(s, lang="fr"):
    """Texte brut échappé (title, meta, attributs)."""
    return html.escape(subst(s or "", lang))

def rich(s, lang):
    """Texte affiché : échappé, [À REMPLACER] surlignés, **gras**, retours à la ligne."""
    e = html.escape(subst(s or "", lang))
    e = TODO_RE.sub(lambda m: f'<span class="todo">{m.group(0)}</span>', e)
    e = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", e)
    return e.replace("\n", "<br>")

ICON = {
 "transfert": '<path d="M4 8h14M14 4l4 4-4 4M20 16H6M10 12l-4 4 4 4"/>',
 "change": '<circle cx="9" cy="9" r="5.5"/><circle cx="15" cy="15" r="5.5"/><path d="M9 6.5v5M15 12.5v5"/>',
 "credit": '<rect x="3" y="6" width="18" height="12" rx="1"/><path d="M3 10h18M7 14.5h4"/>',
 "abonnement": '<rect x="4" y="5" width="16" height="15" rx="1"/><path d="M4 9h16M8 3v4M16 3v4M8 13h3M8 16h6"/>',
 "colis": '<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5 12 12l9-4.5M12 12v9"/>',
 "etoile": '<path d="M12 3v18M3 12h18M5.6 5.6l12.8 12.8M18.4 5.6 5.6 18.4"/>',
}
def icon(name, cls="card__icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICON.get(name, ICON["etoile"])}</svg>'
WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 20Zm4.4-6c-.2-.1-1.4-.7-1.7-.8s-.4-.1-.5.1-.6.8-.8 1-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.6.3 2.7 2.7 0 0 0-.8 2 4.7 4.7 0 0 0 1 2.5 10.7 10.7 0 0 0 4.1 3.6c1.5.7 2.1.7 2.9.6a2.4 2.4 0 0 0 1.6-1.1 2 2 0 0 0 .1-1.1c0-.1-.2-.2-.4-.3Z"/></svg>'
PHONE_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>'

PAGES = {  # clé : (fichier FR, fichier EN, clé de contenu)
 "accueil": ("index.html", "en/index.html"),
 "services": ("services.html", "en/services.html"),
 "a_propos": ("a-propos.html", "en/about.html"),
 "contact": ("contact.html", "en/contact.html"),
 "mentions": ("mentions-legales.html", "en/legal-notice.html"),
 "confidentialite": ("confidentialite.html", "en/privacy.html"),
}
NAV = ["accueil", "services", "a_propos", "contact"]
# Libellés d'interface (fixes, non éditables dans l'admin)
UI = {
 "fr": {"locale": "fr_FR", "skip": "Aller au contenu", "menu": "Menu", "navlabel": "Navigation principale",
        "nav": {"accueil": "Accueil", "services": "Services", "a_propos": "À propos", "contact": "Agences & contact", "mentions": "Mentions légales", "confidentialite": "Confidentialité"},
        "wa": "Écrire sur WhatsApp", "call": "Appeler", "switch": ("EN", "English version", "en"), "home_aria": "Etoile Business, accueil",
        "f_contact": "Contact", "f_pages": "Pages", "f_info": "Informations", "rights": "Tous droits réservés.",
        "brands": "Les marques citées appartiennent à leurs propriétaires respectifs.", "wa_float": "Écrire à Etoile Business sur WhatsApp",
        "see_locations": "Voir nos agences", "directions": "Itinéraire", "address": "Adresse", "hours": "Horaires",
        "ey_services": "Services", "ey_networks": "Réseaux", "ey_steps": "Comment ça marche", "ey_locations": "Agences",
        "toc": "Sommaire des services", "soon": "Bientôt", "notify": "Être prévenu sur WhatsApp", "email": "E-mail",
        "currency": "Devise", "buy": "Achat", "sell": "Vente", "rates_of": "Taux du", "info": "Information :",
        "updated": "Dernière mise à jour : ", "photo_of": "Agence",
        "form": {"nom": "Nom", "tel": "Téléphone ou WhatsApp", "message": "Message", "hp": "Ne pas remplir ce champ", "send": "Envoyer",
                 "tel_hint": "Nous vous rappelons ou vous écrivons sur ce numéro.", "subject": "Nouveau message du site Etoile Business",
                 "privacy": 'Vos données servent uniquement à vous répondre. Voir la <a href="{href}">politique de confidentialité</a>.'},
        "msgs": {"required": "Ce champ est obligatoire.", "phone": "Saisissez un numéro valide, par exemple +243 81 000 0000.", "short": "Votre message est trop court.",
                 "success": "Merci, nous vous répondons rapidement.", "error": "L'envoi a échoué. Écrivez-nous sur WhatsApp."}},
 "en": {"locale": "en_US", "skip": "Skip to content", "menu": "Menu", "navlabel": "Main navigation",
        "nav": {"accueil": "Home", "services": "Services", "a_propos": "About", "contact": "Locations & contact", "mentions": "Legal notice", "confidentialite": "Privacy"},
        "wa": "Message us on WhatsApp", "call": "Call", "switch": ("FR", "Version française", "fr"), "home_aria": "Etoile Business, home",
        "f_contact": "Contact", "f_pages": "Pages", "f_info": "Information", "rights": "All rights reserved.",
        "brands": "Brand names belong to their respective owners.", "wa_float": "Message Etoile Business on WhatsApp",
        "see_locations": "See our locations", "directions": "Directions", "address": "Address", "hours": "Opening hours",
        "ey_services": "Services", "ey_networks": "Networks", "ey_steps": "How it works", "ey_locations": "Locations",
        "toc": "Services list", "soon": "Coming soon", "notify": "Get notified on WhatsApp", "email": "Email",
        "currency": "Currency", "buy": "Buy", "sell": "Sell", "rates_of": "Rates of", "info": "Notice:",
        "updated": "Last updated: ", "photo_of": "Branch",
        "form": {"nom": "Name", "tel": "Phone or WhatsApp", "message": "Message", "hp": "Do not fill in this field", "send": "Send",
                 "tel_hint": "We will call or message you on this number.", "subject": "New message from the Etoile Business website (EN)",
                 "privacy": 'Your data is only used to reply to you. See our <a href="{href}">privacy policy</a>.'},
        "msgs": {"required": "This field is required.", "phone": "Enter a valid number, e.g. +243 81 000 0000.", "short": "Your message is too short.",
                 "success": "Thank you, we will get back to you soon.", "error": "Sending failed. Please message us on WhatsApp."}},
}

def rel(lang):
    return "../" if lang == "en" else ""

def href(lang, key, cur_lang=None):
    cur_lang = cur_lang or lang
    f = PAGES[key][0 if lang == "fr" else 1]
    if cur_lang == "en":
        return f[3:] if lang == "en" else "../" + f
    return f

def url(lang, key):
    return f"{DOM}/{PAGES[key][0 if lang == 'fr' else 1]}".replace("/index.html", "/")

def head(lang, key, extra=""):
    p = rel(lang); seo = C[lang]["seo"][key]; title, desc = plain(seo["titre"], lang), plain(seo["description"], lang)
    robots = "" if S.get("indexer") else '  <meta name="robots" content="noindex">\n'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
{robots}  <link rel="canonical" href="{url(lang, key)}">
  <link rel="alternate" hreflang="fr" href="{url('fr', key)}">
  <link rel="alternate" hreflang="en" href="{url('en', key)}">
  <link rel="alternate" hreflang="x-default" href="{url('fr', key)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Etoile Business">
  <meta property="og:locale" content="{UI[lang]['locale']}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url(lang, key)}">
  <meta property="og:image" content="{DOM}/img/og-image.png">
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

def banner(lang):
    a = S.get(f"annonce_{lang}", "").strip()
    if not a:
        return ""
    return f'  <div class="announce" role="note"><div class="container"><strong>{UI[lang]["info"]}</strong> {rich(a, lang)}</div></div>\n'

def header(lang, key):
    u = UI[lang]; p = rel(lang)
    items = "\n".join(f'          <li><a class="nav__link" href="{href(lang,k)}"{" aria-current=\"page\"" if k==key else ""}>{u["nav"][k]}</a></li>' for k in NAV)
    s_label, s_title, s_lang = u["switch"]
    return f"""<body>
  <a class="skip-link" href="#contenu">{u['skip']}</a>
{banner(lang)}  <header class="header">
    <div class="container header__inner">
      <a class="header__logo" href="{href(lang,'accueil')}" aria-label="{u['home_aria']}"><img src="{p}img/logo.svg" alt="" width="132" height="51"></a>
      <div class="header__tools">
        <nav class="nav" aria-label="{u['navlabel']}">
          <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="nav-list">{u['menu']}</button>
          <ul class="nav__list" id="nav-list">
{items}
            <li><a class="btn btn--primary nav__cta" href="{WA}">{WA_ICON}{u['wa']}</a></li>
          </ul>
        </nav>
        <a class="lang" href="{href(s_lang, key, lang)}" hreflang="{s_lang}" lang="{s_lang}" title="{s_title}"><span aria-hidden="true">{s_label}</span><span class="visually-hidden">{s_title}</span></a>
      </div>
    </div>
  </header>
"""

def footer(lang):
    u = UI[lang]; p = rel(lang)
    pages = "".join(f'<li><a href="{href(lang,k)}">{u["nav"][k]}</a></li>' for k in NAV)
    info = "".join(f'<li><a href="{href(lang,k)}">{u["nav"][k]}</a></li>' for k in ("mentions", "confidentialite"))
    return f"""
  <footer class="footer inverse">
    <div class="container">
      <div class="footer__grid">
        <div>
          <a class="footer__logo" href="{href(lang,'accueil')}" aria-label="{u['home_aria']}"><img loading="lazy" src="{p}img/logo-blanc.svg" alt="" width="150" height="58"></a>
          <p style="margin-top:var(--space-3)">{rich(C[lang]['pied_de_page'], lang)}</p>
        </div>
        <div><h2>{u['f_contact']}</h2><ul>
          <li><a href="{WA}">WhatsApp</a></li>
          <li><a href="{TEL}">{rich(S['telephone_affiche'], lang)}</a></li>
          <li><a href="mailto:{html.escape(S['email_lien'])}">{rich(S['email'], lang)}</a></li>
          <li>{rich(S[f'horaires_{lang}'], lang)}</li></ul></div>
        <div><h2>{u['f_pages']}</h2><ul>{pages}</ul></div>
        <div><h2>{u['f_info']}</h2><ul>{info}</ul></div>
      </div>
      <div class="footer__bottom">
        <p>© <span data-year>{datetime.date.today().year}</span> Etoile Business. {u['rights']}</p>
        <p>{u['brands']}</p>
      </div>
    </div>
    <a class="wa-float" href="{WA}" aria-label="{u['wa_float']}">{WA_ICON}</a>
  </footer>
</body>
</html>
"""

def final_cta(lang, title, text):
    u = UI[lang]
    return f"""
    <section class="section inverse" aria-labelledby="cta-titre">
      <div class="container reveal">
        <p class="eyebrow">Etoile Business</p>
        <h2 id="cta-titre">{rich(title, lang)}</h2>
        <p class="lead">{rich(text, lang)}</p>
        <div class="actions"><a class="btn btn--gold" href="{WA}">{WA_ICON}{u['wa']}</a><a class="btn btn--ghost" href="{TEL}">{PHONE_ICON}{u['call']}</a></div>
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

def agency_block(lang, a, card=True):
    u = UI[lang]; p = rel(lang)
    photo = ""
    if a.get("photo"):
        src = a["photo"].lstrip("/")
        photo = f'<img class="agency__photo" src="{p}{html.escape(src)}" alt="{u["photo_of"]} {plain(a["nom"], lang)}" loading="lazy" width="640" height="400">'
    cls = "card agency" if card else "agency"
    title_tag = "h3"
    return f"""
          <address class="{cls}">{photo}
            <{title_tag} class="card__title">{rich(a['nom'], lang)}</{title_tag}>
            <dl><dt>{u['address']}</dt><dd>{rich(a['adresse'], lang)}, {rich(S['ville'], lang)}</dd><dt>{u['hours']}</dt><dd>{rich(S[f'horaires_{lang}'], lang)}</dd></dl>
            <a class="btn btn--ghost" href="{html.escape(a.get('itineraire') or 'https://www.openstreetmap.org/')}">{u['directions']}</a>
          </address>"""

def rates_block(lang):
    t = S.get("taux") or {}
    lignes = [l for l in t.get("lignes", []) if l.get("devise")]
    if not t.get("afficher") or not lignes:
        return ""
    u = UI[lang]; c = C[lang]["services"]
    rows = "".join(f'<tr><th scope="row">{plain(l["devise"])}</th><td>{plain(str(l.get("achat","")))}</td><td>{plain(str(l.get("vente","")))}</td></tr>' for l in lignes)
    date = f' <span class="muted">— {u["rates_of"]} {plain(t["date"])}</span>' if t.get("date") else ""
    return f"""
    <section class="section section--alt" aria-labelledby="taux-titre">
      <div class="container grid grid--split reveal">
        <div><p class="eyebrow">{UI[lang]['ey_services']}</p><h2 id="taux-titre">{rich(c['taux_titre'], lang)}</h2><p class="muted">{rich(c['taux_note'], lang)}</p></div>
        <div class="table-wrap"><table class="rates"><caption class="visually-hidden">{rich(c['taux_titre'], lang)}</caption><thead><tr><th scope="col">{u['currency']}</th><th scope="col">{u['buy']}</th><th scope="col">{u['sell']}</th></tr></thead><tbody>{rows}</tbody></table><p class="form__hint">{date}</p></div>
      </div>
    </section>"""

# ---------------------------------------------------------------- pages
def home(lang):
    u = UI[lang]; c = C[lang]["accueil"]; sv = C[lang]["services"]["liste"]; p = rel(lang)
    ld = {"@context": "https://schema.org", "@type": "FinancialService", "name": "Etoile Business",
          "url": url(lang, "accueil"), "logo": DOM + "/img/logo.svg", "image": DOM + "/img/og-image.png",
          "description": subst(C[lang]["seo"]["accueil"]["description"], lang), "telephone": S["telephone_lien"], "email": S["email_lien"],
          "address": {"@type": "PostalAddress", "addressLocality": S["ville"], "addressCountry": S["pays_code"]},
          "areaServed": S["pays_code"], "knowsLanguage": ["fr", "en"]}
    extra = f'  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")}</script>\n'
    cards = "".join(f"""
          <article class="card{' card--soon' if s.get('bientot') else ''}">{icon(s.get('icone'))}<h3 class="card__title">{rich(s['nom'], lang)}{f'<span class="badge">{u["soon"]}</span>' if s.get('bientot') else ''}</h3><p>{rich(s['resume'], lang)}</p></article>""" for s in sv)
    nets = "".join(f"<li>{plain(n)}</li>" for n in S["reseaux"] if n)
    steps = "".join(f"<li><div><h3>{rich(e['titre'], lang)}</h3><p>{rich(e['texte'], lang)}</p></div></li>" for e in c["etapes"])
    ag = S["agences"][0] if S["agences"] else {"nom": "", "adresse": "", "itineraire": ""}
    out = head(lang, "accueil", extra) + header(lang, "accueil")
    out += f"""
  <main id="contenu">
    <section class="hero inverse">
      <img class="hero__star" src="{p}img/etoile-or.svg" alt="" width="340" height="340">
      <div class="container">
        <div class="hero__frame">
          <p class="eyebrow">{rich(c['surtitre'], lang)}</p>
          <h1>{rich(c['titre'], lang)}</h1>
          <p class="lead">{rich(c['intro'], lang)}</p>
          <div class="actions"><a class="btn btn--gold" href="{WA}">{WA_ICON}{u['wa']}</a><a class="btn btn--ghost" href="{href(lang,'contact')}">{u['see_locations']}</a></div>
          <p class="hero__trust">{rich(c['confiance'], lang)}</p>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="services-titre">
      <div class="container">
        <p class="eyebrow">{u['ey_services']}</p>
        <h2 id="services-titre">{rich(c['services_titre'], lang)}</h2>
        <div class="grid grid--3 reveal" style="margin-top:var(--space-5)">{cards}
        </div>
        <a class="more" href="{href(lang,'services')}">{rich(c['voir_services'], lang)} →</a>
      </div>
    </section>
{rates_block(lang)}
    <section class="section section--alt" aria-labelledby="reseaux-titre">
      <div class="container grid grid--split reveal">
        <div><p class="eyebrow">{u['ey_networks']}</p><h2 id="reseaux-titre">{rich(c['reseaux_titre'], lang)}</h2></div>
        <div><p class="lead">{rich(c['reseaux_texte'], lang)}</p><ul class="networks">{nets}</ul></div>
      </div>
    </section>

    <section class="section" aria-labelledby="etapes-titre">
      <div class="container grid grid--split reveal">
        <div><p class="eyebrow">{u['ey_steps']}</p><h2 id="etapes-titre">{rich(c['etapes_titre'], lang)}</h2></div>
        <ol class="steps">{steps}</ol>
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="agences-titre">
      <div class="container grid grid--split reveal">
        <div><p class="eyebrow">{u['ey_locations']}</p><h2 id="agences-titre">{rich(c['agences_titre'], lang)}</h2></div>
        <div>{agency_block(lang, ag, card=False)}
          <p style="margin-top:var(--space-3)"><a href="{href(lang,'contact')}">{u['see_locations']} →</a></p>
        </div>
      </div>
    </section>
{final_cta(lang, c['cta_titre'], c['cta_texte'])}
  </main>
"""
    return out + footer(lang)

def services(lang):
    u = UI[lang]; c = C[lang]["services"]
    toc = "".join(f'<li><a href="#{html.escape(s["id"])}">{rich(s["nom"], lang)}</a></li>' for s in c["liste"]) + f'<li><a href="#faq">{rich(c["faq_titre"], lang)}</a></li>'
    body = ""
    for s in c["liste"]:
        lis = "".join(f"<li>{rich(x, lang)}</li>" for x in s.get("details", []) if x)
        ul = f"<ul>{lis}</ul>" if lis else ""
        badge = f'<span class="badge">{u["soon"]}</span>' if s.get("bientot") else ""
        btn = (f'<a class="btn btn--ghost" href="{WA}">{WA_ICON}{u["notify"]}</a>' if s.get("bientot")
               else f'<a class="btn btn--primary" href="{WA}">{WA_ICON}{u["wa"]}</a>')
        body += f"""
        <article class="service reveal" id="{html.escape(s['id'])}">
          <div class="service__head">{icon(s.get('icone'), '')}<h2>{rich(s['nom'], lang)}{badge}</h2></div>
          <div><p class="lead">{rich(s['description'], lang)}</p>{ul}{btn}</div>
        </article>"""
    faqs = "".join(f"<details><summary>{rich(q['question'], lang)}</summary><p>{rich(q['reponse'], lang)}</p></details>" for q in c["faq"])
    out = head(lang, "services") + header(lang, "services")
    out += f"""
  <main id="contenu">{page_hero(lang, 'Etoile Business', rich(c['titre'], lang), rich(c['intro'], lang), f'<nav aria-label="{u["toc"]}"><ul class="toc">{toc}</ul></nav>')}
    <section class="section">
      <div class="container">{body}
      </div>
    </section>
{rates_block(lang)}
    <section class="section section--alt" aria-labelledby="faq">
      <div class="container grid grid--split reveal">
        <div><p class="eyebrow">FAQ</p><h2 id="faq">{rich(c['faq_titre'], lang)}</h2></div>
        <div class="faq">{faqs}</div>
      </div>
    </section>
{final_cta(lang, c['cta_titre'], c['cta_texte'])}
  </main>
"""
    return out + footer(lang)

def about(lang):
    u = UI[lang]; c = C[lang]["a_propos"]
    cards = "".join(f'<article class="card"><h3 class="card__title">{rich(e["titre"], lang)}</h3><p>{rich(e["texte"], lang)}</p></article>' for e in c["engagements"])
    out = head(lang, "a_propos") + header(lang, "a_propos")
    out += f"""
  <main id="contenu">{page_hero(lang, u['nav']['a_propos'], rich(c['titre'], lang), rich(c['intro'], lang))}
    <section class="section" aria-labelledby="histoire">
      <div class="container grid grid--split reveal">
        <div><h2 id="histoire">{rich(c['histoire_titre'], lang)}</h2></div>
        <div><p class="lead">{rich(c['histoire'], lang)}</p></div>
      </div>
    </section>
    <section class="section section--alt" aria-labelledby="engagements">
      <div class="container reveal">
        <h2 id="engagements">{rich(c['engagements_titre'], lang)}</h2>
        <div class="grid grid--3" style="margin-top:var(--space-5)">{cards}</div>
      </div>
    </section>
    <section class="section" aria-labelledby="cadre">
      <div class="container grid grid--split reveal">
        <div><h2 id="cadre">{rich(c['cadre_titre'], lang)}</h2></div>
        <div><p>{rich(c['cadre_texte'], lang)}</p></div>
      </div>
    </section>
{final_cta(lang, c['cta_titre'], c['cta_texte'])}
  </main>
"""
    return out + footer(lang)

def contact(lang):
    u = UI[lang]; c = C[lang]["contact"]; f = u["form"]
    agencies = "".join(agency_block(lang, a) for a in S["agences"])
    quick = (f'<div class="actions"><a class="btn btn--gold" href="{WA}">{WA_ICON}{u["wa"]}</a>'
             f'<a class="btn btn--ghost" href="{TEL}">{PHONE_ICON}{u["call"]} · {rich(S["telephone_affiche"], lang)}</a></div>'
             f'<p class="hero__trust">{u["email"]} : <a href="mailto:{html.escape(S["email_lien"])}">{rich(S["email"], lang)}</a></p>')
    privacy = f["privacy"].replace("{href}", href(lang, "confidentialite"))
    msgs = html.escape(json.dumps(u["msgs"], ensure_ascii=False), quote=True)
    out = head(lang, "contact") + header(lang, "contact")
    out += f"""
  <main id="contenu">{page_hero(lang, 'Etoile Business', rich(c['titre'], lang), rich(c['intro'], lang), quick)}
    <section class="section" aria-labelledby="agences">
      <div class="container reveal">
        <h2 id="agences">{rich(c['agences_titre'], lang)}</h2>
        <div class="grid grid--2" style="margin-top:var(--space-5)">{agencies}
        </div>
      </div>
    </section>
    <section class="section section--alt" aria-labelledby="ecrire">
      <div class="container grid grid--split">
        <div><h2 id="ecrire">{rich(c['formulaire_titre'], lang)}</h2><div class="notice"><p>{rich(c['avertissement'], lang)}</p></div></div>
        <form class="form" action="https://api.web3forms.com/submit" method="post" novalidate data-form data-messages='{msgs}'>
          <div class="form__field"><label class="form__label" for="nom">{f['nom']}</label><input class="form__input" id="nom" name="nom" autocomplete="name" required maxlength="100" aria-describedby="nom-error"><p class="form__error" id="nom-error" aria-live="polite"></p></div>
          <div class="form__field"><label class="form__label" for="tel">{f['tel']}</label><p class="form__hint" id="tel-hint">{f['tel_hint']}</p><input class="form__input" id="tel" name="telephone" type="tel" autocomplete="tel" inputmode="tel" required maxlength="20" aria-describedby="tel-hint tel-error"><p class="form__error" id="tel-error" aria-live="polite"></p></div>
          <div class="form__field"><label class="form__label" for="message">{f['message']}</label><textarea class="form__input" id="message" name="message" required maxlength="2000" aria-describedby="message-error"></textarea><p class="form__error" id="message-error" aria-live="polite"></p></div>
          <input type="hidden" name="access_key" value="{html.escape(S['web3forms_cle'])}">
          <input type="hidden" name="subject" value="{f['subject']}">
          <input type="hidden" name="from_name" value="Site Etoile Business">
          <div class="form__hp" aria-hidden="true"><label for="botcheck">{f['hp']}</label><input id="botcheck" name="botcheck" tabindex="-1" autocomplete="off"></div>
          <p class="form__hint">{privacy}</p>
          <div><button class="btn btn--primary" type="submit">{f['send']}</button></div>
          <p class="form__status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>
  </main>
"""
    return out + footer(lang)

def prose(key):
    def build(lang):
        c = C[lang][key]
        body = "".join(f"<h2>{rich(s['titre'], lang)}</h2><p>{rich(s['texte'], lang)}</p>" for s in c["sections"])
        out = head(lang, key) + header(lang, key)
        out += f"""
  <main id="contenu">
    <section class="section">
      <div class="container prose">
        <h1>{rich(c['titre'], lang)}</h1>
        <p class="muted">{UI[lang]['updated']}{TODAY}</p>
        {body}
      </div>
    </section>
  </main>
"""
        return out + footer(lang)
    return build

def page404():
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
    return re.sub(r'<a ([^>]*?)href="(https?://)', r'<a \1target="_blank" rel="noopener" href="\2', page)

BUILD = {"accueil": home, "services": services, "a_propos": about, "contact": contact,
         "mentions": prose("mentions"), "confidentialite": prose("confidentialite")}

def main():
    os.makedirs(os.path.join(OUT, "en"), exist_ok=True)
    for key, fn in BUILD.items():
        for i, lang in enumerate(("fr", "en")):
            open(os.path.join(OUT, PAGES[key][i]), "w", encoding="utf-8").write(ext(fn(lang)))
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(ext(page404()))
    urls = ""
    for key in PAGES:
        for u in (url("fr", key), url("en", key)):
            urls += f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod>\n    <xhtml:link rel="alternate" hreflang="fr" href="{url("fr", key)}"/>\n    <xhtml:link rel="alternate" hreflang="en" href="{url("en", key)}"/>\n  </url>\n'
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n')
    # L'indexation se règle par la balise meta robots de chaque page (champ « indexer »)
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOM}/sitemap.xml\n")
    print("OK : 13 pages, sitemap.xml, robots.txt" + ("" if S.get("indexer") else " (indexation désactivée)"))

if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, json.JSONDecodeError) as e:
        sys.exit(f"Erreur dans le contenu : champ manquant ou mal formé ({e!r}). Vérifier contenu/*.json.")
