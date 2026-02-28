<?php

use yii\db\Migration;

/**
 * Handles the creation of table `{{%video_files}}`.
 */
class m260228_192516_create_video_files_table extends Migration
{
    /**
     * {@inheritdoc}
     */
    public function safeUp()
    {
        $this->createTable('{{%video_files}}', [
            'id' => $this->primaryKey(),
            'web_camera_video' => $this->text()->notNull(),
            'capture_screen_video' => $this->text()->notNull(),
            'date' => $this->date()->notNull(),
            'user_id' => $this->integer()->notNull(),
            'violations' => $this->json()->defaultValue(null),
            'verify' => $this->integer()->defaultValue(null),
        ]);
    }

    /**
     * {@inheritdoc}
     */
    public function safeDown()
    {
        $this->dropTable('{{%video_files}}');
    }
}
