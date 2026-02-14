<?php
use yii\bootstrap5\ActiveForm;
use yii\bootstrap5\Html;
?>
<?php $form = ActiveForm::begin([
    'id' => 'video_files',
    'enableAjaxValidation' => true, 
    ]); ?>
        <?= $form->field($model, 'user_id')->textInput() ?>
        <?= $form->field($model, 'date')->textInput() ?>
        <?= $form->field($model, 'web_camera_video')->textInput() ?>
        <?= $form->field($model, 'capture_screen_video')->textInput() ?>
        <div class="form-group">
            <?= Html::submitButton('Сохранить', ['class' => 'btn btn-success']) ?>
        </div>
<?php ActiveForm::end(); ?>