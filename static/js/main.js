// --- My code to immediately set the theme from localStorage before the page fully loads
(function () {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme) {
    document.body.className = savedTheme + "-theme";
  } else {
    document.body.className = "dark-theme"; // My default theme
  }
})();

// --- My Theme Switcher Toggle Logic ---
// I'm putting this logic outside the DOMContentLoaded so it runs right away
const themeToggleBtn = document.querySelector(".theme-toggle-btn");
const themePanel = document.querySelector(".color-switcher");

// My code to toggle the theme menu when I click the button
if (themeToggleBtn && themePanel) {
  themeToggleBtn.addEventListener("click", () => {
    themePanel.classList.toggle("active");
    // ADD THIS LINE
    themeToggleBtn.classList.toggle("menu-active");
  });
}

// Close theme menu when clicking outside of it
document.addEventListener("click", (e) => {
  if (themeToggleBtn && themePanel) {
    // Check if click is outside both the button and the menu
    if (!themeToggleBtn.contains(e.target) && !themePanel.contains(e.target)) {
      themePanel.classList.remove("active");
      // ADD THIS LINE
      themeToggleBtn.classList.remove("menu-active");
    }
  }
});

// I want to wait until my whole document is loaded for everything else
document.addEventListener("DOMContentLoaded", function () {
  // --- My Hamburger Menu Logic ---
  const hamburger = document.querySelector(".hamburger-menu");
  const nav = document.querySelector(".main-nav");

  if (hamburger && nav) {
    hamburger.addEventListener("click", function () {
      hamburger.classList.toggle("active");
      nav.classList.toggle("active");
    });
  }

  // --- My Theme Buttons Logic ---
  const themeButtons = document.querySelectorAll(".theme-button");

  themeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const newTheme = this.dataset.theme;

      if (newTheme) {
        document.body.className = newTheme + "-theme";
        localStorage.setItem("theme", newTheme);

        // Close the theme menu after selecting a theme
        if (themePanel && themeToggleBtn) {
          themePanel.classList.remove("active");
          // ADD THIS LINE
          themeToggleBtn.classList.remove("menu-active");
        }
      }
    });
  });

  // ========================================================================
  // CARD SLIDER SYSTEM JAVASCRIPT
  // ========================================================================

  class CardSlider {
    constructor(container) {
      this.container = container;
      this.wrapper =
        container.querySelector("[data-wrapper]") ||
        container.querySelector(".slider-track") ||
        container.querySelector(".card-grid");
      this.prevBtn =
        container.querySelector("[data-prev]") ||
        container.querySelector(".slider-nav.prev") ||
        container.querySelector(".prev");
      this.nextBtn =
        container.querySelector("[data-next]") ||
        container.querySelector(".slider-nav.next") ||
        container.querySelector(".next");

      if (!this.wrapper) {
        console.warn(
          "CardSlider: No wrapper element found in container",
          this.container
        );
        return;
      }

      this.cards = this.wrapper.querySelectorAll(".card-item");
      this.scrollAmount = 300;
      this.isScrolling = false;
      this.init();
    }

    init() {
      if (!this.wrapper || !this.prevBtn || !this.nextBtn) {
        return;
      }
      this.updateScrollAmount();
      this.updateArrowStates();
      this.bindEvents();
      window.addEventListener(
        "resize",
        this.debounce(() => {
          this.updateScrollAmount();
          this.updateArrowStates();
        }, 100)
      );
    }

    bindEvents() {
      if (!this.prevBtn || !this.nextBtn || !this.wrapper) {
        return;
      }
      this.prevBtn.addEventListener("click", () => this.scrollLeft());
      this.nextBtn.addEventListener("click", () => this.scrollRight());
      this.wrapper.addEventListener(
        "scroll",
        this.debounce(() => {
          this.updateArrowStates();
        }, 50)
      );

      let startX = 0;
      let scrollLeft = 0;
      this.wrapper.addEventListener("touchstart", (e) => {
        startX = e.touches[0].pageX - this.wrapper.offsetLeft;
        scrollLeft = this.wrapper.scrollLeft;
      });
      this.wrapper.addEventListener("touchmove", (e) => {
        if (!startX) return;
        e.preventDefault();
        const x = e.touches[0].pageX - this.wrapper.offsetLeft;
        const walk = (x - startX) * 2;
        this.wrapper.scrollLeft = scrollLeft - walk;
      });
      this.wrapper.addEventListener("touchend", () => {
        startX = 0;
        this.updateArrowStates();
      });
    }

    updateScrollAmount() {
      if (this.cards.length > 0) {
        const cardWidth = this.cards[0].offsetWidth;
        const gap = parseFloat(getComputedStyle(this.wrapper).gap) || 20;
        this.scrollAmount = cardWidth + gap;
      }
    }

    scrollLeft() {
      if (this.isScrolling) return;
      this.isScrolling = true;
      this.wrapper.scrollBy({ left: -this.scrollAmount, behavior: "smooth" });
      setTimeout(() => {
        this.isScrolling = false;
        this.updateArrowStates();
      }, 300);
    }

    scrollRight() {
      if (this.isScrolling) return;
      this.isScrolling = true;
      this.wrapper.scrollBy({ left: this.scrollAmount, behavior: "smooth" });
      setTimeout(() => {
        this.isScrolling = false;
        this.updateArrowStates();
      }, 300);
    }

    updateArrowStates() {
      if (!this.wrapper || !this.prevBtn || !this.nextBtn) {
        return;
      }
      const { scrollLeft, scrollWidth, clientWidth } = this.wrapper;
      const isScrollable = scrollWidth > clientWidth;

      if (!isScrollable) {
        this.prevBtn.classList.add("hidden");
        this.nextBtn.classList.add("hidden");
        return;
      }
      this.prevBtn.classList.remove("hidden");
      this.nextBtn.classList.remove("hidden");
      this.prevBtn.disabled = scrollLeft <= 5;
      this.nextBtn.disabled = scrollLeft >= scrollWidth - clientWidth - 5;
    }

    debounce(func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    }
  }

  // Initialize all sliders when DOM is ready
  const sliderSelectors = [
    "[data-slider]",
    ".card-slider",
    ".slider-container",
    ".carousel-container",
  ];
  let slidersFound = false;
  sliderSelectors.forEach((selector) => {
    const sliders = document.querySelectorAll(selector);
    if (sliders.length > 0) {
      sliders.forEach((slider) => {
        try {
          new CardSlider(slider);
          slidersFound = true;
        } catch (error) {
          console.warn(`Failed to initialize slider for ${selector}:`, error);
        }
      });
    }
  });
  if (!slidersFound) {
    console.log(
      "No sliders found. Available selectors checked:",
      sliderSelectors
    );
  }

  // Keyboard navigation
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
      const focusedSlider = document.querySelector(
        ".slider-container:hover, .card-slider:hover"
      );
      if (focusedSlider) {
        e.preventDefault();
        const prevBtn = focusedSlider.querySelector("[data-prev]");
        const nextBtn = focusedSlider.querySelector("[data-next]");

        if (e.key === "ArrowLeft" && prevBtn && !prevBtn.disabled) {
          prevBtn.click();
        }
        if (e.key === "ArrowRight" && nextBtn && !nextBtn.disabled) {
          nextBtn.click();
        }
      }
    }
  });

  // Close theme menu on Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && themePanel && themeToggleBtn) {
      if (themePanel.classList.contains("active")) {
        themePanel.classList.remove("active");
        themeToggleBtn.classList.remove("menu-active");
      }
    }
  });
});
