document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('register_button').addEventListener('click', register);
    document.getElementById('login_button').addEventListener('click', login);
    document.getElementById('logout_button').addEventListener('click', logout);
    document.getElementById('upload_button').addEventListener('click', uploadResume);
});

function register() {
    const username = document.getElementById('register_username').value;
    const password = document.getElementById('register_password').value;

    fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => alert(data.message || data.error))
    .catch(error => console.error('Error:', error));
}

function login() {
    const username = document.getElementById('login_username').value;
    const password = document.getElementById('login_password').value;

    fetch('http://127.0.0.1:8000/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => alert(data.message || data.error))
    .catch(error => console.error('Error:', error));
}

function logout() {
    fetch('http://127.0.0.1:8000/api/logout/', {
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
}

function uploadResume() {
    const fileInput = document.getElementById('resume_file');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('uploaded_resume', file);

    fetch('http://127.0.0.1:8000/api/upload/', {
        method: 'POST',
        body: formData,
        credentials: 'include'  // Para enviar cookies de sesión
    })
    .then(response => response.json())
    .then(data => alert(data.message || data.error))
    .catch(error => console.error('Error:', error));
}
