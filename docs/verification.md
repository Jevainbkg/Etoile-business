# Vérification — Etoile Business (étape 7)

> Date : 2026-10-28 · Version testée : `site/` (13 pages, FR + EN)
> Outils : Playwright (Chromium) à 375 / 768 / 1440 px, axe-core 4.10 (WCAG 2.0/2.1/2.2 A et AA + bonnes pratiques), Lighthouse 12 (mobile), tests du formulaire dans le navigateur (validation, honeypot, envoi vers Web3Forms simulé).
> Légende : **PASS** · **FAIL** · **ATTENTE** = dépend d'une information du client ou de la mise en ligne, pas d'un défaut du site.

## Résultats mesurés
| Page | Défilement horizontal 375/768/1440 | Poids (Ko) | Erreurs axe | Liens cassés |
|---|---|---|---|---|
| index / en/index | aucun | 104 | 0 | 0 |
| services / en/services | aucun | 106 | 0 | 0 |
| a-propos / en/about | aucun | 122 | 0 | 0 |
| contact / en/contact | aucun | 123 | 0 | 0 |
| légales (4 pages) | aucun | 101-102 | 0 | 0 |
| 404 | aucun | 80 | 0 | 0 |

Lighthouse mobile (accueil, services EN, contact) : **Performance 100 · Accessibilité 100 · Bonnes pratiques 100 · SEO 100**. LCP 1,5 à 1,8 s, CLS 0, TBT 0 ms. Les deux remarques restantes (cache, compression) sont réglées par Vercel (compression automatique) et `vercel.json` (cache).

## Accessibilité
| Point | Résultat |
|---|---|
| `lang` sur `<html>` (fr / en) | PASS |
| Un seul H1, titres sans saut | PASS (13/13) |
| Repères header, nav, main, footer | PASS (404 : main seul, page volontairement minimale) |
| Lien « Aller au contenu » | PASS (premier élément au Tab) |
| Contrastes | PASS (axe 0 erreur ; valeurs dans `direction-artistique.md`) |
| Clavier, ordre logique | PASS |
| Focus visible | PASS (contour or foncé 3 px ; or clair sur fond sombre) |
| Cibles ≥ 24 px | PASS (boutons 48 px ; seul le champ anti-spam caché est plus petit, volontairement) |
| `alt` | PASS (images décoratives `alt=""`, liens logo avec `aria-label`) |
| Formulaire : labels, erreurs en texte | PASS (erreurs annoncées, `aria-invalid`, focus sur le 1er champ en erreur) |
| Menu mobile `aria-expanded` / Échap | PASS |
| `prefers-reduced-motion` | PASS |
| Liens explicites | PASS |

## Performance
| Point | Résultat |
|---|---|
| Accueil < 1 Mo | PASS (104 Ko) |
| Images WebP/AVIF dimensionnées | PASS (aucune photo ; uniquement des SVG + 1 PNG Open Graph de 18 Ko) |
| `loading="lazy"` sous la ligne de flottaison | PASS |
| Image hero non lazy | PASS |
| Polices : 1 famille, `swap`, repli système, préchargées | PASS |
| JS minimal en `defer`, aucun framework | PASS (1 fichier, ~3 Ko) |
| Aucun script tiers | PASS |
| Lighthouse mobile ≥ 90 | PASS (100) |
| LCP < 2,5 s, CLS < 0,1 | PASS |
| 3G simulée | PASS (mesure Lighthouse en throttling mobile) |

## Qualité design
| Point | Résultat |
|---|---|
| Promesse + CTA visibles sans défiler (mobile et desktop) | PASS |
| Un CTA principal par écran | PASS (WhatsApp) |
| Valeurs issues de `tokens.css` | PASS (les seuls `style=""` utilisent des variables) |
| Texte ≥ 16 px, lignes ≤ 75 caractères | PASS (17 px, `max-width: 65ch`) |
| Rendu 375 / 768 / 1440 | PASS |
| États hover / focus | PASS |
| Identité propre | PASS (cadre ouvert du logo, étoile or, palette papier/encre) |
| Aucun `[À REMPLACER]` restant | **ATTENTE** — 6 à 14 par page : coordonnées, agences, devises, mentions légales (surlignés en jaune dans le site) |
| Images nettes | ATTENTE — aucune photo réelle fournie (le site fonctionne sans) |

## SEO
| Point | Résultat |
|---|---|
| Title unique ≤ 60 | PASS sur 9 pages. **ATTENTE** sur 4 (accueil FR/EN, à propos, contact) : dépassement dû au texte provisoire « [À REMPLACER : ville] » ; avec « Kinshasa » ils passent sous 60 |
| Meta description unique ≤ 155 | PASS (aucun doublon) |
| H1 avec mot-clé | PASS |
| URLs lisibles | PASS |
| Open Graph + image 1200×630 | PASS |
| JSON-LD `FinancialService` | PASS (structure) · ATTENTE : adresse et téléphone réels |
| sitemap.xml (avec hreflang) + robots.txt | PASS · ATTENTE : domaine final |
| Canonical + hreflang fr/en/x-default | PASS · ATTENTE : domaine final |
| Liens internes | PASS |
| Page 404 utile | PASS (bilingue, retour accueil, WhatsApp) |
| Search Console, Google Business Profile | ATTENTE (après mise en ligne) |

## Sécurité et légal
| Point | Résultat |
|---|---|
| HTTPS + redirection | ATTENTE (automatique sur Vercel, à constater en ligne) |
| Validation client ET serveur | PARTIEL : validation client testée ; côté serveur, Web3Forms filtre le spam mais ne valide pas les champs (choix accepté avec l'hébergement Vercel ; la version PHP validée reste dans `_source/alternative-php/`) |
| Anti-spam honeypot | PASS (testé : champ rempli → ignoré sans envoi) |
| Liens externes `target="_blank" rel="noopener"` | PASS |
| Aucune clé ou donnée sensible | PASS |
| Envoi réel de l'e-mail | ATTENTE (clé Web3Forms à créer, puis test en ligne) |
| Mentions légales complètes | ATTENTE (structure prête, RCCM / hébergeur / agrément à fournir) |
| Politique de confidentialité | PASS (structure) · ATTENTE : durée de conservation |
| Cookies | PASS — aucun traceur, donc pas de bandeau |
| Droits : polices (OFL), icônes (dessinées pour le projet), logo (client) | PASS |
| Logos des partenaires | PASS — non affichés, noms en texte seulement |
| Textes légaux validés par le client / juriste | ATTENTE |

## Bilan
Aucun FAIL. Tous les points en ATTENTE dépendent des informations du client ou de l'hébergement ; ils sont listés dans `livraison/recette-client.md`.
