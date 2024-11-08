# resume_manage/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Resume, Resume_Uploaded
from django.shortcuts import render, redirect
from django.contrib import messages
from access.models import Customer
from itertools import chain
from django.db.models import Value
from django.db.models.functions import Concat

@login_required
@require_POST
@csrf_exempt
def save_resume(request):
    user = request.user
    
    if request.method == 'POST':
        customer = Customer.objects.get(email=user.email)
        
        # Obtén los datos del formulario
        first_name = request.POST.get('first_name')
        surname = request.POST.get('surname')
        birth_date = request.POST.get('birth_date', "1900-01-01")
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        professional_summary = request.POST.get('professional_summary')
        company_name = request.POST.get('company_name', '')
        position = request.POST.get('position', '')
        start_date = request.POST.get('start_date', "1900-01-01")
        description = request.POST.get('description', '')
        degree = request.POST.get('degree', '')
        institution = request.POST.get('institution', '')
        start_date_education = request.POST.get('start_date_education', "1900-01-01")
        end_date_education = request.POST.get('end_date_education', "1900-01-01")
        description_education = request.POST.get('description_education', '')
        skills = request.POST.get('skills', '')
        proficiency_level = request.POST.get('proficiency_level', '')
        language = request.POST.get('language', '')
        fluency = request.POST.get('fluency', '')
        project_name = request.POST.get('project_name', '')
        description_project = request.POST.get('description_project', '')
        title = request.POST.get('title', '')
        institution_certification = request.POST.get('institution_certification', '')
        date_obtained = request.POST.get('date_obtained', "1900-01-01")
        reference_name = request.POST.get('reference_name', '')
        relationship = request.POST.get('relationship', '')
        contact_info = request.POST.get('contact_info', '')

        # Crea un nuevo objeto Resume con los datos obtenidos
        resume = Resume(
            customer=customer,
            first_name=first_name,
            surname=surname,
            birth_date=birth_date,
            email=email,
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
    else:
        messages.error(request, 'Authentication failed. Please check your credentials.')
        return render(request, 'create_resume.html')


def create_resume(request):
    return render(request, 'create_resume.html')


def view_resume(request):
    return render(request, 'show_resume.html')


@login_required
@csrf_exempt
def select_resume(request):
    user = request.user
    try:
        customer = Customer.objects.get(email=user.email)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'No se encontró el cliente.'}, status=404)

    if request.method == "POST":
        resume_id = request.POST.get('resume_id')
        is_uploaded = request.POST.get('uploaded') == "True"

        if is_uploaded:
            resume_uploaded = Resume_Uploaded.objects.filter(id=resume_id, customer=customer).first()
            if resume_uploaded:
                customer.resume_used = None
                customer.resume_uploaded_used = resume_uploaded
                customer.save()
        else:
            resume = Resume.objects.filter(id=resume_id, customer=customer).first()
            if resume:
                customer.resume_used = resume
                customer.resume_uploaded_used = None
                customer.save()

        return redirect('select_resume')
    
    else:
        resumes = list(chain(
            customer.resumes_manage.all().annotate(is_uploaded=Value(False)), 
            customer.resumes_uploaded_manage.all().annotate(is_uploaded=Value(True))
        ))
        return render(request, 'select_resume.html', {'resumes': resumes})



