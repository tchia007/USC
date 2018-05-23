<?php

	ini_set('memory_limit', '1600M');
	//make sure browsers see this page as utf-8 encoded HTML
	header('Content-Type: text/html; charset=utf-8');

	// testing norvig's program
	include 'SpellCorrector.php';
	include 'simple_html_dom.php';

	//preparing for solr 
	$limit = 10;
	$query = isset($_REQUEST['q']) ? $_REQUEST['q'] : false;
	$results = false;

	//sending solr query 
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

			#handling multi word queries 
			$query_split = explode(' ', $query);
			$correction = "";
			foreach($query_split as $word){
				$correction .= SpellCorrector::correct(strtolower($word)) . ' ';
			}
			$correction = substr($correction, 0, -1);

			//need to strip spaces from query
		 	// $query_split = explode(' ', $query);
		 	// $new_query = "";
		 	// foreach($query_split as $q){
		 	// 	$new_query .= trim($q);
		 	// }
		 	// $query = explode(" ", $new_query);
		 	// $query = implode(" ", $query);

		}catch (Exception $e){  
			die("<html><head><title>SEARCH EXCEPTION</title><body><pre>{$e->__toString()}</pre></body></html>");
		}     
	}

	//function for trimming snippet to 160 characters 
	//arr is array of paragraph
	//pos is the position of the query in the array
	//snippetLen is length of the snippet
	function trimSnippet($arr, $snippetLen, $query_arr){
		//trim the end of a snippet

		//handling huge paragraphs
		$arr_str = implode(" ", $arr);
		$arr_str_len = strlen($arr_str);
		$best_match = "";
		$best_match_counter = 0;
		if($arr_str_len > 400 && sizeof($query_arr) >= 2){
			//split into 160 char chunks and check for regular expression match
			$start = 0;
			$length = 160;
			while($start < $arr_str_len){
				$chunk = substr($arr_str, $start, $length);

				$pattern = "/";
				foreach($query_arr as $query){
					$pattern .= "(?=.*\b" . $query . "\b)";
				}
				$pattern .= "/";
				$chunk_lower = strtolower($chunk);
				preg_match($pattern, $chunk, $matches);
				if($matches){
					return $chunk;
				}

				$curr_counter = 0;
				foreach($query_arr as $query){
					if(strpos($chunk_lower, $query) !== false ){
						$curr_counter += 1;
					}
				}
				if($curr_counter > $best_match_counter){
					$best_match = $chunk;
					$best_match_counter = $curr_counter;
				}
				$start += $length;
			}
			if($start != 0){
				return "..." . $best_match . "...";
			}
		}

		$return_str = "";
		$arr_len = sizeof($arr);
		$trim_begin = false;
		for($i = $arr_len; $i > 0; $i--){
			$stripped = strip_tags($arr[$i]);
			$match = true;
			foreach($query_arr as $query){
				//no match, check next query
				if(strpos(strtolower($stripped), $query) !== 0){
					$match = false;
				}
				//matched query
				else{
					$match = true;
					$return_str = implode(' ', $arr) . '...'; 
					$snippetLen = strlen(strip_tags($return_str));
					//if query word is found and snippet length is less than 160
					if($snippetLen <= 160){
						return $return_str;
					}
					//snippetlen > 160, break and jump to trimming beginning
					else{
						$trim_begin = true;
						break;
					}
				}
			}
			if(!$match){
				$snippetLen -= strlen(strip_tags($arr[$i])); //subtracting 2 to account for spaces
				unset($arr[$i]);
				if($snippetLen <= 160){
					$return_str = implode(' ', $arr) . '...'; 
					return $return_str;
				}
			}
		}
		
		if($trim_begin){
			$arr_len = sizeof($arr);
			//trimming beginning of snippet
			for($i = 0; $i < $arr_len; $i++){
				$snippetLen -= strlen($arr[$i]);
				unset($arr[$i]);
				if($snippetLen <= 160){
					$return_str = implode(' ', $arr) . '...'; 
					return "..." . $return_str;
				}
			}
		}
	}

	//function for adding next sentence to snippet if snippet too short
	function addSnippet($arr, $snippet_str, $query){
		$snippetLen = strlen($snippet_str) - 7;
		for($i = 0; $i < sizeof($arr); $i++){
			if($snippetLen + strlen($arr[$i]) >= 160){
				return $snippet_str . "...";
			}
			else{
				if(strpos(strtolower($arr[$i]), $query) !== false ){
					$snippet_str .= ("<b>" . $arr[$i] . "</b>");
				}
				else{
					$snippet_str .= " " . $arr[$i];
				}
				$snippetLen += strlen($arr[$i]);
			}
		}
		return $snippet_str;
	}

	//function to compare return strings
	//counts if both queries appear in string and returns the one with most query terms
	function compareReturn($return_str, $best_str, $query_arr){
		$best_Set = [];
		$return_Set = [];
		if($best_str == ""){
			return $return_str;
		}
		else{
			$count = 0;
			foreach($query_arr as $query){
				if(substr_count(strtolower($best_str), $query) >= 1){
					array_push($best_Set, $query);
				}
				if(substr_count(strtolower($return_str), $query) >= 1){
					array_push($return_Set, $query);
				}
			}
		}
		if(sizeof(array_unique($best_Set)) >= sizeof(array_unique($return_Set))){
			return $best_str;
		}
		else{
			return $return_str;
		}
	}

	//snippet generation function 
	function genSnippet($link, $query_arr){
		//if page can't be reached output error and the header
		$headers = get_headers($link, 1);
		if($headers[0] !='HTTP/1.1 200 OK'){
			return "Error: " . $headers[0];
		}
		//else do html parsing of the paragraph to find match to query
   		else{
   			$addNextSent = false;
   			$return_str = "";
   			$snippetLen = 0;
			$html = file_get_html($link);
			$best_str = "";
			if(!empty($html)){
				//checking in <p> tags of html 
				foreach($html->find('p') as $paragraph){
					$matchedQuery = false;
					$paragraph = explode(' ', $paragraph->plaintext);

					//add next sent flag will be true if found snippet is too short 
					//and we need simply just add the next sentence to the snippet
					if($addNextSent){
						$return_str = addSnippet($paragraph, $return_str, $query);
						if(strlen($return_str) < 160){
							$addNextSent = true;
						}
						else{
							return $return_str;
						}
					}
					else{
						//using regular expressiong to find best paragraph as snippet
						if(sizeof($query_arr) == 1){
							$query = $query_arr[0];
							$pattern = "/\b" . $query . "\b/";
							$par = strtolower(implode(" ", $paragraph));
							preg_match($pattern, $par, $matches);
						}
						else{
							$pattern = "/";
							foreach($query_arr as $query){
								$pattern .= "(?=.*\b" . $query . "\b)";
							}
							$pattern .= "/";
							$par = strtolower(implode(" ", $paragraph));
							preg_match($pattern, $par, $matches);
							if($matches[0]){
								$paragraph = $matches[0];
							}
						}

						if($matches){
							for($i = 0; $i < sizeof($paragraph); $i++){
								//if word and query match, bold the word
								foreach($query_arr as $query){
									if($addNextSent == false && strpos(strtolower($paragraph[$i]), $query) !== false ){
										$matchedQuery = true;
										$paragraph[$i] = preg_replace('/\S*('. $query .')\S*/i', '<b>$1 </b>', $paragraph[$i]);
										// $paragraph[$i] = "<b>" . $paragraph[$i] . " </b>";
										$return_str = implode(' ', $paragraph);
										$snippetLen = strlen(strip_tags($return_str));
									}
								}
							}

							if($matchedQuery){
								//trim snippet if too long
								if($snippetLen > 160){
									$return_str = trimSnippet($paragraph, $snippetLen, $query_arr);
									$best_str = compareReturn($return_str, $best_str, $query_arr);
									break;
								}
								else{//add next sentence if snippet isn't long enough
									// $paragraph[$i] = "<b>" . $paragraph[$i] . " </b>";
									$paragraph[$i] = preg_replace('/\S*('. $query .')\S*/i', '<b>$1 </b>', $paragraph[$i]);
									$return_str = implode(' ', $paragraph);
									$snippetLen = strlen(strip_tags($return_str));
									$addNextSent = true;
								}
							}
						}
						//checking individual query separately
						else{
							foreach($query_arr as $query){
								$pattern = "/\b" . $query . "\b/";
								$par = strtolower(implode(" ", $paragraph));
								preg_match($pattern, $par, $matches);
								if($matches){
									for($i = 0; $i < sizeof($paragraph); $i++){
										//if word and query match, bold the word
										foreach($query_arr as $query){
											if($addNextSent == false && strpos(strtolower($paragraph[$i]), $query) !== false ){
												if(strtolower($paragraph[$i]) == $query){
													$matchedQuery = true;
													$paragraph[$i] = "<b>" . $paragraph[$i] . " </b>";
													$paragraph[$i] = preg_replace('/\S*('. $query .')\S*/i', '<b>$1 </b>', $paragraph[$i]);
													$return_str = implode(' ', $paragraph);
													$snippetLen = strlen(strip_tags($return_str));
												}
											}
										}
									}

									if($matchedQuery){
										//trim snippet if too long
										if($snippetLen > 160){
											$return_str = trimSnippet($paragraph, $snippetLen, $query_arr);
											$best_str = compareReturn($return_str, $best_str, $query_arr);
										}
										else{//add next sentence if snippet isn't long enough
											$paragraph[$i] = "<b>" . $paragraph[$i] . " </b>";
											$paragraph[$i] = preg_replace('/\S*('. $query .')\S*/i', '<b>$1 </b>', $paragraph[$i]);
											$return_str = implode(' ', $paragraph);
											$snippetLen = strlen(strip_tags($return_str));
											$addNextSent = true;
										}
									}
								}
							}
						}
					}
				}
			}
			if($best_str == ""){
				return "N/A";
			}
			else{
				return $best_str;
			}
		}
	}
