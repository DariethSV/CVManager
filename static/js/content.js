let popup_opened = false; // Bandera para controlar la apertura del popup

// Escuchador de mensajes para actualizar los inputs
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'SEND_MATCHED_DICT') {
        const matched_dict = request.data; // Mantenerlo como un objeto, no como cadena

        const inputs = Array.from(document.querySelectorAll('input, select, textarea')).filter((input) => {
            const style = window.getComputedStyle(input);
            return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && input.offsetParent !== null;
        });

        const input_names = inputs.map((input) => input.getAttribute('name'));

        // Iterar sobre cada input y textarea
        inputs.forEach(input => {
            let name = input.getAttribute('name');

            if (matched_dict.hasOwnProperty(name)) {
                input.value = matched_dict[name]; // Actualiza el valor del input
                const event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
            }
        });

        // Si necesitas responder al popup
        sendResponse({ status: 'success', message: 'Formulario autocompletado' });
    }
});


// Función de detectar formulario e inputs
function detect_form_and_inputs() {
    const form = document.querySelector('form');

    if (form && !popup_opened) {
        // Esperar un pequeño tiempo para asegurarse de que el modal esté completamente cargado en el caso que aplique
        setTimeout(() => {
            // Obtener todos los inputs dentro del formulario que sean visibles
            const inputs = Array.from(form.querySelectorAll('input, select, textarea')).filter((input) => {
                const style = window.getComputedStyle(input);
                return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && input.offsetParent !== null;
            });

            if (inputs.length > 0) {

                popup_opened = true;
                // Abrir el popup
                chrome.runtime.sendMessage({ action: 'open_popup' });
                //Enviar los inputs al popup
                

                // Mostrar un resumen de los inputs visibles
                const input_names = inputs.map(input => input.getAttribute('name') || 'sin nombre');
                setTimeout(() => {chrome.runtime.sendMessage({ type: 'FORM_DATA', data: input_names })},500);
            }
        }, 500); // Esperar 500 ms para asegurarse de que el modal esté visible

        return true;
    }

    return false;
}

// Detectar formulario inmediatamente si ya está en la página
if (!detect_form_and_inputs()) {
    // Si no hay formulario o inputs visibles, observar el DOM para detectar cambios
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            // Chequear si el modal y el formulario están visibles
            if (detect_form_and_inputs()) {
                observer.disconnect(); // Dejar de observar una vez detectado el formulario y los inputs
            }
        });
    });

    // Iniciar la observación del DOM para detectar formularios dinámicos o modales
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}





