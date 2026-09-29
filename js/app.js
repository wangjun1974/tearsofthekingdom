/* App bootstrap: korok map + armor guide modes */
(function () {
  "use strict";

  var foundStore = TotkFound.create();
  var ownedStore = TotkOwned.create();
  var totkMap = TotkMap.create("map");
  var mode = "korok";
  var markers = null;
  var armors = null;
  var ui = null;

  var brandEl = document.getElementById("brand-title");
  var armorPanel = document.getElementById("armor-panel");
  var armorBackBtn = document.getElementById("armor-back-map");
  var hideFoundText = document.getElementById("hide-found-text");
  var hideFoundCheckbox = document.getElementById("hide-found");

  function setMode(next) {
    mode = next;
    document.querySelectorAll(".mode-btn").forEach(function (btn) {
      var active = btn.getAttribute("data-mode") === mode;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-selected", active ? "true" : "false");
    });

    if (ui) ui.closeSheet();
    if (armors) {
      armors.clearTempMarker();
    }
    armorBackBtn.hidden = true;

    if (mode === "korok") {
      brandEl.textContent = "呀哈哈地图";
      hideFoundText.textContent = "隐藏已找到";
      armorPanel.hidden = true;
      document.body.classList.remove("mode-armor", "armor-locating");
      if (markers) {
        markers.setVisible(true);
        markers.setHideFound(hideFoundCheckbox.checked);
      }
    } else {
      brandEl.textContent = "套装图鉴";
      hideFoundText.textContent = "隐藏已拥有";
      armorPanel.hidden = false;
      document.body.classList.add("mode-armor");
      document.body.classList.remove("armor-locating");
      if (markers) markers.setVisible(false);
      if (armors) {
        armors.setHideOwned(hideFoundCheckbox.checked);
        armors.renderList();
      }
    }
  }

  ui = TotkUi.init({
    isFound: function (id) {
      return foundStore.isFound(id);
    },
    onLayerChange: function (layer) {
      totkMap.setLayer(layer);
      if (mode === "korok" && markers) {
        markers.showLayer(layer);
        ui.closeSheet();
      }
    },
    onFoundChange: function (id, value) {
      foundStore.setFound(id, value);
      if (markers) markers.refresh();
    },
    onHideFoundChange: function (hide) {
      if (mode === "korok") {
        if (markers) markers.setHideFound(hide);
      } else if (armors) {
        armors.setHideOwned(hide);
      }
    },
    onSheetClose: function () {
      if (armors) armors.closeSheet();
    },
  });

  markers = TotkMarkers.create(totkMap, ui, foundStore);

  armors = TotkArmors.create({
    totkMap: totkMap,
    ownedStore: ownedStore,
    onLocate: function () {
      armorPanel.hidden = true;
      armorBackBtn.hidden = false;
      document.body.classList.add("armor-locating");
      document.body.classList.remove("mode-armor");
      setTimeout(function () {
        totkMap.map.invalidateSize();
      }, 50);
    },
    onBackToList: function () {
      armorPanel.hidden = false;
      armorBackBtn.hidden = true;
      document.body.classList.add("mode-armor");
      document.body.classList.remove("armor-locating");
      if (armors) armors.clearTempMarker();
    },
  });

  document.querySelectorAll(".mode-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      setMode(btn.getAttribute("data-mode"));
    });
  });

  ownedStore.onChange(function () {
    if (mode === "armor" && armors) armors.updateCount();
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

  fetch("data/armors.json")
    .then(function (res) {
      if (!res.ok) throw new Error("无法加载套装数据 (" + res.status + ")");
      return res.json();
    })
    .then(function (data) {
      var meta = armors.load(data);
      console.info("[套装图鉴] 已加载", meta.totalSets, "套");
    })
    .catch(function (err) {
      console.error(err);
    });
})();
