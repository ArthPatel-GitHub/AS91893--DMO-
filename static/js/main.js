// static/js/main.js

// Wait until the DOM is fully loaded before running the script
document.addEventListener("DOMContentLoaded", function () {
  // Get the hamburger menu element by its ID
  const hamburger = document.getElementById("hamburger-menu");
  // Get the main navigation bar element
  const nav = document.querySelector(".main-nav");

  // Check if both elements exist on the page
  if (hamburger && nav) {
    // Add a click event listener to the hamburger menu
    hamburger.addEventListener("click", function () {
      // Toggle the 'active' class on both the hamburger and the nav menu
      // This class will be used by our CSS to show/hide the menu
      hamburger.classList.toggle("active");
      nav.classList.toggle("active");
    });
  }
});
