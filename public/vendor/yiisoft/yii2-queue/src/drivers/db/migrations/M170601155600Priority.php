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
class M170601155600Priority extends Migration
{
    public $tableName = '{{%queue}}';
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
        $this->addColumn($this->tableName, 'priority', $this->integer()->unsigned()->notNull()->defaultValue(1024)->after('delay'));
        $this->createIndex('priority', $this->tableName, 'priority');
    }

    public function down()
    {
        $this->dropIndex('priority', $this->tableName);
        $this->dropColumn($this->tableName, 'priority');
    }
}
