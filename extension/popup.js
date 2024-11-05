document.getElementById("uploadButton").addEventListener("click", async function () {
    const fileInput = document.getElementById("resumeFile");
    const file = fileInput.files[0];

    if (!file) {
        document.getElementById("statusMessage").innerText = "Por favor, selecciona un archivo.";
        return;
    }

    const formData = new FormData();
    formData.append("uploaded_resume", file);

    try {
        const response = await fetch("http://127.0.0.1:8000/api/upload/", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            document.getElementById("statusMessage").innerText = "Archivo subido y procesado con éxito.";
        } else {
            document.getElementById("statusMessage").innerText = "Error: " + data.error;
        }
    } catch (error) {
        document.getElementById("statusMessage").innerText = "Error al subir el archivo.";
    }
});
