// Maneja vistas de inicio, iniciar sesión, registro, cierre de sesión, customer views y admin view
document.addEventListener('DOMContentLoaded', function() {
    const is_logged_in = localStorage.getItem('user_logged_in');
    const is_customer = localStorage.getItem('is_customer');
    const log_out_button = document.getElementById('log_out_button');
    const log_out_button_ad = document.getElementById('log_out_button_ad');
    const login_button_home = document.getElementById('log_in_button_home');
    const signup_button_home = document.getElementById('sign_up_button_home');
    const home_div = document.getElementById('home_div');
    const login_form = document.getElementById('log_in_form_container');
    const signup_form = document.getElementById('sign_up_form_container');

    // Manejo de cierre de sesión
    if (log_out_button) {
        log_out_button.addEventListener('click', log_out);
    }

   

    // Redirección basada en estado de autenticación
    if (is_logged_in) {
        is_customer ? redirect_to_customer_view() : redirect_to_admin_view();
    } else if (home_div) {
        home_div.style.display = 'block';
    }

    // Mostrar formularios de inicio de sesión
    if (login_button_home) {
        login_button_home.addEventListener('click', function() {
            home_div.style.display = 'none';
            login_form.style.display = 'block';
            signup_form.style.display = 'none';
        });
    }

    // Mostrar formulario de registro
    if (signup_button_home) {
        signup_button_home.addEventListener('click', function() {
            home_div.style.display = 'none';
            signup_form.style.display = 'block';
            login_form.style.display = 'none';
        });
    }
});

// Función que verificar si el cliente ya tiene una hoja de vida
function check_customer_resume() {
    fetch('http://localhost:8000/api/check_customer_resume/', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error en la respuesta del servidor: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.has_resume) {
            return true;
        } else {
            return false;
        }
    })
    .catch(error => {
        console.error('Error en fetch:', error);
    });
}


// Función que redirecciona a la vista de cliente SIN hoja de vida aún o con hoja de vida
function redirect_to_customer_view(){
    const customer_view_container = document.getElementById('customer_view_container');
    const login_form_container = document.getElementById('log_in_form_container');
    const has_resume = check_customer_resume();
    const home_button = document.getElementById('home_button');
    const upload_resume = document.getElementById('upload_resume');
    const home_div = document.getElementById('home_div');
    home_div.style.display = 'none';
    customer_view_container.style.display='block';
    login_form_container.style.display='none';

    home_button.style.display='block';
    upload_resume.style.display='block';
}

// Función que redirecciona a la vista de administrador (puede ver los análisis)
function redirect_to_admin_view(){
    const login_form_container = document.getElementById('log_in_form_container');
    const admin_view_container = document.getElementById('admin_view_container');
    const home_div = document.getElementById('home_div');
    home_div.style.display = 'none';
    login_form_container.style.display='none';
    admin_view_container.style.display='block';
    const log_out_button_ad = document.getElementById('log_out_button_ad');

    if (log_out_button_ad) {
        log_out_button_ad.addEventListener('click', log_out);
    }

}

// Función que redirecciona a iniciar sesión
function redirect_to_login_form(){
    const login_form_container = document.getElementById('log_in_form_container');
    const sign_up_form_container = document.getElementById('sign_up_form_container');
    sign_up_form_container.style.display = 'none';
    login_form_container.style.display='block';
}

// Función que obtiene todas las hojas de vida del Cliente


