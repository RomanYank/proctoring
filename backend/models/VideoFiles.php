<?php

namespace backend\models;

use Yii;

/**
 * This is the model class for table "video_files".
 *
 * @property int $id
 * @property string $web_camera_video
 * @property string $capture_screen_video
 * @property string $date
 * @property int $user_id
 *
 * @property User $user
 */
class VideoFiles extends \yii\db\ActiveRecord
{

    const LABEL_STATUS = [
        0 => 'На проверке',
        1 => 'Проверено'
    ];

    /**
     * {@inheritdoc}
     */
    public static function tableName()
    {
        return 'video_files';
    }

    /**
     * {@inheritdoc}
     */
    public function rules()
    {
        return [
            [['web_camera_video', 'capture_screen_video', 'date', 'user_id'], 'required'],
            [['web_camera_video', 'capture_screen_video', 'date', 'violations'], 'string'],
            [['user_id', 'verify'], 'integer'],
            [['user_id'], 'exist', 'skipOnError' => true, 'targetClass' => User::class, 'targetAttribute' => ['user_id' => 'id']],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function attributeLabels()
    {
        return [
            'id' => 'ID',
            'web_camera_video' => 'Web Camera Video',
            'capture_screen_video' => 'Capture Screen Video',
            'date' => 'Date',
            'user_id' => 'User ID',
        ];
    }

    public function viewsTables()
    {
        return VideoFiles::find()
            ->joinWith('user')
            ->orderBy('video_files.id');
    }


    /**
     * Gets query for [[User]].
     *
     * @return \yii\db\ActiveQuery
     */

    public function getUser()
    {
        return $this->hasOne(User::class, ['id' => 'user_id']);
    }

    public function statusLabel() 
    {
        return self::LABEL_STATUS[$this->verify];
    }
}
