<?php
use yii\helpers\Html;
use yii\helpers\Url;

$steps = [
    'Соглашение с правилами',
    'Проверка компьютера',
    'Прохождение экзамена',
    'Отправить'
];

$elements = [
    ['web-camera.svg', 'Подключение веб-камеры и микрофона'],
    ['camera.svg', 'Изображение с веб-камеры'],
    ['connections.svg', 'Сетевое соединение'],
    ['stream.svg', 'Трансляция веб-камеры и рабочего стола'],
];

$timeRecording = $model?->recording_time ?? 60;
?>
<div class="main-proctoring-row">
    <div class="row">
        <div class="container">
                <div class="title">Подготовка к экзамену</div>
                <div class="steps-container">
                    <?php foreach ($steps as $i => $step): ?>
                        <div class="step-name <?= $i === 0 ? 'active' : '' ?>">
                            <?= Html::encode($step) ?>
                            <?php if ($i < count($steps)-1): ?>
                                <span class="selector">></span>
                            <?php endif; ?>
                        </div>
                    <?php endforeach; ?>
                </div>
        </div>
    </div>
    <div class="content-step step-1 active">
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent a ante eu nisi tincidunt tincidunt vitae ac diam. In id ultricies mi, malesuada mattis nulla. Fusce dapibus maximus est, ac pellentesque massa consectetur quis. Proin non dignissim justo. Sed et condimentum tortor, a faucibus dolor. Nulla facilisi. Fusce eget velit eu ante aliquet lobortis. Maecenas eu arcu lorem.</p>

        <p>Sed ornare ante dui, eu bibendum lectus tempus eget. Vestibulum malesuada luctus ornare. Ut porta dolor vel neque tincidunt, a porttitor massa malesuada. Integer at mollis diam, sit amet varius orci. Duis et ante eget velit pretium varius sit amet sed metus. In placerat orci urna, ut aliquam tellus consequat a. Quisque sollicitudin lacus sit amet dolor tempus dictum. Nunc eros massa, aliquam eu pellentesque eu, convallis quis dolor. Mauris ut fermentum neque. Vivamus suscipit purus velit, et elementum turpis semper et. Vivamus tempor feugiat massa id ornare. Pellentesque facilisis sapien quis justo aliquam tempus. Ut vulputate dui sit amet nisl tristique, vel cursus est sodales.</p>

        <p>Vestibulum non augue quis enim congue dapibus. Phasellus at ipsum ac est bibendum convallis. In auctor interdum ex sit amet porta. Vestibulum finibus quam felis, sit amet elementum ante faucibus vitae. Fusce vitae lectus ipsum. Donec venenatis, massa nec consequat dignissim, erat nisi suscipit ex, eget pellentesque diam orci ut est. Curabitur dictum venenatis facilisis. Proin porttitor laoreet vehicula.</p>

        <p>Pellentesque sagittis mi felis, molestie ornare turpis blandit a. Sed pulvinar luctus leo. Quisque posuere velit ut purus egestas condimentum. Vivamus eget magna hendrerit, sagittis diam non, pretium arcu. Proin semper libero vitae molestie bibendum. Mauris lobortis placerat mauris, eu molestie arcu sollicitudin non. Donec in pharetra leo. Etiam porta, lacus id maximus laoreet, diam odio tempor felis, a bibendum lorem nisi non mi. Curabitur ultricies mi eget orci luctus varius. Vivamus nunc ipsum, tempor in augue interdum, ultricies rhoncus tortor. Integer maximus urna at tellus porttitor, vitae consectetur velit finibus. Curabitur eget ullamcorper libero, eu cursus enim. Donec consequat est dictum diam feugiat, ac facilisis nibh ornare. Nunc ut condimentum nisl. Nam non sollicitudin erat, et faucibus sem.</p>

        <p>Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Morbi ut tincidunt neque, eu posuere odio. Phasellus dignissim sagittis feugiat. Mauris condimentum eros vel nisl congue, in pulvinar tellus tincidunt. Donec pulvinar euismod elit nec dignissim. Etiam id felis ipsum. Etiam ultrices ante sit amet turpis fermentum, quis interdum ex dictum.</p>
        
        <div class="container-checkbox">
            <?= Html::checkbox('allow', false, [
                'id' => 'allow',
                'label' => 'Я согласен с правилами проведения онлайн тестирования'
            ]) ?>
        </div>

        <?= Html::button('Продолжить', [
            'class' => 'next-step btn btn-primary',
            'data' => ['change' => 2]
        ]) ?>

    </div>
    <div class="content-step step-2">
        <div class="proctoring-give-permission">
            <div class="proctoring-give-permission-elements">
                <?php foreach ($elements as $i => $el): ?>
                    <div class="proctoring-give-permission-element col-lg-3">
                        <div class="proctoring-give-permission-element-icon proctoring-element-<?= $i+1 ?>">
                            <?= Html::img("@web/img/{$el[0]}") ?>
                            <div class="proctoring-give-permission-element-loader"></div>
                        </div>
                        <div class="proctoring-give-permission-element-description">
                            <?= Html::encode($el[1]) ?>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>
    <div class="content-step step-3">
        <div class="container">
            <video id="video-capture" autoplay muted style="display:  none"   ></video>
            <video id="video" autoplay muted style="display:  none"></video>
            <video id="stream-content" autoplay muted style="display:  none"></video>
        </div>
    </div>
