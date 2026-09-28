/* App bootstrap */
(function () {
  "use strict";

  var foundStore = TotkFound.create();
  var totkMap = TotkMap.create("map");
  var markers;

  var ui = TotkUi.init({
    isFound: function (id) {
      return foundStore.isFound(id);
    },
    onLayerChange: function (layer) {
      totkMap.setLayer(layer);
      markers.showLayer(layer);
      ui.closeSheet();
    },
    onFoundChange: function (id, value) {
      foundStore.setFound(id, value);
      markers.refresh();
    },
    onHideFoundChange: function (hide) {
      markers.setHideFound(hide);
    },
  });

  markers = TotkMarkers.create(totkMap, ui, foundStore);

  foundStore.onChange(function () {
    /* count refresh handled by markers.refresh callers */
  });

  fetch("data/koroks.json")
    .then(function (res) {
      if (!res.ok) throw new Error("无法加载呀哈哈数据 (" + res.status + ")");
      return res.json();
    })
    .then(function (data) {
      var meta = markers.load(data);
      if (meta && meta.total != null) {
        console.info(
          "[呀哈哈地图] 已加载",
          meta.total,
          "个；详述",
          meta.detailed,
          "；分层",
          meta.byLayer,
          "；已找到",
          foundStore.count()
        );
      }
    })
    .catch(function (err) {
      console.error(err);
      document.getElementById("korok-count").textContent = "数据加载失败";
      alert("呀哈哈数据加载失败。请通过本地静态服务器打开本页（不要用 file://）。");
    });
})();
