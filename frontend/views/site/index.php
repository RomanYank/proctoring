<?php

use yii\helpers\Html;
use yii\helpers\Url;

$steps = [
    'Согласие',
    'Проверка оборудования',
    'Тестирование',
    'Завершение',
];

$checks = [
    ['id' => 'cam-mic', 'icon' => 'web-camera.svg', 'title' => 'Камера и микрофон'],
    ['id' => 'camera', 'icon' => 'camera.svg', 'title' => 'Видео с веб-камеры'],
    ['id' => 'network', 'icon' => 'connections.svg', 'title' => 'Сетевое соединение'],
    ['id' => 'screen', 'icon' => 'stream.svg', 'title' => 'Доступ к экрану'],
];

$questions = [
    [
        'id' => 'q1',
        'question' => 'Какой HTTP-код обычно возвращает сервер при успешном GET-запросе?',
        'options' => ['200', '404', '500', '302'],
        'answer' => 0,
    ],
    [
        'id' => 'q2',
        'question' => 'Что из перечисленного относится к реляционным СУБД?',
        'options' => ['Redis', 'PostgreSQL', 'MongoDB', 'Elasticsearch'],
        'answer' => 1,
    ],
    [
        'id' => 'q3',
        'question' => 'Какая команда Git создает новый коммит?',
        'options' => ['git pull', 'git push', 'git commit', 'git clone'],
        'answer' => 2,
    ],
    [
        'id' => 'q4',
        'question' => 'Какой протокол используется для защищенной передачи данных в браузере?',
        'options' => ['HTTP', 'FTP', 'HTTPS', 'SMTP'],
        'answer' => 2,
    ],
    [
        'id' => 'q5',
        'question' => 'Что из списка является JavaScript-фреймворком?',
        'options' => ['Laravel', 'Django', 'React', 'Spring'],
        'answer' => 2,
    ],
    [
        'id' => 'q6',
        'question' => 'Какой оператор SQL используется для выборки данных?',
        'options' => ['INSERT', 'SELECT', 'UPDATE', 'DELETE'],
        'answer' => 1,
    ],
    [
        'id' => 'q7',
        'question' => 'Какой формат чаще всего используется для REST API?',
        'options' => ['XML', 'CSV', 'JSON', 'YAML'],
        'answer' => 2,
    ],
    [
        'id' => 'q8',
        'question' => 'Что делает команда `docker compose up`?',
        'options' => ['Удаляет контейнеры', 'Поднимает сервисы из compose-файла', 'Строит только образы', 'Очищает volume'],
        'answer' => 1,
    ],
];

$timeRecording = (int)($model?->recording_time ?? 180);
if ($timeRecording < 60) {
    $timeRecording = 60;
}
?>