</div>
<script>
$(document).ready(function () {
    const video = $('#video')[0];
    const videoCapture = $('#video-capture')[0];
    const stream = $('#stream-content')[0];
    const uploadUrl = "<?= Url::to(['site/upload']) ?>";
    const saveVideoUrl = "<?= Url::to(['site/save-video']) ?>";

    const fileNameWebCamera = getFileName('WebCamera', 'webm');
    const fileNameCaptureScreen = getFileName('CaptureScreen', 'webm');
    const recordingTime = <?= $timeRecording; ?> * 1000;

    let blobWeb, blobCapture, blobScreen;
    let errorCamera = false, errorCapture = false, errorScreen = false;

    async function startRecording(deviceFn, videoElement) {
        try {
            const stream = await deviceFn();
            if (videoElement) {
                videoElement.srcObject = stream;
            }

            const recorder = RecordRTC(stream, { type: 'video' });
            recorder.startRecording();

            await new Promise(resolve => setTimeout(resolve, recordingTime));
            await new Promise(resolve => recorder.stopRecording(resolve));

            const blob = recorder.getBlob();

            stream.getTracks().forEach(track => track.stop());

            return { success: true, stream, recorder, blob };
        } catch (err) {
            console.error('Ошибка записи:', err);
            return { success: false };
        }
    }

    function getFileName(prefix, ext) {
        const d = new Date();
        return `${prefix}-${d.getUTCFullYear()}${d.getUTCMonth()}${d.getUTCDate()}-${getRandomString()}.${ext}`;
    }

    function getRandomString() {
        return (Math.random() * Date.now()).toString(36).replace(/\./g, '');
    }

    async function uploadBlob(blob, filename) {
        const file = new File([blob], filename, { type: 'video/webm' });
        const formData = new FormData();
        formData.append('video-blob', file);
        formData.append('video-filename', filename);

        const response = await $.ajax({
            url: uploadUrl,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
        });

        console.log(response == 'success' ? `Файл успешно отправлен: ${filename}` : response);
    }

    async function handleStep2() {
        setLoaderState(1, 'preloader');
        setLoaderState(2, 'preloader');
        setLoaderState(4, 'preloader');

        const [webResult, capResult, screenResult] = await Promise.all([
            startRecording(() => navigator.mediaDevices.getUserMedia({ audio: true, video: true }), video),
            startRecording(() => navigator.mediaDevices.getUserMedia({ video: true }), videoCapture),
            startRecording(() => navigator.mediaDevices.getDisplayMedia({ video: true }), stream),
        ]);

        errorCamera = !webResult.success;
        errorCapture = !capResult.success;
        errorScreen = !screenResult.success;

        if (webResult.success) blobWeb = webResult.blob;
        if (screenResult.success) blobScreen = screenResult.blob;

        if (capResult.success) blobCapture = capResult.blob;

        setLoaderState(1, errorCamera ? 'error' : 'active');
        setLoaderState(2, errorCapture ? 'error' : 'active');
        setLoaderState(4, (errorCapture || errorScreen) ? 'error' : 'active');

        $('.proctoring-give-permission .reset, .proctoring-give-permission .next-step').remove();
        $('.proctoring-give-permission').append(
            `<button class="${!errorCamera && !errorCapture && !errorScreen ? 'next-step' : 'reset'}" data-change="3">
                ${!errorCamera && !errorCapture && !errorScreen ? 'Продолжить' : 'Повторить проверку'}
            </button>`
        );
    }

    function setLoaderState(index, state) {
        $(`.proctoring-element-${index} .proctoring-give-permission-element-loader`)
            .removeClass('preloader active error')
            .addClass(state);
    }

    $(document).on('click', '.next-step', async function (e) {
        e.preventDefault();
        if (!$('input[name="allow"]').is(':checked')) {
            alert('Необходимо поставить галочку!');
            return;
        }

        const step = $(this).data('change');
        $('.step-name.active').removeClass('active').next().addClass('active');

        if (step === 2) {
            $('.step-1').removeClass('active');
            $('.step-2').addClass('active');
            await handleStep2();
        }

        $('.proctoring-give-permission').off('click').on('click', '.reset', handleStep2);

        $('.proctoring-give-permission').on('click', '.next-step', async function () {
            $('.step-2').removeClass('active');
            $('.step-3').addClass('active');

            if (blobWeb) await uploadBlob(blobWeb, fileNameWebCamera);
            if (blobScreen) await uploadBlob(blobScreen, fileNameCaptureScreen);

            $.post(saveVideoUrl, {
                web_camera_video: fileNameWebCamera,
                capture_screen_video: fileNameCaptureScreen
            }, console.log);
        });
    });
});
</script>