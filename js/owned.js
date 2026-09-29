/* Persist owned armor piece ids in localStorage */
(function (global) {
  "use strict";

  var KEY = "totk-armor-owned-v1";

  function loadSet() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return {};
      var arr = JSON.parse(raw);
      if (!Array.isArray(arr)) return {};
      var map = {};
      arr.forEach(function (id) {
        if (typeof id === "string") map[id] = true;
      });
      return map;
    } catch (e) {
      return {};
    }
  }

  function saveSet(map) {
    try {
      localStorage.setItem(KEY, JSON.stringify(Object.keys(map)));
    } catch (e) {
      console.warn("[套装图鉴] 无法保存已拥有状态", e);
    }
  }

  function createOwnedStore() {
    var owned = loadSet();
    var listeners = [];

    function notify() {
      listeners.forEach(function (fn) {
        try {
          fn();
        } catch (e) {
          /* ignore */
        }
      });
    }

    return {
      isOwned: function (id) {
        return !!owned[id];
      },
      setOwned: function (id, value) {
        if (value) owned[id] = true;
        else delete owned[id];
        saveSet(owned);
        notify();
      },
      count: function () {
        return Object.keys(owned).length;
      },
      onChange: function (fn) {
        listeners.push(fn);
      },
    };
  }

  global.TotkOwned = { create: createOwnedStore };
})(window);
