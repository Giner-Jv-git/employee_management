function previewImage(input) {
    const previewContainer = input.closest('.flex').querySelector('.w-28.h-28');
    const previewText = previewContainer.querySelector('#profile-preview-text');
    
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            // If there's existing image, replace it, otherwise create new img element
            let img = previewContainer.querySelector('img');
            if (!img) {
                img = document.createElement('img');
                img.setAttribute('id', 'profile-preview');
                img.setAttribute('class', 'w-full h-full object-cover');
                previewContainer.innerHTML = ''; // Clear "No image" text
                previewContainer.appendChild(img);
            }
            img.src = e.target.result;
        };
        
        reader.readAsDataURL(input.files[0]);
    } else {
        // If no file or cleared, show "No image" text again
        let img = previewContainer.querySelector('img');
        if (img) {
            img.remove(); // Remove the image
        }
        if (!previewText) { // Re-add text if it was removed
            const span = document.createElement('span');
            span.setAttribute('id', 'profile-preview-text');
            span.setAttribute('class', 'text-blue-500 text-sm text-center p-2');
            span.textContent = 'No image selected';
            previewContainer.appendChild(span);
        }
    }
}

// Initialize preview if an image already exists (e.g., in an update form)
document.addEventListener('DOMContentLoaded', function() {
    const profilePictureInput = document.getElementById('id_profile_picture');
    const previewContainer = document.querySelector('.w-28.h-28');
    
    if (profilePictureInput && previewContainer) {
        // Check if there's an existing image in the preview container
        const existingImage = previewContainer.querySelector('img');
        if (existingImage && existingImage.src) {
            // If there's an existing image, make sure it's properly displayed
            existingImage.setAttribute('id', 'profile-preview');
            existingImage.setAttribute('class', 'w-full h-full object-cover');
        }
    }
});