var map;

function init() {
    var options = {
        zoom: 4,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('canvas'), options);
    var pos = new google.maps.LatLng("39.30029918615029", "-95.888671875");
    map.setCenter(pos);
    google.maps.event.addListener(map, 'bounds_changed', (function() {
        var timer;
        return function() {
            clearTimeout(timer);
            timer = setTimeout(boundsChanged, 200);
        }
    }()));
}

function updateMap(data) {
    for(i in data) { ( function(i) {
        var lat = data[i].location.coordinates[1];
        var lon = data[i].location.coordinates[0];
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(lat, lon),
            map: map,
        });
        google.maps.event.addListener(marker);
    } )(i) }
}

function getCoords() {
    bounds = map.getBounds();
    coords = "north=";
    coords += bounds.getNorthEast().lat();
    coords += "&east=";
    coords += bounds.getNorthEast().lng();
    coords += "&south=";
    coords += bounds.getSouthWest().lat();
    coords += "&west=";
    coords += bounds.getSouthWest().lng();
    return coords;
}

function boundsChanged() {
    $.get("/api/list?" + getCoords()).done(function(data) {
        updateMap(JSON.parse(data));
    }, 'json');
}

google.maps.event.addDomListener(window, 'load', init);
