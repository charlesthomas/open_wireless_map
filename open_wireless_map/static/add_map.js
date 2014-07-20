var map;

function init() {
    var options = {
        zoom: 16,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('canvas'), options);
    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = new google.maps.LatLng(position.coords.latitude,
                                             position.coords.longitude);
            map.setCenter(pos);
            updatePosition(pos);
            var marker = new google.maps.Marker({
                position: pos,
                map: map,
                draggable: true
            });
            google.maps.event.addListener(marker, 'dragend', function() {
                updatePosition(marker.getPosition());
            });
        }, function() {window.location='/err';});
    } else {window.location='/err';}
}

function updatePosition(position) {
    document.getElementById('latitude').value = position.lat().toString();
    document.getElementById('longitude').value = position.lng().toString();
    document.getElementById('submit').disabled = false;
}

google.maps.event.addDomListener(window, 'load', init);
