/* Persist found Koroks in localStorage */
(function (global) {
  "use strict";

  var KEY = "totk-korok-found-v1";

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
      console.warn("[呀哈哈地图] 无法保存已找到状态", e);
    }
  }

  function createFoundStore() {
    var found = loadSet();
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
      isFound: function (id) {
        return !!found[id];
      },
      setFound: function (id, value) {
        if (value) found[id] = true;
        else delete found[id];
        saveSet(found);
        notify();
      },
      toggle: function (id) {
        this.setFound(id, !this.isFound(id));
        return this.isFound(id);
      },
      count: function () {
        return Object.keys(found).length;
      },
      onChange: function (fn) {
        listeners.push(fn);
      },
    };
  }

  global.TotkFound = { create: createFoundStore };
})(window);
