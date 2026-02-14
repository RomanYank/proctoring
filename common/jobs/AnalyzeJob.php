<?php
namespace common\jobs;

use yii\base\BaseObject;
use yii\queue\JobInterface;
use GuzzleHttp\Client;
use backend\models\VideoFiles;
use Yii;

class AnalyzeJob extends BaseObject implements JobInterface
{
    public $videoPath;
    public $videoId;

    public function execute($queue)
    {
        $client = new Client();
        $url = 'http://127.0.0.1:8000/analyze/';

        try {
            $response = $client->request('POST', $url, [
                'multipart' => [
                    [
                        'name'     => 'video',
                        'contents' => fopen($this->videoPath, 'r'),
                        'filename' => $this->videoPath,
                    ],
                ],
            ]);

            $responseBody = $response->getBody()->getContents();
            $data = json_decode($responseBody, true);

            Yii::info('Analyze response: ' . $responseBody, 'analyze');

            if (isset($data['violations'])) {
                $video = VideoFiles::findOne($this->videoId);

                if ($video) {
                    $video->verify = 1;
                    $video->violations = json_encode($data['violations'], JSON_UNESCAPED_UNICODE);

                    if (!$video->save()) {
                        Yii::error('Ошибка сохранения видео: ' . json_encode($video->errors), 'analyze');
                    }
                }
            } else {
                Yii::error('Ответ от сервера не содержит violations: ' . $responseBody, 'analyze');
            }
        } catch (\Throwable $e) {
            Yii::error('Analyze job failed: ' . $e->getMessage(), 'analyze');
        }
    }
}
