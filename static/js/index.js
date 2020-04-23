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
    window.location.href = 'bars/?lat=' + lat + '&lng=' + lng;
}

function getLatLong() {
    var address = document.getElementById("postcodeInputBox").value;
    var result = "";
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'address': address, 'region': 'uk' }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var lat = results[0].geometry.location.lat();
            var lng = results[0].geometry.location.lng();
            window.location.href = 'bars/?lat=' + lat + '&lng=' + lng;
        } else {
            alert('Unable to locate postcode')
        }
    });
}