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
class M211218163000JobQueueSize extends Migration
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
        if ($this->db->driverName === 'mysql') {
            $this->alterColumn($this->tableName, 'job', 'LONGBLOB NOT NULL');
        }
    }

    public function down()
    {
        if ($this->db->driverName === 'mysql') {
            $this->alterColumn($this->tableName, 'job', $this->binary()->notNull());
        }
    }
}
