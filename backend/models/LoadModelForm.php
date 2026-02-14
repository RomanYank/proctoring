<?php

namespace backend\models;

use yii\base\Model;

class LoadModelForm extends Model
{
    /**
     * @var UploadedFile
     */
    public $modelFile;

    public function rules()
    {
        return [
            [['modelFile'], 'file', 'skipOnEmpty' => false],
        ];
    }

    public function attributeLabels()
    {
        return [
            'modelFile' => 'Файл модели',
        ];
    }
}