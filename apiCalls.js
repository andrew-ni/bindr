var currLocation;

function getLocation()
{
	if (navigator.geolocation) 
	{
		navigator.geolocation.getCurrentPosition(function(position) 
		{
            		currLocation = 
			{
              			lat: position.coords.latitude,
              			lng: position.coords.longitude
            		};
          	});
        } 
	else 
	{
         	// Browser doesn't support Geolocation
         	//  handleLocationError(false, infoWindow, map.getCenter());
        }
}

function displayMap()
{
	//get nearest location
	var locations = [
      	['Bondi Beach', -33.890542, 151.274856, 4],
      	['Coogee Beach', -33.923036, 151.259052, 5],
      	['Cronulla Beach', -34.028249, 151.157507, 3],
      	['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
      	['Maroubra Beach', -33.950198, 151.259302, 1]
    	];

    	var map = new google.maps.Map(document.getElementById('map'), 
	{
      		zoom: 10,
		// center around your current location and set zoom to city view
      		center: new google.maps.LatLng(-33.92, 151.25),
      		mapTypeId: google.maps.MapTypeId.ROADMAP
    	});

    	var infowindow = new google.maps.InfoWindow();

    	var marker, i;

    	for (i = 0; i < locations.length; i++) 
	{ 
      		marker = new google.maps.Marker({
        	position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        	map: map
      		});

      		google.maps.event.addListener(marker, 'hover', (function(marker, i) 
		{
        		return function() 
			{
          			infowindow.setContent(locations[i][0]);
          			infowindow.open(map, marker);
        		}
      		})(marker, i));
    	}
}
getLocation();
displayMap();

