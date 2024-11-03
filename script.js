// Select the necessary elements
const uploadInput = document.querySelector('.upload-input');
const uploadPhoto = document.querySelector('.upload-photo');
const filterBtn = document.getElementById('applyFilter');
const mustache = document.querySelector('.mustache');
const hat = document.querySelector('.hat');

// Handle image upload and display preview
uploadInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            uploadPhoto.src = e.target.result; // Set uploaded image as the source
        };
        reader.readAsDataURL(file);
    }
});

// Toggle filters when button is clicked
filterBtn.addEventListener('click', () => {
    mustache.classList.toggle('show'); // Show/hide mustache
    hat.classList.toggle('show'); // Show/hide hat
});

