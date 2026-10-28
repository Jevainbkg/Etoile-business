<?php
// Etoile Business — réception du formulaire de contact (validation serveur + anti-spam).
// Nécessite un hébergement avec PHP et la fonction mail() (ou remplacer l'envoi par SMTP).
// À configurer : adresse de réception ci-dessous.
const DESTINATAIRE = 'contact@exemple.com'; // [À REMPLACER]
const EXPEDITEUR   = 'site@exemple.com';    // [À REMPLACER] adresse du domaine

header('Content-Type: application/json; charset=utf-8');
function repondre($code, $ok) { http_response_code($code); echo json_encode(['ok' => $ok]); exit; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') repondre(405, false);
if (!empty($_POST['site'])) repondre(200, true); // honeypot rempli : robot, on ignore sans le dire

$nom = trim((string)($_POST['nom'] ?? ''));
$tel = trim((string)($_POST['telephone'] ?? ''));
$msg = trim((string)($_POST['message'] ?? ''));

if ($nom === '' || mb_strlen($nom) > 100) repondre(422, false);
if (!preg_match('/^\+?[0-9 ().-]{8,20}$/', $tel)) repondre(422, false);
if (mb_strlen($msg) < 10 || mb_strlen($msg) > 2000) repondre(422, false);

// Pas de retour à la ligne dans les en-têtes (injection d'en-têtes)
$nom = str_replace(["\r", "\n"], ' ', $nom);

$corps = "Nouveau message depuis le site Etoile Business\n\n"
       . "Nom : $nom\nTéléphone : $tel\n\nMessage :\n$msg\n";
$entetes = 'From: Etoile Business <' . EXPEDITEUR . ">\r\n"
         . "Content-Type: text/plain; charset=utf-8\r\n";

$ok = mail(DESTINATAIRE, '=?UTF-8?B?' . base64_encode('Message du site — ' . $nom) . '?=', $corps, $entetes);
repondre($ok ? 200 : 500, $ok);
