<?php

namespace backend\models;

use yii\base\Model;
use yii\web\UploadedFile;

class TrainForm extends Model
{
    /**
     * @var UploadedFile
     */
    public $csvFile;
    public $classDescFile;
    public $epochs;
    
    public function rules()
    {
        return [
            [['csvFile', 'classDescFile'], 'file', 'extensions' => 'csv'],
            ['epochs', 'integer'],
            [['csvFile', 'classDescFile', 'epochs'], 'required'],
        ];
    }

        /**
     * {@inheritdoc}
     */
    public function attributeLabels()
    {
        return [
            'csvFile' => 'CSV файл с данными',
            'classDescFile' => 'CSV файл с описанием классов',
            'epochs' => 'Количество эпох',
        ];
    }
}
