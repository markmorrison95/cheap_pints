function searchOpen() {
    var search = $('#txtSearch').val()
    var data = {
        search: search
    };
    $.ajax({
        url: '/cheap_pints/barsearch/',
        data: data,
        dataType: 'jsonp',
        jsonp: 'callback',
        jsonpCallback: 'searchResult'
    });
}


function searchResult(data) {
    $("#txtSearch").autocomplete({
        autoFocus: true,
        source: data
    });
}