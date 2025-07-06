<?php
/**
 * @link https://www.yiiframework.com/
 * @copyright Copyright (c) 2008 Yii Software LLC
 * @license https://www.yiiframework.com/license/
 */

namespace yii\queue\db\migrations;
use yii\db\Connection;
use yii\db\Migration;

/**
 * Example of migration for queue message storage.
 *
 * @author Roman Zhuravlev <zhuravljov@gmail.com>
 */
class M161119140200Queue extends Migration
{
    public $tableName = '{{%queue}}';
    public $tableOptions;
    private $_db;

    public function getDb()
    {

        $this->_db = new Connection([
            'dsn' => 'mysql:host=127.0.0.1;dbname=project_db',
            'username' => 'root',
            'password' => 'root',
            'charset' => 'utf8',
        ]);
        $this->_db->open(); 
        return $this->_db;
    }


    public function up()
    {
        $this->createTable($this->tableName, [
            'id' => $this->primaryKey(),
            'channel' => $this->string()->notNull(),
            'job' => $this->binary()->notNull(),
            'created_at' => $this->integer()->notNull(),
            'started_at' => $this->integer(),
            'finished_at' => $this->integer(),
        ], $this->tableOptions);

        $this->createIndex('channel', $this->tableName, 'channel');
        $this->createIndex('started_at', $this->tableName, 'started_at');
    }

    public function down()
    {
        $this->dropTable($this->tableName);
    }
}
