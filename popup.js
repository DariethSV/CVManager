document.getElementById('data_form').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;


    fetch('http://localhost:8000/api/save-data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: name, email: email, phone:phone})
    })
    .then(response => response.json())  
    .then(data => {
        console.log(data.message); 
        alert('Datos guardados correctamente')
    })
    .catch(error => {
        alert('Hubo un error al guardar los datos. Por favor, intente de nuevo')
    });
});

document.getElementById('load_data').addEventListener('click',function(){
    fetch('http://localhost:8000/api/get_data/')
    .then(response => response.json())
    .then(data =>{
        const data_list = document.getElementById('data_list');
        const form_container = document.getElementById('form_container');
        const form_title = document.getElementById('form_title');
        const load_btn = document.getElementById('load_data');
        load_btn.style.display = 'none';
        form_container.style.display = 'none';
        form_title.style.display = 'none';


        data_list.innetHTML='';
        data.resume_data.forEach(resume => {
            const li = document.createElement('li');
            li.textContent = `Nombre: ${resume.name}, Correo: ${resume.email} Teléfono: ${resume.phone}`;
            data_list.appendChild(li);
        });

    })
    .catch(error => {
        alert('Hubo un error al guardar los datos. Por favor, intente de nuevo')
    });
});
