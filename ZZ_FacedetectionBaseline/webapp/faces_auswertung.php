<?php
$imagesDir = 'uncertain/';  // directory with images
$images = glob($imagesDir . '*.{jpg,jpeg,png,gif}', GLOB_BRACE);  // collect all images from directory

$img = $images[0];  // pick first image

if($img == null) {
	echo "<h1 style='color: red;'>Keine Bilder mehr verfügbar!</h1>";
}
?>

<html>
<head>
	<title>Facedetection</title>
	<meta charset="utf-8">
	<style>
		h1 {margin: auto;}
		#outer {text-align: center;}
		#description {margin: auto; width: 35%; font-style: italic;}
		#cover {height: 400px; width: 400px; margin: auto;}
		#form {margin: auto;}
		#input {margin-top: 20px; font-size: 25px;}
	</style>
	<script src="jquery.js"></script>
	<script>$(document).ready(function() {

    loadJSON(); 

});</script>
		<script>
			var images = {};
			var php_img = "<?php echo substr($img, strlen('uncertain/')) ?>";
		</script>
		<script>
		function loadJSON(){

			$.ajax({
				dataType: "json",
				url: "data_uncertain.json",
				success: function(json) {
					thesaurus = json;
					keys = Object.keys(thesaurus);
					for (var i = 0; i < thesaurus[php_img].length; i++) {
						$('#results').append("<b>" + thesaurus[php_img][i] + "</b> ");
					}
				}
			});
		
		}
		</script>
</head>
<body>
	<div id="outer">
		<h1>Wie viele Gesichter sind zu sehen?</h1>
		<div id="description">(Ein Gesicht zählt als solches, wenn man mindestens 3 der 4 folgenden Elemente sicher erkennen kann: Auge, Nase, Mund, Ohr. Diese Elemente zählen auch dann, wenn man sie nur von der Seite sieht.)</div>
		
		<img id="cover" src="<?php echo $img;?>"/>
		
		<div>
			<?php echo $img;?>
		</div>
		
		<div id="results" class="results"><!-- Shows the results after a search term is typed --></div>

		
		<form id="form" method="GET" action="save_auswertung.php">
			<input id="input" name="input" autofocus="autofocus"/>
			<input type="hidden" name="image" value="<?php echo $img; ?>">
			<button type="submit">Weiter</button>
			<br/>
		</form>
		
	</div>
</body>
</html>