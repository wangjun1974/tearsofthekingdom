/* TotK Link wear preview — procedural high-fidelity approximation (no ripped assets) */
(function (global) {
  "use strict";

  var DEFAULT_PREVIEW = {
    skin: "#e8c4a0",
    hair: "#e8c84a",
    head: "#3f6b32",
    body: "#4f7d3c",
    legs: "#2f4f28",
    accent: "#c4a35a",
    undershirt: "#e8e0d0",
    eyes: "#3a6cb0",
    style: "hood",
    outfit: "tunic",
    hairVisible: true,
    metalness: 0.05,
    roughness: 0.78,
  };

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
    renderer.domElement.setAttribute(
      "aria-label",
      "林克穿戴原造型预览，左右拖动可旋转"
    );

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(30, 1, 0.1, 50);
    camera.position.set(0, 1.2, 4.6);
    camera.lookAt(0, 1.05, 0);

    scene.add(new THREE.HemisphereLight(0xfff4e0, 0x2a3a40, 0.95));
    var key = new THREE.DirectionalLight(0xffffff, 1.05);
    key.position.set(2.8, 5, 3.2);
    scene.add(key);
    var rim = new THREE.DirectionalLight(0x88aaff, 0.35);
    rim.position.set(-3, 2, -2.5);
    scene.add(rim);
    var fill = new THREE.DirectionalLight(0xffe8c8, 0.35);
    fill.position.set(-1.5, 1.2, 4);
    scene.add(fill);

    var root = new THREE.Group();
    scene.add(root);

    var mats = {
      skin: std("#e8c4a0", 0.02, 0.62),
      hair: std("#e8c84a", 0.04, 0.55),
      head: std("#3f6b32", 0.05, 0.78),
      body: std("#4f7d3c", 0.05, 0.78),
      legs: std("#2f4f28", 0.05, 0.78),
      accent: std("#c4a35a", 0.35, 0.45),
      undershirt: std("#e8e0d0", 0.02, 0.85),
      eyeWhite: std("#f4f4f0", 0.0, 0.4),
      eyeIris: std("#3a6cb0", 0.05, 0.35),
      eyePupil: std("#1a1a22", 0.0, 0.5),
      lip: std("#d09080", 0.02, 0.55),
      brow: std("#c4a030", 0.04, 0.55),
    };

    var figure = buildFigure(THREE, mats);
    root.add(figure.group);

    function std(hex, metal, rough) {
      return new THREE.MeshStandardMaterial({
        color: new THREE.Color(hex),
        metalness: metal,
        roughness: rough,
      });
    }

    function setColor(m, hex) {
      if (!m || !hex) return;
      m.color.set(hex);
      m.needsUpdate = true;
    }

    function setSurf(m, metal, rough) {
      if (!m) return;
      if (metal != null) m.metalness = metal;
      if (rough != null) m.roughness = rough;
      m.needsUpdate = true;
    }

    function buildFigure(THREE, mats) {
      var g = new THREE.Group();
      var layers = {
        hair: new THREE.Group(),
        helms: {},
        outfits: {},
        cape: new THREE.Group(),
      };

      function add(parent, mesh) {
        parent.add(mesh);
        return mesh;
      }
      function box(parent, w, h, d, m, x, y, z, rx, ry, rz) {
        var mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
        mesh.position.set(x || 0, y || 0, z || 0);
        if (rx) mesh.rotation.x = rx;
        if (ry) mesh.rotation.y = ry;
        if (rz) mesh.rotation.z = rz;
        return add(parent, mesh);
      }
      function sph(parent, r, m, x, y, z, sx, sy, sz) {
        var mesh = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 16), m);
        mesh.position.set(x || 0, y || 0, z || 0);
        mesh.scale.set(sx || 1, sy || 1, sz || 1);
        return add(parent, mesh);
      }
      function cyl(parent, rt, rb, h, m, x, y, z, rx, ry, rz, seg) {
        var mesh = new THREE.Mesh(
          new THREE.CylinderGeometry(rt, rb, h, seg || 14),
          m
        );
        mesh.position.set(x || 0, y || 0, z || 0);
        if (rx) mesh.rotation.x = rx;
        if (ry) mesh.rotation.y = ry;
        if (rz) mesh.rotation.z = rz;
        return add(parent, mesh);
      }

      // --- Body core (TotK-like young adult proportions) ---
      // Boots / lower legs
      box(g, 0.26, 0.55, 0.28, mats.legs, -0.17, 0.36, 0);
      box(g, 0.26, 0.55, 0.28, mats.legs, 0.17, 0.36, 0);
      box(g, 0.28, 0.12, 0.36, mats.accent, -0.17, 0.08, 0.03);
      box(g, 0.28, 0.12, 0.36, mats.accent, 0.17, 0.08, 0.03);
      // Feet tip
      box(g, 0.26, 0.08, 0.16, mats.legs, -0.17, 0.06, 0.18);
      box(g, 0.26, 0.08, 0.16, mats.legs, 0.17, 0.06, 0.18);

      // Hips
      box(g, 0.62, 0.28, 0.34, mats.legs, 0, 0.72, 0);

      // Torso undershirt always present lightly
      box(g, 0.58, 0.55, 0.32, mats.undershirt, 0, 1.12, 0);

      // Default tunic outfit group
      var tunic = new THREE.Group();
      box(tunic, 0.7, 0.78, 0.4, mats.body, 0, 1.12, 0);
      // tunic skirt
      box(tunic, 0.74, 0.28, 0.42, mats.body, 0, 0.72, 0.02);
      // sleeves
      box(tunic, 0.24, 0.55, 0.24, mats.body, -0.48, 1.12, 0);
      box(tunic, 0.24, 0.55, 0.24, mats.body, 0.48, 1.12, 0);
      // belt + buckle
      box(tunic, 0.74, 0.1, 0.43, mats.accent, 0, 0.78, 0);
      box(tunic, 0.14, 0.12, 0.08, mats.accent, 0, 0.78, 0.22);
      layers.outfits.tunic = tunic;
      g.add(tunic);

      // Armor plate outfit
      var armor = new THREE.Group();
      box(armor, 0.74, 0.82, 0.44, mats.body, 0, 1.14, 0);
      box(armor, 0.82, 0.22, 0.5, mats.accent, 0, 1.42, 0.02);
      box(armor, 0.28, 0.62, 0.28, mats.body, -0.52, 1.12, 0);
      box(armor, 0.28, 0.62, 0.28, mats.body, 0.52, 1.12, 0);
      // pauldrons
      sph(armor, 0.2, mats.accent, -0.55, 1.45, 0, 1.2, 0.8, 1);
      sph(armor, 0.2, mats.accent, 0.55, 1.45, 0, 1.2, 0.8, 1);
      box(armor, 0.76, 0.12, 0.46, mats.accent, 0, 0.78, 0);
      layers.outfits.armor = armor;
      g.add(armor);

      // Open chest / spaulder (Desert Voe style)
      var open = new THREE.Group();
      box(open, 0.5, 0.2, 0.36, mats.undershirt, 0, 1.35, 0);
      // spaulder
      box(open, 0.42, 0.18, 0.5, mats.body, -0.28, 1.42, 0.05, 0, 0, 0.2);
      box(open, 0.18, 0.55, 0.18, mats.skin, -0.48, 1.05, 0);
      box(open, 0.18, 0.55, 0.18, mats.skin, 0.48, 1.05, 0);
      // wrap pants already from legs mat on hips - add sash
      box(open, 0.7, 0.35, 0.38, mats.legs, 0, 0.85, 0);
      box(open, 0.72, 0.1, 0.4, mats.accent, 0, 1.0, 0);
      layers.outfits.open = open;
      g.add(open);

      // Full body suit (rubber / stealth / yiga)
      var suit = new THREE.Group();
      box(suit, 0.68, 0.9, 0.38, mats.body, 0, 1.1, 0);
      box(suit, 0.24, 0.7, 0.24, mats.body, -0.48, 1.05, 0);
      box(suit, 0.24, 0.7, 0.24, mats.body, 0.48, 1.05, 0);
      box(suit, 0.7, 0.35, 0.38, mats.legs, 0, 0.7, 0);
      layers.outfits.suit = suit;
      g.add(suit);

      // Robe (mystic)
      var robe = new THREE.Group();
      box(robe, 0.8, 1.15, 0.48, mats.body, 0, 1.0, 0);
      box(robe, 0.28, 0.7, 0.28, mats.body, -0.5, 1.15, 0);
      box(robe, 0.28, 0.7, 0.28, mats.body, 0.5, 1.15, 0);
      layers.outfits.robe = robe;
      g.add(robe);

      // Barbarian / bare midriff
      var barb = new THREE.Group();
      box(barb, 0.55, 0.25, 0.34, mats.body, 0, 1.35, 0);
      box(barb, 0.5, 0.35, 0.32, mats.skin, 0, 1.05, 0);
      box(barb, 0.22, 0.55, 0.22, mats.skin, -0.48, 1.1, 0);
      box(barb, 0.22, 0.55, 0.22, mats.skin, 0.48, 1.1, 0);
      // bone accents
      box(barb, 0.7, 0.12, 0.4, mats.accent, 0, 0.78, 0);
      box(barb, 0.08, 0.35, 0.08, mats.accent, -0.35, 1.4, 0.15);
      box(barb, 0.08, 0.35, 0.08, mats.accent, 0.35, 1.4, 0.15);
      layers.outfits.barbarian = barb;
      g.add(barb);

      // Hands
      sph(g, 0.11, mats.skin, -0.48, 0.62, 0);
      sph(g, 0.11, mats.skin, 0.48, 0.62, 0);

      // Neck + head
      cyl(g, 0.12, 0.14, 0.16, mats.skin, 0, 1.58, 0);
      sph(g, 0.3, mats.skin, 0, 1.88, 0.02, 0.95, 1.05, 0.95);

      // Jaw / chin slightly
      sph(g, 0.16, mats.skin, 0, 1.72, 0.12, 1.1, 0.7, 0.9);

      // Pointed Hylian ears
      var earGeo = new THREE.ConeGeometry(0.07, 0.28, 7);
      var earL = new THREE.Mesh(earGeo, mats.skin);
      earL.position.set(-0.28, 1.9, 0.02);
      earL.rotation.z = 0.65;
      earL.rotation.y = 0.25;
      g.add(earL);
      var earR = new THREE.Mesh(earGeo, mats.skin);
      earR.position.set(0.28, 1.9, 0.02);
      earR.rotation.z = -0.65;
      earR.rotation.y = -0.25;
      g.add(earR);

      // Face: brows, eyes, nose, mouth
      box(g, 0.1, 0.03, 0.04, mats.brow, -0.1, 1.95, 0.26);
      box(g, 0.1, 0.03, 0.04, mats.brow, 0.1, 1.95, 0.26);
      sph(g, 0.055, mats.eyeWhite, -0.1, 1.9, 0.27, 1.1, 0.9, 0.6);
      sph(g, 0.055, mats.eyeWhite, 0.1, 1.9, 0.27, 1.1, 0.9, 0.6);
      sph(g, 0.035, mats.eyeIris, -0.1, 1.9, 0.3);
      sph(g, 0.035, mats.eyeIris, 0.1, 1.9, 0.3);
      sph(g, 0.018, mats.eyePupil, -0.1, 1.9, 0.32);
      sph(g, 0.018, mats.eyePupil, 0.1, 1.9, 0.32);
      // nose
      box(g, 0.06, 0.08, 0.07, mats.skin, 0, 1.84, 0.3);
      // mouth
      box(g, 0.1, 0.025, 0.03, mats.lip, 0, 1.74, 0.28);

      // Classic TotK hair (blonde layered)
      sph(layers.hair, 0.32, mats.hair, 0, 2.05, -0.02, 1.15, 0.75, 1.1);
      // bangs
      box(layers.hair, 0.18, 0.16, 0.12, mats.hair, -0.12, 1.98, 0.22, 0.4);
      box(layers.hair, 0.18, 0.16, 0.12, mats.hair, 0.12, 1.98, 0.22, 0.4);
      box(layers.hair, 0.22, 0.14, 0.1, mats.hair, 0, 2.0, 0.24);
      // sideburns / cheek hair
      box(layers.hair, 0.1, 0.22, 0.1, mats.hair, -0.26, 1.82, 0.12);
      box(layers.hair, 0.1, 0.22, 0.1, mats.hair, 0.26, 1.82, 0.12);
      // back mullet-ish
      box(layers.hair, 0.28, 0.35, 0.16, mats.hair, 0, 1.85, -0.22);
      g.add(layers.hair);

      // Headwear
      layers.helms.hood = (function () {
        var hg = new THREE.Group();
        var hood = new THREE.Mesh(new THREE.SphereGeometry(0.36, 18, 14), mats.head);
        hood.scale.set(1.08, 0.92, 1.2);
        hood.position.set(0, 1.95, -0.04);
        hg.add(hood);
        box(hg, 0.55, 0.4, 0.22, mats.head, 0, 1.62, -0.24);
        // face opening shade
        box(hg, 0.42, 0.08, 0.1, mats.head, 0, 1.78, 0.2);
        g.add(hg);
        return hg;
      })();

      layers.helms.helm = (function () {
        var hg = new THREE.Group();
        var dome = new THREE.Mesh(new THREE.SphereGeometry(0.34, 16, 12), mats.head);
        dome.scale.set(1.12, 0.82, 1.12);
        dome.position.set(0, 2.0, 0);
        hg.add(dome);
        cyl(hg, 0.4, 0.4, 0.07, mats.accent, 0, 1.82, 0);
        // visor
        box(hg, 0.5, 0.12, 0.18, mats.accent, 0, 1.9, 0.22);
        g.add(hg);
        return hg;
      })();

      layers.helms.mask = (function () {
        var hg = new THREE.Group();
        box(hg, 0.52, 0.32, 0.22, mats.head, 0, 1.88, 0.2);
        box(hg, 0.44, 0.18, 0.4, mats.head, 0, 2.05, 0);
        // eye slits
        box(hg, 0.14, 0.06, 0.04, mats.accent, -0.12, 1.9, 0.32);
        box(hg, 0.14, 0.06, 0.04, mats.accent, 0.12, 1.9, 0.32);
        g.add(hg);
        return hg;
      })();

      layers.helms.band = (function () {
        var hg = new THREE.Group();
        var band = new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.045, 8, 24), mats.head);
        band.rotation.x = Math.PI / 2;
        band.position.set(0, 1.98, 0);
        hg.add(band);
        box(hg, 0.14, 0.1, 0.22, mats.accent, 0.3, 1.92, 0);
        g.add(hg);
        return hg;
      })();

      layers.helms.crown = (function () {
        var hg = new THREE.Group();
        cyl(hg, 0.3, 0.34, 0.2, mats.head, 0, 2.08, 0);
        for (var i = 0; i < 6; i++) {
          var a = (i / 6) * Math.PI * 2;
          box(hg, 0.05, 0.18, 0.05, mats.accent, Math.sin(a) * 0.24, 2.22, Math.cos(a) * 0.24);
        }
        g.add(hg);
        return hg;
      })();

      layers.helms.feather = (function () {
        var hg = new THREE.Group();
        // Snowquill headdress: circlet + feathers
        var band = new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.04, 8, 20), mats.accent);
        band.rotation.x = Math.PI / 2;
        band.position.set(0, 1.98, 0);
        hg.add(band);
        box(hg, 0.08, 0.45, 0.08, mats.head, -0.05, 2.25, -0.05, 0, 0, -0.3);
        box(hg, 0.08, 0.5, 0.08, mats.head, 0.08, 2.28, -0.02, 0, 0, 0.25);
        box(hg, 0.06, 0.35, 0.06, mats.accent, 0, 2.2, 0.05);
        g.add(hg);
        return hg;
      })();

      layers.helms.none = new THREE.Group();
      g.add(layers.helms.none);

      // Cape (optional)
      box(layers.cape, 0.7, 0.9, 0.08, mats.head, 0, 1.05, -0.28);
      layers.cape.visible = false;
      g.add(layers.cape);

      // Hide all outfits/helms initially
      Object.keys(layers.outfits).forEach(function (k) {
        layers.outfits[k].visible = false;
      });
      Object.keys(layers.helms).forEach(function (k) {
        layers.helms[k].visible = false;
      });
      layers.outfits.tunic.visible = true;
      layers.helms.hood.visible = true;

      return { group: g, layers: layers };
    }

    function applyPreview(raw) {
      var p = {};
      var k;
      for (k in DEFAULT_PREVIEW) {
        if (Object.prototype.hasOwnProperty.call(DEFAULT_PREVIEW, k)) {
          p[k] = DEFAULT_PREVIEW[k];
        }
      }
      if (raw) {
        for (k in raw) {
          if (Object.prototype.hasOwnProperty.call(raw, k)) p[k] = raw[k];
        }
      }

      setColor(mats.skin, p.skin);
      setColor(mats.hair, p.hair);
      setColor(mats.head, p.head);
      setColor(mats.body, p.body);
      setColor(mats.legs, p.legs);
      setColor(mats.accent, p.accent);
      setColor(mats.undershirt, p.undershirt || "#e8e0d0");
      setColor(mats.eyeIris, p.eyes || "#3a6cb0");
      setColor(mats.brow, p.hair);

      var metal = p.metalness != null ? p.metalness : 0.05;
      var rough = p.roughness != null ? p.roughness : 0.78;
      setSurf(mats.head, metal, rough);
      setSurf(mats.body, metal, rough);
      setSurf(mats.legs, metal, rough);
      setSurf(mats.accent, Math.min(1, metal + 0.25), Math.max(0.25, rough - 0.2));

      figure.layers.hair.visible = p.hairVisible !== false;

      var outfit = p.outfit || "tunic";
      Object.keys(figure.layers.outfits).forEach(function (key) {
        figure.layers.outfits[key].visible = key === outfit;
      });
      if (!figure.layers.outfits[outfit]) {
        figure.layers.outfits.tunic.visible = true;
      }

      var style = p.style || "hood";
      Object.keys(figure.layers.helms).forEach(function (key) {
        figure.layers.helms[key].visible = key === style;
      });
      if (!figure.layers.helms[style]) {
        figure.layers.helms.hood.visible = true;
      }

      figure.layers.cape.visible = !!p.cape;
      if (p.cape) {
        setColor(mats.head, p.head);
      }
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
        root.rotation.y += 0.01;
      } else if (!dragging && Math.abs(vel) > 0.0004) {
        root.rotation.y += vel;
        vel *= 0.94;
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
      var x =
        e.clientX != null
          ? e.clientX
          : e.touches && e.touches[0]
            ? e.touches[0].clientX
            : lastX;
      var dx = x - lastX;
      lastX = x;
      var delta = dx * 0.012;
      root.rotation.y += delta;
      vel = delta;
      if (e.cancelable) e.preventDefault();
    }
    function onPointerUp() {
      dragging = false;
      container.classList.remove("is-dragging");
      setTimeout(function () {
        if (!dragging) autoSpin = true;
      }, 1600);
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
