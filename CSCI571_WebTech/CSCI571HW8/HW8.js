//facebook stuff
window.fbAsyncInit = function(){
    FB.init({
        appId: '1828822820692317',
        xfbml: true, 
        version: 'v2.8', 
    });
};
(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {
        return;
    }
    js = d.createElement(s);
    js.id = id;
    js.src="https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
} (document, 'script', 'facebook-jssdk'));




//global variables
var slidingFlag;
var cords;
var nextUsersPage;
var prevUsersPage;

var nextPagesPage;
var prevPagesPage;

var nextGroupsPage;
var prevGroupsPage;

var nextPlacesPage;
var prevPlacesPage;

var nextEventsPage;
var prevEventsPage;
var detailStarId =[];
var firstAlbumID;
var fbPic;
var fbName;
searchKeyPressed = false;


//getting geo location 
var options ={
	enableHighAccuray: true, 
	maximumAge: 0
}
function success(pos){
	cords = pos.coords;
	console.log(cords);
};

function error(err){
	console.warn(`ERROR($({err.code}): ${err.message}`);
};
navigator.geolocation.getCurrentPosition(success, error, options);

var app = angular.module('HW8', ['ngAnimate']);
app.controller('controller', function ($scope, $http) {

	$scope.loading= false;
	$scope.loadingAlbPo = false;

	//initial search keyword function. makes http request for all tabs
	$scope.userSearch = function () {
		hideEverything();
		$scope.loading = true;
		$scope.searchText = document.getElementById('kw').value;

		// ----------------------------- USERS ---------------------------
		$http({
			method : 'GET',
			// url : 'http://localhost:8080/HW8.php?q=' + $scope.searchText + '&type=user'
			url : 'https://helloworld-162201.appspot.com/HW8.php?q=' + $scope.searchText + '&type=user'
		}).then(function successCallback(response) {
			console.log(response.data);
			$scope.userDetails = (response.data.data);
			$scope.loading = false;
			searchKeyPressed = true;
			if($scope.loading == false){
				if(response.data.paging){
					 nextUsersPage = response.data.paging.next;
					$(".lowerButtonsUsers").css({"display" : "block", "visibility" : "visible"});
					$("#nextUsers").css({"display" : "inline-block", "visibility" : "visible"});
				}
				$(".user").css({"display" : "block", "visibility" : "visible"});
				$(".table-hover").css({"display" : "table", "visibility" : "visible", "width" : "100%"});
			}
		}, function errorCallback(response) {
			console.log(response);
			alert("Error loading. Please refresh and try again");
			return response;
		});

		// ----------------------------- PAGES ---------------------------
		$http({
			method : 'GET',
			// url : 'http://localhost:8080/HW8.php?q=' + $scope.searchText + '&type=page'
			url : 'https://helloworld-162201.appspot.com/HW8.php?q=' + $scope.searchText + '&type=page'
		}).then(function successCallback(response) {
			if(response.data.paging){
				nextPagesPage = response.data.paging.next;
			}
			$scope.pagesDetails = (response.data.data);
		}, function errorCallback(response) {
			return response;
		});

		// ----------------------------- EVENTS ---------------------------
		$http({
			method : 'GET',
			// url : 'http://localhost:8080/HW8.php?q=' + $scope.searchText + '&type=event'
			url : 'https://helloworld-162201.appspot.com/HW8.php?q=' + $scope.searchText + '&type=event'
		}).then(function successCallback(response) {
			if(response.data.paging){
				nextEventsPage = response.data.paging.next;
			}
			$scope.eventsDetails = (response.data.data);
		}, function errorCallback(response) {
			return response;
		});

		// ----------------------------- PLACES ---------------------------
		$http({
			method : 'GET',
			// url : 'http://localhost:8080/HW8.php?q=' + $scope.searchText + '&type=place' + "&lat=" + cords.latitude + "&long=" + cords.longitude
			url : 'https://helloworld-162201.appspot.com/HW8.php?q=' + $scope.searchText + '&type=place' + "&lat=" + cords.latitude + "&long=" + cords.longitude
		}).then(function successCallback(response) {
			if(response.data.paging){
				nextPlacesPage = response.data.paging.next;
			}
			$scope.placesDetails = (response.data.data);
		}, function errorCallback(response) {
			return response;
		});

		// ----------------------------- GROUPS ---------------------------
		$http({
			method : 'GET',
			// url : 'http://localhost:8080/HW8.php?q=' + $scope.searchText + '&type=group'
			url : 'https://helloworld-162201.appspot.com/HW8.php?q=' + $scope.searchText + '&type=group'
		}).then(function successCallback(response) {
			if(response.data.paging){
				nextGroupsPage = response.data.paging.next;
			}
			$scope.groupsDetails = (response.data.data);
		}, function errorCallback(response) {
			return response;
		});
	}

		// ----------------------------- DETAILS PAGE ---------------------------
	$scope.detailsSearch = function(id, picURL,name, type) {
		$scope.loadingAlb = true;
		$scope.loadingPo = true;
		fbPic = picURL;
		fbName = name;
		showDetails();
		$http({
			method : 'GET',
			// url : 'http://localhost:8080/HW8.php?id=' + id
			url : 'https://helloworld-162201.appspot.com/HW8.php?id=' + id
		}).then(function successCallback(response) {
			console.log(response);
			detailStarId = [id, picURL, name, type];
			firstAlbumID = response.data[0].albums[0].id;
			$scope.detailsAlbums = response.data[0].albums;
			$scope.detailsPosts = response.data[1].posts;
			$scope.detailsPic = picURL;
			$scope.detailsName = name;
			$scope.loadingAlb = false;
			$scope.loadingPo = false;
			if($scope.loadingAlb == false){
				$("#body"+firstAlbumID).css({"display" : "block", "visibility" : "visible"});
				$("."+firstAlbumID).css({"display" : "block", "visibility" : "visible"});
			}

			if(localStorage.getItem(id) != null){
				$("#detailStar").removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
			}
			else{
				$("#detailStar").removeClass('glyphicon glyphicon-star').addClass('glyphicon glyphicon-star-empty');
			}
		}, function errorCallback(response) {
			return response;
		});
	}

	$scope.changeDetailStar = function(){
		console.log(detailStarId);
		if(localStorage.getItem(detailStarId[0]) != null){
			$("#detailStar").removeClass('glyphicon glyphicon-star').addClass('glyphicon glyphicon-star-empty');
			localStorage.removeItem(detailStarId[0]);
		}
		else{
			$("#detailStar").removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
			var favoritesItems = 
			{
				"name" : detailStarId[2],
				"url" : detailStarId[1],
				"type" : detailStarId[3], 
				"id" : detailStarId[0]
			};
			localStorage.setItem(detailStarId[0], JSON.stringify(favoritesItems));
			var arr = []
			for(var i = 0; i < localStorage.length; i++){
				var obj = JSON.parse(localStorage.getItem(localStorage.key(i)));
				arr.push({ "name" : obj.name, "url" : obj.url, "type" : obj.type, "id" : obj.id } );
			}
			$scope.localSto = arr;
		}
	}

	//function toggles between stars when clicked and changes local storage
	$scope.changeStar = function(rowNum, name, picURL, type, id){
		if($("#"+id).attr('class') == 'glyphicon glyphicon-star'){ //remove from local storage 
			$("#"+id).removeClass('glyphicon glyphicon-star').addClass('glyphicon glyphicon-star-empty');
			localStorage.removeItem(id);
		}
		else if($("#"+id).attr('class') == 'glyphicon glyphicon-star-empty'){ //need to add to local storage
			$("#"+id).removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
			var favoritesItems = 
			{
				"name" : name, 
				"url" : picURL,
				"type" : type,
				"id" : id
			};
			localStorage.setItem(id, JSON.stringify(favoritesItems));	
		}
		// formatting the localstorage values for ng-repeat 
		var arr = []
		for(var i = 0; i < localStorage.length; i++){
			var obj = JSON.parse(localStorage.getItem(localStorage.key(i)));
			arr.push({ "name" : obj.name, "url" : obj.url, "type" : obj.type, "id" : obj.id } );
		}
		$scope.localSto = arr;
	}

	$scope.removeFav = function(id, type){
		localStorage.removeItem(id);
		$("#"+id).removeClass('glyphicon glyphicon-star').addClass('glyphicon glyphicon-star-empty');
		var arr = []
		for(var i = 0; i < localStorage.length; i++){
			var obj = JSON.parse(localStorage.getItem(localStorage.key(i)));
			arr.push({ "name" : obj.name, "url" : obj.url, "type" : obj.type, "id" : obj.id } );
		}
		$scope.localSto = arr;
		showFavs();
	}

	// -----------------------------------loading next/ previous USERS ---------------------
	$scope.loadNextUsers = function () { 
		if(nextUsersPage){ //handling the next page data 
			$.ajax({
				type: "GET", 
				dataType: "JSONP", 
				url: nextUsersPage,
				success: function(nextResponse){
					$scope.userDetails = nextResponse.data;
					$scope.$apply();
					if(nextResponse.paging.next){
						nextUsersPage = nextResponse.paging.next;
					}
					if(nextResponse.paging.previous){
						$("#previousUsers").css({"display" : "inline-block", "visibility" : "visible", "margin-right": "25px"});
						prevUsersPage = nextResponse.paging.previous;
					}
					else{
						$("#previousUsers").css({"display" : "none", "visibility" : "hidden"});
					}
					for(var i = 0; i < nextResponse.data.length; i++){
						if(localStorage.getItem(nextResponse.data[i].id) != null){
							$("#"+nextResponse.data[i].id).removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
						}
					}
				}
			});
		}
	}

	$scope.loadPrevUsers = function () { 
		if(prevUsersPage){ //handling the next page data 
			$.ajax({
				type: "GET", 
				dataType: "JSONP", 
				url: prevUsersPage,
				success: function(prevResponse){
					$scope.userDetails = prevResponse.data;
					$scope.$apply();
					if(prevResponse.paging.next){
						nextUsersPage = prevResponse.paging.next;
					}
					if(prevResponse.paging.previous){
						prevUsersPage = prevResponse.paging.previous;
					}
					else{
						$("#previousUsers").css({"display" : "none", "visibility" : "hidden"});
					}
					for(var i = 0; i < prevResponse.data.length; i++){
						if(localStorage.getItem(prevResponse.data[i].id) != null){
							$("#"+prevResponse.data[i].id).removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
						}
					}
				}
			});
		}
	}
	// -----------------------------------loading next/ previous PAGES---------------------
	$scope.loadNextPages = function () { 
		if(nextPagesPage){ //handling the next page data 
			$.ajax({
				type: "GET", 
				dataType: "JSONP", 
				url: nextPagesPage,
				success: function(nextResponse){
					$scope.pagesDetails = nextResponse.data;
					$scope.$apply();
					if(nextResponse.paging.next){
						nextPagesPage = nextResponse.paging.next;
					}
					if(nextResponse.paging.previous){
						$("#previousPages").css({"display" : "inline-block", "visibility" : "visible", "margin-right": "25px"});
						prevPagesPage = nextResponse.paging.previous;
					}
					else{
						$("#previousPages").css({"display" : "none", "visibility" : "hidden"});
					}
					for(var i = 0; i < nextResponse.data.length; i++){
						if(localStorage.getItem(nextResponse.data[i].id) != null){
							$("#"+nextResponse.data[i].id).removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
						}
					}
				}
			});
		}
	}

	$scope.loadPrevPages = function () { 
		if(prevPagesPage){ //handling the next page data 
			$.ajax({
				type: "GET", 
				dataType: "JSONP", 
				url: prevPagesPage,
				success: function(prevResponse){
					$scope.pagesDetails = prevResponse.data;
					$scope.$apply();
					if(prevResponse.paging.next){
						nextPagesPage = prevResponse.paging.next;
					}
					if(prevResponse.paging.previous){
						prevPagesPage = prevResponse.paging.previous;
					}
					else{
						$("#previousPages").css({"display" : "none", "visibility" : "hidden"});
					}
					for(var i = 0; i < prevResponse.data.length; i++){
						if(localStorage.getItem(prevResponse.data[i].id) != null){
							$("#"+prevResponse.data[i].id).removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
						}
					}
				}
			});
		}
	}

	// -----------------------------------loading next/ previous GROUPS ---------------------
	$scope.loadNextGroups = function () { 
		if(nextGroupsPage){ //handling the next page data 
			$.ajax({
				type: "GET", 
				dataType: "JSONP", 
				url: nextGroupsPage,
				success: function(nextResponse){
					$scope.groupsDetails = nextResponse.data;
					$scope.$apply();
					if(nextResponse.paging.next){
						nextGroupsPage = nextResponse.paging.next;
					}
					if(nextResponse.paging.previous){
						$("#previousGroups").css({"display" : "inline-block", "visibility" : "visible", "margin-right": "25px"});
						prevGroupsPage = nextResponse.paging.previous;
					}
					else{
						$("#previousGroups").css({"display" : "none", "visibility" : "hidden"});
					}
					for(var i = 0; i < nextResponse.data.length; i++){
						if(localStorage.getItem(nextResponse.data[i].id) != null){
							$("#"+nextResponse.data[i].id).removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
						}
					}
				}
			});
		}
	}

	$scope.loadPrevGroups = function () { 
		if(prevGroupsPage){ //handling the next page data 
			$.ajax({
				type: "GET", 
				dataType: "JSONP", 
				url: prevGroupsPage,
				success: function(prevResponse){
					$scope.groupsDetails = prevResponse.data;
					$scope.$apply();
					if(prevResponse.paging.next){
						nextGroupsPage = prevResponse.paging.next;
					}
					if(prevResponse.paging.previous){
						prevGroupsPage = prevResponse.paging.previous;
					}
					else{
						$("#previousGroups").css({"display" : "none", "visibility" : "hidden"});
					}
					for(var i = 0; i < prevResponse.data.length; i++){
						if(localStorage.getItem(prevResponse.data[i].id) != null){
							$("#"+prevResponse.data[i].id).removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
						}
					}
				}
			});
		}
	}

	// -----------------------------------loading next/ previous EVENTS ---------------------
	$scope.loadNextEvents = function () { 
		if(nextEventsPage){ //handling the next page data 
			$.ajax({
				type: "GET", 
				dataType: "JSONP", 
				url: nextEventsPage,
				success: function(nextResponse){
					$scope.eventsDetails = nextResponse.data;
					$scope.$apply();
					//checking for next pages
					if(nextResponse.paging.next){
						nextEventsPage = nextResponse.paging.next;
					}
					else if(typeof nextResponse.paging.next.data == "undefined") {
						$("#nextEvents").css({"display" : "none", "visibility" : "hidden"});
					}
					//checking for previous pages
					if(nextResponse.paging.previous){
						$("#previousEvents").css({"display" : "inline-block", "visibility" : "visible", "margin-right": "25px"});
						prevEventsPage = nextResponse.paging.previous;
					}
					else if(typeof nextResponse.previous.data == "undefined"){
						$("#previousEvents").css({"display" : "none", "visibility" : "hidden"});
					}
					for(var i = 0; i < nextResponse.data.length; i++){
						if(localStorage.getItem(nextResponse.data[i].id) != null){
							$("#"+nextResponse.data[i].id).removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
						}
					}
				}
			});
		}
	}

	$scope.loadPrevEvents = function () { 
		if(prevEventsPage){ //handling the next page data 
			$.ajax({
				type: "GET", 
				dataType: "JSONP", 
				url: prevEventsPage,
				success: function(prevResponse){
					$scope.eventDetails = prevResponse.data;
					$scope.$apply();
					if(prevResponse.paging.next){
						nextEventsPage = prevResponse.paging.next;
					}
					if(prevResponse.paging.previous){
						prevEventsPage = prevResponse.paging.previous;
					}
					else{
						$("#previousEvents").css({"display" : "none", "visibility" : "hidden"});
					}
					for(var i = 0; i < prevResponse.data.length; i++){
						if(localStorage.getItem(prevResponse.data[i].id) != null){
							$("#"+prevResponse.data[i].id).removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
						}
					}
				}
			});
		}
	}

	// -----------------------------------loading next/ previous PLACES ---------------------
	$scope.loadNextPlaces = function () { 
		if(nextPlacesPage){ //handling the next page data 
			$.ajax({
				type: "GET", 
				dataType: "JSONP", 
				url: nextPlacesPage,
				success: function(nextResponse){
					$scope.placesDetails = nextResponse.data;
					$scope.$apply();
					if(nextResponse.paging.next){
						nextPlacesPage = nextResponse.paging.next;
					}
					if(nextResponse.paging.previous){
						$("#previousPlaces").css({"display" : "inline-block", "visibility" : "visible", "margin-right": "25px"});
						prevPlacesPage = nextResponse.paging.previous;
					}
					else{
						$("#previousPlaces").css({"display" : "none", "visibility" : "hidden"});
					}
					for(var i = 0; i < nextResponse.data.length; i++){
						if(localStorage.getItem(nextResponse.data[i].id) != null){
							$("#"+nextResponse.data[i].id).removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
						}
					}
				}
			});
		}
	}

	$scope.loadPrevPlaces = function () { 
		if(prevPlacesPage){ //handling the next page data 
			$.ajax({
				type: "GET", 
				dataType: "JSONP", 
				url: prevPlacesPage,
				success: function(prevResponse){
					$scope.placesDetails = prevResponse.data;
					$scope.$apply();
					if(prevResponse.paging.next){
						nextPlacesPage = prevResponse.paging.next;
					}
					if(prevResponse.paging.previous){
						prevPlacesPage = prevResponse.paging.previous;
					}
					else{
						$("#previousPlaces").css({"display" : "none", "visibility" : "hidden"});
					}
					for(var i = 0; i < prevResponse.data.length; i++){
						if(localStorage.getItem(prevResponse.data[i].id) != null){
							$("#"+prevResponse.data[i].id).removeClass('glyphicon glyphicon-star-empty').addClass('glyphicon glyphicon-star');
						}
					}
				}
			});
		}
	}

	$scope.goBack = function(){
		showUsers();
	}

	$scope.showDetsPics = function(id){
		if($("#body"+id).css('display') == "none"){
			$("#body"+id).css({"display" : "block", "visibility" : "visible"});
			$("."+id).css({"display" : "block", "visibility" : "visible"});
		}
		else{
			$("#body"+id).css({"display" : "none", "visibility" : "hidden"});
			$("." +id).css({"display" : "none", "visibility" : "hidden"});
		}
	}

	$scope.fbPost = function(){
		FB.ui({
			appId: '1828822820692317',
			method: 'feed', 
			picture: fbPic,
			name: fbName, 
			caption: 'FB SEARCH FROM USC CSCI571', 
			}, function(response){
				if(response && !response.error_message){
					alert("Posted successfully");
					console.log("success");
					console.log(response);
				}
				else{
					alert("Not posted.");
				}
		});
	}


});


