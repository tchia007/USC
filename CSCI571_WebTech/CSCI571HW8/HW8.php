<?php 
header("Access-Control-Allow-Origin: *");

$url = "https://graph.facebook.com/v2.8/search?q=";
$url2 = "&fields=id,name,picture.width(700).height(700)&access_token=EAAZAZCTf6VoV0BABMo03a8GVZCk7Fc4dYSDRy1UCdvhi9Wk79SdyBDQXfmR8OKGUlGTVZAnRtgZBLeg8w2lp2rUnUliVZAiBcZCOn8DEn7ZCyZAZCcQ3ZBH8Hwn0h2uXo6MH2qqXe14trJoHfN73JSUbHoq";
$access_token = "EAAZAZCTf6VoV0BABMo03a8GVZCk7Fc4dYSDRy1UCdvhi9Wk79SdyBDQXfmR8OKGUlGTVZAnRtgZBLeg8w2lp2rUnUliVZAiBcZCOn8DEn7ZCyZAZCcQ3ZBH8Hwn0h2uXo6MH2qqXe14trJoHfN73JSUbHoq";

if(isset($_GET['q']) && isset($_GET['type'])){
	if(isset($_GET['lat'])){
		$placesUrl = $url . $_GET['q'] . "&type=place&center=" . $_GET['lat'] . ',' . $_GET['long'] . $url2;
		$response = file_get_contents($placesUrl);
		header('Content-Type: application/json');
		echo $response;
	}
	else{
		$full_url = $url . $_GET['q'] . "&type=" . $_GET['type'] . $url2;
		$response = file_get_contents($full_url);
		header('Content-Type: application/json');
		echo $response;	
	}
}

if(isset($_GET['id'])){
	$detailsURL = "https://graph.facebook.com/v2.8/" . $_GET['id'] . "?fields=id,name,picture.width(700).height(700),albums.limit(5){name,photos.limit(2){name,picture}},posts.limit(5)&access_token=EAAZAZCTf6VoV0BABMo03a8GVZCk7Fc4dYSDRy1UCdvhi9Wk79SdyBDQXfmR8OKGUlGTVZAnRtgZBLeg8w2lp2rUnUliVZAiBcZCOn8DEn7ZCyZAZCcQ3ZBH8Hwn0h2uXo6MH2qqXe14trJoHfN73JSUbHoq";

	//header('Content-Type: application/json');
	//echo file_get_contents($detailsURL);

	$response = array();
	$decoded = json_decode(file_get_contents($detailsURL), true);

	if(isset($decoded['albums'])){
		foreach($decoded['albums'] as $item){
			$albums = array();
			$tempPic;
			$tempName;
			foreach($item as $data){
				if(isset($data['name'])){
					$tempName = $data['name'];
				}
				if(isset($data['photos'])){
					$picsArr = array();
					$idsArr = array();
					foreach($data['photos']['data'] as $picData){
						foreach($picData as $key => $value){
							if($key == "id"){
								$picUrl = "https://graph.facebook.com/v2.8/" . $value . "/picture?access_token=" . $access_token;
								$tempPic = $value;
								$tempID = $value;
								array_push($picsArr, $picUrl);
								array_push($idsArr, $value);
							}
						}
					}
				}
				if(isset($tempName) and isset($tempPic)){
					array_push($albums, array('name' => $tempName, 'picture' => $picsArr, "id" => $tempID));
					$tempPic = NULL;
					$tempName = NULL;
				}

			}
			if(!empty($albums)){
				array_push($response, array("albums" => $albums));
			}	
		}
	}
	else{
		$tempAl = array();
		array_push($tempAl, array('response' => 'No data found.'));
		array_push($response, array("albums" => $tempAl));
	}
	
	if(isset($decoded['posts'])){
		foreach($decoded['posts'] as $key => $value){
			$posts = array();
			$tempMes;
			$tempTime;
			if($key == "data"){
				foreach($value as $key2 => $item){
					foreach($item as $key3 => $value3){
						if($key3 == "message"){
							$tempMes = $value3;
						}
						if($key3 == "created_time"){
							$tempTime  = substr($value3, 0, 10) . " ".  substr($value3, 11, 8);
						}
					}
					array_push($posts, array('message' => $tempMes, 'time' => $tempTime));
				}
				array_push($response, array('posts' => $posts));
			}
		}
	}
	else{
		$tempPo = array();
		array_push($tempPo, array("response" => "No data found."));
		array_push($response, array("posts" => $tempPo));
	}
	header('Content-Type: application/json');
	echo json_encode($response);

	//not this one
	//echo json_encode( (array('data' => $response))) ;
}
?>


