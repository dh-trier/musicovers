<?php
$imagesDir = 'images/';  // directory with images
$images = glob($imagesDir . '*.{jpg,jpeg,png,gif}', GLOB_BRACE);  // collect all images from directory

$img = $images[rand(0, 499)];  // pick random image

if($img == null) {
	echo "<h1 style='color: red;'>Keine Bilder mehr verfügbar!</h1>";
}
?>

<html>
<head>
	<title>Facedetection</title>
	<meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="css/style.css"/>
    <script src="js/jquery.js"></script>
</head>
<body>
	<div id="outer">
		<h1>Wie viele Gesichter sind zu sehen?</h1>
		<div id="description">(Ein Gesicht zählt als solches, wenn man mindestens 3 der 4 folgenden Elemente sicher erkennen kann: Auge, Nase, Mund, Ohr. Diese Elemente zählen auch dann, wenn man sie nur von der Seite sieht.)</div>
		
		<img id="cover" src="<?php echo $img;?>"/>
		
		<form id="form" method="GET" action="save.php">
			<input id="input" name="input" autofocus="autofocus"/>
			<input type="hidden" name="image" value="<?php echo $img; ?>">
			<button type="submit">Senden</button>
		</form>
		
	</div>
</body>
</html>