function showUsers(){
	$(".user").css({"display" : "block", "visibility" : "visible"});
	$(".pages").css({"display" : "none", "visibility" : "hidden"});
	$(".events").css({"display" : "none", "visibility" : "hidden"});
	$(".places").css({"display" : "none", "visibility" : "hidden"});
	$(".groups").css({"display" : "none", "visibility" : "hidden"});
	$(".favs").css({"display" : "none", "visibility" : "hidden"});
	$(".detailsPage").css({"display" : "none", "visibility" : "hidden"});
	hideOtherButtons();
	$(".lowerButtonsUsers").css({"display" : "block", "visibility" : "visible"});
	hideDetailsData();

}

function showPages(){
	$(".user").css({"display" : "none", "visibility" : "hidden"});
	$(".pages").css({"display" : "block", "visibility" : "visible"});
	$(".events").css({"display" : "none", "visibility" : "hidden"});
	$(".places").css({"display" : "none", "visibility" : "hidden"});
	$(".groups").css({"display" : "none", "visibility" : "hidden"});
	$(".favs").css({"display" : "none", "visibility" : "hidden"});
	$(".detailsPage").css({"display" : "none", "visibility" : "hidden"});
	hideOtherButtons();
	if(searchKeyPressed){
		$(".lowerButtonsPages").css({"display" : "block", "visibility" : "visible"});
		$("#nextPages").css({"display" : "inline-block", "visibility" : "visible"});
	}
	hideDetailsData();
}

