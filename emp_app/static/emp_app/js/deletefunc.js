function confirmDelete(pk, name) {
    if (confirm(`Are you sure you want to delete "${name}"?`)) {
        window.location.href = `/employees/delete/${pk}/`;
    }
}