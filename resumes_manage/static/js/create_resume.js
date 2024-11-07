// Función para mostrar el modal de confirmación de eliminación
function showConfirmationModal(resumeId) {
    window.selectedResumeId = resumeId;
}

// Función que se ejecuta al confirmar la eliminación
function confirmDeletion(resumeId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/resume/${resumeId}/delete/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if (response.ok) {
            
            alert("Resume deleted successfully");
            location.reload(); 
        } else {
            alert("Error deleting resume");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
