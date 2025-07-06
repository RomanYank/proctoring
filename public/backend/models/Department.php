<?php

namespace backend\models;

use Yii;

/**
 * This is the model class for table "recording_settings".
 *
 * @property int $id
 * @property int $recording_time
 * @property int $user_id
 *
 * @property User $user
 */
class Department extends \yii\db\ActiveRecord
{
    /**
     * {@inheritdoc}
     */
    public static function tableName()
    {
        return 'department';
    }

    /**
     * {@inheritdoc}
     */
    public function rules()
    {
        return [
            ['recording_time', 'integer'],
            ['name', 'string'],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function attributeLabels()
    {
        return [
            'id' => 'ID',
            'name' => 'Название организации',
            'recording_time' => 'Время на тест',
        ];
    }
}