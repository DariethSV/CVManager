// Maneja vistas de inicio, iniciar sesión, registro y cierre de sesión
document.addEventListener('DOMContentLoaded', function() {
    const is_logged_in = localStorage.getItem('user_logged_in');
    const is_customer = localStorage.getItem('is_customer');
    const log_out_button = document.getElementById('log_out_button');
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
        .then(response => response.json())
        .then(data => {
            if (data.has_resume) {
                return true
            }
            else{
                return false
            }
        })
        .catch(error => {
            console.error('Error:', error);
    });
}

// Función que redirecciona a la vista de cliente SIN hoja de vida aún
function redirect_to_customer_view(){
    const customer_view_container = document.getElementById('customer_view_container');
    const login_form_container = document.getElementById('log_in_form_container');
    const has_resume = check_customer_resume();
    const show_resume_button = document.getElementById('show_resume_button');
    const create_resume_button = document.getElementById('create_resume_button');
    const upload_resume = document.getElementById('upload_resume');
    const home_div = document.getElementById('home_div');
    home_div.style.display = 'none';
    customer_view_container.style.display='block';
    login_form_container.style.display='none';
    if(has_resume){
        show_resume_button.style.display='block';
        create_resume_button.style.display='none';
        upload_resume.style.display='none'
    }
    else{
        show_resume_button.style.display='none';
        create_resume_button.style.display='block';
        upload_resume.style.display='block'
    }
}

// Función que redirecciona a la vista de administrador (puede ver los análisis)
function redirect_to_admin_view(){
    const login_form_container = document.getElementById('log_in_form_container');
    const admin_view_container = document.getElementById('admin_view_container');
    const home_div = document.getElementById('home_div');
    home_div.style.display = 'none';
    login_form.style.display='none';
    admin_view_container.style.display='block';

}

//Función que redirige al formulario de inicio de sesión
function redirect_to_login_form(){
    const login_form_container = document.getElementById('log_in_form_container');
    const signup_form_container = document.getElementById('sign_up_form_container');
    const home_div = document.getElementById('home_div');
    home_div.style.display = 'none';
    signup_form_container.style.display='none';
    login_form_container.style.display='block';
}
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
                    alert(data.error);
                } else {
                    alert(data.message);
                    redirect_to_login_form();
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
                    alert(data.error);
                } else {
                    alert(data.message);
                    localStorage.setItem('user_logged_in', 'true');
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
    localStorage.removeItem('user_logged_in');
    localStorage.removeItem('is_customer');
    localStorage.removeItem('is_admin');
    window.location.reload(); 
}

// Función para crear hoja de vida
document.getElementById('create_resume_button').addEventListener('click', function(){
    window.open('http://localhost:8000/resume/create_resume/', '_blank');
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
            alert('Archivo subido exitosamente');
        })
        .catch(error => {
            alert('Error al subir el archivo:', error);
        });
    }
});

// Sección de detección de formularios

document.addEventListener('DOMContentLoaded', function() {
    chrome.storage.local.get('formDetected', function(result) {
        if (result.formDetected) {
            const formContainer = document.getElementById('detected_form_container');
            const customerViewContainer = document.getElementById('customer_view_container');

            if (customerViewContainer) {
                customerViewContainer.style.display = 'none';
            }

            if (formContainer) {
                formContainer.style.display = 'block';
            }


            chrome.storage.local.remove('formDetected');
        }
    });
});