function showEvents(){
	$(".user").css({"display" : "none", "visibility" : "hidden"});
	$(".pages").css({"display" : "none", "visibility" : "hidden"});
	$(".events").css({"display" : "block", "visibility" : "visible"});
	$(".places").css({"display" : "none", "visibility" : "hidden"});
	$(".groups").css({"display" : "none", "visibility" : "hidden"});
	$(".favs").css({"display" : "none", "visibility" : "hidden"});
	$(".detailsPage").css({"display" : "none", "visibility" : "hidden"});
	hideOtherButtons();
	if(searchKeyPressed){
		$(".lowerButtonsEvents").css({"display" : "block", "visibility" : "visible"});
		$("#nextEvents").css({"display" : "inline-block", "visibility" : "visible"});
	}
	hideDetailsData();
}

function showPlaces(){
	$(".user").css({"display" : "none", "visibility" : "hidden"});
	$(".pages").css({"display" : "none", "visibility" : "hidden"});
	$(".events").css({"display" : "none", "visibility" : "hidden"});
	$(".places").css({"display" : "block", "visibility" : "visible"});
	$(".groups").css({"display" : "none", "visibility" : "hidden"});
	$(".favs").css({"display" : "none", "visibility" : "hidden"});
	$(".detailsPage").css({"display" : "none", "visibility" : "hidden"});
	hideOtherButtons();
	if(searchKeyPressed){
		$(".lowerButtonsPlaces").css({"display" : "block", "visibility" : "visible"});
		$("#nextPlaces").css({"display" : "inline-block", "visibility" : "visible"});		
	}
	hideDetailsData();
}

