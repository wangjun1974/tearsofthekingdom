/* Armor set list, detail sheet, map locate */
(function (global) {
  "use strict";

  var SLOT_LABEL = { head: "头", body: "身", legs: "腿" };
  var STAR_LABEL = { star1: "★", star2: "★★", star3: "★★★", star4: "★★★★" };

  function $(id) {
    return document.getElementById(id);
  }

  function createArmorUi(options) {
    var totkMap = options.totkMap;
    var ownedStore = options.ownedStore;
    var onLocate = options.onLocate;
    var onBackToList = options.onBackToList;

    var sets = [];
    var hideOwned = false;
    var query = "";
    var listEl = $("armor-list");
    var searchEl = $("armor-search");
    var countEl = $("korok-count");
    var sheet = $("detail-sheet");
    var backdrop = $("sheet-backdrop");
    var korokBlocks = $("sheet-korok");
    var armorBlocks = $("sheet-armor");
    var tempMarker = null;
    var currentSet = null;

    function pieceOwnedCount(set) {
      var n = 0;
      (set.pieces || []).forEach(function (p) {
        if (ownedStore.isOwned(p.id)) n += 1;
      });
      return n;
    }

    function filteredSets() {
      var q = query.trim().toLowerCase();
      return sets.filter(function (s) {
        if (hideOwned && pieceOwnedCount(s) >= (s.pieces || []).length) return false;
        if (!q) return true;
        if ((s.name || "").toLowerCase().indexOf(q) !== -1) return true;
        return (s.pieces || []).some(function (p) {
          return (p.name || "").toLowerCase().indexOf(q) !== -1;
        });
      });
    }

    function updateCount() {
      var totalPieces = 0;
      sets.forEach(function (s) {
        totalPieces += (s.pieces || []).length;
      });
      countEl.textContent =
        "套装 " +
        filteredSets().length +
        "/" +
        sets.length +
        " · 已有 " +
        ownedStore.count() +
        "/" +
        totalPieces;
    }

    function renderList() {
      listEl.innerHTML = "";
      var list = filteredSets();
      if (!list.length) {
        var empty = document.createElement("p");
        empty.className = "armor-empty";
        empty.textContent = "没有匹配的套装";
        listEl.appendChild(empty);
        updateCount();
        return;
      }
      list.forEach(function (s) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "armor-item";
        var owned = pieceOwnedCount(s);
        var total = (s.pieces || []).length;
        var tags = [];
        if (s.amiibo) tags.push("amiibo");
        if (!s.upgradable) tags.push("不可强化");
        btn.innerHTML =
          '<span class="armor-item-name">' +
          escapeHtml(s.name) +
          "</span>" +
          '<span class="armor-item-meta">' +
          owned +
          "/" +
          total +
          (tags.length ? " · " + tags.join(" · ") : "") +
          "</span>";
        btn.addEventListener("click", function () {
          openSet(s);
        });
        listEl.appendChild(btn);
      });
      updateCount();
    }

    function escapeHtml(str) {
      return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }

    function formatMats(mats) {
      if (!mats || !mats.length) return "—";
      return mats
        .map(function (m) {
          return m.item + " ×" + m.count;
        })
        .join("、");
    }

    function formatUpgrades(set, piece) {
      var ups = (piece && piece.upgrades) || set.upgrades;
      if (!set.upgradable || !ups) {
        return '<p class="armor-note">不可强化。</p>';
      }
      var rupees = ups.rupees || { star1: 10, star2: 50, star3: 200, star4: 500 };
      var html = '<ul class="armor-upgrades">';
      ["star1", "star2", "star3", "star4"].forEach(function (key) {
        if (!ups[key]) return;
        html +=
          "<li><strong>" +
          STAR_LABEL[key] +
          "</strong>（" +
          (rupees[key] || "?") +
          " 卢比）：" +
          escapeHtml(formatMats(ups[key])) +
          "</li>";
      });
      html += "</ul>";
      return html;
    }

    function clearTempMarker() {
      if (tempMarker) {
        totkMap.map.removeLayer(tempMarker);
        tempMarker = null;
      }
    }

    function locatePiece(piece) {
      var loc = piece.location;
      if (!loc) return;
      clearTempMarker();
      var layer = loc.layer || "surface";
      totkMap.setLayer(layer);
      document.querySelectorAll(".layer-btn").forEach(function (b) {
        var active = b.getAttribute("data-layer") === layer;
        b.classList.toggle("is-active", active);
        b.setAttribute("aria-selected", active ? "true" : "false");
      });
      var ll = totkMap.gameToLatLng(loc.x, loc.z);
      tempMarker = L.marker(ll, {
        title: piece.name,
        icon: L.divIcon({
          className: "armor-pin",
          html: '<span class="armor-pin-dot"></span>',
          iconSize: [18, 18],
          iconAnchor: [9, 9],
        }),
      }).addTo(totkMap.map);
      closeSheet();
      if (onLocate) onLocate(piece, loc);
      setTimeout(function () {
        totkMap.map.invalidateSize();
        totkMap.map.setView(ll, Math.max(totkMap.map.getZoom(), 5), { animate: true });
      }, 50);
    }

    function openSet(set) {
      currentSet = set;
      korokBlocks.hidden = true;
      armorBlocks.hidden = false;
      $("sheet-found-row").hidden = true;

      $("sheet-title").textContent = set.name;
      var bonus = set.setBonus || {};
      var bonusText = bonus.level2 || "无";
      if (bonus.note) bonusText += "（" + bonus.note + "）";

      var body = $("sheet-armor-body");
      var html = "";
      html += '<p class="armor-desc">' + escapeHtml(set.description || "") + "</p>";
      html +=
        '<dl class="sheet-meta armor-meta"><div><dt>套装效果</dt><dd>' +
        escapeHtml(bonusText) +
        "</dd></div><div><dt>可强化</dt><dd>" +
        (set.upgradable ? "是" : "否") +
        "</dd></div></dl>";

      html += '<section class="armor-pieces"><h3>部件</h3>';
      (set.pieces || []).forEach(function (p) {
        html += '<article class="armor-piece" data-piece-id="' + escapeHtml(p.id) + '">';
        html +=
          "<header><strong>" +
          escapeHtml(SLOT_LABEL[p.slot] || p.slot) +
          " · " +
          escapeHtml(p.name) +
          "</strong></header>";
        if (p.defense && p.defense.length) {
          html +=
            '<p class="armor-def">防御：' +
            escapeHtml(p.defense.join(" → ")) +
            "</p>";
        }
        if (p.effect) {
          html += '<p class="armor-effect">效果：' + escapeHtml(p.effect) + "</p>";
        }
        html += "<p>" + escapeHtml(p.howToGet || "暂无获取说明。") + "</p>";
        html +=
          '<label class="owned-check"><input type="checkbox" data-owned="' +
          escapeHtml(p.id) +
          '"' +
          (ownedStore.isOwned(p.id) ? " checked" : "") +
          " /> 已拥有</label>";
        if (p.location) {
          html +=
            '<button type="button" class="locate-btn" data-locate="' +
            escapeHtml(p.id) +
            '">在地图上显示</button>';
        }
        html += "</article>";
      });
      html += "</section>";

      html += "<section class=\"armor-upgrade-block\"><h3>升级材料</h3>";
      html += formatUpgrades(set, null);
      html +=
        '<p class="armor-note">强化在大妖精之泉进行；解锁的大妖精数量决定可强化星级上限。</p>';
      html += "</section>";

      body.innerHTML = html;

      body.querySelectorAll("[data-owned]").forEach(function (input) {
        input.addEventListener("change", function () {
          ownedStore.setOwned(input.getAttribute("data-owned"), input.checked);
          renderList();
        });
      });
      body.querySelectorAll("[data-locate]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var id = btn.getAttribute("data-locate");
          var piece = (set.pieces || []).find(function (p) {
            return p.id === id;
          });
          if (piece) locatePiece(piece);
        });
      });

      backdrop.hidden = false;
      sheet.classList.add("is-open");
      sheet.setAttribute("aria-hidden", "false");
      document.body.classList.add("sheet-open");
    }

    function closeSheet() {
      sheet.classList.remove("is-open");
      sheet.setAttribute("aria-hidden", "true");
      backdrop.hidden = true;
      document.body.classList.remove("sheet-open");
      currentSet = null;
    }

    searchEl.addEventListener("input", function () {
      query = searchEl.value || "";
      renderList();
    });

    $("armor-back-map").addEventListener("click", function () {
      clearTempMarker();
      if (onBackToList) onBackToList();
    });

    return {
      load: function (payload) {
        sets = (payload && payload.sets) || [];
        renderList();
        return payload.meta || {};
      },
      renderList: renderList,
      setHideOwned: function (value) {
        hideOwned = !!value;
        renderList();
      },
      closeSheet: closeSheet,
      clearTempMarker: clearTempMarker,
      updateCount: updateCount,
    };
  }

  global.TotkArmors = { create: createArmorUi };
})(window);
