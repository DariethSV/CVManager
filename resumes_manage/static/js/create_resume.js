document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('create_resume_form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const full_name_input = document.getElementById('full_name').value;
        const birth_date_input = document.getElementById('birth_date').value;
        const resume_email_input = document.getElementById('resume_email').value;
        const phone_number_input = document.getElementById('phone_number').value;
        const professional_summary_input = document.getElementById('professional_summary').value;

        const data = {
            full_name: full_name_input,
            birth_date: birth_date_input,
            resume_email: resume_email_input,
            phone_number: phone_number_input,
            professional_summary: professional_summary_input
        };

        fetch('../save_resume/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json())
        .then( data => {
            if (data.success) {
                alert('Resume created successfully!');
            } else {
                alert('Error: ' + data.error);
            }
        })
    });
   
});