<div class="main-proctoring-row" id="proctoring-app">
    <div class="row">
        <div class="container">
            <div class="title">Подготовка к онлайн-тестированию</div>
            <div class="steps-container">
                <?php foreach ($steps as $i => $step): ?>
                    <div class="step-name<?= $i === 0 ? ' active' : '' ?>">
                        <?= Html::encode($step) ?>
                        <?php if ($i < count($steps) - 1): ?>
                            <span class="selector">&gt;</span>
                        <?php endif; ?>
                    </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>

    <div class="content-step step-1 active">
        <h3>Правила прохождения</h3>
        <p>Перед началом убедитесь, что находитесь в тихом помещении и в кадре только вы.</p>
        <p>Во время теста не переключайтесь между вкладками, не выключайте камеру и не закрывайте демонстрацию экрана.</p>
        <p>После проверки оборудования запись видео начнется только по кнопке «Продолжить».</p>

        <div class="container-checkbox">
            <?= Html::checkbox('allow', false, [
                'id' => 'allow',
                'label' => 'Я согласен с правилами прохождения онлайн-тестирования',
            ]) ?>
        </div>

        <button class="next-step btn btn-primary" id="go-to-checks">Продолжить</button>
    </div>

    <div class="content-step step-2">
        <h3>Проверка оборудования</h3>
        <p>Сейчас система проверит доступ к устройствам.</p>

        <div class="proctoring-give-permission-elements">
            <?php foreach ($checks as $check): ?>
                <div class="proctoring-give-permission-element col-lg-3" data-check="<?= Html::encode($check['id']) ?>">
                    <div class="proctoring-give-permission-element-icon">
                        <?= Html::img("@web/img/{$check['icon']}") ?>
                        <div class="proctoring-give-permission-element-loader"></div>
                    </div>
                    <div class="proctoring-give-permission-element-description">
                        <?= Html::encode($check['title']) ?>
                    </div>
                    <div class="check-status">Ожидание</div>
                </div>
            <?php endforeach; ?>
        </div>

        <div class="check-actions">
            <button class="btn btn-outline-secondary" id="retry-checks">Повторить проверку</button>
            <button class="btn btn-primary" id="start-exam" disabled>Продолжить</button>
        </div>
    </div>

    <div class="content-step step-3">
        <div class="exam-header">
            <h3>Тестирование</h3>
            <div id="exam-timer" class="exam-timer">--:--</div>
        </div>

        <p id="screen-permission-note" class="exam-note">Ожидаем разрешение на демонстрацию экрана. После подтверждения запустится таймер и откроются вопросы.</p>

        <div id="exam-content" class="exam-layout" style="display: none;">
            <div class="exam-video-preview">
                <div>
                    <label>Веб-камера</label>
                    <video id="webcam-preview" autoplay muted playsinline></video>
                </div>
                <div>
                    <label>Экран</label>
                    <video id="screen-preview" autoplay muted playsinline></video>
                </div>
            </div>

            <form id="exam-form" class="exam-questions">
                <div id="question-progress" class="question-progress"></div>
                <?php foreach ($questions as $idx => $q): ?>
                    <fieldset class="question-block" data-answer="<?= (int)$q['answer'] ?>" data-index="<?= (int)$idx ?>">
                        <legend><?= ($idx + 1) . '. ' . Html::encode($q['question']) ?></legend>
                        <?php foreach ($q['options'] as $optIdx => $opt): ?>
                            <label>
                                <input type="radio" name="<?= Html::encode($q['id']) ?>" value="<?= (int)$optIdx ?>">
                                <?= Html::encode($opt) ?>
                            </label>
                        <?php endforeach; ?>
                    </fieldset>
                <?php endforeach; ?>

                <button type="submit" class="btn btn-success" id="finish-exam-btn" style="display:none;">Завершить и отправить</button>
            </form>
        </div>
    </div>

    <div class="content-step step-4">
        <div class="exam-result-box">
            <h3>Тест завершен</h3>
            <p id="exam-result-score"></p>
            <p id="exam-result-upload"></p>
            <a class="btn btn-primary" href="<?= Url::to(['site/index']) ?>">Начать заново</a>
        </div>
    </div>
</div>

