# Etoile Business — site vitrine

Site statique bilingue (FR / EN) d'Etoile Business, messagerie financière : transfert de fonds, change, paiement de crédit et d'abonnements.

## Organisation
- `contenu/` : **tout le contenu modifiable** — `site.json` (coordonnées, agences, annonce, taux du jour, réglages), `fr.json` et `en.json` (textes des pages).
- `.pages.yml` : configuration de l'espace admin [Pages CMS](https://app.pagescms.org) qui édite `contenu/`.
- `_source/build.py` : génère `site/` à partir de `contenu/` (Python 3, sans dépendance).
- `site/` : le site généré (HTML, CSS, JS, polices, images). Ne pas modifier les `.html` à la main : ils sont réécrits à chaque déploiement.
- `site/img/uploads/` : photos envoyées depuis l'admin.
- `vercel.json` : commande de build, dossier publié, en-têtes de sécurité et cache.
- `_source/alternative-php/` : formulaire PHP et `.htaccess` pour un hébergement cPanel (non utilisés sur Vercel).
- `docs/` : rapport de déploiement, vérification, recette, guide de mise à jour.

## Fonctionnement
Admin (Pages CMS) → commit sur `main` → Vercel lance `python3 _source/build.py` → site en ligne en environ une minute.

## Hébergement
Vercel, production = branche `main`, **Root Directory = racine du dépôt** (`./`), preset **Other** ; build et dossier publié viennent de `vercel.json`.
Formulaire : Web3Forms (clé dans `contenu/site.json`).
