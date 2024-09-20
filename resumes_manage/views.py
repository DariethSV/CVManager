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
        
        # Datos del formulario
        full_name = data.get('full_name')
        birth_date = data.get('birth_date')
        resume_email = data.get('resume_email')
        phone_number = data.get('phone_number')
        professional_summary = data.get('professional_summary')
        
        # Validación básica
        if not full_name or not resume_email:
            return JsonResponse({'error': 'Faltan datos obligatorios'}, status=400)

        # Crear el objeto Resume
        resume = Resume.objects.create(
            full_name=full_name,
            birth_date=birth_date,
            resume_email=resume_email,
            phone_number=phone_number,
            professional_summary=professional_summary
        )

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
