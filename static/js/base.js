function searchOpen() {
    var search = $('#txtSearch').val()
    var data = {
        search: search
    };
    $.ajax({
        url: '/cheap_pints/search.json',
        data: data,
        dataType: 'jsonp',
        jsonp: 'callback',
        jsonpCallback: 'searchResult'
    });
}


function searchResult(data) {
    console.log(data);
    $("#txtSearch").autocomplete({
        source: data
    });
}
// You pass-in jQuery and then alias it with the $-sign
// So your internal code doesn't change