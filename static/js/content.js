

let popup_opened = false; // Bandera para controlar la apertura del popup

// Escuchador de mensajes para actualizar los inputs
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'SEND_MATCHED_DICT') {
        const matched_dict = request.data.matched_dict; 
        const dict_labels_inputs = request.data.dict_labels_inputs;

        // Iterar sobre cada input y textarea
        for (let key in dict_labels_inputs){
            let input = document.getElementById(dict_labels_inputs[key]);
            if ((input.type !== 'file') && matched_dict[key]){
                input.value = matched_dict[key]; // Actualiza el valor del input
                const event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
                }
            }
    }
    
    return true;
});

// Función que limpia los labels
function clean_label(label) {
        return label
            .trim() // Eliminar espacios en blanco al inicio y al final
            .replace(/\n/g, '') // Eliminar saltos de línea
            .replace(/\r/g, '') // Eliminar retornos de carro (carriage returns)
            .replace(/\t/g, '') // Eliminar tabulaciones
            .replace(/\xa0/g, ' ') // Reemplazar espacios no separables con espacios normales
            .replace(/ +/g, ' '); // Reemplazar múltiples espacios con un solo espacio
}
// Función para obtener los labels del formulario
function get_labels() {
    return Array.from(document.querySelectorAll('label')).filter(label => {
        const style = window.getComputedStyle(label);
        return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && label.offsetParent !== null;
    });
}

// Función que crea un diccionario de la forma{ (texto del label) :  (id del input asociado) }
function create_dict_labels_inputs(labels) {
    const dict = {};

    labels.forEach(label => {
        let input_id = label.getAttribute('for');
        if (!input_id) {
            // Si el label no tiene un atributo "for", busca el primer input visible dentro del contenedor
            input_id = get_first_visible_input(label);
        }
        const input_element = document.getElementById(input_id);

        // Solo incluir si el input asociado existe
        if (input_element) {
            dict[clean_label(label.textContent)] = input_id;
        }
    });

    return dict;
}

// Función que obtiene el primer input visible (usado en caso de que no se tenga atributo "for" en el label)
function get_first_visible_input(label) {
    const inputs = Array.from(label.querySelectorAll('input, select, textarea')).filter(input => {
        const style = window.getComputedStyle(input);
        return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && input.offsetParent !== null;
    });

    return inputs.length > 0 ? inputs[0].id : null;
}


// Función de detectar formulario 
function detect_form() {
    const form = document.querySelector('form');
    
    if (form && !popup_opened) {
        setTimeout(() => {
            const visible_labels = get_labels(); // Obtener los labels visibles
            const dict_labels_inputs = create_dict_labels_inputs(visible_labels); 

            if (Object.keys(dict_labels_inputs).length > 0) {
                popup_opened = true;
                chrome.runtime.sendMessage({ action: 'open_popup' });

                // Enviar el diccionario de inputs al popup
                setTimeout(() => {
                    const cleaned_keys = Object.keys(dict_labels_inputs);
                    chrome.runtime.sendMessage({ 
                        type: 'FORM_DATA', 
                        data: {
                            cleaned_keys: cleaned_keys,
                            dict:  dict_labels_inputs

                        } 
                    });
                }, 500);
            }
        }, 500); // Esperar 500 ms para asegurarse de que el modal esté visible

        return true;
    }

    return false;
}

// Detectar formulario inmediatamente si ya está en la página
if (!detect_form()) {
    // Si no hay formulario o inputs visibles, observar el DOM para detectar cambios
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            // Chequear si el modal y el formulario están visibles
            if (detect_form()) {
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





