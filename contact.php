<?php
/**
 * Churchill Medical Clinic — contact form handler.
 *
 * Deliberately minimal. It does not store anything, and it is not a channel for
 * personal health information: the form itself tells patients to telephone for
 * anything clinical.
 *
 * BEFORE LAUNCH: set $to to the clinic's real monitored mailbox.
 */
declare(strict_types=1);

$to       = 'REPLACE-WITH-CLINIC-EMAIL@example.com';
$fromAddr = 'noreply@www.churchillmedicalclinic.ca';   // must be a domain this server is allowed to send as
$subject  = 'Website enquiry — Churchill Medical Clinic';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: contact.html');
    exit;
}

// Honeypot: a real person never fills this in.
if (!empty($_POST['website'] ?? '')) {
    header('Location: thank-you.html');
    exit;
}

$clean = static function (string $key, int $max = 500): string {
    $v = trim((string)($_POST[$key] ?? ''));
    $v = str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v);   // header-injection guard
    return mb_substr($v, 0, $max);
};

$name    = $clean('name', 120);
$phone   = $clean('phone', 40);
$email   = $clean('email', 160);
$reason  = $clean('reason', 120);
$message = mb_substr(trim((string)($_POST['message'] ?? '')), 0, 3000);

if ($name === '' || $phone === '' || $reason === '' || $message === '') {
    header('Location: contact.html?error=missing');
    exit;
}
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    header('Location: contact.html?error=email');
    exit;
}

$body = "Website enquiry\n\n"
      . "Name:    {$name}\n"
      . "Phone:   {$phone}\n"
      . "Email:   " . ($email !== '' ? $email : '(not given)') . "\n"
      . "Subject: {$reason}\n\n"
      . "Message:\n{$message}\n\n"
      . '---'."\n"
      . 'Sent ' . date('Y-m-d H:i:s T') . ' from ' . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n";

// From is a build-time constant, never $_SERVER['HTTP_HOST']: that header is
// client-controlled, and it is the one value that would otherwise reach the
// mail headers without passing through the sanitiser above.
$headers  = 'From: Churchill Medical Clinic <' . $fromAddr . ">\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
if ($email !== '') {
    $headers .= 'Reply-To: ' . $email . "\r\n";
}

// The fifth argument sets the envelope sender. Without it, cPanel's Exim uses
// the hosting account default, so SPF authenticates a hostgator.com hostname
// while the From: header claims the clinic's domain. That misalignment is what
// puts the message in the spam folder, or gets it rejected outright.
$sent = @mail($to, $subject, $body, $headers, '-f ' . $fromAddr);
header('Location: ' . ($sent ? 'thank-you.html' : 'contact.html?error=send'));
exit;
