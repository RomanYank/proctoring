<?php

namespace frontend\components;

use Yii;
use yii\base\Component;
use yii\base\Exception;

/**
 * VideoCompressor компонент для сжатия видео файлов
 * Использует ffmpeg для масштабирования и переккодирования видео
 */
class VideoCompressor extends Component
{
    /**
     * Целевое разрешение высоты видео
     */
    public $targetHeight = 480;
    
    /**
     * Целевое количество кадров в секунду
     */
    public $targetFps = 15;
    
    /**
     * Качество видео (0-51, меньше = лучше). По умолчанию 28
     */
    public $quality = 28;
    
    /**
     * Максимальный размер видео в МБ. Если видео больше, будет сжиматься больше
     */
    public $maxSizeMb = 50;

    /**
     * Проверяет наличие ffmpeg
     *
     * @return bool
     * @throws Exception
     */
    public function checkFfmpegAvailable()
    {
        $command = 'which ffmpeg';
        $output = shell_exec($command);
        
        if (empty($output)) {
            throw new Exception('ffmpeg не установлен на сервере');
        }
        
        return true;
    }

    /**
     * Получает информацию о видео файле
     *
     * @param string $videoPath путь к видео файлу
     * @return array информация о видео
     * @throws Exception
     */
    public function getVideoInfo($videoPath)
    {
        if (!file_exists($videoPath)) {
            throw new Exception("Видео файл не найден: {$videoPath}");
        }

        $cmd = sprintf(
            'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of default=noprint_wrappers=1 %s',
            escapeshellarg($videoPath)
        );

        $output = shell_exec($cmd);
        if (empty($output)) {
            throw new Exception("Не удалось получить информацию о видео");
        }

        preg_match('/width=(\d+)/', $output, $widthMatch);
        preg_match('/height=(\d+)/', $output, $heightMatch);
        preg_match('/r_frame_rate=(\d+)\/(\d+)/', $output, $fpsMatch);

        $width = $widthMatch[1] ?? 1280;
        $height = $heightMatch[1] ?? 720;
        $fps = !empty($fpsMatch) ? ($fpsMatch[1] / $fpsMatch[2]) : 30;
        $fileSize = filesize($videoPath) / (1024 * 1024);

        return [
            'width' => (int)$width,
            'height' => (int)$height,
            'fps' => (float)$fps,
            'size_mb' => round($fileSize, 2),
        ];
    }

    /**
     * Сжимает видео файл
     *
     * @param string $inputPath путь к исходному видео
     * @param string $outputPath путь для сохранения сжатого видео
     * @return array результат сжатия
     * @throws Exception
     */
    public function compress($inputPath, $outputPath)
    {
        $this->checkFfmpegAvailable();

        if (!file_exists($inputPath)) {
            throw new Exception("Входной видео файл не найден: {$inputPath}");
        }

        $videoInfo = $this->getVideoInfo($inputPath);
        $originalSize = $videoInfo['size_mb'];
        $originalWidth = $videoInfo['width'];
        $originalHeight = $videoInfo['height'];
        $originalFps = $videoInfo['fps'];

        $newHeight = min($originalHeight, $this->targetHeight);
        $newWidth = (int)(($newHeight / $originalHeight) * $originalWidth);

        $newWidth = ($newWidth % 2 === 0) ? $newWidth : $newWidth - 1;
        $newHeight = ($newHeight % 2 === 0) ? $newHeight : $newHeight - 1;

        $newFps = min((int)$originalFps, $this->targetFps);

        // Строим команду ffmpeg
        $cmd = sprintf(
            'ffmpeg -i %s -vf "scale=%d:%d" -r %d -c:v libx264 -crf %d -c:a aac -q:a 5 -y %s 2>&1',
            escapeshellarg($inputPath),
            $newWidth,
            $newHeight,
            $newFps,
            $this->quality,
            escapeshellarg($outputPath)
        );

        Yii::info("Сжатие видео: {$cmd}", __METHOD__);
        
        $output = shell_exec($cmd);
        
        if (!file_exists($outputPath) || filesize($outputPath) === 0) {
            Yii::error("Ошибка сжатия видео: {$output}", __METHOD__);
            throw new Exception("Не удалось сжать видео: " . (string)$output);
        }

        $compressedSize = filesize($outputPath) / (1024 * 1024);
        $compressionRatio = (1 - ($compressedSize / $originalSize)) * 100;

        return [
            'success' => true,
            'input_path' => $inputPath,
            'output_path' => $outputPath,
            'original_size_mb' => round($originalSize, 2),
            'compressed_size_mb' => round($compressedSize, 2),
            'compression_ratio' => round($compressionRatio, 1),
            'original_resolution' => "{$originalWidth}x{$originalHeight}",
            'compressed_resolution' => "{$newWidth}x{$newHeight}",
            'original_fps' => round($originalFps, 1),
            'compressed_fps' => $newFps,
        ];
    }

    /**
     * Сжимает видео в место с автоматическим именем
     *
     * @param string $inputPath путь к исходному видео
     * @param string $outputDir директория для сохранения
     * @return string путь к сжатому видео
     * @throws Exception
     */
    public function compressToDirectory($inputPath, $outputDir)
    {
        if (!is_dir($outputDir)) {
            mkdir($outputDir, 0777, true);
        }

        $fileName = pathinfo($inputPath, PATHINFO_FILENAME);
        $outputPath = $outputDir . DIRECTORY_SEPARATOR . 'compressed-' . $fileName . '.mp4';

        $this->compress($inputPath, $outputPath);

        return $outputPath;
    }
}
