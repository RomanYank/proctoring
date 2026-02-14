<?php

namespace backend\controllers;

use Yii;
use yii\web\Controller;
use yii\web\UploadedFile;
use backend\models\TrainForm;
use common\jobs\TrainJob;

class TrainController extends Controller
{
    public function actionIndex()
    {
        $model = new TrainForm();

        if (Yii::$app->request->isPost) {
            $model->csvFile = UploadedFile::getInstance($model, 'csvFile');
            $model->classDescFile = UploadedFile::getInstance($model, 'classDescFile');
            $model->epochs = Yii::$app->request->post('TrainForm')['epochs'];

            if ($model->validate()) {
                $csvPath = Yii::getAlias('@runtime/uploads/' . uniqid() . '_' . $model->csvFile->name);
                $classDescPath = Yii::getAlias('@runtime/uploads/' . uniqid() . '_' . $model->classDescFile->name);

                $model->csvFile->saveAs($csvPath);
                $model->classDescFile->saveAs($classDescPath);

                Yii::$app->queue->push(new TrainJob([
                    'csvPath' => $csvPath,
                    'csvName' => $model->csvFile->name,
                    'classDescPath' => $classDescPath,
                    'classDescName' => $model->classDescFile->name,
                    'epochs' => $model->epochs,
                ]));

                return $this->goHome();
            }
        }

        return $this->render('train', ['model' => $model]);
    }
}
