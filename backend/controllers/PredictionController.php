<?php

namespace backend\controllers;

use Yii;
use yii\web\Controller;
use yii\web\UploadedFile;
use yii\helpers\Json;
use backend\models\LoadModelForm;
use backend\models\EvaluateForm;
use GuzzleHttp\Client;

class PredictionController extends Controller
{
    private $fastApiBaseUrl = 'http://localhost:8000';

    public function actionLoad()
    {
        $model = new LoadModelForm();
    
        if (Yii::$app->request->isPost) {
            $model->modelFile = UploadedFile::getInstance($model, 'modelFile');
    
            if ($model->validate()) {
                $tempPath = tempnam(sys_get_temp_dir(), 'model_');
                $model->modelFile->saveAs($tempPath);
    
                $client = new Client();
                $response = $client->post($this->fastApiBaseUrl . '/load/', [
                    'multipart' => [
                        [
                            'name' => 'model',
                            'contents' => fopen($tempPath, 'r'),
                            'filename' => $model->modelFile->name,
                        ],
                    ],
                ]);
    
                unlink($tempPath);
    
                $data = Json::decode($response->getBody()->getContents());
                Yii::$app->session->setFlash('loadModelResponse', $data['message'] ?? $data['error'] ?? 'Неизвестный ответ');
            }
        }
    
        return $this->render('load', ['model' => $model]);
    }
    
    public function actionEvaluate()
    {
        $model = new EvaluateForm();
    
        $predictionTable = '';
        $annotatedImage = '';
        if (Yii::$app->request->isPost) {
            $model->imageFile = UploadedFile::getInstance($model, 'imageFile');
    
            if ($model->validate()) {
                $client = new \GuzzleHttp\Client();
                $tempFile = tempnam(sys_get_temp_dir(), 'yii');
                $model->imageFile->saveAs($tempFile);
    
                $response = $client->post($this->fastApiBaseUrl . '/evaluate/', [
                    'multipart' => [
                        [
                            'name' => 'image',
                            'contents' => fopen($tempFile, 'r'),
                            'filename' => $model->imageFile->name,
                        ],
                    ],
                ]);
                unlink($tempFile);
    
                $data = \yii\helpers\Json::decode($response->getBody()->getContents());
                $predictionTable = $data['predictions'];
                $annotatedImage = $data['image'];
            }
        }
    
        return $this->render('evaluate', [
            'model' => $model,
            'predictionTable' => $predictionTable,
            'annotatedImage' => $annotatedImage,
        ]);
    }    
}
