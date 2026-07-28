(function () {
  if (document.body.dataset.contentProtection !== "true") {
    return;
  }

  if (document.querySelector(".admin-page")) {
    return;
  }

  function isInteractive(target) {
    let el = target;
    while (el && el !== document.body) {
      const tag = el.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "BUTTON" || tag === "SELECT") {
        return true;
      }
      if (el.isContentEditable) {
        return true;
      }
      el = el.parentElement;
    }
    return false;
  }

  document.addEventListener("contextmenu", (event) => {
    if (!isInteractive(event.target)) {
      event.preventDefault();
    }
  });

  ["copy", "cut", "paste"].forEach((eventName) => {
    document.addEventListener(eventName, (event) => {
      if (!isInteractive(event.target)) {
        event.preventDefault();
      }
    });
  });

  document.addEventListener("keydown", (event) => {
    if (isInteractive(event.target)) {
      return;
    }

    const key = event.key.toLowerCase();
    const mod = event.ctrlKey || event.metaKey;

    if (mod && ["c", "a", "s", "p", "u"].includes(key)) {
      event.preventDefault();
    }

    if (key === "f12") {
      event.preventDefault();
    }
  });

  document.addEventListener("dragstart", (event) => {
    if (!isInteractive(event.target)) {
      event.preventDefault();
    }
  });
})();
