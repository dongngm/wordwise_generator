<?php

chdir('..');

$bookfile = $argv[1];
$bookfilename = pathinfo($bookfile, PATHINFO_FILENAME);
if (!file_exists($bookfilename)) {
	mkdir($bookfilename, 0777, true);
}
$bookpath = realpath('./' . $bookfilename);
$hint_level = $argv[2];
$langww = $argv[3];

echo "[+] File cần tạo: $bookfilename \n";
echo "[+] Mức độ: $hint_level \n";

//Load Stop Words
$stopwords = file('./data/filter.txt', FILE_IGNORE_NEW_LINES);

//Load Dict from CSV
if($langww == 1){
	$lines = explode( "\n", file_get_contents( './data/vn.csv' ) );
	echo "[+] Ngôn ngữ Word Wise: Tiếng Việt\n";
} 
else if($langww == 2){
	$lines = explode( "\n", file_get_contents( './data/en.csv' ) ); 
	echo "[+] Ngôn ngữ Word Wise: Tiếng Anh\n";
} 
else {
	$lines = explode( "\n", file_get_contents( './data/custom.csv' ) ); 
	echo "[+] Ngôn ngữ Word Wise: Tự khởi tạo\n";
}
$headers = str_getcsv( array_shift( $lines ) );
$data = array();
foreach ( $lines as $line ) {

	$row = array();

	foreach ( str_getcsv( $line ) as $key => $field )
		$row[ $headers[ $key ] ] = $field;

	$row = array_filter( $row );

	$data[] = $row;

}
$wordwise_dict = $data;

//clean temp
if(file_exists('book_dump.htmlz')){
	unlink('book_dump.htmlz');
}
if(file_exists('book_dump_html')){
	deleteDir('book_dump_html');
}

//Convert Book to HTML
echo "[+] Chuyển sách sang dạng HTML \n";
shell_exec('ebook-convert "'.$bookfile.'" .\book_dump.htmlz');
shell_exec('ebook-convert .\book_dump.htmlz .\book_dump_html');

if(!file_exists('book_dump_html/index1.html')){
	die('Lỗi!!!! Hãy kiểm tra xem máy bạn đã có Calibre chưa? File còn nguyên trạng, còn ở thư mục không?');
}

//Get content
echo "[+] Tải nội dung sách \n";
$bookcontent = file_get_contents('book_dump_html/index1.html');
$bookcontent_arr = explode(" ",$bookcontent);

//Process Word
echo "[+] Có (".count($bookcontent_arr).") từ cần xử lí \n";
sleep(5);

for ($i=0; $i<=count($bookcontent_arr); $i++) { 

	if(isset($bookcontent_arr[$i]) AND $bookcontent_arr[$i] != ''){
		
		$word = cleanword($bookcontent_arr[$i]);

		//check is stopword ?		
		$is_stopword = array_search($word, $stopwords);
		if($is_stopword != FALSE){
			continue; //SKIP
		}

		$key_found = array_search(strtolower($word) , array_column($wordwise_dict, 'word'));
		//echo $key_found;
		//print_r($wordwise_dict[$key_found]);
		if($key_found != FALSE){

			$wordwise = $wordwise_dict[$key_found];

			//Check hint_level of current matched word
			if($wordwise['hint_level'] > $hint_level) continue; //SKIP all higher hint_level word

			echo "[>>] Xử lí từ: $i \n";

			echo "[#] bookcontent_arr[$i]: ".$bookcontent_arr[$i]." \n";

			//Replace Original Word with Wordwised
			$bookcontent_arr[$i] = preg_replace(
				'/('.$word.')/i',
				'<ruby>$1<rt>'.$wordwise['short_def'].'</rt></ruby>',
				$bookcontent_arr[$i]
				);

			echo "[#] word: ".$word." \n";
			echo "[#] bookcontent_arr ĐÃ THAY: ".$bookcontent_arr[$i]." \n";

		}

	}

}


echo "[+] Tạo sách mới với Word Wise \n";
$new_bookcontent_with_wordwised = implode(' ', $bookcontent_arr);
file_put_contents('book_dump_html/index1.html', $new_bookcontent_with_wordwised);
shell_exec('tar.exe -a -c -f book_dump_html.zip .\book_dump_html');
shell_exec('ebook-convert .\book_dump_html.zip "'.$bookpath.'/'.$bookfilename.'-wordwised.epub"');
shell_exec('ebook-convert .\book_dump_html.zip "'.$bookpath.'/'.$bookfilename.'-wordwised.azw3"');
shell_exec('ebook-convert .\book_dump_html.zip "'.$bookpath.'/'.$bookfilename.'-wordwised.pdf"');

//clean temp
echo "[+] Dọn bỏ file tạm \n";
if(file_exists('book_dump.htmlz')){
	unlink('book_dump.htmlz');
}
if(file_exists('book_dump_html')){
	deleteDir('book_dump_html');
}
if(file_exists('book_dump_html.zip')){
	unlink('book_dump_html.zip');
}

echo "[+] Sách đã được tạo thành công. Hãy kiểm tra thư mục ".$bookfilename."!\nChúc bạn đọc sách vui vẻ ^^. Nếu chương trình có lỗi hãy nhắn tin cho mình qua fb: https://www.facebook.com/doduc.dnad/ \n";



function deleteDir($dirPath) {
    if (! is_dir($dirPath)) {
        throw new InvalidArgumentException("$dirPath must be a directory");
    }
    if (substr($dirPath, strlen($dirPath) - 1, 1) != '/') {
        $dirPath .= '/';
    }
    $files = glob($dirPath . '*', GLOB_MARK);
    foreach ($files as $file) {
        if (is_dir($file)) {
            deleteDir($file);
        } else {
            unlink($file);
        }
    }
    rmdir($dirPath);
}

function cleanword($word){

	$word = strip_tags($word); //strip html tags

	$specialchar = array(',','<','>',';','&','*','~','/','"','[',']','#','?','`','–','.',"'",'"','"','!','“','”',':','.'); // recheck when apply this rule, may conflict with standard URL because it trim all char like ? and # and /

    $word = str_replace($specialchar,'',$word); //strip special chars
    $word = preg_replace("/[^ \w]+/", '', $word); //strip special chars - all non word and non space characters
    //$word = strtolower($word); //lowercase URL

    return $word;

}

?>