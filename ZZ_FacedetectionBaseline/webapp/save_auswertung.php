<?php 

$img_orig = $_GET['image'];  // Get image name
$faces = $_GET['input'];  // Get user input

/* remove folder name from image name */
$prefix = 'uncertain/';
if (substr($img_orig, 0, strlen($prefix)) == $prefix) {
    $img = substr($img_orig, strlen($prefix));
} 

/* move image to another folder */
rename($img_orig, 'uncertain_corrected/' . $img);

/* write user input to file */
$file = fopen('data_uncertain_corrected.csv', 'a');
fwrite($file, $img . "\t" . $faces . "\n");
fclose($file);

/* redirect */
header("Location: http://noeffingtonpost.de/trier/praxisdh/faces_auswertung.php");
exit;
?>