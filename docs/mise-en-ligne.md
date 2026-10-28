# Mise en ligne — Etoile Business

> Aucun déploiement n'a été fait. Ce document liste ce qu'il faut faire, dans l'ordre, le jour où le client a ses informations et son hébergement.
> Site : dossier `site/` (statique, aucun build). Hébergement : Vercel. Formulaire : Web3Forms. Configuration : `site/vercel.json`.

## Avant
- [ ] Toutes les checklists en PASS : **oui pour le code** ; restent les points ATTENTE de `../verification.md`.
- [ ] Coordonnées réelles saisies dans `_source/donnees.json`, puis `python3 build.py` (ou modification directe des HTML, voir `guide-mise-a-jour.md`).
- [ ] Clé Web3Forms saisie dans `donnees.json` (`web3forms_cle`), liée à l'adresse qui doit recevoir les messages.
- [ ] Plus aucun `[À REMPLACER]` / `[TO REPLACE]` : rechercher ces textes dans le dossier `site/`.
- [ ] Mentions légales et confidentialité complétées et relues par le client.
- [ ] Recette client signée (`recette-client.md`).
- [ ] Hébergement : Vercel (gratuit), relié au dépôt GitHub `etoile-business`. Nom de domaine acheté (facultatif au début : l'adresse `*.vercel.app` fonctionne).
- [ ] `domaine` renseigné dans `donnees.json` → canonical, hreflang, sitemap, robots et Open Graph se mettent à jour.

## Pendant
- [ ] Vercel → **Add New → Project** → importer `etoile-business`, **Root Directory** = `site`, preset **Other**, aucune commande de build (D17), nom court (D18).
- [ ] Domaine : Vercel → Settings → Domains ; HTTPS automatique.
- [ ] Quand tout est rempli : retirer `X-Robots-Tag: noindex` de `vercel.json`.
- [ ] Pas d'ancien site connu : aucune redirection 301 nécessaire.

## Après (tests sur le vrai domaine)
- [ ] `http://` redirige vers `https://`.
- [ ] Les 12 pages et la 404 (`/une-page-qui-nexiste-pas`) s'affichent ; le sélecteur FR / EN fonctionne.
- [ ] Le bouton WhatsApp ouvre la bonne conversation ; « Appeler » compose le bon numéro (test sur téléphone).
- [ ] Formulaire : un vrai message arrive à la bonne adresse (vérifier aussi les spams) ; un envoi vide affiche les erreurs.
- [ ] Google Search Console : propriété validée, `sitemap.xml` soumis.
- [ ] Fiche Google Business Profile créée ou mise à jour pour chaque agence (essentiel pour « transfert d'argent + ville »).
- [ ] Analytics : aucun prévu. Si le client en veut un, ajouter un bandeau de consentement.
- [ ] Remettre au client : accès hébergement, `guide-mise-a-jour.md`, archive du site livré.

## Retour arrière
- Vercel → Deployments → version précédente → **Promote to Production**. L'archive `etoile-business-site.zip` reste une copie de secours.
- Déclencheurs : une page ne s'affiche plus, le bouton WhatsApp ou le formulaire ne fonctionne plus, le certificat HTTPS est en erreur.
