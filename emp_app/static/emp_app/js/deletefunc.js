function confirmDelete(pk, name) {
    if (confirm(`Are you sure you want to delete "${name}"?`)) {
        window.location.href = `/employees/delete/${pk}/`;
    }
}

// Check for deleted employee name in sessionStorage when page loads
document.addEventListener('DOMContentLoaded', function() {
    const deletedEmployeeName = sessionStorage.getItem('deletedEmployeeName');
    if (deletedEmployeeName) {
        // Clear the stored name
        sessionStorage.removeItem('deletedEmployeeName');
    }
});