// Función de registro de usuarios
document.getElementById('sign_up_form').addEventListener('submit',  function(event){
    event.preventDefault();
    const email_sign_up =  document.getElementById('email_sign_up');
    const name_sign_up =  document.getElementById('name_sign_up');
    const password_sign_up =  document.getElementById('password_sign_up');
    const confirm_password_sign_up =  document.getElementById('confirm_password_sign_up');

        fetch('http://localhost:8000/access/register/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        'email': email_sign_up.value,
                        'name': name_sign_up.value,
                        'password': password_sign_up.value,
                        'confirm_password': confirm_password_sign_up.value
                        })
            }).then( response => response.json())
            .then(data => {
                if (data.error) {
                    Swal.fire({
                        title: 'Error',
                        text: data.error,
                        icon: 'error',
                        confirmButtonText: 'OK',
                        background: '#f0f0f0',
                        confirmButtonColor: '#d33'
                    });
                } else {
                    Swal.fire({
                        title: '¡Éxito!',
                        text: 'Registro de usuario exitoso',
                        icon: 'success',
                        confirmButtonText: 'OK',
                        background: '#f0f0f0',
                        confirmButtonColor: '#038b71',
                    }).then((result) => {
                        if (result.isConfirmed) {
                            redirect_to_login_form();
                        }
                    });
                    
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        
});

// Función de inicio de sesión de usuarios
document.getElementById('log_in_form').addEventListener('submit',  function(event){
    event.preventDefault();
    const email_log_in =  document.getElementById('email_log_in');
    const password_log_in =  document.getElementById('password_log_in');


        fetch('http://localhost:8000/access/login/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        'email': email_log_in.value,
                        'password': password_log_in.value,
                        })
            }).then( response => response.json())
            .then(data => {
                if (data.error) {
                    Swal.fire({
                        title: 'Error',
                        text: data.error,
                        icon: 'error',
                        confirmButtonText: 'OK',
                        background: '#f0f0f0',
                        confirmButtonColor: '#d33'
                    });
                } else {
                    
                    Swal.fire({
                        title: '¡Éxito!',
                        text: data.message,
                        icon: 'success',
                        confirmButtonText: 'OK',
                        background: '#f0f0f0',
                        confirmButtonColor: '#038b71',
                    });
                    localStorage.setItem('user_logged_in', 'true');
                    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
                        chrome.tabs.sendMessage(tabs[0].id, { type: "set_login_status", status: true });
                    });
                    if(data.customer){
                        localStorage.setItem('is_customer', 'true');
                        redirect_to_customer_view();
                    

                    } 
                    else{
                        redirect_to_admin_view();
                    }
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        
});

// Función de cerrar sesión
function log_out() {
    // Limpiar el estado de la sesión
    fetch('http://localhost:8000/access/logout/',{
        method:"POST"
    })
    .then(response => {
        if (response.ok) {
            localStorage.removeItem('user_logged_in');
            localStorage.removeItem('is_customer');
            localStorage.removeItem('is_admin');
            chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
                chrome.tabs.sendMessage(tabs[0].id, { action: "set_login_status", status: false });
            });
            window.location.reload();
        } else {
            console.error("Error al cerrar sesión en el servidor.");
        }
    })
    .catch(error => {
        console.error("Error al hacer la solicitud de cierre de sesión:", error);
    });
}

// Función para crear hoja de vida
document.getElementById('home_button').addEventListener('click', function() {
    fetch('http://localhost:8000/resume/api/check_user_role/', {
        method: 'GET',
        credentials: 'include'  // Incluye las cookies para autenticación
    })
    .then(response => response.json())
    .then(data => {
        if (data.role === 'admin') {
            // Redirige a la página del administrador
            window.open('http://localhost:8000/resume/admin_dashboard/', '_blank'); 
        } else if (data.role === 'specific_user') {
            // Redirige a una página para el usuario específico
            window.open('http://localhost:8000/resume/admin_dashboard/', '_blank');  
        } else {
            // Redirige a la página regular
            window.open('http://localhost:8000/resume/view_resume/', '_blank');
        }
    })
    .catch(error => {
        console.error('Error al verificar el rol del usuario:', error);
        // Opcionalmente, redirige a la página regular en caso de error
        window.open('http://localhost:8000/resume/view_resume/', '_blank');
    });
});


// Función que envia el documento cargado a Django
document.getElementById('upload_resume_input').addEventListener('change', function(event) {
    // El evento "change"  se dispara cuando el usuario cambia el valor de un input

    const fileInput = event.target; // Obtiene el archivo del input que activó el evento "change"
    const file = fileInput.files[0]; // Captura el archivo seleccionado

    if (file) {
        const formData = new FormData();
        formData.append('uploaded_resume', file); // Agrega el archivo al FormData

        // Realiza la petición fetch al servidor Django, en este caso no se necesita el headers, el formData lo hace automáticamente 
        fetch('http://localhost:8000/api/upload/', { 
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) { // Verifica que se hizo la conexión con el servidor
                return response.json();
            } else {
                throw new Error('Error al conectar con el servidor');
            }
        })
        .then(data => {
            // Maneja la respuesta del servidor
            Swal.fire({
                title: '¡Éxito!',
                text: 'Archivo subido exitosamente',
                icon: 'success',
                confirmButtonText: 'OK',
                background: '#f0f0f0',
                confirmButtonColor: '#038b71',
            });
        })
        .catch(error => {
            Swal.fire({
                title: 'Error',
                text: 'Hubo un error en la conexión con el servidor.',
                icon: 'error',
                confirmButtonText: 'OK',
                background: '#f0f0f0',
                confirmButtonColor: '#d33'
            });
        });
    }
});



