// Wait until the DOM is fully loaded before running the script
document.addEventListener("DOMContentLoaded", function () {
  // --- Hamburger Menu Logic ---
  const hamburger = document.getElementById("hamburger-menu");
  const nav = document.querySelector(".main-nav");

  if (hamburger && nav) {
    hamburger.addEventListener("click", function () {
      hamburger.classList.toggle("active");
      nav.classList.toggle("active");
    });
  }
  // --- Image Carousel Logic (NEW) ---
  const carouselContainer = document.querySelector(".carousel-container");
  const slides = document.querySelector(".carousel-slides");
  const prevButton = document.querySelector(".carousel-button.prev");
  const nextButton = document.querySelector(".carousel-button.next");

  // Check if carousel elements exist on the page
  if (carouselContainer && slides && prevButton && nextButton) {
    let currentSlide = 0;
    const totalSlides = slides.children.length;

    // Function to move to a specific slide
    function showSlide(index) {
      currentSlide = (index + totalSlides) % totalSlides;
      const offset = -currentSlide * 100;
      slides.style.transform = `translateX(${offset}%)`;
    }

    // Event listener for the "Next" button
    nextButton.addEventListener("click", function () {
      showSlide(currentSlide + 1);
    });

    // Event listener for the "Previous" button
    prevButton.addEventListener("click", function () {
      showSlide(currentSlide - 1);
    });
  }
});
// ========================================================================
// CARD SLIDER SYSTEM JAVASCRIPT
// ========================================================================

class CardSlider {
    constructor(container) {
        this.container = container;
        this.wrapper = container.querySelector('[data-wrapper]');
        this.prevBtn = container.querySelector('[data-prev]');
        this.nextBtn = container.querySelector('[data-next]');
        this.cards = this.wrapper.querySelectorAll('.card-item');
        
        this.scrollAmount = 300;
        this.isScrolling = false;
        
        this.init();
    }
    
    init() {
        this.updateScrollAmount();
        this.updateArrowStates();
        this.bindEvents();
        
        // Update on window resize
        window.addEventListener('resize', this.debounce(() => {
            this.updateScrollAmount();
            this.updateArrowStates();
        }, 100));
    }
    
    bindEvents() {
        this.prevBtn.addEventListener('click', () => this.scrollLeft());
        this.nextBtn.addEventListener('click', () => this.scrollRight());
        
        // Update arrow states when scrolling manually
        this.wrapper.addEventListener('scroll', this.debounce(() => {
            this.updateArrowStates();
        }, 50));
        
        // Touch/swipe support
        let startX = 0;
        let scrollLeft = 0;
        
        this.wrapper.addEventListener('touchstart', (e) => {
            startX = e.touches[0].pageX - this.wrapper.offsetLeft;
            scrollLeft = this.wrapper.scrollLeft;
        });
        
        this.wrapper.addEventListener('touchmove', (e) => {
            if (!startX) return;
            e.preventDefault();
            const x = e.touches[0].pageX - this.wrapper.offsetLeft;
            const walk = (x - startX) * 2;
            this.wrapper.scrollLeft = scrollLeft - walk;
        });
        
        this.wrapper.addEventListener('touchend', () => {
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
        
        this.wrapper.scrollBy({
            left: -this.scrollAmount,
            behavior: 'smooth'
        });
        
        setTimeout(() => {
            this.isScrolling = false;
            this.updateArrowStates();
        }, 300);
    }
    
    scrollRight() {
        if (this.isScrolling) return;
        this.isScrolling = true;
        
        this.wrapper.scrollBy({
            left: this.scrollAmount,
            behavior: 'smooth'
        });
        
        setTimeout(() => {
            this.isScrolling = false;
            this.updateArrowStates();
        }, 300);
    }
    
    updateArrowStates() {
        const { scrollLeft, scrollWidth, clientWidth } = this.wrapper;
        
        // Check if content is scrollable
        const isScrollable = scrollWidth > clientWidth;
        
        if (!isScrollable) {
            this.prevBtn.classList.add('hidden');
            this.nextBtn.classList.add('hidden');
            return;
        }
        
        this.prevBtn.classList.remove('hidden');
        this.nextBtn.classList.remove('hidden');
        
        // Update disabled states
        this.prevBtn.disabled = scrollLeft <= 5;
        this.nextBtn.disabled = scrollLeft >= scrollWidth - clientWidth - 5;
    }
    
    // Debounce function for performance
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
document.addEventListener('DOMContentLoaded', () => {
    const sliders = document.querySelectorAll('[data-slider]');
    sliders.forEach(slider => new CardSlider(slider));
});

// Optional: Keyboard navigation
// Initialize all sliders when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Select all elements with the class 'card-slider'
    const sliders = document.querySelectorAll('.card-slider');
    
    // Loop through each of them and create a new CardSlider instance
    sliders.forEach(slider => new CardSlider(slider));
});
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        const focusedSlider = document.querySelector('.slider-container:hover');
        if (focusedSlider) {
            e.preventDefault();
            const prevBtn = focusedSlider.querySelector('[data-prev]');
            const nextBtn = focusedSlider.querySelector('[data-next]');
            
            if (e.key === 'ArrowLeft' && !prevBtn.disabled) {
                prevBtn.click();
            }
            if (e.key === 'ArrowRight' && !nextBtn.disabled) {
                nextBtn.click();
            }
        }
    }
});