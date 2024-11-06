// This file contains the JavaScript code for the create_resume.html template.

function showConfirmationModal() {
    // Muestra el modal de confirmación
    var confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
    confirmationModal.show();
}

function confirmDeletion() {
    // Envía el formulario cuando se confirma la eliminación
    document.getElementById('deleteForm').submit();
}
