document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('upload_button').addEventListener('click', uploadResume);
});

function uploadResume() {
    const fileInput = document.getElementById('resume_file');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('uploaded_resume', file);

    fetch('http://127.0.0.1:8000/api/upload/', {
        method: 'POST',
        body: formData,
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        alert(data.message || data.error);
        if (data.warnings && data.warnings.length > 0) {
            alert("Advertencias:\n" + data.warnings.join("\n"));
        }
    })
    .catch(error => console.error('Error:', error));
}
