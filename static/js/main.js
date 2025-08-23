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

    // --- Theme Switcher Logic ---
    const themeSwitcher = document.getElementById('theme-switcher');
    const body = document.body;

    // Load saved theme from localStorage or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    body.classList.add(savedTheme + '-theme');

    if (themeSwitcher) {
        themeSwitcher.addEventListener('click', function (event) {
            if (event.target.tagName === 'BUTTON') {
                // Remove existing theme classes
                body.classList.remove('dark-theme', 'light-theme');

                // Get the new theme from the button's data-theme attribute
                const newTheme = event.target.dataset.theme;

                // Apply the new theme class
                body.classList.add(newTheme + '-theme');

                // Save the new theme to localStorage
                localStorage.setItem('theme', newTheme);
            }
        });
    }
    // --- End Theme Switcher Logic ---

    // --- Image Carousel Logic ---
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
        this.wrapper = container.querySelector('[data-wrapper]') || container.querySelector('.slider-track') || container.querySelector('.card-grid');
        this.prevBtn = container.querySelector('[data-prev]') || container.querySelector('.slider-nav.prev') || container.querySelector('.prev');
        this.nextBtn = container.querySelector('[data-next]') || container.querySelector('.slider-nav.next') || container.querySelector('.next');
        
        // Check if required elements exist
        if (!this.wrapper) {
            console.warn('CardSlider: No wrapper element found');
            return;
        }
        
        this.cards = this.wrapper.querySelectorAll('.card-item');
        
        this.scrollAmount = 300;
        this.isScrolling = false;
        
        this.init();
    }
    
    init() {
        // Only initialize if we have required elements
        if (!this.wrapper || !this.prevBtn || !this.nextBtn) {
            return;
        }
        
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
        if (!this.prevBtn || !this.nextBtn || !this.wrapper) {
            return;
        }
        
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
        if (!this.wrapper || !this.prevBtn || !this.nextBtn) {
            return;
        }
        
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
    // Try multiple selectors to find sliders
    const sliderSelectors = [
        '[data-slider]',
        '.card-slider', 
        '.slider-container',
        '.carousel-container'
    ];
    
    let slidersFound = false;
    
    sliderSelectors.forEach(selector => {
        const sliders = document.querySelectorAll(selector);
        if (sliders.length > 0) {
            sliders.forEach(slider => {
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
        console.log('No sliders found. Available selectors checked:', sliderSelectors);
    }
});

// Keyboard navigation
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