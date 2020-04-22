function initMap() {
    var map = new google.maps.Map(document.getElementById('map-container-google-9'), {
        center: new google.maps.LatLng(0, 0),
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        zoom: 15
    });
    google.maps.event.addListener(map, 'bounds_changed', function() {
        var bounds = map.getBounds();
    });
    var service = new google.maps.places.PlacesService(map);
    var bar = document.getElementById("barId").value;
    service.getDetails({
        placeId: bar
    }, function(place, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {

            // Create marker
            var marker = new google.maps.Marker({
                map: map,
                position: place.geometry.location
            });

            // Center map on place location
            map.setCenter(place.geometry.location);
            google.maps.event.trigger(map, 'resize');
        }
    })
}