<?php

namespace frontend\controllers;
use Yii;
use yii\rest\ActiveController;
use backend\models\VideoFiles;
use backend\models\User;

class VideoController extends ActiveController
{
    public $modelClass = 'backend\models\Video';

    public function actions()
    {
        $actions = parent::actions();

        unset($actions['delete'], $actions['index'], $actions['update'], $actions['create']);

        return $actions;
    }

    /* Просмотр всех записей */
    public function actionIndex()
    {
        return VideoFiles::find()->all();
    }

    /* Удаление записи */
    public function actionDelete($id)
    {
        $model = $this->findModel($id);
        if (!empty($model) && $model->delete()) {
            return ['message' => 'Видеопротокол удален'];
        }
        Yii::$app->response->statusCode = 404;
        return ['message' => 'Не удалось удалить видеопротокол'];
    }

    /*Обновление записи*/
    public function actionUpdate($id)
    {
        $model = $this->findModel($id);
        $params = Yii::$app->request->post();
        if(!empty($model)) {
            if (isset($params['web_camera_video'])) {
                $model->web_camera_video = $params['web_camera_video'];
            }

            if (isset($params['capture_screen_video'])) {
                $model->capture_screen_video = $params['capture_screen_video'];
            }

            if (isset($params['date'])) {
                $model->date = $params['date'];
            }

            if (isset($params['user_id'])) {
                $user = User::findOne($params['user_id']);
                if(!empty($user)) {
                    $model->user_id = $user->id;
                } else {
                    return ['message' => 'Пользователь не найден'];
                }
            }

            if ($model->save()) {
                return ['message' => 'Видеопротокол обновлён', 'data' => $model];
            }
        }
        Yii::$app->response->statusCode = 404;
        return ['message' => 'Не удалось обновить данные видеопротокола'];
    }

    /*Создание записи*/
    public function actionCreate()
    {
        $model = new VideoFiles();
        $params = Yii::$app->request->post();
        if(!empty($params)) {
            if (isset($params['web_camera_video'])) {
                $model->web_camera_video = $params['web_camera_video'];
            } else {
                Yii::$app->response->statusCode = 404;
                return ['message' => 'Необходимо заполнить web_camera_video'];
            }

            if (isset($params['capture_screen_video'])) {
                $model->capture_screen_video = $params['capture_screen_video'];
            } else {
                Yii::$app->response->statusCode = 404;
                return ['message' => 'Необходимо заполнить capture_screen_video'];
            }

            if (isset($params['date']) ) {
                $model->date = $params['date'];
            } else {
                Yii::$app->response->statusCode = 404;
                return ['message' => 'Необходимо заполнить date'];
            }

            if (isset($params['user_id'])) {
                $user = User::findOne($params['user_id']);
                if(!empty($user)) {
                    $model->user_id = $user->id;
                } else {
                    return ['message' => 'Пользователь не найден'];
                }
            } else {
                Yii::$app->response->statusCode = 404;
                return ['message' => 'Необходимо заполнить user_id'];
            }

            if ($model->save()) {
                return ['message' => 'Видеопротокол создан', 'data' => $model];
            }
        }
    }

    protected function findModel($id)
    {
        $model = VideoFiles::findOne($id);
        if (!empty($model)) {
            return $model;
        }
    }
}