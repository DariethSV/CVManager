from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import *
from django.shortcuts import render


@login_required
@require_POST
@csrf_exempt
def save_resume(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Validar información personal
        if not data.get('full_name') or not data.get('birth_date') or not data.get('resume_email') or not data.get('phone_number') or not data.get('professional_summary'):
            return JsonResponse({'error': 'Por favor, llene todos los campos de información personal'}, status=400)

        resume = Resume(
            full_name=data['full_name'],
            birth_date=data['birth_date'],
            resume_email=data['resume_email'],
            phone_number=data['phone_number'],
            professional_summary=data['professional_summary']
        )
        resume.save()

        # Procesar experiencia laboral
        work_experiences = data.get('work_experiences', [])
        for experience in work_experiences:
            work_experience = WorkExperience(
                resume=resume,
                company_name=experience['company_name'],
                position=experience['position'],
                start_date=experience['start_date'],
                end_date=experience['end_date'],
                description=experience['description']
            )
            work_experience.save()  # Guardar cada objeto WorkExperience

        # Procesar educación
        educations = data.get('educations', [])
        for edu in educations:
            education = Education(
                resume=resume,
                degree=edu['degree'],
                institution=edu['institution'],
                start_date=edu['start_date'],
                end_date=edu['end_date'],
                description=edu['description']
            )
            education.save()  # Guardar cada objeto Education

        # Procesar habilidades
        skills = data.get('skills', [])
        for skill in skills:
            skill_obj = Skill(
                resume=resume,
                skill_name=skill['skill_name'],
                proficiency_level=skill['proficiency_level']
            )
            skill_obj.save()  # Guardar cada objeto Skill

        # Procesar idiomas
        languages = data.get('languages', [])
        for lang in languages:
            language = Language(
                resume=resume,
                language=lang['language'],
                fluency=lang['fluency']
            )
            language.save()  # Guardar cada objeto Language

        # Procesar proyectos
        projects = data.get('projects', [])
        for project in projects:
            project_obj = Project(
                resume=resume,
                project_name=project['project_name'],
                description=project['description'],
                technologies_used=project['technologies_used']
            )
            project_obj.save()  # Guardar cada objeto Project

        # Procesar certificaciones
        certifications = data.get('certifications', [])
        for cert in certifications:
            certification = Certification(
                resume=resume,
                title=cert['title'],
                institution=cert['institution'],
                date_obtained=cert['date_obtained']
            )
            certification.save()  # Guardar cada objeto Certification

        # Procesar referencias
        references = data.get('references', [])
        for reference in references:
            reference_obj = Reference(
                resume=resume,
                reference_name=reference['reference_name'],
                relationship=reference['relationship'],
                contact_info=reference['contact_info']
            )
            reference_obj.save()  # Guardar cada objeto Reference

        return JsonResponse({'success': 'Hoja de vida guardada exitosamente'})

    else:
        return JsonResponse({'error': 'Error en la decodificación JSON'}, status=400)
    
    
def create_resume(request):
    return render(request, 'create_resume.html')

def show_resume(request):
    return render(request, 'show_resume.html')
