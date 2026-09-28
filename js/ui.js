/* Layer switch + bottom sheet UI */
(function (global) {
  "use strict";

  function $(id) {
    return document.getElementById(id);
  }

  function initUi(options) {
    var onLayerChange = options.onLayerChange;
    var sheet = $("detail-sheet");
    var backdrop = $("sheet-backdrop");
    var closeBtn = $("sheet-close");
    var countEl = $("korok-count");
    var touchStartY = null;

    document.querySelectorAll(".layer-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var layer = btn.getAttribute("data-layer");
        document.querySelectorAll(".layer-btn").forEach(function (b) {
          var active = b === btn;
          b.classList.toggle("is-active", active);
          b.setAttribute("aria-selected", active ? "true" : "false");
        });
        if (onLayerChange) onLayerChange(layer);
      });
    });

    function closeSheet() {
      sheet.classList.remove("is-open");
      sheet.setAttribute("aria-hidden", "true");
      backdrop.hidden = true;
      document.body.classList.remove("sheet-open");
    }

    function openSheet(korok, layerLabel) {
      $("sheet-title").textContent =
        korok.typeLabel + (korok.kind === "carry" ? "（×2）" : "");
      $("sheet-coords").textContent =
        "X " +
        korok.x.toFixed(1) +
        " · Y " +
        korok.y.toFixed(1) +
        " · Z " +
        korok.z.toFixed(1);
      $("sheet-layer").textContent = layerLabel;
      $("sheet-region").textContent = korok.region || "—";
      $("sheet-type").textContent = korok.typeLabel + (korok.typeEn ? " / " + korok.typeEn : "");
      $("sheet-howto").textContent = korok.howToFind || "暂无说明。";
      var note = $("sheet-guide-note");
      if (korok.guideStatus !== "detailed") {
        note.hidden = false;
        note.textContent = "说明为类型模板，细节待补充。";
      } else {
        note.hidden = true;
        note.textContent = "";
      }

      backdrop.hidden = false;
      sheet.classList.add("is-open");
      sheet.setAttribute("aria-hidden", "false");
      document.body.classList.add("sheet-open");
    }

    closeBtn.addEventListener("click", closeSheet);
    backdrop.addEventListener("click", closeSheet);

    sheet.addEventListener(
      "touchstart",
      function (e) {
        if (sheet.scrollTop <= 0) {
          touchStartY = e.touches[0].clientY;
        } else {
          touchStartY = null;
        }
      },
      { passive: true }
    );

    sheet.addEventListener(
      "touchend",
      function (e) {
        if (touchStartY == null) return;
        var dy = e.changedTouches[0].clientY - touchStartY;
        if (dy > 80) closeSheet();
        touchStartY = null;
      },
      { passive: true }
    );

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeSheet();
    });

    return {
      openSheet: openSheet,
      closeSheet: closeSheet,
      setCount: function (visible, total) {
        countEl.textContent = "本层 " + visible + " / 共 " + total;
      },
    };
  }

  global.TotkUi = { init: initUi };
})(window);
