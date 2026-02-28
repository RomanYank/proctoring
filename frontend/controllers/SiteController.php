<?php

namespace frontend\controllers;

use backend\models\Department;
use frontend\models\ResendVerificationEmailForm;
use frontend\models\VerifyEmailForm;
use Yii;
use yii\base\InvalidArgumentException;
use yii\web\BadRequestHttpException;
use yii\web\Controller;
use yii\web\Response;
use yii\filters\VerbFilter;
use yii\filters\AccessControl;
use frontend\models\LoginForm;
use frontend\models\PasswordResetRequestForm;
use frontend\models\ResetPasswordForm;
use frontend\models\SignupForm;
use frontend\models\ContactForm;
#use frontend\models\Employees;
use frontend\models\Video;
use yii\web\UploadedFile;
use common\jobs\AnalyzeJob;

/**
 * Site controller
 */
class SiteController extends Controller
{
    /**
     * {@inheritdoc}
     */
    public function behaviors()
    {
        return [
            'access' => [
                'class' => AccessControl::class,
                'only' => ['logout', 'signup'],
                'rules' => [
                    [
                        'actions' => ['signup'],
                        'allow' => true,
                        'roles' => ['?'],
                    ],
                    [
                        'actions' => ['logout'],
                        'allow' => true,
                        'roles' => ['@'],
                    ],
                ],
            ],
            'verbs' => [
                'class' => VerbFilter::class,
                'actions' => [
                    'logout' => ['post'],
                ],
            ],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function actions()
    {
        return [
            'error' => [
                'class' => \yii\web\ErrorAction::class,
            ],
            'captcha' => [
                'class' => \yii\captcha\CaptchaAction::class,
                'fixedVerifyCode' => YII_ENV_TEST ? 'testme' : null,
            ],
        ];
    }

    /**
     * Displays homepage.
     *
     * @return mixed
     */


    public function actionIndex() {
        if(!empty(Yii::$app->user->identity)) {
            $departmentId = Yii::$app->user->identity->department_id;
            $model = Department::findOne($departmentId);
            return $this->render('index', [
                'model' => $model,
            ]);
        } else {
            return $this->actionLogin();
        }
    }

    /**
     * Logs in a user.
     *
     * @return mixed
     */
    public function actionLogin()
    {
        if (!Yii::$app->user->isGuest) {
            return $this->goHome();
        }

        $model = new LoginForm();
        if ($model->load(Yii::$app->request->post()) && $model->login()) {
            return $this->goBack();
        }

        $model->password_hash = '';

        return $this->render('login', [
            'model' => $model,
        ]);
    }

    /**
     * Logs out the current user.
     *
     * @return mixed
     */
    public function actionLogout()
    {
        Yii::$app->user->logout();

        return $this->goHome();
    }

    /**
     * Displays contact page.
     *
     * @return mixed
     */
    public function actionContact()
    {
        $model = new ContactForm();
        if ($model->load(Yii::$app->request->post()) && $model->validate()) {
            if ($model->sendEmail(Yii::$app->params['adminEmail'])) {
                Yii::$app->session->setFlash('success', 'Thank you for contacting us. We will respond to you as soon as possible.');
            } else {
                Yii::$app->session->setFlash('error', 'There was an error sending your message.');
            }

            return $this->refresh();
        }

        return $this->render('contact', [
            'model' => $model,
        ]);
    }

    /**
     * Displays about page.
     *
     * @return mixed
     */
    public function actionAbout()
    {
        return $this->render('about');
    }

    /**
     * Signs user up.
     *
     * @return mixed
     */
    public function actionSignup()
    {
        $model = new SignupForm();
        if ($model->load(Yii::$app->request->post()) && $model->signup()) {
            Yii::$app->session->setFlash('success', 'Thank you for registration. Please check your inbox for verification email.');
            return $this->goHome();
        }

        return $this->render('signup', [
            'model' => $model,
        ]);
    }

    /**
     * Requests password reset.
     *
     * @return mixed
     */
    public function actionRequestPasswordReset()
    {
        $model = new PasswordResetRequestForm();
        if ($model->load(Yii::$app->request->post()) && $model->validate()) {
            if ($model->sendEmail()) {
                Yii::$app->session->setFlash('success', 'Check your email for further instructions.');

                return $this->goHome();
            }

            Yii::$app->session->setFlash('error', 'Sorry, we are unable to reset password for the provided email address.');
        }

        return $this->render('requestPasswordResetToken', [
            'model' => $model,
        ]);
    }

    /**
     * Resets password.
     *
     * @param string $token
     * @return mixed
     * @throws BadRequestHttpException
     */
    public function actionResetPassword($token)
    {
        try {
            $model = new ResetPasswordForm($token);
        } catch (InvalidArgumentException $e) {
            throw new BadRequestHttpException($e->getMessage());
        }

        if ($model->load(Yii::$app->request->post()) && $model->validate() && $model->resetPassword()) {
            Yii::$app->session->setFlash('success', 'New password saved.');

            return $this->goHome();
        }

        return $this->render('resetPassword', [
            'model' => $model,
        ]);
    }

    /**
     * Verify email address
     *
     * @param string $token
     * @throws BadRequestHttpException
     * @return yii\web\Response
     */
    public function actionVerifyEmail($token)
    {
        try {
            $model = new VerifyEmailForm($token);
        } catch (InvalidArgumentException $e) {
            throw new BadRequestHttpException($e->getMessage());
        }
        if (($user = $model->verifyEmail()) && Yii::$app->user->login($user)) {
            Yii::$app->session->setFlash('success', 'Your email has been confirmed!');
            return $this->goHome();
        }

        Yii::$app->session->setFlash('error', 'Sorry, we are unable to verify your account with provided token.');
        return $this->goHome();
    }

    /**
     * Resend verification email
     *
     * @return mixed
     */
    public function actionResendVerificationEmail()
    {
        $model = new ResendVerificationEmailForm();
        if ($model->load(Yii::$app->request->post()) && $model->validate()) {
            if ($model->sendEmail()) {
                Yii::$app->session->setFlash('success', 'Check your email for further instructions.');
                return $this->goHome();
            }
            Yii::$app->session->setFlash('error', 'Sorry, we are unable to resend verification email for the provided email address.');
        }

        return $this->render('resendVerificationEmail', [
            'model' => $model
        ]);
    }

    public function actionUpload()
    {
        Yii::$app->response->format = Response::FORMAT_HTML;
        Yii::$app->response->headers->set('Access-Control-Allow-Origin', '*');

        try {
            if (!Yii::$app->request->isPost) {
                throw new BadRequestHttpException('Invalid request method.');
            }

            $fileName = Yii::$app->request->post('video-filename');
            if (empty($fileName)) {
                throw new \Exception('Empty file name.');
            }

            $allowedExtensions = ['webm', 'wav', 'mp4', 'mkv', 'mp3', 'ogg'];
            $extension = pathinfo($fileName, PATHINFO_EXTENSION);

            if (!$extension || !in_array($extension, $allowedExtensions)) {
                throw new \Exception('Invalid file extension: ' . $extension);
            }

            $file = UploadedFile::getInstanceByName('video-blob');
            if (!$file || !$file->tempName) {
                throw new \Exception('No uploaded file found or invalid temp name.');
            }

            $uploadPath = Yii::getAlias('@frontend/web/record/video');
            if (!is_dir($uploadPath)) {
                mkdir($uploadPath, 0777, true);
            }

            $savePath = $uploadPath . DIRECTORY_SEPARATOR . $fileName;

            if (!$file->saveAs($savePath)) {
                if ($file->error) {
                    $uploadErrors = [
                        UPLOAD_ERR_INI_SIZE   => 'The uploaded file exceeds the upload_max_filesize directive in php.ini.',
                        UPLOAD_ERR_FORM_SIZE  => 'The uploaded file exceeds the MAX_FILE_SIZE directive that was specified in the HTML form.',
                        UPLOAD_ERR_PARTIAL    => 'The uploaded file was only partially uploaded.',
                        UPLOAD_ERR_NO_FILE    => 'No file was uploaded.',
                        UPLOAD_ERR_NO_TMP_DIR => 'Missing a temporary folder.',
                        UPLOAD_ERR_CANT_WRITE => 'Failed to write file to disk.',
                        UPLOAD_ERR_EXTENSION  => 'A PHP extension stopped the file upload.',
                    ];

                    $errorMsg = $uploadErrors[$file->error] ?? ('Unknown upload error #' . $file->error);
                    throw new \Exception($errorMsg);
                } else {
                    throw new \Exception('Problem saving file: ' . $file->tempName);
                }
            }

            return 'success';
        } catch (\Throwable $e) {
            return '<h2>Upload failed.</h2><br><p>' . $e->getMessage() . '</p>';
        }
    }

    public function actionSaveVideo() {
        $model = new Video();
        Yii::$app->response->format = Response::FORMAT_JSON;
        if (Yii::$app->request->isAjax) {
            $data = Yii::$app->request->post();
            $model->user_id = Yii::$app->user->identity->id;
            $model->date = date("y/m/d");
            $model->web_camera_video = $data['web_camera_video'];
            $model->capture_screen_video = $data['capture_screen_video'];
            $model->verify = 0;
            if ($model->save()) {
                Yii::$app->queue->push(new AnalyzeJob([
                    'videoPath' => Yii::getAlias('@frontend/web/record/video/' . $model->web_camera_video),
                    'videoId' => $model->id,
                ]));
                return ['response' => true];
            } else {
                return ['response' => false];
            }
        }
    }
}
