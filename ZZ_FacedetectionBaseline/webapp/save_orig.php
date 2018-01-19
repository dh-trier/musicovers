<?php 

$img_orig = $_GET['image'];
$faces = $_GET['input'];

$prefix = 'images/';

if (substr($img_orig, 0, strlen($prefix)) == $prefix) {
    $img = substr($img_orig, strlen($prefix));
} 

// rename($img_orig, 'fertig/' . $img);

$file = fopen('data.csv', 'a');
fwrite($file, $img . "\t" . $faces . "\n");
fclose($file);

header("Location: http://noeffingtonpost.de/trier/praxisdh/faces.php");
exit;

?>