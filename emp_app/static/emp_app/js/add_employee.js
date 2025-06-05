function previewImage(input) {
    const preview = document.getElementById('profile-preview');
    const file = input.files[0];
    const reader = new FileReader();
    
    preview.innerHTML = '';
    
    if (file) {
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'w-full h-full object-cover';
            preview.appendChild(img);
        }
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = '<span class="text-gray-500">{{ employee.name|first|upper }}</span>';
    }
}

// Initialize form fields
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        if (input.type !== 'file' && input.type !== 'radio') {
            input.classList.add(
                'block', 'w-full', 'rounded-md', 'border-gray-300', 'shadow-sm',
                'focus:border-blue-500', 'focus:ring-blue-500', 'sm:text-sm',
                'py-2', 'px-3', 'border'
            );
        }
    });
    
    document.querySelector('textarea').classList.add('h-24');
});