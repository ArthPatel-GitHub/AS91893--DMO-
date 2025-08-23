document.addEventListener('DOMContentLoaded', () => {

    // Find all elements with the class 'card-slider'
    const sliders = document.querySelectorAll('.card-slider');

    // Loop through each slider and initialize it
    sliders.forEach(slider => {
        const sliderTrack = slider.querySelector('.slider-track');
        const cards = Array.from(sliderTrack.children);
        const nextButton = slider.querySelector('.slider-next');
        const prevButton = slider.querySelector('.slider-prev');
        let currentCardIndex = 0;
        const cardWidth = cards[0].offsetWidth; // Assuming all cards have the same width

        // Function to move the slider to the specified card index
        function moveToCard(index) {
            sliderTrack.style.transform = `translateX(-${index * cardWidth}px)`;
        }

        // Add event listener for the 'next' button
        nextButton.addEventListener('click', () => {
            currentCardIndex = (currentCardIndex + 1) % cards.length;
            moveToCard(currentCardIndex);
        });

        // Add event listener for the 'previous' button
        prevButton.addEventListener('click', () => {
            currentCardIndex = (currentCardIndex - 1 + cards.length) % cards.length;
            moveToCard(currentCardIndex);
        });
    });
});