<?php

use yii\grid\GridView;
use yii\helpers\Html;
use yii\bootstrap5\Modal;
$this->title = 'Протоколы обучения';
$this->params['breadcrumbs'][] = $this->title;
?>
<style>
.modal-body {
    display: flex;
    justify-content: space-between;
}
.modal-body video {
    max-width: 70%;
}
.modal-body .violations-box {
    width: 25%;
    max-height:580px; 
    overflow-y:auto;
}
</style>
<h1><?= Html::encode($this->title) ?></h1>
<?= GridView::widget([
    'dataProvider' => $dataProvider,
    'columns' => [
        'id',
        [
            'attribute' => 'user.full_name',
            'label' => 'ФИО',
        ],
        [
            'label' => 'Видео с веб-камеры',
            'format' => 'raw',
            'value' => function ($model) {
                $violationsJson = $model->violations;
                $uniqueViolations = [];
                if(!empty($violationsJson)) {
                    $violations = json_decode($violationsJson, true);
            
                    foreach ($violations as $v) {
                        $key = $v['time'] . ' - ' . $v['violation'];
                        $uniqueViolations[$key] = $v;
                    }
                }
                ob_start();
        
                Modal::begin([
                    'title' => '<div class="title-modal">Видео с веб-камеры</div>',
                    'size' => Modal::SIZE_EXTRA_LARGE,
                    'toggleButton' => [
                        'label' => '<svg xmlns="http://www.w3.org/2000/svg" width="25px" height="25px" viewBox="0 0 1024 1024"><path fill="#000000" d="M512 160c320 0 512 352 512 352S832 864 512 864 0 512 0 512s192-352 512-352zm0 64c-225.28 0-384.128 208.064-436.8 288 52.608 79.872 211.456 288 436.8 288 225.28 0 384.128-208.064 436.8-288-52.608-79.872-211.456-288-436.8-288zm0 64a224 224 0 1 1 0 448 224 224 0 0 1 0-448zm0 64a160.192 160.192 0 0 0-160 160c0 88.192 71.744 160 160 160s160-71.808 160-160-71.744-160-160-160z"/></svg>',
                        'tag' => 'button',
                        'class' => 'btn btn-click-video-modal',
                    ],
                    'options' => ['id' => 'modal-video-' . $model->id]
                ]);
        
                echo Html::tag('video', '', [
                    'src' => '/public/frontend/web/record/video/' . $model['web_camera_video'],
                    'controls' => true,
                    'style' => 'width:100%;',
                    'id' => 'video-' . $model->id,
                ]);
        
                echo '<div class="violations-box"> 
                        <h3>Список зафиксированных нарушений</h3>
                        <ul style="list-style:none; padding:0;">';
                foreach ($uniqueViolations as $uv) {
                    list($m, $s) = explode(':', $uv['time']);
                    $seconds = ((int)$m) * 60 + ((int)$s);
        
                    echo '<li style="cursor:pointer; padding:5px 0; border-bottom:1px solid #ddd;" ' .
                        'class="violation-item" ' .
                        'data-video-id="video-' . $model->id . '" ' .
                        'data-time="' . $seconds . '">' .
                        htmlspecialchars($uv['time'] . ' - ' . $uv['violation']) .
                        '</li>';
                }
                echo '</ul>';
                echo '</div>';
        
                Modal::end();
        
                $js = <<<JS
                $(document).on('click', '.violation-item', function() {
                    var video = document.getElementById($(this).data('video-id'));
                    if (video) {
                        video.currentTime = $(this).data('time');
                        video.play();
                    }
                });
                JS;
        
                \yii\web\YiiAsset::register(Yii::$app->view);
                Yii::$app->view->registerJs($js);
        
                return ob_get_clean();
            }
        ],
        [
            'label' => 'Демонстрация экрана',
            'format' => 'raw',
            'value' => function ($model) {
                ob_start();
                Modal::begin([
                    'title' => '<div class="title-modal">Демонстрация экрана</div>',
                    'size' => 'modal-xl',
                    'toggleButton' => [
                        'label' => '<svg xmlns="http://www.w3.org/2000/svg" width="25px" height="25px" viewBox="0 0 1024 1024"><path fill="#000000" d="M512 160c320 0 512 352 512 352S832 864 512 864 0 512 0 512s192-352 512-352zm0 64c-225.28 0-384.128 208.064-436.8 288 52.608 79.872 211.456 288 436.8 288 225.28 0 384.128-208.064 436.8-288-52.608-79.872-211.456-288-436.8-288zm0 64a224 224 0 1 1 0 448 224 224 0 0 1 0-448zm0 64a160.192 160.192 0 0 0-160 160c0 88.192 71.744 160 160 160s160-71.808 160-160-71.744-160-160-160z"/></svg>',
                        'tag' => 'button',
                        'class' => 'btn btn-click-video-modal',
                    ],
                ]);
                echo Html::tag('video', '', [
                    'src' => '/public/frontend/web/record/video/' . $model['capture_screen_video'],
                    'controls' => true,
                    'style' => 'width:100%;'
                ]);
                Modal::end();
                return ob_get_clean();
            }
        ],
        [
            'attribute' => 'date',
            'label' => 'Дата',
        ],
        [
            'attribute' => 'verify',
            'label' => 'Статус проверки',
            'value' => function($model) {
                return $model->statusLabel();
            }
        ]
    ],
]); ?>
