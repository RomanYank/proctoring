<?php

namespace frontend\controllers;
use Yii;
use backend\models\Department;
use yii\rest\ActiveController;

class DepartmentController extends ActiveController
{
    public $modelClass = 'backend\models\Department';

    public function actions()
    {
        $actions = parent::actions();

        unset($actions['delete'], $actions['index'], $actions['update'], $actions['create']);

        return $actions;
    }

    /* Просмотр всех записей */
    public function actionIndex()
    {
        return Department::find()->all();
    }

    /* Удаление записи */
    public function actionDelete($id)
    {
        $model = $this->findModel($id);
        if (!empty($model) && $model->delete()) {
            return ['message' => 'Организация удалена'];
        }
        Yii::$app->response->statusCode = 404;
        return ['message' => 'Не удалось удалить организацию'];
    }

    /*Обновление записи*/
    public function actionUpdate($id)
    {
        $model = $this->findModel($id);
        $params = Yii::$app->request->post();
        if(!empty($model)) {
            if (isset($params['name'])) {
                $model->name = $params['name'];
            }

            if (isset($params['recording_time'])) {
                $model->recording_time = $params['recording_time'];
            }

            if ($model->save()) {
                return ['message' => 'Организация обнавлена', 'data' => $model];
            }
        }
        Yii::$app->response->statusCode = 404;
        return ['message' => 'Не удалось обновить данные организации'];
    }

    /*Создание записи*/
    public function actionCreate()
    {
        $model = new Department();
        $params = Yii::$app->request->post();
        if(!empty($params)) {
            if (isset($params['name'])) {
                $model->name = $params['name'];
            } else {
                Yii::$app->response->statusCode = 404;
                return ['message' => 'Необходимо заполнить name'];
            }

            if (isset($params['recording_time'])) {
                $model->recording_time = $params['recording_time'];
            } else {
                Yii::$app->response->statusCode = 404;
                return ['message' => 'Необходимо заполнить recording_time'];
            }

            if ($model->save()) {
                return ['message' => 'Организация создана', 'data' => $model];
            }
        }
    }

    protected function findModel($id)
    {
        $model = Department::findOne($id);
        if (!empty($model)) {
            return $model;
        }
    }
}