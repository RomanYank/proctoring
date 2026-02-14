/*$(document).ready(function() {
    var video = $('#video')[0];
    var video_capture = $('#video-capture')[0];
    var stream = $('#stream-content');
    var recorder_web;
    var recorder_caputre;
    var recorder_screen;
    var error_camera = false;
    var error_capture = false;
    var error_screen = false;
    var fileNameWebCaemra = getFileNameWebCamera('webm');
    var fileNameCaptureScreen = getFileNameCaptureScreen('webm');
    var recordingTime;


    function webCamera(callback) {
        navigator.mediaDevices.getUserMedia({ audio: true, video: true }).then(function(camera) {
            video.srcObject = camera;

            recorder_web = RecordRTC(camera, { type: 'video'});

            recorder_web.startRecording();
                 setTimeout(function() {
                    recorder_web.stopRecording(function(){
                        var blob = recorder_web.getBlob();
                        var fileObject = new File([blob], fileNameWebCaemra, {
                            type: 'video/webm'
                        });
                        var formData = new FormData();
                        formData.append('video-blob', fileObject);
                        formData.append('video-filename', fileObject.name);
                        var upload_url = '/frontend/web/record/save.php';
                        $.ajax({
                            url: upload_url,
                            data: formData,
                            cache: false,
                            contentType: false,
                            processData: false,
                            type: 'POST',
                            success: function(response) {
                                if (response === 'success') {
                                    console.log('Файл WebCamera успешно отправлен', fileNameWebCaemra);
                                } else {
                                    console.log(response);
                                }
                            }
                        });
                        video.srcObject.getTracks().forEach(function(track) {
                            track.stop();
                        });
                    })
                }, recordingTime);
            callback(null,  camera);

        }).catch(function(error) {
            console.log('Ошибка подключения камеры или микрофона', error);
            error_camera = true;
            callback(error_camera, null)
        });
    }

    function captureCamera(callback) {
        navigator.mediaDevices.getUserMedia({video: true }).then(function(capture_camera) {
            video_capture.srcObject = capture_camera;
            recorder_caputre = RecordRTC(capture_camera, {type: 'video'});
            recorder_caputre.startRecording();
            callback(null, capture_camera);
        }).catch(function(error) {
            console.log('Ошибка камеры', error);
            error_capture = true
            callback(error, null)
        });
    }

    function captureScreen(callback) {
        navigator.mediaDevices.getDisplayMedia({video: true}).then(function(screen) {
            stream.srcObject = screen;
            recorder_screen = RecordRTC(screen, {type: 'video'});
            recorder_screen.startRecording();
                setTimeout(function() {
                    recorder_screen.stopRecording(function(){
                        var blob = recorder_screen.getBlob();
                        var fileObject = new File([blob], fileNameCaptureScreen, {
                            type: 'video/webm'
                        });
                        var formData = new FormData();
                        formData.append('video-blob', fileObject);
                        formData.append('video-filename', fileObject.name);
                        var upload_url = '/frontend/web/record/save.php';

                        $.ajax({
                            url: upload_url,
                            data: formData,
                            cache: false,
                            contentType: false,
                            processData: false,
                            type: 'POST',
                            success: function(response) {
                                if (response === 'success') {
                                    console.log('Файл captureScreen успешно отправлен', fileNameCaptureScreen);
                                } else {
                                    console.log(response);
                                }
                            }
                        });
                        stream.srcObject.getTracks().forEach(function(track) {
                            track.stop();
                        });
                    })
                }, recordingTime);
            callback(null, screen);
        }).catch(function(error) {
            console.log('Ошибка демонстрации экрана', error);
            error_screen = true;
            callback(error, null)
        });
    }

    function getFileNameWebCamera(fileExtension) {
        var d = new Date();
        var year = d.getUTCFullYear();
        var month = d.getUTCMonth();
        var date = d.getUTCDate();
        return 'WebCamera-' + year + month + date + '-' + getRandomString() + '.' + fileExtension;
    }

    function getFileNameCaptureScreen(fileExtension) {
        var d = new Date();
        var year = d.getUTCFullYear();
        var month = d.getUTCMonth();
        var date = d.getUTCDate();
        return 'CaptureScreen-' + year + month + date + '-' + getRandomString() + '.' + fileExtension;
    }

    function getRandomString() {
        if (window.crypto && window.crypto.getRandomValues && navigator.userAgent.indexOf('Safari') === -1) {
            var a = window.crypto.getRandomValues(new Uint32Array(3)),
                token = '';
            for (var i = 0, l = a.length; i < l; i++) {
                token += a[i].toString(36);
            }
            return token;
        } else {
            return (Math.random() * new Date().getTime()).toString(36).replace(/\./g, '');
        }
    }


    $('.next-step').on('click', function(e){
        e.preventDefault();
        if(!$('input[name="allow"]').is(':checked')){
            alert('Необходимо поставить галочку!');
            return;
        }
        var change_step = $(this).data('change');
        $('.step-name.active').removeClass('active').next().addClass('active');
        if (change_step === 2){
            $('.step-1').removeClass('active');
            $('.step-2').addClass('active');

            $('.prcotroing-give-permission-element-loader').addClass('preloader');

            webCamera(function(error, camera){
                if(error_camera) {
                    $('.proctoring-element-1 .prcotroing-give-permission-element-loader').removeClass('preloader').addClass('error');
                } else {
                    $('.proctoring-element-1 .prcotroing-give-permission-element-loader').removeClass('preloader').addClass('active');
                }
            });

            captureCamera(function(error, capture_camera) {
                if(error_capture){
                    $('.proctoring-element-2 .prcotroing-give-permission-element-loader').removeClass('preloader').addClass('error');
                } else {
                    $('.proctoring-element-2 .prcotroing-give-permission-element-loader').removeClass('preloader').addClass('active');
                }
                captureScreen(function(error, screen) {
                    if(error_capture || error_screen) {
                        $('.proctoring-element-4 .prcotroing-give-permission-element-loader').removeClass('preloader').addClass('error');
                    } else {
                        $('.proctoring-element-4 .prcotroing-give-permission-element-loader').removeClass('preloader').addClass('active');
                    }
                    if(!error_camera && !error_capture && !error_screen) {
                        $('.prcotroing-give-permission').append('<button class="next-step" data-change="3">Продолжить</button>');
                     } else {
                         $('.prcotroing-give-permission').append('<button class="reset">Повторить проверку</button>');
                    }
                });
            });


            $('.prcotroing-give-permission').on('click', '.reset', function() {
                error_camera = false;
                error_capture = false;
                error_screen = false;

                $('.prcotroing-give-permission .reset').remove();
                $('.proctoring-element-1  .prcotroing-give-permission-element-loader, .proctoring-element-2  .prcotroing-give-permission-element-loader, .proctoring-element-4  .prcotroing-give-permission-element-loader').removeClass('active').removeClass('error').addClass('preloader');

                webCamera(function(error, camera){
                    if(error_camera) {
                        $('.proctoring-element-1 .prcotroing-give-permission-element-loader').removeClass('preloader').addClass('error');
                    } else {
                        $('.proctoring-element-1 .prcotroing-give-permission-element-loader').removeClass('preloader').addClass('active');
                    }
                });

                captureCamera(function(error, capture_camera) {
                    if(error_capture){
                        $('.proctoring-element-2 .prcotroing-give-permission-element-loader').removeClass('preloader').addClass('error');
                    } else {
                        $('.proctoring-element-2 .prcotroing-give-permission-element-loader').removeClass('preloader').addClass('active');
                    }

                    captureScreen(function(error, screen) {
                        if(error_capture || error_screen) {
                            $('.proctoring-element-4 .prcotroing-give-permission-element-loader').removeClass('preloader').addClass('error');
                        } else {
                            $('.proctoring-element-4 .prcotroing-give-permission-element-loader').removeClass('preloader').addClass('active');
                        }
                        if(!error_camera && !error_capture && !error_screen) {
                            $('.prcotroing-give-permission').append('<button class="next-step" data-change="3">Продолжить</button>');
                        } else {
                            $('.prcotroing-give-permission').append('<button class="reset">Повторить проверку</button>');
                        }
                    });
                });
            });

            $('.prcotroing-give-permission').on('click', '.next-step', function() {
                var change_step = $(this).data('change');
                $('.step-name.active').removeClass('active').next().addClass('active');
                if (change_step === 3) {
                    $('.step-2').removeClass('active');
                    $('.step-3').addClass('active');
                    var formData = {
                        web_camera_video: fileNameWebCaemra,
                        capture_screen_video: fileNameCaptureScreen
                    }
                    setTimeout(
                        function() {
                            $.ajax({
                                url: '/frontend/web/site/save-video',
                                type: 'POST',
                                data: formData,
                                success: function(response) {
                                    console.log(response);
                                }
                            });
                        }, recordingTime
                    );

                }
            });
        };
    });
});*/