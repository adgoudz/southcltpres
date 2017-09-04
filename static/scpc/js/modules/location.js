
import mapStyle from 'data/location/map-style';

const mapOptions = {
    center: {lat: 35.045339, lng: -80.848933},
    zoom: 14,
    styles: mapStyle,
    fullscreenControl: false,
    mapTypeControl: false,
};

const iconOptions = {
    path: 'M11 2c-3.9 0-7 3.1-7 7 0 5.3 7 13 7 13 0 0 7-7.7 7-13 0-3.9-3.1-7-7-7Zm0 9.5c-1.4 0-2.5-1.1-2.5-2.5 0-1.4 1.1-2.5 2.5-2.5 1.4 0 2.5 1.1 2.5 2.5 0 1.4-1.1 2.5-2.5 2.5Z',
    fillColor: '#006D62',
    strokeColor: '#006D62',
    fillOpacity: 1.0,
    strokeOpacity: 0,
    scale: 2.8,
};

const markerOptions = {
    position: {lat: 35.037379, lng: -80.856044},
    title: 'Ballantyne Elementary',
    icon: iconOptions,
};

window.initMap = function() {
    let map = new google.maps.Map(document.getElementById('map'), mapOptions);

    iconOptions['anchor'] = new google.maps.Point(11, 22); // Ideally this should be definable above

    let marker = new google.maps.Marker(markerOptions);
    marker.setMap(map);
};