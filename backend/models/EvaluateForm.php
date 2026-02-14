<?php

namespace backend\models;

use yii\base\Model;
use yii\web\UploadedFile;

class EvaluateForm extends Model
{
    /** @var UploadedFile */
    public $imageFile;

    public function rules()
    {
        return [
            [['imageFile'], 'file', 'skipOnEmpty' => false, 'extensions' => 'png, jpg, jpeg'],
        ];
    }

    public function attributeLabels()
    {
        return [
            'imageFile' => 'Изображение для оценки',
        ];
    }
}
