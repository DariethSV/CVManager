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
        resume = Resume.objects.create(
            full_name=data['full_name'],
            birth_date=data['birth_date'],
            resume_email=data['resume_email'],
            phone_number=data['phone_number'],
            professional_summary=data['professional_summary']
            
        )

        # Procesar experiencia laboral
        work_experiences = data.get('work_experiences', [])
        for experience in work_experiences:
            WorkExperience.objects.create(
                resume=resume,
                company_name=experience['company_name'],
                position=experience['position'],
                start_date=experience['start_date'],
                end_date=experience['end_date'],
                description=experience['description']
            )

        # Procesar educación
        educations = data.get('educations', [])
        for edu in educations:
            Education.objects.create(
                resume=resume,
                degree=edu['degree'],
                institution=edu['institution'],
                start_date=edu['start_date'],
                end_date=edu['end_date'],
                description=edu['description']
            )

        # Procesar habilidades
        skills = data.get('skills', [])
        for skill in skills:
            Skill.objects.create(
                resume=resume,
                skill_name=skill['skill_name'],
                proficiency_level=skill['proficiency_level']
            )

        # Procesar idiomas
        languages = data.get('languages', [])
        for lang in languages:
            Language.objects.create(
                resume=resume,
                language=lang['language'],
                fluency=lang['fluency']
            )

        # Procesar proyectos
        projects = data.get('projects', [])
        for project in projects:
            Project.objects.create(
                resume=resume,
                project_name=project['project_name'],
                description=project['description'],
                technologies_used=project['technologies_used']
            )

        # Procesar certificaciones
        certifications = data.get('certifications', [])
        for cert in certifications:
            Certification.objects.create(
                resume=resume,
                title=cert['title'],
                institution=cert['institution'],
                date_obtained=cert['date_obtained']
            )

        # Procesar referencias
        references = data.get('references', [])
        for reference in references:
            Reference.objects.create(
                resume=resume,
                reference_name=reference['reference_name'],
                relationship=reference['relationship'],
                contact_info=reference['contact_info']
            )

        
        return JsonResponse({'success': 'Hoja de vida guardada exitosamente'})

    else:
        return JsonResponse({'error': 'Error en la decodificación JSON'}, status=400)
    
    
def create_resume(request):
    return render(request, 'create_resume.html')

def show_resume(request):
    return render(request, 'show_resume.html')
