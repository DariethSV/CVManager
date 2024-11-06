from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from access.models import Customer
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

@login_required
@require_POST
@csrf_exempt

def save_resume(request):
    user = request.user
    
    if request.method == 'POST':
        customer = Customer.objects.get(email=user.email)
        full_name = request.POST.get('full_name')
        id_card = request.POST.get('id_card')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        resume_email = request.POST.get('resume_email')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')
        city = request.POST.get('city')
        expected_salary = request.POST.get('expected_salary')
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
            id_card=id_card,
            birth_date=birth_date,
            gender=gender,
            resume_email=resume_email,
            phone_number=phone_number,
            country=country,
            city=city,
            expected_salary=expected_salary,
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
    
    pass

def resume_list(request):
    resumes = Resume.objects.filter(customer=request.user)
    return render(request, 'show_resume.html', {'resumes': resumes})
     
    
def create_resume(request):
    return render(request, 'create_resume.html')

def delete_resume(request, id):
    resume = get_object_or_404(Resume, id=id)
    resume.delete()
    return redirect('show_resume')

def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=id)

    if request.method == 'POST':
        # Obtener los datos del formulario
        full_name = request.POST.get('full_name')
        experience = request.POST.get('experience')
        education = request.POST.get('education')
        skills = request.POST.get('skills')
        

        
        if full_name:
           
            resume.full_name = full_name
            resume.experience = experience
            resume.education = education
            resume.skills = skills
            resume.save()  

            return redirect('resume_detail', id=resume.id)  

        else:
            # Mostrar un mensaje de error si los campos obligatorios no están completos
            context = {
                'resume': resume,
                'error_message': 'Los campos Nombre completo y Título de trabajo son obligatorios.'
            }
            return render(request, 'edit_resume.html', context)


    context = {
        'resume': resume,
    }
    return render(request, 'edit_resume.html', context)



def generate_pdf(request, resume_id):
    # Se obtienen los datos de la hoja de vida del modelo usando el `resume_id`
    resume = Resume.objects.get(id=resume_id)
    
    # Se configura la respuesta para enviar un archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="resume_{resume_id}.pdf"'
    
    # Se crea un canvas para el PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Resume of {resume.full_name}")
    p.drawString(100, 730, f"ID: {resume.id_card}")
    p.drawString(100, 710, f"Email: {resume.resume_email}")
    p.drawString(100, 690, f"Phone: {resume.phone_number}")

    p.showPage()
    p.save()

    return response