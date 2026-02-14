<?php

namespace backend\models;
use Yii;
use backend\models\VideoFiles;
/**
 * This is the model class for table "user".
 *
 * @property int $id
 * @property string $username
 * @property string $full_name
 * @property string $password
 * @property int $status
 * @property string $auth_key
 * @property int $role
 *
 * @property VideoFiles[] $videoFiles
 */
class User extends \yii\db\ActiveRecord
{
    /**
     * {@inheritdoc}
     */
    public static function tableName()
    {
        return 'user';
    }

    /**
     * {@inheritdoc}
     */
    public function rules()
    {
        return [
            [['username', 'full_name', 'password', 'status', 'auth_key', 'role'], 'required'],
            [['username', 'full_name', 'password', 'auth_key'], 'string'],
            [['status', 'role', 'department_id'], 'integer']
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function attributeLabels()
    {
        return [
            'id' => 'ID',
            'username' => 'Логин',
            'full_name' => 'ФИО',
            'password' => 'Пароль',
            'status' => 'Статус',
            'role' => 'Роль',
            'department_id' => 'ID Организации'
        ];
    }

    /**
     * Gets query for [[VideoFiles]].
     *
     * @return \yii\db\ActiveQuery
     */
    public function getVideoFiles()
    {
        return $this->hasMany(VideoFiles::class, ['user_id' => 'id']);
    }

    public function getDepartment()
    {
        return $this->hasMany(Department::class, ['id' => 'department_id']);
    }
}
