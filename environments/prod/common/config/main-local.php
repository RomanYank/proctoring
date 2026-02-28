<?php

return [
    'components' => [
        'db' => [
            'class' => \yii\db\Connection::class,
            'dsn' => 'mysql:host=db;dbname=proctoring_db;charset=utf8;ssl-mode=DISABLED',
            'username' => 'proctoring_user',
            'password' => 'proctoring_pass',
        ],
        'mailer' => [
            'class' => \yii\symfonymailer\Mailer::class,
            'viewPath' => '@common/mail',
        ],
    ],
];
