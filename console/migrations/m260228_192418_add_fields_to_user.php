<?php

use yii\db\Migration;

class m260228_192418_add_fields_to_user extends Migration
{
    /**
     * {@inheritdoc}
     */
    public function safeUp()
    {
        $this->addColumn('{{%user}}', 'full_name', $this->text()->notNull());
        $this->addColumn('{{%user}}', 'role', $this->integer()->notNull());
        $this->addColumn('{{%user}}', 'department_id', $this->integer()->notNull());
    }

        /**
     * {@inheritdoc}
     */
    public function safeDown()
    {
        $this->dropColumn('{{%user}}', 'department_id');
        $this->dropColumn('{{%user}}', 'role');
        $this->dropColumn('{{%user}}', 'full_name');
    }
}
