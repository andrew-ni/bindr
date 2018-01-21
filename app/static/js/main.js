// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
var map, infoWindow;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 6
  });

  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: new google.maps.LatLng(-33.92, 151.25),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });

  var infowindow = new google.maps.InfoWindow();

  var marker, i;

  for (i = 0; i < eventsJSON.length; i++) {  
    marker = new google.maps.Marker({
      position: new google.maps.LatLng(parseFloat(eventsJSON[i]['lat']), parseFloat(eventsJSON[i]['long'])),
      map: map
    });

    google.maps.event.addListener(marker, 'click', (function(marker, i) {
      return function() {
        infowindow.setContent(
          '<div style="text-align:left;">'+
          '<b>Where:</b> '+eventsJSON[i]['loc_name']+
          '<br/><b>Subject:</b> '+eventsJSON[i]['subject']+
          '<br/><b>Date:</b> '+eventsJSON[i]['date']+
          '<br/><b>Start:</b> '+eventsJSON[i]['start']+
          '<br/><b>End:</b> '+eventsJSON[i]['end']+
          '<br/><b>Desc:</b> '+eventsJSON[i]['desc']+
          '</div>'
        );
        infowindow.open(map, marker);
      }
    })(marker, i));
  }

  infoWindow = new google.maps.InfoWindow;

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      marker = new google.maps.Marker({
        position: pos,
        icon: {
          path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
          scale: 4
        },
        map: map
      });

      infoWindow.setPosition(pos);
      infoWindow.setContent('You are here!');
      infoWindow.open(map);
      map.setCenter(pos);
    }, function() {
      handleLocationError(true, infoWindow, map.getCenter());
    });
  } else {
    handleLocationError(false, infoWindow, map.getCenter());
  }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
  infoWindow.open(map);
}