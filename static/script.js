// you need to add your own mapquest key before running
var view = new ol.View({
    projection: 'EPSG:4326',
    zoom: 5,
    center: [53, 33]
});

var osm = new ol.layer.Tile({
    source: new ol.source.OSM(),
    title: 'osm'
});

var iranWMS = new ol.layer.Tile({
    source: new ol.source.TileWMS({
        url: 'http://localhost:8080/geoserver/wms',
        params: {
            LAYERS: 'cite:Ostan'
        }
    }),
    title: 'iranWMS'
});

var turkeyWMS = new ol.layer.Tile({
    source: new ol.source.TileWMS({
        url: 'http://localhost:8080/geoserver/wms',
        params: {
            LAYERS: 'cite:TUR_adm1'
        }
    }),
    title: 'turkeyWMS'
});

var AfghanistanWMS = new ol.layer.Tile({
    source: new ol.source.TileWMS({
        url: 'http://localhost:8080/geoserver/wms',
        params: {
            LAYERS: 'cite:AFG_adm1'
        }
    }),
    title: 'AfghanistanWMS'
});

// call for overlay message by dom
const container = document.getElementById('popup');
const content = document.getElementById('popup-content');
const closer = document.getElementById('popup-closer');

// define overlay message
const overlay = new ol.Overlay({
    element: container,
    autoPan: {
    },
});

var myControl = new ol.control.Control({ element: document.getElementById('mapChng')});
var zoom = new ol.control.Zoom();
var map = new ol.Map({
    controls: [myControl, zoom],
    target: 'map',
    view: view,
    layers: [osm, iranWMS, turkeyWMS, AfghanistanWMS],
    overlays: [overlay]
});


// define message closing function
closer.onclick = function () {
    overlay.setPosition(undefined);
    closer.blur();
    return false;
};

//add off/on option to enviroment
turkeyWMS.setVisible(false);
AfghanistanWMS.setVisible(false);
const boxLayers = document.querySelectorAll('input[type=checkbox]');
for (let i = 0; i < Object.keys(boxLayers).length; i++) {
    boxLayers[i].addEventListener('change', function () {
        window[boxLayers[i]["value"]].setVisible(boxLayers[i]["checked"])
    })
};

function Get(Url) {
    var Httpreq = new XMLHttpRequest(); //a new request
    Httpreq.open("GET", Url, false);
    Httpreq.send(null);
    return Httpreq.responseText;
};

map.on('singleclick', function (evt) {
    if (osm.getVisible()) {
        content.innerHTML = "";
        const url = `http://www.mapquestapi.com/geocoding/v1/reverse?key={"Your key"}=${evt.coordinate[1].toFixed(6)},${evt.coordinate[0].toFixed(6)}&includeRoadMetadata=true&includeNearestIntersection=true`;
        overlay.setPosition(evt.coordinate);
        var jsonObj = JSON.parse(Get(url));
        const array = [1, 3, 4, 5, 6, "street", "postalCode"];
        array.forEach(function (i) {
            if (typeof (i) === 'number') {
                var node = document.createElement("h4");
                var textnode = document.createTextNode(jsonObj["results"][0]["locations"][0][`adminArea${i}Type`] + ": " + jsonObj["results"][0]["locations"][0][`adminArea${i}`]);
                node.appendChild(textnode);
                content.appendChild(node);
            } else {
                var node = document.createElement("h4");
                var textnode = document.createTextNode(i + ": " + jsonObj["results"][0]["locations"][0][`${i}`]);
                node.appendChild(textnode);
                content.appendChild(node);
            };
        });
    } else {
        overlay.setPosition(evt.coordinate);
        content.innerHTML = "<p style = 'font-size:13px;'> You need to activate open street map layer. </p>";
    }
});