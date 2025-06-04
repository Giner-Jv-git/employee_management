function previewImage(input) {
        const previewContainer = input.closest('.flex').querySelector('.w-24.h-24'); // Find the preview div
        const previewText = previewContainer.querySelector('#profile-preview-text'); // Get the text span
        
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
                span.setAttribute('class', 'text-blue-500 text-xs text-center p-2');
                span.textContent = 'No image selected';
                previewContainer.appendChild(span);
            }
        }
    }

    // Initialize preview if an image already exists (e.g., in an update form)
    document.addEventListener('DOMContentLoaded', function() {
        const profilePictureInput = document.getElementById('id_profile_picture');
        if (profilePictureInput && profilePictureInput.value) {
            // If the form is pre-filled with an existing image,
            // we need a way to display it initially.
            // This usually means Django passes the URL of the existing image.
            // Your form is for 'Add Employee', so this part might be less critical,
            // but good practice for 'Edit Employee'.
            // For 'Add', it typically won't have an initial value unless there's a problem.
            
            // To display existing image from Django if form.profile_picture.value exists:
            // Ensure your initial HTML for the preview includes an <img> tag if there's a value.
            // I've updated the HTML above to include this check.
        }
    });