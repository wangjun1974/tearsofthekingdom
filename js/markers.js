/* Korok markers + clustering */
(function (global) {
  "use strict";

  var ICON = L.divIcon({
    className: "korok-icon",
    html: '<img src="assets/korok.png" alt="" width="28" height="28" />',
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });

  function createMarkerController(totkMap, ui) {
    var cluster = L.markerClusterGroup({
      showCoverageOnHover: false,
      maxClusterRadius: 50,
      spiderfyOnMaxZoom: true,
      disableClusteringAtZoom: 6,
      animate: false,
    });
    totkMap.map.addLayer(cluster);

    var allKoroks = [];
    var byLayer = { surface: [], sky: [], depths: [] };

    function clear() {
      cluster.clearLayers();
    }

    function showLayer(layerName) {
      clear();
      var list = byLayer[layerName] || [];
      var markers = list.map(function (k) {
        var m = L.marker(totkMap.gameToLatLng(k.x, k.z), {
          icon: ICON,
          keyboard: true,
          title: k.typeLabel,
        });
        m.on("click", function () {
          ui.openSheet(k, totkMap.layerLabel(k.layer));
        });
        return m;
      });
      cluster.addLayers(markers);
      ui.setCount(list.length, allKoroks.length);
    }

    return {
      load: function (payload) {
        allKoroks = payload.koroks || [];
        byLayer = { surface: [], sky: [], depths: [] };
        allKoroks.forEach(function (k) {
          if (byLayer[k.layer]) byLayer[k.layer].push(k);
          else byLayer.surface.push(k);
        });
        showLayer(totkMap.currentLayer);
        return payload.meta || {};
      },
      showLayer: showLayer,
      getAll: function () {
        return allKoroks;
      },
    };
  }

  global.TotkMarkers = { create: createMarkerController };
})(window);
