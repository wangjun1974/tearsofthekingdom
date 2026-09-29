/* TotK Link 2D front-view wear preview (SVG; no ripped sprites; no 360°) */
(function (global) {
  "use strict";

  var DEFAULT = {
    skin: "#e8c4a0",
    hair: "#e8c84a",
    eyes: "#3a6cb0",
    head: "#3f6b32",
    body: "#4f7d3c",
    legs: "#2f4f28",
    accent: "#c4a35a",
    undershirt: "#e8e0d0",
    style: "hood",
    outfit: "tunic",
    hairVisible: true,
    metalness: 0.05,
    roughness: 0.78,
    weapon: null,
  };

  function mergePreview(raw) {
    var p = {};
    var k;
    for (k in DEFAULT) {
      if (Object.prototype.hasOwnProperty.call(DEFAULT, k)) p[k] = DEFAULT[k];
    }
    if (raw) {
      for (k in raw) {
        if (Object.prototype.hasOwnProperty.call(raw, k)) p[k] = raw[k];
      }
    }
    return p;
  }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
  }

  function clothFilter(id, roughness) {
    var blur = roughness > 0.7 ? 0.15 : 0.05;
    return (
      '<filter id="' +
      id +
      '" x="-10%" y="-10%" width="120%" height="120%">' +
      '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" result="n"/>' +
      '<feDiffuseLighting in="n" lighting-color="#ffffff" surfaceScale="' +
      (roughness > 0.6 ? "0.6" : "0.25") +
      '"><feDistantLight azimuth="45" elevation="55"/></feDiffuseLighting>' +
      '<feComposite in2="SourceGraphic" operator="in"/>' +
      '<feBlend in="SourceGraphic" mode="multiply" result="m"/>' +
      '<feGaussianBlur in="m" stdDeviation="' +
      blur +
      '"/>' +
      "</filter>"
    );
  }

  function metalShine(id) {
    return (
      '<linearGradient id="' +
      id +
      '" x1="0" y1="0" x2="1" y2="1">' +
      '<stop offset="0%" stop-color="#ffffff" stop-opacity="0.45"/>' +
      '<stop offset="45%" stop-color="#ffffff" stop-opacity="0"/>' +
      '<stop offset="100%" stop-color="#000000" stop-opacity="0.25"/>' +
      "</linearGradient>"
    );
  }

  function buildSvg(p, setName) {
    var metal = p.metalness >= 0.35;
    var skin = esc(p.skin);
    var hair = esc(p.hair);
    var eyes = esc(p.eyes);
    var head = esc(p.head);
    var body = esc(p.body);
    var legs = esc(p.legs);
    var accent = esc(p.accent);
    var shirt = esc(p.undershirt || "#e8e0d0");
    var fillBody = metal ? "url(#metalBody)" : body;
    var fillHead = metal ? "url(#metalHead)" : head;
    var fillLegs = metal ? "url(#metalLegs)" : legs;

    var hairLayer = "";
    if (p.hairVisible !== false) {
      hairLayer =
        '<g id="hair">' +
        '<ellipse cx="100" cy="48" rx="28" ry="18" fill="' +
        hair +
        '"/>' +
        '<path d="M78 55 Q70 78 76 92" stroke="' +
        hair +
        '" stroke-width="10" fill="none" stroke-linecap="round"/>' +
        '<path d="M122 55 Q130 78 124 92" stroke="' +
        hair +
        '" stroke-width="10" fill="none" stroke-linecap="round"/>' +
        '<path d="M85 58 Q100 72 115 58" fill="' +
        hair +
        '"/>' +
        '<path d="M88 70 Q100 50 112 70 L108 62 Q100 54 92 62 Z" fill="' +
        hair +
        '"/>' +
        '<rect x="86" y="78" width="8" height="18" rx="3" fill="' +
        hair +
        '"/>' +
        '<rect x="106" y="78" width="8" height="18" rx="3" fill="' +
        hair +
        '"/>' +
        "</g>";
    }

    var headwear = buildHeadwear(p.style, head, accent, fillHead);
    var outfit = buildOutfit(p.outfit, body, legs, accent, shirt, skin, fillBody, fillLegs, metal);
    var weapon = buildWeapon(p.weapon, accent, body);

    return (
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 320" class="armor-preview-svg" role="img" aria-label="' +
      esc(setName || "林克穿戴") +
      '">' +
      "<defs>" +
      clothFilter("cloth", p.roughness || 0.78) +
      metalShine("metalBody") +
      metalShine("metalHead") +
      metalShine("metalLegs") +
      '<linearGradient id="metalBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="' +
      body +
      '"/><stop offset="100%" stop-color="' +
      accent +
      '" stop-opacity="0.85"/></linearGradient>' +
      '<linearGradient id="metalHead" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="' +
      head +
      '"/><stop offset="100%" stop-color="' +
      accent +
      '"/></linearGradient>' +
      '<linearGradient id="metalLegs" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="' +
      legs +
      '"/><stop offset="100%" stop-color="' +
      accent +
      '" stop-opacity="0.7"/></linearGradient>' +
      '<radialGradient id="bgGlow" cx="50%" cy="70%" r="55%"><stop offset="0%" stop-color="#c8e07a" stop-opacity="0.18"/><stop offset="100%" stop-color="#0f1a12" stop-opacity="0"/></radialGradient>' +
      "</defs>" +
      '<rect width="200" height="320" fill="url(#bgGlow)"/>' +
      // boots
      '<rect x="72" y="278" width="22" height="28" rx="4" fill="' +
      fillLegs +
      '"/>' +
      '<rect x="106" y="278" width="22" height="28" rx="4" fill="' +
      fillLegs +
      '"/>' +
      '<rect x="70" y="298" width="26" height="10" rx="3" fill="' +
      accent +
      '"/>' +
      '<rect x="104" y="298" width="26" height="10" rx="3" fill="' +
      accent +
      '"/>' +
      // legs
      '<rect x="74" y="210" width="20" height="72" rx="6" fill="' +
      fillLegs +
      '"/>' +
      '<rect x="106" y="210" width="20" height="72" rx="6" fill="' +
      fillLegs +
      '"/>' +
      outfit +
      // neck
      '<rect x="92" y="118" width="16" height="14" rx="4" fill="' +
      skin +
      '"/>' +
      // head
      '<ellipse cx="100" cy="88" rx="26" ry="30" fill="' +
      skin +
      '"/>' +
      // ears (Hylian pointed)
      '<path d="M74 88 L62 70 L76 82 Z" fill="' +
      skin +
      '"/>' +
      '<path d="M126 88 L138 70 L124 82 Z" fill="' +
      skin +
      '"/>' +
      // face
      '<rect x="88" y="82" width="8" height="3" rx="1" fill="' +
      hair +
      '"/>' +
      '<rect x="104" y="82" width="8" height="3" rx="1" fill="' +
      hair +
      '"/>' +
      '<ellipse cx="90" cy="90" rx="4.5" ry="5" fill="#f4f4f0"/>' +
      '<ellipse cx="110" cy="90" rx="4.5" ry="5" fill="#f4f4f0"/>' +
      '<circle cx="90" cy="90" r="2.6" fill="' +
      eyes +
      '"/>' +
      '<circle cx="110" cy="90" r="2.6" fill="' +
      eyes +
      '"/>' +
      '<circle cx="90.5" cy="90" r="1.1" fill="#1a1a22"/>' +
      '<circle cx="110.5" cy="90" r="1.1" fill="#1a1a22"/>' +
      '<path d="M98 94 L102 100 L98 100 Z" fill="' +
      skin +
      '" stroke="' +
      accent +
      '" stroke-opacity="0.15" stroke-width="0.5"/>' +
      '<rect x="94" y="106" width="12" height="3" rx="1.5" fill="#d09080"/>' +
      hairLayer +
      headwear +
      weapon +
      "</svg>"
    );
  }

  function buildHeadwear(style, head, accent, fillHead) {
    switch (style) {
      case "none":
        return "";
      case "helm":
        return (
          '<g id="helm">' +
          '<path d="M72 88 Q72 48 100 46 Q128 48 128 88 L120 92 Q100 70 80 92 Z" fill="' +
          fillHead +
          '"/>' +
          '<rect x="74" y="86" width="52" height="8" rx="2" fill="' +
          accent +
          '"/>' +
          '<rect x="82" y="78" width="36" height="10" rx="2" fill="' +
          accent +
          '" opacity="0.85"/>' +
          "</g>"
        );
      case "mask":
        return (
          '<g id="mask">' +
          '<rect x="78" y="78" width="44" height="28" rx="8" fill="' +
          fillHead +
          '"/>' +
          '<rect x="84" y="86" width="12" height="6" rx="2" fill="' +
          accent +
          '"/>' +
          '<rect x="104" y="86" width="12" height="6" rx="2" fill="' +
          accent +
          '"/>' +
          '<rect x="86" y="58" width="28" height="24" rx="6" fill="' +
          fillHead +
          '"/>' +
          "</g>"
        );
      case "band":
        return (
          '<g id="band">' +
          '<rect x="74" y="68" width="52" height="10" rx="4" fill="' +
          fillHead +
          '"/>' +
          '<rect x="122" y="66" width="14" height="12" rx="3" fill="' +
          accent +
          '"/>' +
          "</g>"
        );
      case "crown":
        return (
          '<g id="crown">' +
          '<path d="M78 70 L84 52 L92 66 L100 48 L108 66 L116 52 L122 70 Z" fill="' +
          fillHead +
          '"/>' +
          '<circle cx="84" cy="52" r="3" fill="' +
          accent +
          '"/>' +
          '<circle cx="100" cy="48" r="3.5" fill="' +
          accent +
          '"/>' +
          '<circle cx="116" cy="52" r="3" fill="' +
          accent +
          '"/>' +
          "</g>"
        );
      case "feather":
        return (
          '<g id="feather">' +
          '<rect x="74" y="66" width="52" height="9" rx="4" fill="' +
          accent +
          '"/>' +
          '<path d="M96 66 Q88 30 100 28 Q108 40 104 66 Z" fill="' +
          head +
          '"/>' +
          '<path d="M104 66 Q112 34 118 32 Q120 48 110 66 Z" fill="' +
          head +
          '" opacity="0.9"/>' +
          '<path d="M92 66 Q80 38 78 36 Q86 50 96 66 Z" fill="' +
          accent +
          '" opacity="0.85"/>' +
          "</g>"
        );
      case "hood":
      default:
        return (
          '<g id="hood">' +
          '<path d="M70 92 Q68 48 100 42 Q132 48 130 92 L118 100 Q100 78 82 100 Z" fill="' +
          fillHead +
          '"/>' +
          '<path d="M78 100 Q100 88 122 100 L118 130 Q100 120 82 130 Z" fill="' +
          fillHead +
          '"/>' +
          "</g>"
        );
    }
  }

  function buildOutfit(outfit, body, legs, accent, shirt, skin, fillBody, fillLegs, metal) {
    switch (outfit) {
      case "armor":
        return (
          '<g id="outfit-armor">' +
          '<rect x="64" y="130" width="72" height="88" rx="10" fill="' +
          fillBody +
          '"/>' +
          '<rect x="60" y="128" width="80" height="22" rx="6" fill="' +
          accent +
          '"/>' +
          '<ellipse cx="62" cy="140" rx="14" ry="12" fill="' +
          accent +
          '"/>' +
          '<ellipse cx="138" cy="140" rx="14" ry="12" fill="' +
          accent +
          '"/>' +
          '<rect x="48" y="138" width="18" height="58" rx="6" fill="' +
          fillBody +
          '"/>' +
          '<rect x="134" y="138" width="18" height="58" rx="6" fill="' +
          fillBody +
          '"/>' +
          '<rect x="66" y="200" width="68" height="14" rx="4" fill="' +
          accent +
          '"/>' +
          (metal
            ? '<path d="M70 150 L130 150 L126 190 L74 190 Z" fill="#ffffff" opacity="0.12"/>'
            : "") +
          "</g>"
        );
      case "open":
        return (
          '<g id="outfit-open">' +
          '<rect x="70" y="150" width="60" height="28" rx="6" fill="' +
          shirt +
          '"/>' +
          '<path d="M58 130 L100 145 L70 160 Z" fill="' +
          fillBody +
          '"/>' +
          '<path d="M58 130 Q50 150 56 170 L78 155 Z" fill="' +
          accent +
          '"/>' +
          '<rect x="48" y="145" width="14" height="50" rx="5" fill="' +
          skin +
          '"/>' +
          '<rect x="138" y="145" width="14" height="50" rx="5" fill="' +
          skin +
          '"/>' +
          '<path d="M68 185 Q100 200 132 185 L128 220 Q100 235 72 220 Z" fill="' +
          fillLegs +
          '"/>' +
          '<rect x="66" y="182" width="68" height="10" rx="3" fill="' +
          accent +
          '"/>' +
          "</g>"
        );
      case "suit":
        return (
          '<g id="outfit-suit">' +
          '<rect x="66" y="128" width="68" height="92" rx="12" fill="' +
          fillBody +
          '"/>' +
          '<rect x="48" y="136" width="20" height="70" rx="8" fill="' +
          fillBody +
          '"/>' +
          '<rect x="132" y="136" width="20" height="70" rx="8" fill="' +
          fillBody +
          '"/>' +
          '<rect x="68" y="200" width="64" height="24" rx="8" fill="' +
          fillLegs +
          '"/>' +
          '<line x1="100" y1="132" x2="100" y2="210" stroke="' +
          accent +
          '" stroke-width="2" opacity="0.5"/>' +
          "</g>"
        );
      case "robe":
        return (
          '<g id="outfit-robe">' +
          '<path d="M62 128 L138 128 L150 230 L50 230 Z" fill="' +
          fillBody +
          '"/>' +
          '<rect x="48" y="136" width="20" height="70" rx="8" fill="' +
          fillBody +
          '"/>' +
          '<rect x="132" y="136" width="20" height="70" rx="8" fill="' +
          fillBody +
          '"/>' +
          '<path d="M70 128 Q100 150 130 128" fill="none" stroke="' +
          accent +
          '" stroke-width="3"/>' +
          "</g>"
        );
      case "barbarian":
        return (
          '<g id="outfit-barb">' +
          '<rect x="72" y="128" width="56" height="26" rx="6" fill="' +
          fillBody +
          '"/>' +
          '<rect x="76" y="154" width="48" height="40" rx="6" fill="' +
          skin +
          '"/>' +
          '<rect x="50" y="140" width="16" height="55" rx="5" fill="' +
          skin +
          '"/>' +
          '<rect x="134" y="140" width="16" height="55" rx="5" fill="' +
          skin +
          '"/>' +
          '<rect x="68" y="198" width="64" height="14" rx="4" fill="' +
          accent +
          '"/>' +
          '<rect x="78" y="120" width="6" height="28" fill="' +
          accent +
          '"/>' +
          '<rect x="116" y="120" width="6" height="28" fill="' +
          accent +
          '"/>' +
          "</g>"
        );
      case "tunic":
      default:
        return (
          '<g id="outfit-tunic">' +
          '<rect x="68" y="130" width="64" height="78" rx="8" fill="' +
          fillBody +
          '"/>' +
          '<path d="M66 200 L134 200 L140 230 L60 230 Z" fill="' +
          fillBody +
          '"/>' +
          '<rect x="50" y="138" width="18" height="55" rx="6" fill="' +
          fillBody +
          '"/>' +
          '<rect x="132" y="138" width="18" height="55" rx="6" fill="' +
          fillBody +
          '"/>' +
          '<rect x="66" y="188" width="68" height="12" rx="3" fill="' +
          accent +
          '"/>' +
          '<rect x="94" y="190" width="12" height="10" rx="2" fill="' +
          accent +
          '"/>' +
          "</g>"
        );
    }
  }

  function buildWeapon(weapon, accent, body) {
    if (!weapon) return "";
    if (weapon === "fierce_deity_sword") {
      return (
        '<g id="weapon" transform="translate(150 150) rotate(-18)">' +
        '<rect x="0" y="0" width="8" height="90" rx="2" fill="' +
        accent +
        '"/>' +
        '<rect x="-4" y="88" width="16" height="18" rx="2" fill="' +
        body +
        '"/>' +
        '<path d="M4 0 L10 -20 L4 -14 L-2 -20 Z" fill="' +
        accent +
        '"/>' +
        "</g>"
      );
    }
    if (weapon === "traveler_shield") {
      return (
        '<g id="weapon" transform="translate(42 160)">' +
        '<ellipse cx="0" cy="20" rx="16" ry="22" fill="' +
        accent +
        '" stroke="' +
        body +
        '" stroke-width="3"/>' +
        "</g>"
      );
    }
    return "";
  }

  function createPreview(container) {
    function showSet(set) {
      var p = mergePreview(set && set.preview);
      container.innerHTML = buildSvg(p, set && set.name);
    }

    function stop() {
      /* 2D static: nothing to animate */
    }

    function resize() {
      /* SVG scales via CSS */
    }

    return {
      showSet: showSet,
      stop: stop,
      start: function () {},
      resize: resize,
      dispose: function () {
        container.innerHTML = "";
      },
    };
  }

  global.TotkArmorPreview = { create: createPreview };
})(window);
