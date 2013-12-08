var list = {}
var storeid = 0
window.onload = function() {	
	 store();
}

function store() {
	console.log("here");
	$('#inven').click(function(){
		var retrievedObject = localStorage.getItem('storeid');
		storeid = JSON.parse(retrievedObject)
		console.log(storeid)
		document.location.href="http://127.0.0.1:8000/Customer/inventory_list/"+storeid;				
	});	
}

function maps() {
			$.ajax({url: "http://127.0.0.1:8000/Customer/maps",
					type: 'GET',
					contentType: "application/json; charset=utf-8",
					dataType: "json",
					data:JSON.stringify({
						"abcd":'abcd'}),
					success: function (data) {
						list = data
						var map;
						var i;
						var marker;
						var abcd = [];
						var infowindow = null;		
						var geocoder1 = new google.maps.Geocoder();
						console.log(data.stores.length); //checking
						console.log(data.stores[0].lat);
						console.log(data.stores[0].long);
						console.log(data.stores[1].address);
						console.log(data.stores[1].city);
						
						
						for (i = 0; i < data.stores.length; i++) 
						{ 
							geocoder1.geocode({ 'address':data.stores[i].address}, function(results, status) 
							{	
								if (status == google.maps.GeocoderStatus.OK) 
								{
									var a = results[0].geometry.location;
									var b = results[0].formatted_address;
									var c = results[0].address_components;
									marker = new google.maps.Marker
									({
										position: new google.maps.LatLng(a.lat(),a.lng()),
										map: map											 
									});			  
									  google.maps.event.addListener(marker, 'click', function ()
									  {
										console.log("format",b);
										console.log("address_components",c);
										var lat = a.lat();
										var lng = a.lng();	
										console.log("lat and long",lat,lng);
											$.ajax({url: "http://127.0.0.1:8000/Customer/render_storeid",
											type: 'POST',
											contentType: "application/json; charset=utf-8",
											dataType: "json",
											data:JSON.stringify({"format":b}),
											success: function (data) {
												storeid = data.storeid;
												localStorage.setItem('storeid', JSON.stringify(storeid));
												var retrievedObject = localStorage.getItem('storeid');
												console.log('retrievedObject after set: ', JSON.parse(retrievedObject))
												document.location.href="http://127.0.0.1:8000/Customer/customer_home";			
											}
											});	
									  });
								}
								else  
								{
									alert("Geocode was not successful for the following reason: " + status);
								}
							});
						}
  
						var map = new google.maps.Map(document.getElementById('map'), {
							zoom: 2,
							center: new google.maps.LatLng(49.8705556, 8.6494444),
							mapTypeId: google.maps.MapTypeId.ROADMAP
						});					
			}
	});
}	