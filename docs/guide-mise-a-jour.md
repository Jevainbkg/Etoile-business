# Guide de mise à jour — site Etoile Business

Le site est fait de fichiers HTML simples : il s'ouvre dans un navigateur et se met en ligne par simple copie. Aucun abonnement ni logiciel n'est nécessaire.

## Structure
```
site/
├── index.html, services.html, a-propos.html, contact.html   ← pages françaises
├── mentions-legales.html, confidentialite.html, 404.html
├── en/            ← pages anglaises (mêmes pages)
├── css/tokens.css ← couleurs, polices, tailles (seul fichier à toucher pour le style)
├── css/base.css, css/components.css
├── js/main.js     ← menu mobile, formulaire
├── img/           ← logo, étoile, image de partage
├── fonts/         ← police Jost
├── vercel.json    ← réglages Vercel : en-têtes de sécurité, cache, blocage Google provisoire
├── sitemap.xml, robots.txt
_source/
├── donnees.json   ← coordonnées du client
└── build.py       ← régénère toutes les pages à partir de donnees.json
```

## Changer les coordonnées (téléphone, WhatsApp, adresse, horaires, ville, domaine)
**Méthode conseillée** (Python 3 installé) :
1. Ouvrir `_source/donnees.json` et remplacer chaque `[À REMPLACER …]`.
   - `telephone_affiche` : tel qu'il s'affiche, ex. `+243 81 234 5678`
   - `telephone_lien` : sans espaces, ex. `+243812345678`
   - `whatsapp_lien` : chiffres seuls avec l'indicatif, ex. `243812345678`
   - `agences` : une ligne par agence (nom, adresse, lien d'itinéraire)
2. Lancer `python3 build.py` dans le dossier `_source/`. Les 13 pages, le sitemap et le robots.txt sont régénérés.
3. Les textes des pages (services, FAQ, mentions légales…) se trouvent aussi dans `build.py`, en clair, en français puis en anglais.

**Sans Python** : ouvrir chaque fichier HTML (FR et EN) dans un éditeur de texte et utiliser « Rechercher / Remplacer » sur `[À REMPLACER` et `[TO REPLACE`. Attention : une page régénérée ensuite avec `build.py` écrasera ces modifications.

## Changer une couleur ou une police
Uniquement dans `css/tokens.css`. Garder un contraste suffisant (vérifier sur webaim.org/resources/contrastchecker, minimum 4,5:1 pour le texte).

## Formulaire de contact
Le formulaire passe par Web3Forms (gratuit). La clé d'accès se met dans `web3forms_cle` de `donnees.json`. Pour changer l'adresse qui reçoit les messages, aller sur web3forms.com et créer une nouvelle clé avec la nouvelle adresse.
Une version PHP (hébergement cPanel) est gardée dans `_source/alternative-php/`.

## Mettre en ligne une modification
Le site est hébergé sur Vercel et relié au dépôt GitHub : toute modification fusionnée dans la branche `main` est mise en ligne automatiquement en une minute. En cas de problème, Vercel → Deployments → choisir la version précédente → **Promote to Production**.

## Ouvrir le site à Google
Tant que les coordonnées sont provisoires, `vercel.json` contient `X-Robots-Tag: noindex`. Quand tout est rempli, supprimer ce bloc puis soumettre `sitemap.xml` dans Google Search Console.

## Ce qu'il ne faut pas faire
- Afficher les logos MoneyGram, Ria, etc. sans l'accord écrit du réseau.
- Ajouter de faux avis ou des chiffres non vérifiés.
- Ajouter Google Analytics ou un pixel publicitaire sans bandeau de consentement.
