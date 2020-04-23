function searchOpen() {
    var search = $('#txtSearch').val()
    var data = {
        search: search
    };
    $.ajax({
        url: '/cheap_pints/search/',
        data: data,
        dataType: 'jsonp',
        jsonp: 'callback',
        jsonpCallback: 'searchResult'
    });
}


function searchResult(data) {
    $("#txtSearch").autocomplete({
        source: data
    });
}