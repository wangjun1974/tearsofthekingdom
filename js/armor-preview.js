/* Stylized Link mannequin with drag-to-spin 360° preview (Three.js) */
(function (global) {
  "use strict";

  function createPreview(container) {
    if (!global.THREE) {
      console.warn("[穿戴预览] Three.js 未加载");
      return null;
    }
    var THREE = global.THREE;
    var width = 0;
    var height = 0;
    var running = false;
    var raf = 0;
    var autoSpin = true;
    var dragging = false;
    var lastX = 0;
    var vel = 0;

    var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setClearColor(0x000000, 0);
    if (THREE.SRGBColorSpace && renderer.outputColorSpace !== undefined) {
      renderer.outputColorSpace = THREE.SRGBColorSpace;
    } else if (renderer.outputEncoding !== undefined && THREE.sRGBEncoding !== undefined) {
      renderer.outputEncoding = THREE.sRGBEncoding;
    }
    container.appendChild(renderer.domElement);
    renderer.domElement.className = "armor-preview-canvas";
    renderer.domElement.setAttribute("aria-label", "林克穿戴预览，左右拖动可旋转");

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(32, 1, 0.1, 50);
    camera.position.set(0, 1.15, 4.2);
    camera.lookAt(0, 0.95, 0);

    var hemi = new THREE.HemisphereLight(0xf0ffe8, 0x2a3a28, 1.05);
    scene.add(hemi);
    var key = new THREE.DirectionalLight(0xffffff, 0.85);
    key.position.set(2.5, 4, 3);
    scene.add(key);
    var fill = new THREE.DirectionalLight(0xa0c8ff, 0.25);
    fill.position.set(-3, 1, -2);
    scene.add(fill);

    var root = new THREE.Group();
    scene.add(root);

    var mats = {
      skin: mat("#e8c4a0"),
      hair: mat("#f2d060"),
      head: mat("#4a6e38"),
      body: mat("#5b7f40"),
      legs: mat("#3a552c"),
      accent: mat("#c4a35a"),
    };

    var parts = buildLink(THREE, mats);
    root.add(parts.group);
    var helmParts = parts.helms;

    function mat(hex) {
      return new THREE.MeshStandardMaterial({
        color: new THREE.Color(hex),
        roughness: 0.72,
        metalness: 0.08,
      });
    }

    function setMatColor(m, hex) {
      if (!m || !hex) return;
      m.color.set(hex);
      m.needsUpdate = true;
    }

    function buildLink(THREE, mats) {
      var g = new THREE.Group();
      function box(w, h, d, m, x, y, z) {
        var mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
        mesh.position.set(x || 0, y || 0, z || 0);
        g.add(mesh);
        return mesh;
      }
      function sphere(r, m, x, y, z, sx, sy, sz) {
        var mesh = new THREE.Mesh(new THREE.SphereGeometry(r, 16, 12), m);
        mesh.position.set(x || 0, y || 0, z || 0);
        mesh.scale.set(sx || 1, sy || 1, sz || 1);
        g.add(mesh);
        return mesh;
      }

      // Legs / boots
      var legL = box(0.28, 0.7, 0.3, mats.legs, -0.18, 0.38, 0);
      var legR = box(0.28, 0.7, 0.3, mats.legs, 0.18, 0.38, 0);
      box(0.3, 0.14, 0.38, mats.accent, -0.18, 0.08, 0.02);
      box(0.3, 0.14, 0.38, mats.accent, 0.18, 0.08, 0.02);

      // Torso + arms
      var torso = box(0.72, 0.85, 0.4, mats.body, 0, 1.05, 0);
      box(0.22, 0.7, 0.22, mats.body, -0.5, 1.0, 0);
      box(0.22, 0.7, 0.22, mats.body, 0.5, 1.0, 0);
      sphere(0.12, mats.skin, -0.5, 0.58, 0);
      sphere(0.12, mats.skin, 0.5, 0.58, 0);

      // Belt
      box(0.76, 0.1, 0.42, mats.accent, 0, 0.72, 0);

      // Neck + head
      box(0.18, 0.16, 0.18, mats.skin, 0, 1.55, 0);
      var head = sphere(0.28, mats.skin, 0, 1.82, 0, 1, 1.05, 1);
      // Ears
      var earGeo = new THREE.ConeGeometry(0.08, 0.22, 6);
      var earL = new THREE.Mesh(earGeo, mats.skin);
      earL.position.set(-0.26, 1.86, 0);
      earL.rotation.z = 0.55;
      g.add(earL);
      var earR = new THREE.Mesh(earGeo, mats.skin);
      earR.position.set(0.26, 1.86, 0);
      earR.rotation.z = -0.55;
      g.add(earR);

      // Hair
      sphere(0.26, mats.hair, 0, 1.95, -0.02, 1.15, 0.7, 1.05);
      box(0.12, 0.28, 0.12, mats.hair, -0.22, 1.7, 0.1);
      box(0.12, 0.28, 0.12, mats.hair, 0.22, 1.7, 0.1);

      // Headwear variants (toggle visibility)
      var helms = {};
      helms.hood = (function () {
        var hg = new THREE.Group();
        var h = new THREE.Mesh(new THREE.SphereGeometry(0.34, 16, 12), mats.head);
        h.scale.set(1.05, 0.95, 1.15);
        h.position.set(0, 1.88, -0.02);
        hg.add(h);
        var cape = box(0.5, 0.35, 0.2, mats.head, 0, 1.55, -0.22);
        hg.add(cape);
        g.add(hg);
        return hg;
      })();
      helms.helm = (function () {
        var hg = new THREE.Group();
        var h = new THREE.Mesh(new THREE.SphereGeometry(0.33, 16, 10), mats.head);
        h.scale.set(1.1, 0.85, 1.1);
        h.position.set(0, 1.92, 0);
        hg.add(h);
        var brim = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.06, 16), mats.accent);
        brim.position.set(0, 1.78, 0);
        hg.add(brim);
        g.add(hg);
        return hg;
      })();
      helms.mask = (function () {
        var hg = new THREE.Group();
        var m = box(0.5, 0.28, 0.2, mats.head, 0, 1.82, 0.18);
        hg.add(m);
        var top = box(0.42, 0.16, 0.36, mats.head, 0, 2.02, 0);
        hg.add(top);
        g.add(hg);
        return hg;
      })();
      helms.band = (function () {
        var hg = new THREE.Group();
        var b = new THREE.Mesh(new THREE.TorusGeometry(0.28, 0.05, 8, 20), mats.head);
        b.rotation.x = Math.PI / 2;
        b.position.set(0, 1.95, 0);
        hg.add(b);
        var knot = box(0.12, 0.12, 0.18, mats.accent, 0.28, 1.9, 0);
        hg.add(knot);
        g.add(hg);
        return hg;
      })();
      helms.crown = (function () {
        var hg = new THREE.Group();
        var c = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.32, 0.18, 10), mats.head);
        c.position.set(0, 2.05, 0);
        hg.add(c);
        for (var i = 0; i < 5; i++) {
          var spike = box(0.06, 0.16, 0.06, mats.accent, Math.sin((i / 5) * Math.PI * 2) * 0.22, 2.18, Math.cos((i / 5) * Math.PI * 2) * 0.22);
          hg.add(spike);
        }
        g.add(hg);
        return hg;
      })();
      helms.none = new THREE.Group();
      g.add(helms.none);

      return { group: g, helms: helms, torso: torso, legL: legL, legR: legR, head: head };
    }

    function setStyle(style) {
      var key;
      for (key in helmParts) {
        if (Object.prototype.hasOwnProperty.call(helmParts, key)) {
          helmParts[key].visible = key === (style || "hood");
        }
      }
      if (!helmParts[style || "hood"]) {
        helmParts.hood.visible = true;
      }
    }

    function applyPreview(preview) {
      var p = preview || {};
      setMatColor(mats.skin, p.skin);
      setMatColor(mats.hair, p.hair);
      setMatColor(mats.head, p.head);
      setMatColor(mats.body, p.body);
      setMatColor(mats.legs, p.legs);
      setMatColor(mats.accent, p.accent);
      setStyle(p.style || "hood");
    }

    function resize() {
      var rect = container.getBoundingClientRect();
      width = Math.max(1, Math.floor(rect.width));
      height = Math.max(1, Math.floor(rect.height));
      var dpr = Math.min(global.devicePixelRatio || 1, 2);
      renderer.setPixelRatio(dpr);
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
    }

    function frame() {
      if (!running) return;
      if (!dragging && autoSpin) {
        root.rotation.y += 0.008;
      } else if (!dragging && Math.abs(vel) > 0.0005) {
        root.rotation.y += vel;
        vel *= 0.95;
      }
      renderer.render(scene, camera);
      raf = requestAnimationFrame(frame);
    }

    function start() {
      if (running) return;
      running = true;
      resize();
      raf = requestAnimationFrame(frame);
    }

    function stop() {
      running = false;
      if (raf) cancelAnimationFrame(raf);
      raf = 0;
    }

    function onPointerDown(e) {
      dragging = true;
      autoSpin = false;
      vel = 0;
      lastX = e.clientX != null ? e.clientX : e.touches[0].clientX;
      container.classList.add("is-dragging");
    }
    function onPointerMove(e) {
      if (!dragging) return;
      var x = e.clientX != null ? e.clientX : (e.touches && e.touches[0] ? e.touches[0].clientX : lastX);
      var dx = x - lastX;
      lastX = x;
      var delta = dx * 0.01;
      root.rotation.y += delta;
      vel = delta;
      if (e.cancelable) e.preventDefault();
    }
    function onPointerUp() {
      dragging = false;
      container.classList.remove("is-dragging");
      // resume gentle auto-spin after a pause
      setTimeout(function () {
        if (!dragging) autoSpin = true;
      }, 1800);
    }

    var el = renderer.domElement;
    el.addEventListener("pointerdown", onPointerDown);
    global.addEventListener("pointermove", onPointerMove, { passive: false });
    global.addEventListener("pointerup", onPointerUp);
    el.addEventListener(
      "touchmove",
      function (e) {
        if (dragging && e.cancelable) e.preventDefault();
      },
      { passive: false }
    );

    var ro = null;
    if (global.ResizeObserver) {
      ro = new ResizeObserver(function () {
        if (running) resize();
      });
      ro.observe(container);
    }

    return {
      showSet: function (set) {
        applyPreview((set && set.preview) || null);
        start();
        resize();
      },
      stop: stop,
      start: start,
      resize: resize,
      dispose: function () {
        stop();
        el.removeEventListener("pointerdown", onPointerDown);
        global.removeEventListener("pointermove", onPointerMove);
        global.removeEventListener("pointerup", onPointerUp);
        if (ro) ro.disconnect();
        renderer.dispose();
        if (renderer.domElement.parentNode) {
          renderer.domElement.parentNode.removeChild(renderer.domElement);
        }
      },
    };
  }

  global.TotkArmorPreview = { create: createPreview };
})(window);