function showGroups(){
	$(".user").css({"display" : "none", "visibility" : "hidden"});
	$(".pages").css({"display" : "none", "visibility" : "hidden"});
	$(".events").css({"display" : "none", "visibility" : "hidden"});
	$(".places").css({"display" : "none", "visibility" : "hidden"});
	$(".groups").css({"display" : "block", "visibility" : "visible"});
	$(".favs").css({"display" : "none", "visibility" : "hidden"});
	$(".detailsPage").css({"display" : "none", "visibility" : "hidden"});
	hideOtherButtons();
	if(searchKeyPressed){
		$(".lowerButtonsGroups").css({"display" : "block", "visibility" : "visible"});
		$("#nextGroups").css({"display" : "inline-block", "visibility" : "visible"});		
	}
	hideDetailsData();
}

function showFavs(){
	$(".user").css({"display" : "none", "visibility" : "hidden"});
	$(".pages").css({"display" : "none", "visibility" : "hidden"});
	$(".events").css({"display" : "none", "visibility" : "hidden"});
	$(".places").css({"display" : "none", "visibility" : "hidden"});
	$(".groups").css({"display" : "none", "visibility" : "hidden"});
	$(".favs").css({"display" : "block", "visibility" : "visible"});
	$(".detailsPage").css({"display" : "none", "visibility" : "hidden"});	
	hideOtherButtons();
	hideDetailsData();
}

