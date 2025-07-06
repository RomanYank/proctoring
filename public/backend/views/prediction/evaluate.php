<?php
use yii\widgets\ActiveForm;
use yii\helpers\Html;

$this->title = 'Выполнить предсказание';
?>
<style>
table{
	border: 1px solid #eee;
	table-layout: fixed;
	width: 100%;
	margin-bottom: 20px;
}
table th {
	font-weight: bold;
	padding: 5px;
	background: #efefef;
	border: 1px solid #dddddd;
}
table td{
	padding: 5px 10px;
	border: 1px solid #eee;
	text-align: left;
}
table tbody tr:nth-child(odd){
	background: #fff;
}
table tbody tr:nth-child(even){
	background: #F7F7F7;
}
</style>
<h1><?= Html::encode($this->title) ?></h1>

<?php if (!empty($predictionTable)): ?>
    <h3>Результаты предсказания</h3>
    <?= $predictionTable ?>

    <h3>Аннотированное изображение</h3>
    <img src="data:image/png;base64,<?= $annotatedImage ?>" alt="Результат" style="margin-bottom: 20px; max-width: 100%; height: auto; width: 450px" />
<?php endif; ?>

<?php $form = ActiveForm::begin(['options' => ['enctype'=>'multipart/form-data']]); ?>

<?= $form->field($model, 'imageFile')->fileInput() ?>

<div class="form-group" style="margin-top: 15px">
    <?= Html::submitButton('Отправить', ['class' => 'btn btn-primary']) ?>
</div>

<?php ActiveForm::end(); ?>
