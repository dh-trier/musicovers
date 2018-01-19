<?php
$imagesDir = 'uncertain/';  // directory with images
$images = glob($imagesDir . '*.{jpg,jpeg,png,gif}', GLOB_BRACE);  // collect all images from directory

// $img = $images[0];  // pick first image
$img = $images[rand(0,129)];  // pick random image

if($img == null) {
	/* redirect */
	header("Location: http://noeffingtonpost.de/trier/praxisdh/faces_auswertung.php");
	exit;
}
?>

<html>
<head>
	<title>Facedetection</title>
	<meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="css/style.css"/>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
</head>
<body>
	<div id="outer">
		<h1>Wie viele Gesichter sind zu sehen?</h1>
		<div id="description"><!-- empty --></div>
		
		<div id="inner">
			<div id="inner_left">
				<img id="cover" src="<?php echo $img;?>"/>
				
				<div id="img_name">
					Filename: <?php echo $img;?>
				</div>
				
				<form id="form" method="GET" action="save_auswertung.php">
					<!-- <input id="input" name="input" autofocus="autofocus"/> -->
					<input type="hidden" name="image" value="<?php echo $img; ?>">
					<button id="submit" type="submit">Weiter</button>
					<br/>
				</form>
				
			</div>
		
			<div id="inner_right">
				<div id="results"><ul><!-- Shows the results --></div>
			</div>
			
		</div>
		
	</div>
	
<!-- JavaScript -->
<script>
$(document).ready(function() {

    loadJSON(); 

});

var images = {};
var php_img = "<?php echo substr($img, strlen('uncertain/')) ?>";

function loadJSON(){
	$.ajax({
		dataType: "json",
		url: "js/data_uncertain.json",
		success: function(json) {
			data = json;
			keys = Object.keys(data);
			for (var i = 0; i < data[php_img].length; i++) {
				$('#results').append("<ul><li><b>" + data[php_img][i] + "</b></li></ul>");
			}
		}
	});	
}
</script>
</body>
</html>