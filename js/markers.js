/* Korok markers + clustering */
(function (global) {
  "use strict";

  function makeIcon(found) {
    return L.divIcon({
      className: "korok-icon" + (found ? " is-found" : ""),
      html: '<img src="assets/korok.png" alt="" width="28" height="28" />',
      iconSize: [28, 28],
      iconAnchor: [14, 14],
    });
  }

  function createMarkerController(totkMap, ui, foundStore) {
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
    var hideFound = false;

    function clear() {
      cluster.clearLayers();
    }

    function layerList(layerName) {
      return byLayer[layerName] || [];
    }

    function visibleList(layerName) {
      var list = layerList(layerName);
      if (!hideFound) return list;
      return list.filter(function (k) {
        return !foundStore.isFound(k.id);
      });
    }

    function updateCount(layerName) {
      var layer = layerList(layerName);
      var visible = visibleList(layerName);
      ui.setCount(visible.length, layer.length, foundStore.count(), allKoroks.length);
    }

    function showLayer(layerName) {
      clear();
      var list = visibleList(layerName);
      var markers = list.map(function (k) {
        var found = foundStore.isFound(k.id);
        var m = L.marker(totkMap.gameToLatLng(k.x, k.z), {
          icon: makeIcon(found),
          keyboard: true,
          title: k.typeLabel + (found ? "（已找到）" : ""),
          opacity: found ? 0.7 : 1,
        });
        m.on("click", function () {
          ui.openSheet(k, totkMap.layerLabel(k.layer));
        });
        return m;
      });
      cluster.addLayers(markers);
      updateCount(layerName);
    }

    function refresh() {
      showLayer(totkMap.currentLayer);
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
      setHideFound: function (value) {
        hideFound = !!value;
        refresh();
      },
      refresh: refresh,
      getAll: function () {
        return allKoroks;
      },
    };
  }

  global.TotkMarkers = { create: createMarkerController };
})(window);
