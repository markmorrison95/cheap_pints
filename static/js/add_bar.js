function initAutocomplete() {
    var autocomplete = new google.maps.places.Autocomplete((document.getElementById('id_barName')), { types: ['establishment'] });
    autocomplete.setFields(
        ['place_id', 'name', 'photos']);

    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.name) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }
        // If the place has a geometry, then present it on a map.
        var id = place.place_id
        var name = place.name;
        name = name.split(',')[0]
        document.getElementById('id_barName').value = name;
        document.getElementById('id_googleId').value = id;
        document.getElementById("submit").disabled = false;
    })
}