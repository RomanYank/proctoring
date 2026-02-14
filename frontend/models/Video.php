<?php

namespace frontend\models;

use yii\db\ActiveRecord;

class Video extends ActiveRecord {
    public static function tableName() {
        return 'video_files';
    }
    public function attributeLabels() {
        return [
            'user_id' => 'ID пользователя',
            'date' => 'Дата',
            'web_camera_video' => 'Видео с камеры',
            'capture_screen_video' => 'Демонстрация экрана'
        ];
    }
    public function rules(){
        return [
            [['user_id', 'verify'], 'integer'],
            [['date', 'web_camera_video', 'capture_screen_video'], 'string']
        ];
    }
}