function showDetails(){
	$("#detailsAlbumsData").css({"display" : "block", "visibility" : "visible"});
	$("#detailsPostsData").css({"display" : "block", "visibility" : "visible"});
	$(".lowerButtons").css({"display" : "none", "visibility" : "hidden"});
	$(".user").css({"display" : "none", "visibility" : "hidden"});
	$(".pages").css({"display" : "none", "visibility" : "hidden"});
	$(".events").css({"display" : "none", "visibility" : "hidden"});
	$(".places").css({"display" : "none", "visibility" : "hidden"});
	$(".groups").css({"display" : "none", "visibility" : "hidden"});
	$(".favs").css({"display" : "none", "visibility" : "hidden"});
	$(".detailsPage").css({"display" : "block", "visibility" : "visible"});
	hideOtherButtons();

}

function hideEverything(){
	$(".lowerButtonsUsers").css({"display" : "none", "visibility" : "hidden"});
	$(".lowerButtonsPages").css({"display" : "none", "visibility" : "hidden"});
	$(".lowerButtonsPlaces").css({"display" : "none", "visibility" : "hidden"});
	$(".lowerButtonsEvents").css({"display" : "none", "visibility" : "hidden"});
	$(".lowerButtonsGroups").css({"display" : "none", "visibility" : "hidden"});
	$(".user").css({"display" : "none", "visibility" : "hidden"});
	$(".pages").css({"display" : "none", "visibility" : "hidden"});
	$(".events").css({"display" : "none", "visibility" : "hidden"});
	$(".places").css({"display" : "none", "visibility" : "hidden"});
	$(".groups").css({"display" : "none", "visibility" : "hidden"});
	$(".favs").css({"display" : "none", "visibility" : "hidden"});
	$(".detailsPage").css({"display" : "none", "visibility" : "hidden"});
	hideDetailsData();
}


function hideOtherButtons(){
	$(".lowerButtonsUsers").css({"display" : "none", "visibility" : "hidden"});
	$(".lowerButtonsPages").css({"display" : "none", "visibility" : "hidden"});
	$(".lowerButtonsPlaces").css({"display" : "none", "visibility" : "hidden"});
	$(".lowerButtonsEvents").css({"display" : "none", "visibility" : "hidden"});
	$(".lowerButtonsGroups").css({"display" : "none", "visibility" : "hidden"});
}

function hideDetailsData(){
	$("#detailsAlbumsData").css({"display" : "none", "visibility" : "hidden"});
	$("#detailsPostsData").css({"display" : "none", "visibility" : "hidden"});
}

$(window).unload(function() {
	localStorage.clear();
});
