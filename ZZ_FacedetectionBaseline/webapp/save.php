<?php 

$img_orig = $_GET['image'];  // Get image name
$faces = $_GET['input'];  // Get user input

/* remove folder name from image name */
$prefix = 'images/';
if (substr($img_orig, 0, strlen($prefix)) == $prefix) {
    $img = substr($img_orig, strlen($prefix));
} 

/* write user input to file */
$file = fopen('data.csv', 'a');
fwrite($file, $img . "\t" . $faces . "\n");
fclose($file);

/* redirect */
header("Location: http://noeffingtonpost.de/trier/praxisdh/faces.php");
exit;

?>