# Etoile Business — site vitrine

Site statique bilingue (FR / EN) d'Etoile Business, messagerie financière : transfert de fonds, change, paiement de crédit et d'abonnements.

- `site/` : le site, prêt à servir tel quel (HTML, CSS, JS, polices, SVG). Aucun build.
- `site/vercel.json` : en-têtes de sécurité, cache, `noindex` provisoire.
- `_source/donnees.json` : coordonnées du client ; `python3 _source/build.py` régénère les pages.
- `_source/alternative-php/` : formulaire PHP et `.htaccess` pour un hébergement cPanel (non utilisés sur Vercel).
- `docs/` : rapport de déploiement, vérification, recette, guide de mise à jour.

## Hébergement
Vercel, production = branche `main`, **Root Directory = `site`**, preset **Other**, aucune commande de build.
Formulaire : Web3Forms (clé dans `_source/donnees.json`).
