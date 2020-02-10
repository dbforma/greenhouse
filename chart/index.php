<?php
	$config = parse_ini_file('../config/config.ini'); // INI-Dateipfad (absolut oder relativ)
	
	$username = $config['user']; 
    $password = $config['password'];   
    $host = $config['host'];
    $database= $config['database'];
	
	$conn = new mysqli($host, $username, $password, $database);
	if ($conn->connect_errno) {
		die("Verbindung fehlgeschlagen: " . $conn->connect_error);
	}
	
	$sql = "SELECT * FROM chartViewTemp";
	$result = $conn->query($sql);
	
	$rows = array();
	$table = array();
	$table['cols'] = array(
		array('label' => 'Messzeitpunkt', 'type' => 'string'),
		array('label' => 'Luft', 'type' => 'number'),
		array('label' => 'Boden', 'type' => 'number')
		);
		
	foreach($result as $r) {
		$temp = array();
		
		$temp[] = array('v' => $r['DatumStunde']);
		
		$temp[] = array('v' => $r['LuftTemp']);
		$temp[] = array('v' => $r['BodenTemp']);
		$rows[] = array('c' => $temp);
	}
	
	$table['rows'] = $rows;


	$jsonTableTemp = json_encode($table);
	//echo $jsonTableTemp;
	
	
	$sql = "SELECT * FROM chartViewFeuchte";
	$result = $conn->query($sql);
	
	$rows = array();
	$table = array();
	$table['cols'] = array(
		array('label' => 'Messzeitpunkt', 'type' => 'string'),
		array('label' => 'Luft', 'type' => 'number'),
		array('label' => 'Boden', 'type' => 'number')
		);
		
	foreach($result as $r) {
		$temp = array();
		
		$temp[] = array('v' => $r['DatumStunde']);
		
		$temp[] = array('v' => $r['LuftFeuchte']);
		$temp[] = array('v' => $r['BodenFeuchte']);
		$rows[] = array('c' => $temp);
	}
	
	$table['rows'] = $rows;

	mysqli_close($conn);

	$jsonTableFeuchte = json_encode($table);
	//echo $jsonTableFeuchte;
?>

<html>
	<head>
	  <!--Load the Ajax API-->
	  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
	  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
	  <script type="text/javascript">
	  
	  google.charts.load('current', {'packages':['corechart']});
	  google.charts.setOnLoadCallback(drawChart);
	  
	  function drawChart() {

      var data = new google.visualization.DataTable(<?=$jsonTableTemp?>);

	  var options = {
		  title: 'Temperaturen',
		  legend: { position: 'bottom' },
	  };
	  
      var chart = new google.visualization.LineChart(document.getElementById('line_chart_temp'));
	  
      chart.draw(data, options);
      }
	  </script>
	  <script type="text/javascript">
	  
	  google.charts.load('current', {'packages':['corechart']});
	  google.charts.setOnLoadCallback(drawChart);
	  
	  function drawChart() {

      var data = new google.visualization.DataTable(<?=$jsonTableFeuchte?>);

	  var options = {
		  title: 'Feuchtigkeiten',
		  legend: { position: 'bottom' },
	  };
	  
      var chart = new google.visualization.LineChart(document.getElementById('line_chart_feuchte'));
	  
      chart.draw(data, options);
      }
	  </script>
	</head>
	
	<body>
	  <div id="line_chart_temp" style="width: 1200; height: 400"></div>
	  <div id="line_chart_feuchte" style="width: 1200; height: 400px"></div>
	</body>
</html>
