# Guide de mise à jour — site Etoile Business

Tout le contenu du site se modifie dans un **espace admin en ligne** (Pages CMS), sans toucher au code. Chaque enregistrement met le site à jour en environ une minute.

## Se connecter à l'admin
1. Aller sur **app.pagescms.org**.
2. Se connecter avec **GitHub** (propriétaire du dépôt), ou avec le lien reçu par e-mail si vous avez été invité comme collaborateur (pas besoin de compte GitHub).
3. Choisir le dépôt **Etoile-business**, branche **main**.

## Ce que l'on peut modifier
| Menu de l'admin | Contenu |
|---|---|
| **Coordonnées, agences et taux** | Ville, téléphone, WhatsApp, e-mail, horaires, agences (nom, adresse, itinéraire, photo), réseaux partenaires, bandeau d'annonce, tableau des taux du jour, clé du formulaire, ouverture à Google |
| **Textes du site (français)** | Tous les titres et textes des pages, services, FAQ, engagements, mentions légales, confidentialité, titres et descriptions Google |
| **Textes du site (anglais)** | Les mêmes, pour la version anglaise |

Penser à modifier **les deux langues** quand un texte change.

## Écrire dans les champs
- `**mot**` met le mot en **gras** ; un retour à la ligne est conservé.
- Variables remplacées automatiquement partout : `{ville}`, `{telephone}`, `{email}`, `{horaires}`, `{reseaux}`.
- Un texte `[À REMPLACER …]` est surligné en jaune sur le site : c'est un rappel qu'une information manque.

## Cas fréquents
- **Annoncer une fermeture** : *Coordonnées* → **Bandeau d'annonce** (FR et EN). Vider le champ pour retirer le bandeau.
- **Publier les taux du jour** : *Coordonnées* → **Taux du jour** → cocher **Afficher**, mettre la date et les lignes. Le tableau apparaît sur l'accueil et la page Services. Décocher pour le masquer.
- **Ajouter une agence** : *Coordonnées* → **Agences** → **Ajouter**. Photo facultative, en JPG ou WebP de moins de 300 Ko (sinon le site ralentit sur mobile).
- **Ouvrir un nouveau service** : *Textes* → **Page Services** → **Services**. Décocher « Pas encore disponible » pour retirer le badge « Bientôt ».
- **Ouvrir le site à Google** : quand plus rien n'est `[À REMPLACER]`, cocher **Ouvrir le site à Google**, puis soumettre `sitemap.xml` dans Google Search Console.

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
