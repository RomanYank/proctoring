<?php

use yii\helpers\Html;
use yii\widgets\ActiveForm;

/** @var \yii\web\View $this */
/** @var \app\models\TrainForm $model */
$this->title = 'Дообучение модели';
$this->params['breadcrumbs'][] = $this->title;
?>
<style>
.upload-group .form-group {
    display: flex;
    flex-direction: column;
}
</style>
<div class="row user-form">
    <h1><?= Html::encode($this->title) ?></h1>

    <?php $form = ActiveForm::begin([
        'options' => ['enctype' => 'multipart/form-data']
    ]); ?>
    <div class="form-group upload-group" style="margin-top: 15px;">
        <?= $form->field($model, 'csvFile')->fileInput();?>
    </div>
    <div class="form-group upload-group" style="margin-top: 15px">
        <?= $form->field($model, 'classDescFile')->fileInput();?>
    </div>
    <div class="form-group" style="margin-top: 15px">
        <?= $form->field($model, 'epochs')->textInput();?>
    </div>

    <div class="form-group" style="margin-top: 15px">
        <?= Html::submitButton('Обучить', ['class' => 'btn btn-primary']) ?>
    </div>

    <?php ActiveForm::end(); ?>
</div>
