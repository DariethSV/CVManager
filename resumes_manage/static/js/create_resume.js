const personalInfoForm = document.getElementById('personal_info_form');
const workexperienceForm = document.getElementById('work_experience_form');
const educationForm = document.getElementById('education_form');
const skillsForm = document.getElementById('skills_form');
const languagesForm = document.getElementById('languages_form');
const projectsForm = document.getElementById('projects_form');
const certificationsForm = document.getElementById('certifications_form');
const referencesForm = document.getElementById('references_form');

//Añado event listener para los botones de next 
document.getElementById('next-step-1').addEventListener('click', function() {
    document.getElementById('step-1').style.display = 'none';
    document.getElementById('step-2').style.display = 'block';
});

document.getElementById('next-step-2').addEventListener('click', function() {
    document.getElementById('step-2').style.display = 'none';
    document.getElementById('step-3').style.display = 'block';
});

document.getElementById('next-step-3').addEventListener('click', function() {
    document.getElementById('step-3').style.display = 'none';
    document.getElementById('step-4').style.display = 'block';
});

document.getElementById('next-step-4').addEventListener('click', function() {
    document.getElementById('step-4').style.display = 'none';
    document.getElementById('step-5').style.display = 'block';
});

document.getElementById('next-step-5').addEventListener('click', function() {
    document.getElementById('step-5').style.display = 'none';
    document.getElementById('step-6').style.display = 'block';
});

document.getElementById('next-step-6').addEventListener('click', function() {
    document.getElementById('step-6').style.display = 'none';
    document.getElementById('step-7').style.display = 'block';
});

document.getElementById('next-step-7').addEventListener('click', function() {
    document.getElementById('step-7').style.display = 'none';
    document.getElementById('step-8').style.display = 'block';
});


document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('create_resume_form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData();

        formData.append('personal_info', JSON.stringify({
            full_name_input: document.getElementById('full_name').value,
            birth_date_input: document.getElementById('birth_date').value,
            resume_email_input: document.getElementById('resume_email').value,
            phone_number_input: document.getElementById('phone').value,
            proffessional_summary_input: document.getElementById('proffessional_summary').value
        }));

        formData.append('work_experience', JSON.stringify({
            company_name_input: document.getElementById('company_name').value,
            position_input: document.getElementById('position').value,
            start_date_input: document.getElementById('start_date').value,
            end_date_input: document.getElementById('end_date').value,
            description_input: document.getElementById('description').value
        }));

        formData.append('education', JSON.stringify({
            degree_input: document.getElementById('degree').value,
            institution_input: document.getElementById('institution').value,
            start_date_education_input: document.getElementById('start_date_education').value,
            end_date_education_input: document.getElementById('end_date_education').value,
            description_input: document.getElementById('description_education').value
        }));

        formData.append('skills', JSON.stringify({  
            skill_input: document.getElementById('skill').value,
            proficiency_level_input: document.getElementById('proficiency_level').value
        }));

        formData.append('languages', JSON.stringify({
            language_input: document.getElementById('language').value,
            fluency_input: document.getElementById('fluency').value
        }));

        formData.append('projects', JSON.stringify({
            project_name_input: document.getElementById('project_name').value,
            project_description_input: document.getElementById('project_description').value,
            technologies_used_input: document.getElementById('technologies_used').value
        }));

        formData.append('certifications', JSON.stringify({
            title_input: document.getElementById('title').value,
            institution_certification_input: document.getElementById('institution_certification').value,
            date_obtained_input: document.getElementById('date_obtained').value
        }));

        formData.append('references', JSON.stringify({
            reference_name_input: document.getElementById('reference_name').value,
            relationship_input: document.getElementById('relationship').value,
            contact_info_input: document.getElementById('contact_info').value
        }));


        fetch('../save_resume/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'multipart/form-data'
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