// This file contains the JavaScript code for the create_resume.html template.

document.getElementById('create_resume_form').addEventListener('submit', event => {
    event.preventDefault();
    const data = {
        personal_info: {
            full_name: document.getElementById('full_name').value,
            birth_date: document.getElementById('birth_date').value,
            resume_email: document.getElementById('resume_email').value,
            phone_number: document.getElementById('phone_number').value,
            professional_summary: document.getElementById('professional_summary').value
            
        },
        work_experience: {
            company_name: document.getElementById('company_name').value,
            position: document.getElementById('position').value,
            start_date: document.getElementById('start_date').value,
            end_date: document.getElementById('end_date').value,
            description: document.getElementById('description').value
        },
        education: {
            degree: document.getElementById('degree').value,
            institution: document.getElementById('institution').value,
            start_date: document.getElementById('start_date_education').value,
            end_date: document.getElementById('end_date_education').value,
            description: document.getElementById('description_education').value
        },
        skills: {
            skill: document.getElementById('skill_name').value,
            proficiency_level: document.getElementById('proficiency_level').value
        },
        languages: {
            language: document.getElementById('language').value,
            fluency: document.getElementById('fluency').value
        },
        projects: {
            project_name: document.getElementById('project_name').value,
            project_description: document.getElementById('project_description').value,
            technologies_used: document.getElementById('technologies_used').value
        },
        certifications: {
            title: document.getElementById('title').value,
            institution: document.getElementById('institution_certification').value,
            date_obtained: document.getElementById('date_obtained').value
        },
        references: {
            reference_name: document.getElementById('reference_name').value,
            relationship: document.getElementById('relationship').value,
            contact_info: document.getElementById('contact_info').value
        }
    };

    fetch('/save_resume/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Resume created successfully!');
        } else {
            alert('Error: ' + data.error);
        }
    })
});