<script>
$(function() {
    var uploadUrl = "<?= Url::to(['site/upload']) ?>";
    var saveVideoUrl = "<?= Url::to(['site/save-video']) ?>";
    var recordingSeconds = <?= (int)$timeRecording ?>;

    var $app = $('#proctoring-app');
    var $stepNames = $app.find('.step-name');
    var $stepBlocks = $app.find('.content-step');
    var $allowCheckbox = $('#allow');

    var $retryChecksButton = $('#retry-checks');
    var $startExamButton = $('#start-exam');
    var $goToChecksButton = $('#go-to-checks');

    var webcamPreview = $('#webcam-preview')[0];
    var screenPreview = $('#screen-preview')[0];
    var $examForm = $('#exam-form');
    var examForm = $examForm[0];
    var $examTimer = $('#exam-timer');
    var $examContent = $('#exam-content');
    var $screenPermissionNote = $('#screen-permission-note');
    var $questionProgress = $('#question-progress');
    var $finishExamButton = $('#finish-exam-btn');
    var $resultScore = $('#exam-result-score');
    var $resultUpload = $('#exam-result-upload');
    var questionBlocks = $.makeArray($examForm.find('.question-block'));

    var webcamStream = null;
    var screenStream = null;
    var webcamRecorder = null;
    var screenRecorder = null;
    var webcamChunks = [];
    var screenChunks = [];
    var recordingStopped = false;
    var examInterval = null;
    var secondsLeft = recordingSeconds;
    var currentQuestionIndex = 0;

    function switchStep(stepNumber) {
        $stepNames.each(function(idx) {
            $(this).toggleClass('active', idx === stepNumber - 1);
        });
        $stepBlocks.each(function(idx) {
            $(this).toggleClass('active', idx === stepNumber - 1);
        });
    }

    function setCheckState(checkId, state, text) {
        var $root = $app.find('[data-check="' + checkId + '"]');
        if (!$root.length) {
            return;
        }
        var $loader = $root.find('.proctoring-give-permission-element-loader');
        var $status = $root.find('.check-status');

        $loader.removeClass('preloader active error');
        if (state) {
            $loader.addClass(state);
        }
        $status.text(text);
    }

    function stopTracks(stream) {
        if (!stream) {
            return;
        }
        stream.getTracks().forEach(function(track) {
            track.stop();
        });
    }

    async function runPreChecks() {
        $startExamButton.prop('disabled', true);
        ['cam-mic', 'camera', 'network', 'screen'].forEach(function(check) {
            setCheckState(check, 'preloader', 'Проверка...');
        });

        var camMicOk = false;
        var cameraOk = false;
        var networkOk = false;
        var screenOk = false;
        var tempCamMic = null;
        var tempCamera = null;
        var tempScreen = null;

        try {
            tempCamMic = await navigator.mediaDevices.getUserMedia({video: true, audio: true});
            camMicOk = true;
            setCheckState('cam-mic', 'active', 'Доступ разрешен');
        } catch (e) {
            setCheckState('cam-mic', 'error', 'Нет доступа');
        }

        try {
            tempCamera = await navigator.mediaDevices.getUserMedia({video: true});
            cameraOk = true;
            setCheckState('camera', 'active', 'Видео доступно');
        } catch (e) {
            setCheckState('camera', 'error', 'Камера недоступна');
        }

        networkOk = navigator.onLine;
        setCheckState('network', networkOk ? 'active' : 'error', networkOk ? 'Подключено' : 'Нет сети');

        try {
            tempScreen = await navigator.mediaDevices.getDisplayMedia({video: true});
            screenOk = true;
            setCheckState('screen', 'active', 'Доступ разрешен');
        } catch (e) {
            setCheckState('screen', 'error', 'Нет доступа');
        }

        stopTracks(tempCamMic);
        stopTracks(tempCamera);
        stopTracks(tempScreen);

        var allPassed = camMicOk && cameraOk && networkOk && screenOk;
        $startExamButton.prop('disabled', !allPassed);
        return allPassed;
    }

    function getSupportedMimeType() {
        var mimeTypes = [
            'video/webm;codecs=vp9,opus',
            'video/webm;codecs=vp8,opus',
            'video/webm',
        ];
        var result = '';
        mimeTypes.some(function(type) {
            if (MediaRecorder.isTypeSupported(type)) {
                result = type;
                return true;
            }
        });
        return result;
    }

    function createRecorder(stream, onData) {
        var mimeType = getSupportedMimeType();
        var options = mimeType ? {mimeType: mimeType} : {};
        var recorder = new MediaRecorder(stream, options);
        recorder.ondataavailable = function(event) {
            if (event.data && event.data.size > 0) {
                onData(event.data);
            }
        };
        return recorder;
    }

    function getFileName(prefix, ext) {
        var d = new Date();
        var stamp = '' + d.getUTCFullYear() + String(d.getUTCMonth() + 1).padStart(2, '0') + String(d.getUTCDate()).padStart(2, '0') + String(d.getUTCHours()).padStart(2, '0') + String(d.getUTCMinutes()).padStart(2, '0') + String(d.getUTCSeconds()).padStart(2, '0');
        var rand = Math.random().toString(36).slice(2, 10);
        return prefix + '-' + stamp + '-' + rand + '.' + ext;
    }

    async function uploadBlob(blob, filename) {
        var file = new File([blob], filename, {type: 'video/webm'});
        var formData = new FormData();
        formData.append('video-blob', file);
        formData.append('video-filename', filename);

        await $.ajax({
            url: uploadUrl,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
        });
    }

    function updateTimer() {
        var mm = String(Math.floor(secondsLeft / 60)).padStart(2, '0');
        var ss = String(secondsLeft % 60).padStart(2, '0');
        $examTimer.text(mm + ':' + ss);
    }

    function startTimer() {
        secondsLeft = recordingSeconds;
        updateTimer();
        examInterval = setInterval(function() {
            secondsLeft -= 1;
            updateTimer();
            if (secondsLeft <= 0) {
                clearInterval(examInterval);
                examForm.requestSubmit();
            }
        }, 1000);
    }

    function stopTimer() {
        if (examInterval) {
            clearInterval(examInterval);
            examInterval = null;
        }
    }

    function renderQuestionStep() {
        questionBlocks.forEach(function(block, idx) {
            $(block).toggle(idx === currentQuestionIndex);
        });
        $questionProgress.text('Вопрос ' + (currentQuestionIndex + 1) + ' из ' + questionBlocks.length);
        $finishExamButton.toggle(currentQuestionIndex === questionBlocks.length - 1);
    }

    function resetQuestionFlow() {
        currentQuestionIndex = 0;
        renderQuestionStep();
    }

    async function startExamRecording() {
        try {
            screenStream = await navigator.mediaDevices.getDisplayMedia({video: true});
            webcamStream = await navigator.mediaDevices.getUserMedia({video: true, audio: true});
        } catch (error) {
            stopTracks(screenStream);
            stopTracks(webcamStream);
            screenStream = null;
            webcamStream = null;
            throw error;
        }

        webcamPreview.srcObject = webcamStream;
        screenPreview.srcObject = screenStream;

        webcamRecorder = createRecorder(webcamStream, function(chunk) {
            webcamChunks.push(chunk);
        });
        screenRecorder = createRecorder(screenStream, function(chunk) {
            screenChunks.push(chunk);
        });

        webcamRecorder.start(1000);
        screenRecorder.start(1000);

        $screenPermissionNote.hide();
        $examContent.css('display', 'flex');
        startTimer();
    }

    async function stopRecorders() {
        if (recordingStopped) {
            return;
        }
        recordingStopped = true;
        stopTimer();

        var stopOne = function(recorder) {
            return new Promise(function(resolve) {
                if (!recorder || recorder.state === 'inactive') {
                    resolve();
                    return;
                }
                recorder.onstop = resolve;
                recorder.stop();
            });
        };

        await Promise.all([stopOne(webcamRecorder), stopOne(screenRecorder)]);
        stopTracks(webcamStream);
        stopTracks(screenStream);
    }

    function calculateResult() {
        var correct = 0;
        $examForm.find('.question-block').each(function() {
            var rightAnswer = $(this).data('answer');
            var selected = $(this).find('input[type="radio"]:checked');
            if (selected.length && selected.val() == rightAnswer) {
                correct += 1;
            }
        });
        return {correct: correct, total: questionBlocks.length};
    }

    async function finalizeExam() {
        await stopRecorders();

        var webBlob = new Blob(webcamChunks, {type: 'video/webm'});
        var screenBlob = new Blob(screenChunks, {type: 'video/webm'});
        var webFileName = getFileName('WebCamera', 'webm');
        var screenFileName = getFileName('CaptureScreen', 'webm');

        await uploadBlob(webBlob, webFileName);
        await uploadBlob(screenBlob, screenFileName);

        var saveResponse = await $.ajax({
            url: saveVideoUrl,
            type: 'POST',
            dataType: 'json',
            data: {
                web_camera_video: webFileName,
                capture_screen_video: screenFileName,
            },
        });

        if (!saveResponse || !saveResponse.response) {
            throw new Error('Не удалось сохранить запись в базе.');
        }
    }

    $goToChecksButton.on('click', function(e) {
        e.preventDefault();
        if (!$allowCheckbox.is(':checked')) {
            alert('Необходимо принять правила.');
            return;
        }
        switchStep(2);
        runPreChecks();
    });

    $retryChecksButton.on('click', function() {
        runPreChecks();
    });

    $startExamButton.on('click', async function() {
        try {
            recordingStopped = false;
            webcamChunks = [];
            screenChunks = [];
            switchStep(3);
            $examContent.hide();
            $screenPermissionNote.show().text('Подтвердите демонстрацию экрана в системном окне браузера.');
            $examTimer.text('--:--');
            resetQuestionFlow();
            await startExamRecording();
        } catch (e) {
            alert('Не удалось запустить запись. Проверьте разрешения камеры и экрана.');
            switchStep(2);
            runPreChecks();
        }
    });

    $examForm.on('change', 'input[type="radio"]', function() {
        if (currentQuestionIndex < questionBlocks.length - 1) {
            currentQuestionIndex += 1;
            renderQuestionStep();
        }
    });

    $examForm.on('submit', async function(e) {
        e.preventDefault();
        $finishExamButton.prop('disabled', true);
        var result = calculateResult();
        $resultScore.text('Результат теста: ' + result.correct + ' из ' + result.total + '.');
        $resultUpload.text('Идет сохранение записей...');

        try {
            await finalizeExam();
            $resultUpload.text('Записи камеры и экрана успешно сохранены.');
        } catch (error) {
            $resultUpload.text('Ошибка сохранения: ' + error.message);
        }

        switchStep(4);
    });
});
</script>