//Vista al detectar formulario
document.addEventListener('DOMContentLoaded', function() {
    chrome.storage.local.get('form_detected', function(result) {
        if (result.form_detected) {
            const formContainer = document.getElementById('detected_form_container');
            const customerViewContainer = document.getElementById('customer_view_container');

            if (customerViewContainer) {
                customerViewContainer.style.display = 'none';
            }

            if (formContainer) {
                formContainer.style.display = 'block';
            }


            chrome.storage.local.remove('form_detected');
        }
    });
});



// Función que obtiene la información de la base de datos
async function get_data() {
    try {
        const response = await fetch('http://localhost:8000/api/get_data/', {
            method: 'GET',
            credentials: 'include'
        });

        const data = await response.json();

        if (!data.error) {
            return data.resume_data; // Retornar los datos si no hay error
        } else {
            throw new Error(data.error); // Lanzar un error si hay uno
        }
    } catch (error) {
        Swal.fire({
            title: 'Error',
            text: 'Hubo un error en la conexión con el servidor.',
            icon: 'error',
            confirmButtonText: 'OK',
            background: '#f0f0f0',
            confirmButtonColor: '#d33'
        });
    }
}

// Función que hace match de los inputs names y la información de la base de datos
async function match_inputs_info(labels) {
    try {
        const response = await fetch('http://localhost:8000/api/strategy_function/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ labels: labels 
            }) 
        });

        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }

        const data = await response.json();
        if (data.success){
            return data['matched_dict'];
        }
        
    } catch (error) {
        Swal.fire({
            title: 'Error',
            text: 'Hubo un error en la conexión con el servidor.',
            icon: 'error',
            confirmButtonText: 'OK',
            background: '#f0f0f0',
            confirmButtonColor: '#d33'
        });
    }
}

var labels = [];
var dict_labels_inputs = {};
// Función que recoge los inputs detectados en la página
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'FORM_DATA') {
        labels = request.data.cleaned_keys;
        dict_labels_inputs = request.data.dict;
    }
});

// Función que detecta cuándo se hace click al botón autocompletar
document.getElementById('autocomplete_button').addEventListener('click', async function() {
    const sweet_alert_container = document.getElementById('sweet_alert_container');
    const form_container = document.getElementById('detected_form_container');

    sweet_alert_container.style.display = 'block'
    form_container.style.display = 'none'

    Swal.fire({
        title: 'Autocompletando...',
        text: 'Por favor, espera mientras autocompletamos el formulario.',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            Swal.showLoading();  // Muestra el spinner de carga
        }
    });

    const stored_labels = labels
    if (stored_labels && stored_labels.length > 0 ) {
        const matched_dict = await match_inputs_info(stored_labels);
        
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { type: 'SEND_MATCHED_DICT', data: {matched_dict:matched_dict,dict_labels_inputs:dict_labels_inputs} },function(response){
            Swal.close();  // Cierra el alert de cargando
            Swal.fire({
                title: '¡Éxito!',
                text: 'Formulario autocompletado con éxito.',
                icon: 'success',
                confirmButtonText: 'OK',
                background: '#f0f0f0',
                confirmButtonColor: '#038b71',
            }).then((result) => {
                if (result.isConfirmed) {
                    // Cerrar el popup cuando se haga clic en "OK"
                    window.close();
                }
            });
        });
        });
        
    }
});



// Evento para el botón de autocompletar
document.getElementById('autocomplete_button').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: "start_autocomplete" }, (response) => {
            if (response && response.status === 'success') {
                console.log('Información de la página recolectada y guardada con éxito:', response.pageInfo);
                alert('Información de la página recolectada y guardada.');
            } else {
                console.error('No se pudo recolectar la información de la página:', response ? response.message : "Respuesta nula");
                alert('Error al recolectar la información de la página: ' + (response ? response.message : "Respuesta nula"));
            }
        });
    });
});



document.getElementById('admin_view').addEventListener('click', () => {
    // Redirigir a la página de administración
    window.open('http://127.0.0.1:8000/resume/admin_dashboard/', '_blank');
});
