<?php
    use yii\helpers\Html;
    use yii\widgets\ActiveForm;
?>
<?php $form = ActiveForm::begin(); ?>

<?= $form->field($model, 'name')->textInput() ?>
 
<?= $form->field($model, 'surname')->textInput() ?>
 
<?= $form->field($model, 'phone')->textInput() ?>
 
<?= $form->field($model, 'post')->textInput() ?>

<?= $form->field($model, 'status')->textInput() ?>

<?= $form->field($model, 'salary')->input('number') ?>

<div class="form-group">
    <?= Html::submitButton('Сохранить', ['class' => 'btn btn-success']) ?>
</div>
 
<?php ActiveForm::end(); ?>