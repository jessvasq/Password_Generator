//This file contains the javascript code for the progress bar

//This function is called when the page is loaded, sets the progress bar to 0 
document.addEventListener('DOMContentLoaded', function() {
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = '0%';
});

//This function is called when the mouse is clicked on the progress bar
function startDrag(e) {
    //Prevents the default action of the mouse click
    e.preventDefault();
    //Adds event listeners for the mousemove and mouseup events
    document.addEventListener('mousemove', handleDrag);
    document.addEventListener('mouseup', stopDrag);
}

//This function is called when the mouse is moved while the mouse button is pressed
function handleDrag(e) {
    const progressBar = document.getElementById('progressBar');
    const progressContainer = document.getElementById('progressContainer');
    const containerWidth = progressContainer.clientWidth;

    //Calculates the new position of the progress bar by subtracting the left position of the progress container from the x position of the mouse
    let newPosition = e.clientX - progressContainer.getBoundingClientRect().left;
    //newPosition is set to 0 if it is less than 0, and set to the width of the progress container if it is greater than the width of the progress container
    newPosition = Math.max(0, Math.min(newPosition, containerWidth));
    //The width of the progress bar is set to the new position as a percentage of the width of the progress container
    const percentage = (newPosition / containerWidth) * 100;
    //The width of the progress bar is set to the new position as a percentage of the width of the progress container
    progressBar.style.width = percentage + '%';

    //The count is set to the percentage rounded to the nearest integer and displayed on the page
    const count = document.getElementById('count');
    count.innerHTML = Math.round(percentage);
    
}

//This function is called when the mouse button is released which removes the event listeners for the mousemove and mouseup events
function stopDrag() {
    document.removeEventListener('mousemove', handleDrag);
    document.removeEventListener('mouseup', stopDrag);
}
