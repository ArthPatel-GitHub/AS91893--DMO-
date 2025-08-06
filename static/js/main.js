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
