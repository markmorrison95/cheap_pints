function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Location is not supported by this browser.");
    }
}

function showPosition(position) {
    var lat = position.coords.latitude.toString();
    var lng = position.coords.longitude.toString();
    var userLocation = lat + ',' + lng;
    window.location.href = 'bars/' + userLocation + '/';
}

function getLatLong() {
    var address = document.getElementById("postcodeInputBox").value;
    var result = "";
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'address': address, 'region': 'uk' }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var lat = results[0].geometry.location.lat();
            var lng = results[0].geometry.location.lng();
            var userLocation = lat + ',' + lng;
            window.location.href = 'bars/' + userLocation + '/';
        } else {
            alert('Unable to locate postcode')
        }
    });
}