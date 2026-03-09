<?php

use yii\bootstrap5\Modal;
use yii\grid\GridView;
use yii\helpers\Html;
use yii\helpers\Url;

$this->title = 'Протоколы обучения';
$this->params['breadcrumbs'][] = $this->title;

$this->registerCss(<<<CSS
.proctoring-modal-wrap {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 16px;
}
.proctoring-violations {
    max-height: 72vh;
    overflow-y: auto;
    border-left: 1px solid #e5e5e5;
    padding-left: 12px;
}
.violation-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 10px;
    padding: 8px;
    cursor: pointer;
}
.violation-card:hover {
    border-color: #198754;
}
.violation-title {
    font-weight: 700;
    margin-bottom: 6px;
}
.violation-thumb {
    width: 100%;
    border-radius: 6px;
    border: 1px solid #e5e5e5;
}
.proctoring-summary {
    display: flex;
    gap: 10px;
    margin-bottom: 16px;
}
.summary-item {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 10px 12px;
    min-width: 160px;
}
.summary-item.filter-item {
    cursor: pointer;
}
.summary-item.filter-item.active {
    border-color: #198754;
    background: #eefaf3;
}
.summary-item .label {
    font-size: 12px;
    color: #666;
}
.summary-item .value {
    font-size: 20px;
    font-weight: 700;
}
CSS);
?>

<h1><?= Html::encode($this->title) ?></h1>

<?= GridView::widget([
    'dataProvider' => $dataProvider,
    'columns' => [
        'id',
        [
            'attribute' => 'user.full_name',
            'label' => 'Пользователь',
        ],
        [
            'attribute' => 'date',
            'label' => 'Дата записи',
        ],
        [
            'attribute' => 'verify',
            'label' => 'Статус проверки',
            'value' => static function ($model) {
                return $model->statusLabel();
            },
        ],
        [
            'label' => 'Веб-камера и нарушения',
            'format' => 'raw',
            'value' => static function ($model) {
                $violations = [];
                if (!empty($model->violations)) {
                    $decoded = json_decode($model->violations, true);
                    if (is_array($decoded)) {
                        $violations = $decoded;
                    }
                }

                $totalViolations = count($violations);
                $violationGroups = [];
                foreach ($violations as $v) {
                    $key = $v['violation'] ?? 'Unknown';
                    $violationGroups[$key] = ($violationGroups[$key] ?? 0) + 1;
                }
                $uniqueTypes = count($violationGroups);

                $modalId = 'proctoring-modal-' . $model->id;
                $videoId = 'webcam-video-' . $model->id;
                $screenId = 'screen-video-' . $model->id;
                $frontendHost = rtrim((string)\Yii::$app->request->hostInfo, '/');
                $frontendHost = preg_replace('#^http://admin\.localhost$#i', 'http://localhost', $frontendHost);
                $frontendHost = preg_replace('#^https://admin\.localhost$#i', 'https://localhost', $frontendHost);

                $cameraUrl = $frontendHost . '/record/video/' . ltrim((string)$model->web_camera_video, '/');
                $screenUrl = $frontendHost . '/record/video/' . ltrim((string)$model->capture_screen_video, '/');

                ob_start();

                Modal::begin([
                    'title' => 'Протокол записи №' . (int)$model->id,
                    'size' => Modal::SIZE_EXTRA_LARGE,
                    'options' => ['id' => $modalId],
                    'toggleButton' => [
                        'label' => 'Открыть протокол',
                        'class' => 'btn btn-outline-primary',
                    ],
                ]);

                echo '<div class="proctoring-summary">';
                echo '<div class="summary-item"><div class="label">Типов нарушений</div><div class="value">' . (int)$uniqueTypes . '</div></div>';
                echo '<div class="summary-item filter-item active" data-filter="all" data-modal="' . Html::encode($modalId) . '"><div class="label">Все логи</div><div class="value">' . (int)$totalViolations . '</div></div>';
                foreach ($violationGroups as $type => $count) {
                    echo '<div class="summary-item filter-item" data-filter="' . Html::encode($type) . '" data-modal="' . Html::encode($modalId) . '"><div class="label">' . Html::encode($type) . '</div><div class="value">' . (int)$count . '</div></div>';
                }
                echo '</div>';

                echo '<div class="proctoring-modal-wrap">';
                echo '<div>';
                echo Html::tag('h6', 'Видео с веб-камеры');
                echo Html::tag('video', '', [
                    'id' => $videoId,
                    'src' => $cameraUrl,
                    'controls' => true,
                    'style' => 'width:100%; margin-bottom: 16px;',
                ]);

                echo Html::tag('h6', 'Запись экрана');
                echo Html::tag('video', '', [
                    'id' => $screenId,
                    'src' => $screenUrl,
                    'controls' => true,
                    'style' => 'width:100%;',
                ]);
                echo '</div>';

                echo '<div class="proctoring-violations">';
                echo '<h6>Лог нарушений</h6>';

                if (!$violations) {
                    echo '<p>Нарушения не зафиксированы.</p>';
                } else {
                    foreach ($violations as $idx => $v) {
                        $time = $v['time'] ?? '00:00';
                        $violation = $v['violation'] ?? 'Unknown';
                        $imgLog = $v['img_log'] ?? '';

                        [$m, $s] = array_pad(explode(':', $time), 2, '0');
                        $seconds = ((int)$m) * 60 + (int)$s;

                        echo '<div class="violation-card jump-to-time" data-modal="' . Html::encode($modalId) . '" data-violation="' . Html::encode($violation) . '" data-video-id="' . Html::encode($videoId) . '" data-seconds="' . (int)$seconds . '">';
                        echo '<div class="violation-title">' . Html::encode(($idx + 1) . '. ' . $time . ' - ' . $violation) . '</div>';
                        if (!empty($imgLog)) {
                            echo '<img class="violation-thumb" alt="Violation screenshot" src="data:image/jpeg;base64,' . Html::encode($imgLog) . '">';
                        } else {
                            echo '<div class="text-muted">Скриншот отсутствует</div>';
                        }
                        echo '</div>';
                    }
                }

                echo '</div>';
                echo '</div>';

                Modal::end();

                return ob_get_clean();
            },
        ],
    ],
]); ?>

<?php
$this->registerJs(<<<JS
    $(document).on('click', '.jump-to-time', function () {
        var videoId = $(this).data('video-id');
        var seconds = parseInt($(this).data('seconds'), 10) || 0;
        var video = document.getElementById(videoId);
        if (!video) {
            return;
        }
        video.currentTime = seconds;
        video.play();
    });

    $(document).on('click', '.filter-item', function () {
        var modalId = $(this).data('modal');
        var filter = $(this).data('filter');
        var modal = $('#' + modalId);

        modal.find('.filter-item').removeClass('active');
        $(this).addClass('active');

        modal.find('.violation-card').each(function () {
            var type = $(this).data('violation');
            if (filter === 'all' || type === filter) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
JS);
?>
