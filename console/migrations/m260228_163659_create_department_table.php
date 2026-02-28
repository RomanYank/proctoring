<?php

use yii\db\Migration;

/**
 * Handles the creation of table `{{%department}}`.
 */
class m260228_163659_create_department_table extends Migration
{
    public function safeUp()
    {
        $this->createTable('department', [
            'id' => $this->primaryKey(),
            'name' => $this->text()->notNull(),
            'recording_time' => $this->integer()->notNull(),
        ]);
    }

    public function safeDown()
    {
        $this->dropTable('department');
    }
}
