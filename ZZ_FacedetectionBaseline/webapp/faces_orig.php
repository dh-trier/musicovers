<?php
$imagesDir = 'images/';

$images = glob($imagesDir . '*.{jpg,jpeg,png,gif}', GLOB_BRACE);

// $img = $images[array_rand($images)]; // See comments
$img = $images[rand(0,499)];

if($img == null) {
	echo "<h1 style='color: red;'>Keine Bilder mehr verfügbar!</h1>";
}
?>

<html>
<head>
<title>Facedetection</title>
<meta charset="utf-8">
</head>
<body>
	<div id="outer" style="text-align: center;">
	<h1 style="margin: auto;">Wie viele Gesichter sind zu sehen?</h1>
	<div style="margin: auto; width: 35%;"><i>(Ein Gesicht zählt als solches, wenn man mindestens 3 der 4 folgenden Elemente sicher erkennen kann: Auge, Nase, Mund, Ohr. Diese Elemente zählen auch dann, wenn man sie nur von der Seite sieht.)</i></div>
	<img src="<?php echo $img;?>" style="height: 300px; width: 300px; margin: auto;"/>
	<form method="GET" action="save.php" style="margin: auto;">
		<input id="input" name="input" style="margin-top: 20px; font-size: 25px;" autofocus="autofocus"/>
		<input type="hidden" name="image" value="<?php echo $img; ?>">
		<button type="submit">Senden</button>
	</form>
	</div>
</body>
</html>