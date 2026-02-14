<?php
namespace common\jobs;

use yii\base\BaseObject;
use yii\queue\JobInterface;
use GuzzleHttp\Client;
use Yii;
#запуск таски php yii queue/run
class TrainJob extends BaseObject implements JobInterface
{
    public $csvPath;
    public $csvName;
    public $classDescPath;
    public $classDescName;
    public $epochs;

    public function execute($queue)
    {
        $client = new Client();
        $url = 'http://127.0.0.1:8000/train/';

        $postData = [
            [
                'name' => 'csv_file',
                'contents' => fopen($this->csvPath, 'r'),
                'filename' => $this->csvName
            ],
            [
                'name' => 'class_desc_file',
                'contents' => fopen($this->classDescPath, 'r'),
                'filename' => $this->classDescName
            ],
            [
                'name' => 'epochs',
                'contents' => $this->epochs
            ],
        ];

        $response = $client->request('POST', $url, [
            'multipart' => $postData,
        ]);

        Yii::info('Train response: ' . $response->getBody()->getContents(), 'train');
    }
}
