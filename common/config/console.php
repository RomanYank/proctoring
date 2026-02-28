<?php

return [
    'id' => 'app-console',
    'basePath' => dirname(__DIR__),
    'bootstrap' => ['queue'],
    'components' => [
        'db' => [
            'class' => yii\db\Connection::class,
            'dsn' => 'mysql:host=db;dbname=proctoring_db;charset=utf8;ssl-mode=DISABLED',
            'username' => 'proctoring_user',
            'password' => 'proctoring_pass',
        ],
        'queue' => [
            'class' => yii\queue\db\Queue::class,
            'db' => 'db',
            'tableName' => '{{%queue}}',
            'channel' => 'default',
            'mutex' => yii\mutex\MysqlMutex::class,
        ],
    ],
];