?>
<!DOCTYPE html>
<html>   
	<head>   
		<title>PHP Solr Client Example</title>
		<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
		<script src="http://code.jquery.com/jquery-1.12.4.min.js"></script>
		<script src="http://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
	</head>   
	<body>
		<form accept-charset="utf-8" method="get" id="searchForm">
			<div class="ui-widget">
				Search:
				<input id="q" name="q" type="text" value="<?php echo htmlspecialchars($query, ENT_QUOTES, 'utf-8'); ?>"/> <input type="submit"/> 
				<input type="radio" name="choice" value="solr" 
				<?php 
					if((!isset($_GET['choice'])) || (isset($_GET['choice']) && $choice == "solr")){
						echo 'checked="checked"';
					}
				?> 
				>Solr (Default)
				<input type="radio" name="choice" value="pagerank" <?php if(isset($_GET['choice']) && $choice == "pagerank"){echo 'checked="checked"';} ?> >PageRank <br>
			</div>
		</form>
		<?php
			if(strtolower($correction) != strtolower($query)){
				//creating new link for using correct spelling
				$fixed_link = 'http://localhost/hw5?q=' . str_replace(' ', '+', $correction) . '&choice=' . $choice;
				echo "<div class='didumean'> Did you mean: <a href=" . $fixed_link . ">" . $correction . "</a></div>";
				$correction = $query;
			}

			// display results
			if($results){
				$total = (int) $results->response->numFound;
				$start = min(1, $total);
				$end = min($limit, $total);
		?>
				<div>Results <?php echo $start; ?> - <?php echo $end;?> of <?php echo $total; ?>:</div>
				<ol>
					<?php
					 // iterate result documents to grab each field
					$link = "";
					foreach ($results->response->docs as $doc){
						foreach ($doc as $field => $value){
							if($field == "title"){
								$title = $value;
								if(empty($title)){
									$title = "N/A";
								}
							}
							if($field == "og_url"){
								$link = $value;
								if(empty($link)){
									$link = "N/A";
								}								
							}
							if($field == "id"){
								$id = $value;
								if(empty($id)){
									$id = "N/A";
								}
							}
							if($field == "og_description"){
								$desc = $value;
								if(empty($desc)){
									$desc = "N/A";
								}
							}
						}
						if($link){
							//need to strip spaces from query 
						 	$query_split = explode(' ', $query);
						 	$new_query = "";
						 	foreach($query_split as $q){
						 		$temp = trim(strtolower($q));
						 		if(strlen($temp) > 0){
						 			$new_query .= $temp . " ";
						 		}
						 	}
						 	$new_query = substr($new_query, 0, -1);
						 	$query_arr = explode(" ", $new_query);
							$snippet = genSnippet($link, $query_arr);
						}
					?>
						<!-- Displaying each field with the title and url as clickable links -->
						<li>
							<table stlye =1px solid black; text-align: left;">
								<tr>
									<b>Title:</b> <a href = <?php echo $link; ?>> <?php echo $title; ?></a><br>
									<b>URL:</b>  <a href = <?php echo $link; ?>> <?php echo $link; ?></a><br>
									<b>ID:</b> <?php echo $id; ?><br>
									<b>Snippet:</b> <?php echo $snippet; ?><br>
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

<script type="text/javascript">
//doing autocomplete here 
$(document).ready(function(){
	$("#q").autocomplete({
		source: function(request, response){
			//need to check for multi word query before sending ajax request
			var suggestionList = [];
			var splitQuery = (request.term).split(' ');
			for(var i = 0; i < splitQuery.length-1; i++){
				suggestionList.push(splitQuery[i]);
			}

			var suggestTerm = splitQuery[splitQuery.length-1].toLowerCase();
			if(!suggestTerm){
				suggestTerm = "";
			}
			//making ajax call with desired suggest term
			$.ajax({
				url : "http://localhost:8983/solr/myexample/suggest?q=" + suggestTerm, 
				dataType: "jsonp", 
				success: function(data){
					//parsing the json get request from solr 
					var suggest = data.suggest.suggest;
					var docs = JSON.stringify(suggest);
					var jsonData = JSON.parse(docs);
					var result = jsonData[suggestTerm].suggestions;

					//handling autocomplete for multiple queries. solr only suggests 1 word at a time
					var finalSuggestion = []
					var savedSuggestion = "";
					if(suggestionList.length >= 1){
						for(var j = 0; j < suggestionList.length; j++){
							savedSuggestion += suggestionList[j] + " ";
						}
					}

					//creating final suggestion list
					if(!suggestTerm){
						finalSuggestion.push(savedSuggestion);
					}
					else{
						for(var i = 0; i < result.length; i++){
							if(result[i].term != suggestTerm){
								if(savedSuggestion == ""){
									finalSuggestion.push(result[i].term);
								}
								else{
									finalSuggestion.push(savedSuggestion + " " + result[i].term);
								}
							}
						}
					}

					//formating suggestionList to the way autocomplete wants data
					response($.map(finalSuggestion, function(item){
						return { label: item, value: item};
					}));
				}, 
				crossDomain: true,
				jsonp: 'json.wrf',
			});
		}, 
		minLength : 1, 
		select: function(event, ui){
			$('#q').val(ui.item.label);
			$('#searchForm').submit();
			$('.didumean').css("visibility", "hidden");
			$('.didumean').css("display", "none");
		}
	});
});

$('.didumean').click(function(){
	$('.didumean').css("visibility", "hidden");
	$('.didumean').css("display", "none");
});
</script>