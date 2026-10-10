<?php
// Copy to private.php only for local development. In production, prefer
// environment variables or place the private file outside the public webroot.
return [
    'mode' => 'mock', // Change to 'telegram' only after adding credentials.
    'telegram_bot_token' => '',
    'telegram_chat_id' => '',
];
