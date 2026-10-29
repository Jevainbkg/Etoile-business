# Guide de mise à jour — site Etoile Business

Tout le contenu du site se trouve dans 3 fichiers JSON sur GitHub, sans toucher au code. Chaque modification enregistrée met le site à jour en environ une minute.

## Modifier un fichier
1. Sur github.com, ouvrir le dépôt **Etoile-business**, puis le dossier **contenu/**.
2. Ouvrir le fichier, cliquer sur le crayon ✏️ (Edit).
3. Changer uniquement le texte **entre guillemets**, puis **Commit changes**.

| Fichier | Contenu |
|---|---|
| `contenu/site.json` | Ville, téléphone, WhatsApp, e-mail, horaires, agences (nom, adresse, itinéraire, photo), réseaux partenaires, bandeau d'annonce, taux du jour, clé du formulaire, ouverture à Google |
| `contenu/fr.json` | Tous les titres et textes en français : pages, services, FAQ, engagements, mentions légales, confidentialité, titres et descriptions Google |
| `contenu/en.json` | Les mêmes, en anglais |

Penser à modifier **les deux langues** quand un texte change.

## Règles d'écriture JSON
- Garder les guillemets `"…"`, les deux-points et les virgules entre les éléments.
- Un guillemet dans un texte s'écrit `\"`. Préférer les guillemets français « ».
- `true` / `false` s'écrivent sans guillemets.
- En cas d'oubli, Vercel refuse la mise à jour et l'ancienne version reste en ligne : rien ne casse.

## Écrire dans les textes
- `**mot**` met le mot en **gras** ; `\n` fait un retour à la ligne.
- Variables remplacées automatiquement partout : `{ville}`, `{telephone}`, `{email}`, `{horaires}`, `{reseaux}`.
- Un texte `[À REMPLACER …]` est surligné en jaune sur le site : c'est un rappel qu'une information manque.

## Cas fréquents (dans `site.json`)
- **Annoncer une fermeture** : remplir `annonce_fr` et `annonce_en`. Les vider (`""`) pour retirer le bandeau.
- **Publier les taux du jour** : dans `taux`, mettre `"afficher": true`, la `date` et les `lignes`. Le tableau apparaît sur l'accueil et la page Services. Remettre `false` pour le masquer.
- **Ajouter une agence** : copier un bloc `{ … }` de `agences`, le coller après une virgule, et le modifier. Photo facultative : la déposer dans `site/img/uploads/` (JPG ou WebP de moins de 300 Ko) et indiquer `"photo": "/img/uploads/nom.jpg"`.
- **Ouvrir un nouveau service** (dans `fr.json` et `en.json`) : `services` → `liste` → mettre `"bientot": false` pour retirer le badge « Bientôt ».
- **Ouvrir le site à Google** : quand plus rien n'est `[À REMPLACER]`, mettre `"indexer": true`, puis soumettre `sitemap.xml` dans Google Search Console.

## Si quelque chose ne va pas
- Le site ne change pas après un enregistrement : sur vercel.com → projet → **Deployments**, ouvrir le dernier déploiement et lire le journal. Une erreur de contenu y est expliquée ; tant qu'elle n'est pas corrigée, l'ancienne version reste en ligne.
- Revenir en arrière : Vercel → **Deployments** → version précédente → **Promote to Production**. L'historique de chaque modification est aussi visible sur GitHub.

## Ce qu'il ne faut pas faire
- Afficher les logos MoneyGram, Ria, etc. sans l'accord écrit du réseau.
- Ajouter de faux avis ou des chiffres non vérifiés.
- Ajouter Google Analytics ou un pixel publicitaire sans bandeau de consentement.
- Modifier les fichiers `site/*.html` directement : ils sont régénérés à chaque déploiement.

## Pour un développeur
Contenu : `contenu/*.json` · génération : `python3 _source/build.py` · styles : `site/css/tokens.css` (couleurs, polices), `base.css`, `components.css` · admin : `.pages.yml`.
