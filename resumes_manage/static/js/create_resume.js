console.log("Archivo create_resume.js cargado");
// Función para mostrar el modal de confirmación de eliminación
function showConfirmationModal(resumeId) {
    window.selectedResumeId = resumeId;
}

// Función que se ejecuta al confirmar la eliminación
function confirmDeletion(resumeId) {
    console.log("Botón de confirmación presionado para ID:", resumeId);  
    
    fetch(`/delete_resume/${resumeId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            console.log("Eliminación exitosa");  
            location.reload();  // Recargar la página para ver los cambios
        } else {
            alert("Error al eliminar la hoja de vida.");
            console.error("Error en la respuesta del servidor:", response.status);
        }
    })
    .catch(error => {
        console.error("Error en la solicitud:", error);
    });
}
