<?php

namespace frontend\controllers;
use Yii;
use yii\rest\ActiveController;
use backend\models\User;
use backend\models\Department;
class UserController extends ActiveController
{

    public $modelClass = 'backend\models\User';

    public function actions()
    {
        $actions = parent::actions();

        unset($actions['delete'], $actions['index'], $actions['update']);

        return $actions;
    }

    /* Просмотр всех пользователей */
    public function actionIndex()
    {
        return User::find()->all();
    }

    /* Удаление пользователя */
    public function actionDelete($id)
    {
        $model = $this->findModel($id);
        if (!empty($model) && $model->delete()) {
            return ['message' => 'Пользователь удалён'];
        }
        Yii::$app->response->statusCode = 422;
        return ['message' => 'Не удалось удалить пользователя'];
    }

    /*Обновление пользователя*/
    public function actionUpdate($id)
    {
        $model = $this->findModel($id);
        $params = Yii::$app->request->post();
        if(!empty($model)) {
            if (isset($params['username'])) {
                $model->username = $params['username'];
            }

            if (isset($params['full_name'])) {
                $model->full_name = $params['full_name'];
            }

            if (isset($params['department_id'])) {
                $department = Department::findOne($params['department_id']);
                if(!empty($department_id)) {
                    $model->department_id = $department->id;
                } else {
                    return ['message' => 'Организация не найдена'];
                }
            }

            if ($model->save(false)) {
                return ['message' => 'Пользователь обновлён', 'data' => $model];
            }
        }
        Yii::$app->response->statusCode = 422;
        return ['message' => 'Не удалось обновить данные пользователя'];
    }

    protected function findModel($id)
    {
        $model = User::findOne($id);
        if (!empty($model)) {
            return $model;
        }
    }
}