(function () {
  const searchInput = document.getElementById("faq-search");
  const searchClear = document.getElementById("search-clear");
  const visibleCount = document.getElementById("visible-count");
  const suggestionsEl = document.getElementById("search-suggestions");
  const noResults = document.getElementById("no-results");
  const clearSearchBtn = document.getElementById("clear-search-btn");
  const expandAllBtn = document.getElementById("expand-all");
  const collapseAllBtn = document.getElementById("collapse-all");
  const themeToggle = document.getElementById("theme-toggle");
  const mobileMenuBtn = document.getElementById("mobile-menu-btn");
  const mobileNav = document.getElementById("mobile-nav");
  const backToTop = document.getElementById("back-to-top");
  const scrollProgress = document.getElementById("scroll-progress");
  const faqsSection = document.getElementById("faqs");
  const quickNav = document.getElementById("quick-nav");
  const faqBlockTop = document.getElementById("faq-block-top");
  const faqItems = Array.from(document.querySelectorAll("[data-faq]"));
  const categories = Array.from(document.querySelectorAll(".faq-category"));
  const totalFaqs = faqItems.length;

  function prefersReducedMotion() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function scrollToId(id) {
    const el = document.getElementById(id);
    if (!el) return;
    const y = el.getBoundingClientRect().top + window.scrollY - 72;
    window.scrollTo({ top: y, behavior: prefersReducedMotion() ? "auto" : "smooth" });
    mobileNav.classList.add("hidden");
    mobileMenuBtn.setAttribute("aria-expanded", "false");
  }

  document.querySelectorAll("[data-scroll]").forEach((btn) => {
    btn.addEventListener("click", () => scrollToId(btn.dataset.scroll));
  });

  function initTheme() {
    const stored = localStorage.getItem("arvind-gcc-theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const dark = stored ? stored === "dark" : prefersDark;
    document.documentElement.classList.toggle("dark", dark);
    document.querySelector(".theme-icon-moon")?.classList.toggle("hidden", dark);
    document.querySelector(".theme-icon-sun")?.classList.toggle("hidden", !dark);
  }

  themeToggle?.addEventListener("click", () => {
    const dark = !document.documentElement.classList.contains("dark");
    document.documentElement.classList.toggle("dark", dark);
    localStorage.setItem("arvind-gcc-theme", dark ? "dark" : "light");
    document.querySelector(".theme-icon-moon")?.classList.toggle("hidden", dark);
    document.querySelector(".theme-icon-sun")?.classList.toggle("hidden", !dark);
  });

  mobileMenuBtn?.addEventListener("click", () => {
    mobileNav.classList.toggle("hidden");
    const isOpen = !mobileNav.classList.contains("hidden");
    mobileMenuBtn.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });

  window.addEventListener("scroll", () => {
    const total = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = total > 0 ? window.scrollY / total : 0;
    scrollProgress.style.transform = `scaleX(${ratio})`;
    backToTop.classList.toggle("hidden", window.scrollY <= 500);
  }, { passive: true });

  backToTop?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: prefersReducedMotion() ? "auto" : "smooth" });
  });

  function getSearchTerms(query) {
    return query.trim().toLowerCase().split(/\s+/).filter(Boolean);
  }

  function matchesSearch(text, terms) {
    if (!terms.length) return true;
    const haystack = text.toLowerCase();
    return terms.every((term) => haystack.includes(term));
  }

  function highlightText(text, query) {
    const terms = getSearchTerms(query);
    if (!terms.length) return escapeHtml(text);

    let result = escapeHtml(text);
    terms.forEach((term) => {
      const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const re = new RegExp(`(${escaped})`, "gi");
      result = result.replace(re, "<mark>$1</mark>");
    });
    return result;
  }

  function escapeHtml(text) {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  faqItems.forEach((item) => {
    const questionEl = item.querySelector(".faq-question");
    const bodyEl = item.querySelector(".accordion-body");
    if (questionEl && !questionEl.dataset.original) {
      questionEl.dataset.original = questionEl.textContent.trim();
    }
    if (bodyEl && !bodyEl.dataset.original) {
      bodyEl.dataset.original = bodyEl.textContent.trim();
    }
  });

  function jumpToFAQ(item) {
    item.open = true;
    const y = item.getBoundingClientRect().top + window.scrollY - 90;
    window.scrollTo({ top: y, behavior: prefersReducedMotion() ? "auto" : "smooth" });
  }

  function applySearch() {
    const query = searchInput.value.trim();
    const terms = getSearchTerms(query);
    const isSearching = terms.length > 0;

    searchClear.classList.toggle("hidden", !isSearching);
    faqsSection.classList.toggle("search-active", isSearching);
    quickNav.classList.toggle("hidden", isSearching);

    let visible = 0;
    const matches = [];

    faqItems.forEach((item) => {
      const text = item.dataset.searchText || "";
      const match = matchesSearch(text, terms);
      item.classList.toggle("filtered-out", !match);

      if (match) {
        visible += 1;
        if (isSearching) {
          matches.push(item);
          item.open = true;
        }
      } else {
        item.open = false;
      }

      const questionEl = item.querySelector(".faq-question");
      const bodyEl = item.querySelector(".accordion-body");
      if (questionEl) {
        const original = questionEl.dataset.original || questionEl.textContent.trim();
        questionEl.innerHTML = isSearching ? highlightText(original, query) : original;
      }
      if (bodyEl) {
        const original = bodyEl.dataset.original || bodyEl.textContent.trim();
        bodyEl.innerHTML = isSearching ? highlightText(original, query) : original;
      }
    });

    const visibleTop = faqBlockTop.querySelectorAll("[data-faq]:not(.filtered-out)").length;
    faqBlockTop.classList.toggle("hidden", isSearching && visibleTop === 0);

    categories.forEach((cat) => {
      const visibleInCat = cat.querySelectorAll("[data-faq]:not(.filtered-out)").length;
      cat.classList.toggle("hidden", isSearching && visibleInCat === 0);
    });

    visibleCount.textContent = String(visible);
    noResults.classList.toggle("hidden", visible > 0 || !isSearching);

    if (isSearching && matches.length) {
      const shown = matches.slice(0, 8);
      suggestionsEl.classList.remove("hidden");
      suggestionsEl.innerHTML = `
        <div class="suggestions-header">
          <span>Top ${shown.length} match${shown.length === 1 ? "" : "es"} for “${escapeHtml(query)}”</span>
          <span class="suggestions-hint">Click to jump</span>
        </div>
        <ul class="suggestions-list">
          ${shown.map((item) => {
            const original = item.querySelector(".faq-question")?.dataset.original || "";
            const label = item.dataset.categoryName || "FAQ";
            return `
              <li>
                <button type="button" class="suggestion-item" data-jump="${item.dataset.key}">
                  <span class="suggestion-q">Q</span>
                  <span class="suggestion-content">
                    <span class="suggestion-label">${escapeHtml(label)}</span>
                    <span class="suggestion-question">${highlightText(original, query)}</span>
                  </span>
                </button>
              </li>
            `;
          }).join("")}
        </ul>
      `;

      suggestionsEl.querySelectorAll("[data-jump]").forEach((btn) => {
        btn.addEventListener("click", () => {
          const target = faqItems.find((item) => item.dataset.key === btn.dataset.jump);
          if (target) jumpToFAQ(target);
        });
      });
    } else if (isSearching) {
      suggestionsEl.classList.add("hidden");
      suggestionsEl.innerHTML = "";
    } else {
      suggestionsEl.classList.add("hidden");
      suggestionsEl.innerHTML = "";
    }
  }

  searchInput?.addEventListener("input", applySearch);
  searchClear?.addEventListener("click", () => {
    searchInput.value = "";
    applySearch();
    searchInput.focus();
  });
  clearSearchBtn?.addEventListener("click", () => {
    searchInput.value = "";
    applySearch();
    searchInput.focus();
  });

  expandAllBtn?.addEventListener("click", () => {
    faqItems.forEach((item) => {
      if (!item.classList.contains("filtered-out")) item.open = true;
    });
  });

  collapseAllBtn?.addEventListener("click", () => {
    faqItems.forEach((item) => (item.open = false));
  });

  document.addEventListener("keydown", (e) => {
    const tag = e.target.tagName;
    const typing = ["INPUT", "TEXTAREA", "SELECT"].includes(tag) || e.target.isContentEditable;
    const isSlash = e.key === "/" && !e.metaKey && !e.ctrlKey && !e.altKey;
    const isCmdK = (e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k";
    if ((isSlash && !typing) || isCmdK) {
      e.preventDefault();
      searchInput?.focus();
      searchInput?.select();
    }
  });

  document.getElementById("copy-email")?.addEventListener("click", async () => {
    const email = "helpline@arvindgcc.com";
    const btn = document.getElementById("copy-email");
    const originalLabel = "Copy email";
    try {
      await navigator.clipboard.writeText(email);
      btn.textContent = "Copied";
      btn.classList.add("btn-copied");
      window.setTimeout(() => {
        btn.textContent = originalLabel;
        btn.classList.remove("btn-copied");
      }, 2000);
    } catch {
      /* noop */
    }
  });

  document.querySelectorAll("[data-feedback]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const helpful = btn.dataset.feedback === "yes";
      try {
        await fetch("/api/feedback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ helpful }),
        });
      } catch {
        /* noop */
      }
      document.getElementById("feedback-form").classList.add("hidden");
      const thanks = document.getElementById("feedback-thanks");
      thanks.classList.remove("hidden");
      thanks.textContent = helpful
        ? "Thank you for your feedback. We're glad this was helpful."
        : "Thank you for your feedback. Please connect with the relevant SPOC for additional clarification.";
    });
  });

  initTheme();
  visibleCount.textContent = String(totalFaqs);
})();
