<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, max-age=0');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: same-origin');

function respond(int $status, array $payload): never
{
    http_response_code($status);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    respond(405, ['ok' => false, 'message' => 'Method not allowed.']);
}

$secure = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off');
session_set_cookie_params([
    'lifetime' => 0,
    'path' => '/',
    'secure' => $secure,
    'httponly' => true,
    'samesite' => 'Lax',
]);
session_start();

$token = (string)($_POST['csrf_token'] ?? '');
$sessionToken = (string)($_SESSION['csrf_token'] ?? '');
if ($sessionToken === '' || $token === '' || !hash_equals($sessionToken, $token)) {
    respond(403, ['ok' => false, 'message' => 'Invalid form session.']);
}

if (trim((string)($_POST['website'] ?? '')) !== '') {
    respond(400, ['ok' => false, 'message' => 'Invalid submission.']);
}

$now = time();
$window = 600;
$limit = 3;
$attempts = array_values(array_filter((array)($_SESSION['form_attempts'] ?? []), static fn($time) => is_int($time) && $time > $now - $window));
if (count($attempts) >= $limit) {
    respond(429, ['ok' => false, 'message' => 'Too many attempts. Please try again later.']);
}
$attempts[] = $now;
$_SESSION['form_attempts'] = $attempts;

function clean(string $value): string
{
    $value = str_replace(["\r\n", "\r"], "\n", trim($value));
    return preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $value) ?? '';
}

$name = clean((string)($_POST['name'] ?? ''));
$contact = clean((string)($_POST['contact'] ?? ''));
$message = clean((string)($_POST['message'] ?? ''));
$language = (string)($_POST['language'] ?? 'uk');
$source = clean((string)($_POST['source'] ?? '/'));
$consent = (string)($_POST['consent'] ?? '');

$length = static fn(string $value): int => function_exists('mb_strlen') ? mb_strlen($value, 'UTF-8') : strlen($value);

if ($length($name) < 2 || $length($name) > 80) {
    respond(422, ['ok' => false, 'message' => 'Please provide a valid name.']);
}
$phoneDigits = preg_replace('/\D+/', '', $contact) ?? '';
if ($length($contact) > 24 || strlen($phoneDigits) < 7 || strlen($phoneDigits) > 15 || !preg_match('/^[+0-9()\s-]+$/', $contact)) {
    respond(422, ['ok' => false, 'message' => 'Please provide a valid phone number.']);
}
if ($length($message) < 10 || $length($message) > 3000) {
    respond(422, ['ok' => false, 'message' => 'Please provide a project description.']);
}
if ($consent !== 'yes') {
    respond(422, ['ok' => false, 'message' => 'Consent is required.']);
}
if (!in_array($language, ['uk', 'en'], true)) {
    $language = 'uk';
}
if (!preg_match('#^/(?:uk|en)/(?:[a-z0-9-]+/)*$#', $source)) {
    $source = '/';
}

$config = [
    'mode' => getenv('CONTACT_MODE') ?: 'mock',
    'telegram_bot_token' => getenv('TELEGRAM_BOT_TOKEN') ?: '',
    'telegram_chat_id' => getenv('TELEGRAM_CHAT_ID') ?: '',
];

$privateConfig = dirname(__DIR__) . '/config/private.php';
if (is_file($privateConfig)) {
    $fileConfig = require $privateConfig;
    if (is_array($fileConfig)) {
        $config = array_merge($config, $fileConfig);
    }
}

if (($config['mode'] ?? 'mock') === 'mock') {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    respond(200, ['ok' => true, 'delivered' => false, 'mode' => 'mock']);
}

if (($config['mode'] ?? '') !== 'telegram') {
    respond(500, ['ok' => false, 'message' => 'Invalid server configuration.']);
}

$botToken = (string)($config['telegram_bot_token'] ?? '');
$chatId = (string)($config['telegram_chat_id'] ?? '');
if ($botToken === '' || $chatId === '') {
    respond(503, ['ok' => false, 'message' => 'Messaging is not configured.']);
}
if (!function_exists('curl_init')) {
    respond(503, ['ok' => false, 'message' => 'Server transport is unavailable.']);
}

$e = static fn(string $value): string => htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$serverTime = (new DateTimeImmutable('now'))->format('Y-m-d H:i:s T');
$telegramText = "<b>New website enquiry</b>\n"
    . "<b>Time:</b> " . $e($serverTime) . "\n"
    . "<b>Name:</b> " . $e($name) . "\n"
    . "<b>Phone:</b> " . $e($contact) . "\n"
    . "<b>Language:</b> " . $e(strtoupper($language)) . "\n"
    . "<b>Source:</b> " . $e($source) . "\n\n"
    . "<b>Message:</b>\n" . $e($message);

$url = 'https://api.telegram.org/bot' . rawurlencode($botToken) . '/sendMessage';
$curl = curl_init($url);
curl_setopt_array($curl, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => http_build_query([
        'chat_id' => $chatId,
        'text' => $telegramText,
        'parse_mode' => 'HTML',
        'disable_web_page_preview' => 'true',
    ]),
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CONNECTTIMEOUT => 5,
    CURLOPT_TIMEOUT => 10,
    CURLOPT_HTTPHEADER => ['Content-Type: application/x-www-form-urlencoded'],
]);
$response = curl_exec($curl);
$status = (int)curl_getinfo($curl, CURLINFO_HTTP_CODE);
$curlError = curl_errno($curl);
curl_close($curl);

$decoded = is_string($response) ? json_decode($response, true) : null;
if ($curlError !== 0 || $status !== 200 || !is_array($decoded) || ($decoded['ok'] ?? false) !== true) {
    error_log('Telegram delivery failed. HTTP status: ' . $status . '; cURL error: ' . $curlError);
    respond(502, ['ok' => false, 'message' => 'Delivery failed.']);
}

$_SESSION['csrf_token'] = bin2hex(random_bytes(32));
respond(200, ['ok' => true, 'delivered' => true, 'mode' => 'telegram']);
