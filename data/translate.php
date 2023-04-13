<?php

use GuzzleHttp\Client;

// Đường dẫn đến file CSV cần dịch
$file = './en.csv';

$data = array_map('str_getcsv', file($file));

// Lấy danh sách các dòng trong file CSV (loại bỏ header)
$rows = array_slice($data, 1);

// Khai báo API key và đường dẫn đến API của Google Translate
$apiKey = 'API_KEY';
$apiEndpoint = 'https://translation.googleapis.com/language/translate/v2';

$client = new Client();

// Vòng lặp qua từng dòng trong file CSV để dịch cột
foreach ($rows as &$row) {
    // Lấy giá trị của cột cần dịch (cột thứ 0 trong code này)
    $text = $row[0];

    // Tạo request để gọi API của Google Translate
    $response = $client->post($apiEndpoint, [
        'query' => [
            'key' => $apiKey,
            'source' => 'en',
            'target' => 'vi',
            'q' => $text
        ]
    ]);

    // Lấy kết quả từ API và gán lại vào mảng dữ liệu
    $translatedText = json_decode($response->getBody()->getContents(), true)['data']['translations'][0]['translatedText'];
    $row[0] = $translatedText;
}

// Ghi lại nội dung mới đã được dịch sang file CSV
$handle = fopen($file, 'w');
foreach ($data as $row) {
    fputcsv($handle, $row);
}
fclose($handle);