(() => {
  const FALLBACK_BEAMLINE = "x99sa";
  const BEAMLINE_RE = /^x\d{2}[a-z]{2}$/;
  const RENDERED_BEAMLINE_RE = /\bx\d{2}[a-z]{2}\b/gi;
  const PLACEHOLDER_RE = /<(xname|XNAME)>/g;

  function detectBeamlineName(hostname = window.location.hostname) {
    const normalizedHostname = String(hostname || "").toLowerCase();
    const firstLabel = normalizedHostname.split(".")[0] || "";
    const candidate = firstLabel.split("-")[0] || "";
    return BEAMLINE_RE.test(candidate) ? candidate : FALLBACK_BEAMLINE;
  }

  function replaceBeamlineText(node, beamlineName) {
    const original = node.nodeValue;
    if (!original) {
      return;
    }

    const replaced = original
      .replace(PLACEHOLDER_RE, (_, token) =>
        token === "XNAME" ? beamlineName.toUpperCase() : beamlineName
      )
      .replace(RENDERED_BEAMLINE_RE, (match) =>
        match === match.toUpperCase() ? beamlineName.toUpperCase() : beamlineName
      );

    if (replaced !== original) {
      node.nodeValue = replaced;
    }
  }

  function updateRenderedContent() {
    const beamlineName = detectBeamlineName();
    const root = document.querySelector(".md-content");
    if (!root) {
      return;
    }

    window.BEC_DOCS = {
      ...(window.BEC_DOCS || {}),
      beamlineName,
    };

    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        const parent = node.parentElement;
        if (!parent) {
          return NodeFilter.FILTER_REJECT;
        }

        if (parent.closest("script, style, textarea")) {
          return NodeFilter.FILTER_REJECT;
        }

        if (!node.nodeValue || (!RENDERED_BEAMLINE_RE.test(node.nodeValue) && !PLACEHOLDER_RE.test(node.nodeValue))) {
          RENDERED_BEAMLINE_RE.lastIndex = 0;
          PLACEHOLDER_RE.lastIndex = 0;
          return NodeFilter.FILTER_REJECT;
        }

        RENDERED_BEAMLINE_RE.lastIndex = 0;
        PLACEHOLDER_RE.lastIndex = 0;
        return NodeFilter.FILTER_ACCEPT;
      },
    });

    const nodes = [];
    while (walker.nextNode()) {
      nodes.push(walker.currentNode);
    }

    nodes.forEach((node) => replaceBeamlineText(node, beamlineName));
  }

  updateRenderedContent();
})();
