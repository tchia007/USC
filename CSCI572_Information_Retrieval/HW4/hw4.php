<?php
	//make sure browsers see this page as utf-8 encoded HTML
	header('Content-Type: text/html; charset=utf-8');

	$limit = 10;
	$query = isset($_REQUEST['q']) ? $_REQUEST['q'] : false;
	$results = false;

	if ($query){  
		require_once('solr-php-client/Apache/Solr/Service.php');

		// create a new solr service instance - host, port, and corename
		// path (all defaults in this example)
		$solr = new Apache_Solr_Service('localhost', 8983, 'solr/myexample');

		// if magic quotes is enabled then stripslashes will be needed
	 	if(get_magic_quotes_gpc() == 1){     
	 		$query = stripslashes($query);   
	 	}
		try{    
			// getting the algorithm of choice: solr or pagerank
			$choice = $_GET['choice'];
			if(empty($choice)){
				$choice = "solr";
			}
			if($choice == "solr"){
				$results = $solr->search($query, 0, $limit); 
			}
			else{
				$additionalParameters = array('sort'=>'pageRankFile desc');
				$results = $solr->search($query, 0, $limit, $additionalParameters); 
			}

		}catch (Exception $e){  
			die("<html><head><title>SEARCH EXCEPTION</title><body><pre>{$e->__toString()}</pre></body></html>");
		}     
	}
?>
<html>   
	<head>   
		<title>PHP Solr Client Example</title>
	</head>   
	<body>
		<form accept-charset="utf-8" method="get">
			<label for="q">Search:</label>
			<input id="q" name="q" type="text" value="<?php echo htmlspecialchars($query, ENT_QUOTES, 'utf-8'); ?>"/>
			<input type="radio" name="choice" value="solr" <?php if(isset($_GET['choice']) && $choice == "solr"){echo 'checked="checked"';} ?> >Solr (Default)
			<input type="radio" name="choice" value="pagerank" <?php if(isset($_GET['choice']) && $choice == "pagerank"){echo 'checked="checked"';} ?> >PageRank
			<input type="submit"/>
		</form>
		<?php
			// display results
			if ($results){
				$total = (int) $results->response->numFound;
				$start = min(1, $total);
				$end = min($limit, $total);
		?>
				<div>Results <?php echo $start; ?> - <?php echo $end;?> of <?php echo $total; ?>:</div>
				<ol>
					<?php
					 // iterate result documents to grab each field
					foreach ($results->response->docs as $doc){
						foreach ($doc as $field => $value){
							if($field == "title"){
								$title = $value;
							}
							if($field == "og_url"){
								$link = $value;
							}
							if($field == "id"){
								$id = $value;
							}
							if($field == "og_description"){
								$desc = $value;
								if(empty($desc)){
									$desc = "N/A";
								}
							}
						}
					?>
						<!-- Displaying each field with the title and url as clickable links -->
						<li>
							<table stlye =1px solid black; text-align: left;">
								<tr>
									<b>Title:</b> <a href = <?php echo $link; ?>> <?php echo $title; ?></a><br>
									<b>URL:</b>  <a href = <?php echo $link; ?>> <?php echo $link; ?></a><br>
									<b>ID:</b> <?php $arr = explode("/", $id); echo $arr[8]; ?><br>
									<b>Description:</b> <?php echo $desc; ?>
								</tr>
							</table>
							<br>
				 		</li>
				 							
				 	<?php
					}
					?>
				</ol>
		<?php
		}
		?>
 </body>
</html>


















