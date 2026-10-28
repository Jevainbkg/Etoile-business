# Rapport de déploiement — Etoile Business

> Skill : `anthropic-skills:deploy` v2026.10.23.1 · Démarré le 2026-10-28
> Légende : **VU** (capture / sortie) · **CODE** (lu dans le projet) · **SUPPOSÉ**

## Inventaire (CODE)
- Site statique, aucun build : dossier `site/` (13 pages FR/EN, CSS, JS, polices, SVG). Pas de `package.json`, pas de Node.
- Formulaire : `site/envoyer.php` (PHP + `mail()`) → ne fonctionne que sur un hébergement PHP.
- Config serveur : `site/.htaccess` (Apache) → ignoré par Cloudflare Pages et Vercel.
- Pas de base de données, pas d'authentification, pas de rôles : la porte « connexion par rôle / isolation » ne s'applique pas.
- Coordonnées encore en `[À REMPLACER]` (`_source/donnees.json`).
- Pas encore de dépôt GitHub pour ce site (SUPPOSÉ : aucun dépôt Etoile Business dans les dépôts connectés).

## Leçons du registre applicables
| Leçon | Statut |
|---|---|
| D01 · GitHub, « Only select repositories » | À appliquer à la création du dépôt |
| D11 · Réseau, l'utilisateur fait les actions console, captures à l'appui | S'applique |
| D13 · repartir de `main` après fusion | S'applique |
| D08, D09, D10 · Cloudflare Pages (flux Pages, pas Workers ; NODE_VERSION ; deploy hook secret) | Si Cloudflare est choisi (NODE_VERSION inutile : pas de build) |
| D17, D18, D19 · Vercel (preset Other, nom court, prod = `main`) | Si Vercel est choisi |
| D02-D06, D14-D16 · Supabase | Ne s'applique pas (aucune base) |
| D12 · renommage de dépôt | Ne s'applique pas pour l'instant |

## Cible (décidée le 2026-10-28)
- Hébergement : **Vercel** (gratuit), production = branche `main` (D19), racine du projet Vercel = racine du dépôt, préréglage « Other » ; `vercel.json` : build `python3 _source/build.py`, sortie `site`.
- Admin : **Pages CMS** (app.pagescms.org), édite `contenu/*.json` ; chaque enregistrement = commit sur `main` = redéploiement. Collaborateurs invités par e-mail sans compte GitHub.
- Formulaire : **Web3Forms** (clé d'accès publique dans le HTML, destinée à l'être). Validation client (JS) + filtrage anti-spam Web3Forms + honeypot `botcheck`. Limite : pas de validation serveur des champs comme avec `envoyer.php` ; accepté pour un site vitrine.
- Config : `vercel.json` à la racine (build, en-têtes de sécurité, cache). Indexation pilotée par le champ « Ouvrir le site à Google » (balise meta robots). `envoyer.php` et `.htaccess` déplacés dans `_source/alternative-php/`.
- Dépôt : `jevainbkg/etoile-business` (privé).

## Plan
1. Choix de l'hébergement et préparation des fichiers de config.
2. Dépôt GitHub (créé par l'utilisateur, accès limité au seul dépôt : D01) et premier envoi du site.
3. Formulaire : compte du service d'envoi, adresse de réception.
4. Hébergeur : import du dépôt, URL publique, en-têtes de sécurité.
5. Domaine et HTTPS (quand le client l'a), puis `domaine` dans `donnees.json`.
6. Recette en ligne (porte de mise en ligne) et PASS / FAIL.

## Journal des étapes
| Date | Étape | Résultat |
|---|---|---|
| 2026-10-28 | Inventaire + leçons | Fait (CODE) |
| 2026-10-28 | Étape 1 : choix Vercel + Web3Forms | Fait. Formulaire adapté, testé avec réponse simulée (CODE) : clé provisoire → message d'erreur ; clé renseignée → succès, champs `nom telephone message access_key subject from_name botcheck` envoyés |
| 2026-10-28 | Étape 2 : dépôt GitHub | Dépôt `jevainbkg/etoile-business` créé (vide) par l'utilisateur. Premier envoi sur `claude/project-thread-801tga` (commit 8b87ed2, VU : `git ls-remote`). Puis `main` créée à la demande de l'utilisateur (VU : `refs/heads/main` = 8b87ed2). Reste : `main` comme branche par défaut |
| 2026-10-28 | Espace admin | Choix Pages CMS. Contenu FR/EN déplacé dans `contenu/`, `build.py` rendu tolérant aux champs vides (CODE, testé) ; ajouts : bandeau d'annonce, photo d'agence, taux du jour (testés à 375 / 1440 px). Écart de texte avec la version précédente : 4 lignes (CODE, diff). PR vers `main` |

## Retour arrière
Archive `livraison/etoile-business-site.zip` ; sur Vercel / Cloudflare, « Promote » / « Rollback » vers le déploiement précédent.
