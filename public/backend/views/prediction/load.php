<?php
use yii\widgets\ActiveForm;
use yii\helpers\Html;

$this->title = 'Загрузка модели';
?>

<h1><?= Html::encode($this->title) ?></h1>

<?php if (Yii::$app->session->hasFlash('loadModelResponse')): ?>
    <div class="alert alert-info"><?= Yii::$app->session->getFlash('loadModelResponse') ?></div>
<?php endif; ?>

<?php $form = ActiveForm::begin([
    'options' => ['enctype' => 'multipart/form-data']
]); ?>

<?= $form->field($model, 'modelFile')->fileInput() ?>

<div class="form-group" style="margin-top: 15px">
    <?= Html::submitButton('Загрузить модель', ['class' => 'btn btn-primary']) ?>
</div>

<?php ActiveForm::end(); ?>