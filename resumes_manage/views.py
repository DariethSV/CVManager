from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import *
from django.shortcuts import render
from django.contrib import messages
from access.models import Customer

@login_required
@require_POST
@csrf_exempt

def save_resume(request):
    user = request.user
    
    if request.method == 'POST':
        customer = Customer.objects.get(email=user.email)
        full_name = request.POST.get('full_name')
        birth_date = request.POST.get('birth_date')
        resume_email = request.POST.get('resume_email')
        phone_number = request.POST.get('phone_number')
        professional_summary = request.POST.get('professional_summary')
        company_name = request.POST.get('company_name')
        position = request.POST.get('position')
        start_date = request.POST.get('start_date')

        if  not start_date:
            start_date="1900-01-01"

        description = request.POST.get('description')
        degree = request.POST.get('degree')
        institution = request.POST.get('institution')
        start_date_education = request.POST.get('start_date_education')
        end_date_education = request.POST.get('end_date_education')
        
        if  not end_date_education:
            end_date_education="1900-01-01"

        description_education = request.POST.get('description_education')
        skills = request.POST.get('skills')
        proficiency_level = request.POST.get('proficiency_level')
        language = request.POST.get('language')
        fluency = request.POST.get('fluency')
        project_name = request.POST.get('project_name')
        description_project = request.POST.get('description_project')
        title = request.POST.get('title')
        institution_certification = request.POST.get('institution_certification')
        date_obtained = request.POST.get('date_obtained')
        if  not date_obtained:
            date_obtained="1900-01-01"

        reference_name = request.POST.get('reference_name')
        relationship = request.POST.get('relationship')
        contact_info = request.POST.get('contact_info')

        print("PERSONAL INFORMATION: ")
        print("FULL NAME: ")
        print(full_name)
        print("BIRTH DATE: ")
        print(birth_date)
        print("RESUME EMAIL: ")
        print(resume_email)
        print("PHONE NUMBER: ")
        print(phone_number)
        print("PROFESSIONAL SUMMARY: ")
        print(professional_summary)
        print("\n")
        print("EXPERIENCE: ")
        print("COMPANY NAME: ")
        print(company_name)
        print("FECHA DE EMPLEO: ")
        print(start_date)
        print("\n")
        print("EDUCATION: ")
        print("DEGREE: ")
        print(degree)
        print("INSTITUTION: ")
        print(institution)
        print("\n")
        print("PROJECTS: ")
        print("PROJECT NAME: ")
        print(project_name)
        print("\n")
        print("Languanges: ")
        print("FLUENCY LEVEL: ")
        print(fluency)
        print("\n")
        print("SKILLS: ")
        print("SKILLS: ")
        print(skills)
        print("PROFICIENCY LEVEL: ")
        print(proficiency_level)
        print("\n")
        print("LANGUAGE: ")
        print(language)

            
        resume = Resume(
            customer=customer,
            full_name=full_name,
            birth_date=birth_date,
            resume_email=resume_email,
            phone_number=phone_number,
            professional_summary=professional_summary,
            company_name=company_name,
            position=position,
            start_date=start_date,
            description=description,
            degree=degree,
            institution=institution,
            start_date_education=start_date_education, 
            end_date_education=end_date_education,
            description_education=description_education,
            skill_name=skills,
            proficiency_level=proficiency_level,
            language=language,
            fluency=fluency,
            project_name=project_name,
            description_project=description_project,
            title=title,
            institution_certification=institution_certification,
            date_obtained=date_obtained,
            reference_name=reference_name,
            relationship=relationship,
            contact_info=contact_info
        )
        resume.save()       
        messages.success(request, 'Hoja de vida creada exitosamente')
        return render(request, 'create_resume.html')

#
    else:
        messages.error(request, 'Authentication failed. Please check your credentials.')
        return render(request, 'create_resume.html')
    
        
    
    
def create_resume(request):
    return render(request, 'create_resume.html')



def show_resume(request):
    return render(request, 'show_resume.html')
