<?php
return [
    'components' => [
        'db' => [
            'class' => 'yii\db\Connection',
            'dsn' => 'mysql:host=db;dbname=proctoring_db',
            'username' => 'proctoring_user',
            'password' => 'proctoring_pass',
            'charset' => 'utf8',
        ],
    ],
];