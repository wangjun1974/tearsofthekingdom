/* TotK Leaflet map: Zelda Dungeon CRS + layered tiles */
(function (global) {
  "use strict";

  var MAP_SIZE_COORDS = 12032;
  var TILE_SIZE = 564;
  var MAP_SIZE_PIXELS = 36096; // 564 * 64
  var MAX_ZOOM = 6;

  var TILE_BASE =
    "https://raw.githubusercontent.com/zeldadungeon/maps/develop/public/totk/tiles";

  var LAYER_LABELS = {
    surface: "地表",
    sky: "天空",
    depths: "地底",
  };

  function createTotkCrs() {
    var scale = TILE_SIZE / MAP_SIZE_COORDS;
    var offset = TILE_SIZE / 2;
    return L.extend({}, L.CRS.Simple, {
      transformation: new L.Transformation(scale, offset, -scale, offset),
    });
  }

  /** Game coords (x, y height, z) -> Leaflet LatLng (lat=-z, lng=x) */
  function gameToLatLng(x, z) {
    return L.latLng(-z, x);
  }

  function createMap(elementId) {
    var crs = createTotkCrs();
    var bounds = L.latLngBounds(
      crs.pointToLatLng(L.point(0, MAP_SIZE_PIXELS), MAX_ZOOM),
      crs.pointToLatLng(L.point(MAP_SIZE_PIXELS, 0), MAX_ZOOM)
    );

    var map = L.map(elementId, {
      crs: crs,
      minZoom: 0,
      maxZoom: MAX_ZOOM,
      zoom: MAX_ZOOM - 2,
      center: gameToLatLng(0, 0),
      maxBounds: bounds.pad(0.35),
      zoomControl: false,
      attributionControl: false,
      preferCanvas: true,
    });

    L.control
      .zoom({
        position: "bottomright",
      })
      .addTo(map);

    var tileLayers = {};
    ["surface", "sky", "depths"].forEach(function (layer) {
      tileLayers[layer] = L.tileLayer(TILE_BASE + "/" + layer + "/{z}/{x}_{y}.jpg", {
        tileSize: TILE_SIZE,
        minZoom: 0,
        maxZoom: MAX_ZOOM,
        bounds: bounds,
        noWrap: true,
        keepBuffer: 1,
      });
    });

    tileLayers.surface.addTo(map);

    return {
      map: map,
      tileLayers: tileLayers,
      bounds: bounds,
      currentLayer: "surface",
      setLayer: function (layerName) {
        if (!tileLayers[layerName] || layerName === this.currentLayer) {
          return this.currentLayer;
        }
        map.removeLayer(tileLayers[this.currentLayer]);
        tileLayers[layerName].addTo(map);
        this.currentLayer = layerName;
        return layerName;
      },
      gameToLatLng: gameToLatLng,
      layerLabel: function (layer) {
        return LAYER_LABELS[layer] || layer;
      },
    };
  }

  global.TotkMap = {
    create: createMap,
    gameToLatLng: gameToLatLng,
    LAYER_LABELS: LAYER_LABELS,
  };
})(window);
