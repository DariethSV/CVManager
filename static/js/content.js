function detect_forms() {
    console.log('Iniciando la detección de formularios');
    const forms = document.querySelectorAll('form');
    console.log(`Número de formularios encontrados: ${forms.length}`);

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input:not([type="hidden"]), textarea, select');
        console.log(`Número de inputs encontrados en el formulario: ${inputs.length}`);

        inputs.forEach(input => {

            if (input.parentNode.querySelector('.custom-container')) {
                return; 
            }

            const container = document.createElement('div');
            container.classList.add('custom-container');
            container.style.display = 'flex';
            container.style.alignItems = 'center';
            container.style.marginBottom = '10px'; 

            const button = document.createElement('span');
            button.textContent = 'Autocompletar';
            button.style.marginLeft = '10px'; 
            button.style.cursor = 'pointer';
            button.style.color = 'blue';
            button.style.textDecoration = 'underline';

            button.onclick = () => fill_input(input);

            input.parentNode.insertBefore(container, input);

            container.appendChild(input);

            container.appendChild(button);
        });
    });
}


function fill_input(input) {
    fetch('http://localhost:8000/api/get_data/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrf_token // Incluir el token CSRF en el header
        }
    })
    .then(response => response.json())
    .then(data => {
        const resume_data = data.resume_data[0];
        if (resume_data) {
            const key = (input.name).toLowerCase();
            if (key && resume_data[key] !== undefined) {
                input.value = resume_data[key];
            } else {
                alert(`No se encontró un valor para "${key}" en los datos.`);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error al cargar los datos. Por favor, intenta de nuevo.');
    });
    }


// Llama a la función para detectar formularios
detect_forms();
