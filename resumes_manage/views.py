from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Resume
from django.shortcuts import render

@login_required
@require_POST
@csrf_exempt  


def save_resume(request):
    if request.method == 'POST':    
        data = json.loads(request.body)
        
        # Datos del formulario de información personal
        personal_info = data['personal_info']
        full_name = personal_info['full_name']
        birth_date = personal_info['birth_date']
        resume_email = personal_info['resume_email']
        phone_number = personal_info['phone_number']
        professional_summary = personal_info['professional_summary']
        
        # Validación básica
        if not full_name or not resume_email:
            return JsonResponse({'error': 'Faltan datos obligatorios'}, status=400)

        # Datos de la experiencia laboral
        work_experience = data.get('work_experience')
        company_name = work_experience.get('company_name')
        position = work_experience.get('position')
        start_date = work_experience.get('start_date')
        end_date = work_experience.get('end_date')
        description = work_experience.get('description')
        if not experience.get('company_name') or not experience.get('position'):
            return JsonResponse({'error': 'Faltan datos obligatorios'}, status=400)
                
        # Datos de la educación
        education = data['education']
        degree = data.get('degree')
        institution = data.get('institution')
        start_date_education = data.get('start_date_education')
        end_date_education = data.get('end_date_education')
        description_education = data.get('description_education')
        
        # Datos de las habilidades
        skills = data['skills']    
        skill = data.get('skill')
        proficiency_level = data.get('proficiency_level')
        
        # Datos de los idiomas
        languages_data = data.get('languages')
        language = data.get('language')
        fluency = data.get('fluency')
        
        # Datos de los proyectos
        prpjects_data = data.get('projects')
        project = data.get('project')
        description_project = data.get('description_project')
        technologies_used = data.get('technologies_used')
        
        # Datos de las certificaciones
        certifications_data = data.get('certifications')
        title = data.get('title')
        institution_certification = data.get('institution_certification')
        date_obtained = data.get('date_obtained')
        
        # Datos de las referencias
        references_data = data.get('references')
        reference_name = data.get('reference_name')
        relationship = data.get('relationship')
        contact_info = data.get('contact_info')
                

        # Crear el objeto Resume
        resume = Resume(
            full_name=full_name,
            birth_date=birth_date,
            resume_email=resume_email,
            phone_number=phone_number,
            professional_summary=professional_summary,
            work_experience=work_experience,
            education=education,
            skills=skills,
            languages=languages_data,
            projects=projects_data,
            certifications=certifications_data,
            references=references_data
            
        )
        
        #Guardar la hoja de vida en la base de datos
        resume.save()
        
        
        # Guardar experiencia laboral si está presente en los datos
        work_experience_data = data.get('work_experience')
        if work_experience_data:
            for experience in work_experience_data:
                resume.workexperience_set.create(
                    company_name=experience.get('company_name'),
                    position=experience.get('position'),
                    start_date=experience.get('start_date'),
                    end_date=experience.get('end_date'),
                    description=experience.get('description')
                )

        # Guardar educación
        education_data = data.get('education')
        if education_data:
            for edu in education_data:
                resume.education_set.create(
                    degree=edu.get('degree'),
                    institution=edu.get('institution'),
                    start_date=edu.get('start_date'),
                    end_date=edu.get('end_date'),
                    description=edu.get('description')
                )

        # Guardar habilidades
        skills_data = data.get('skills')
        if skills_data:
            for skill in skills_data:
                resume.skill_set.create(
                    skill_name=skill.get('skill_name'),
                    proficiency_level=skill.get('proficiency_level')
                )

        # Guardar idiomas
        languages_data = data.get('languages')
        if languages_data:
            for lang in languages_data:
                resume.language_set.create(
                    language=lang.get('language'),
                    fluency=lang.get('fluency')
                )

        # Guardar proyectos
        projects_data = data.get('projects')
        if projects_data:
            for project in projects_data:
                resume.project_set.create(
                    project_name=project.get('project_name'),
                    description=project.get('description'),
                    technologies_used=project.get('technologies_used')
                )

        # Guardar certificaciones
        certifications_data = data.get('certifications')
        if certifications_data:
            for cert in certifications_data:
                resume.certification_set.create(
                    title=cert.get('title'),
                    institution=cert.get('institution'),
                    date_obtained=cert.get('date_obtained')
                )

        # Guardar referencias
        references_data = data.get('references')
        if references_data:
            for reference in references_data:
                resume.reference_set.create(
                    reference_name=reference.get('reference_name'),
                    relationship=reference.get('relationship'),
                    contact_info=reference.get('contact_info')
                )

        return JsonResponse({'success': 'Hoja de vida guardada exitosamente'})

    else:
        return JsonResponse({'error': 'Error en la decodificación JSON'}, status=400)
    
def create_resume(request):
    return render(request, 'create_resume.html')

def show_resume(request):
    return render(request, 'show_resume.html')
