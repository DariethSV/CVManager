from itertools import chain
import json
from multiprocessing import Value
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from access.models import Customer
from itertools import chain
from django.db.models import Value
from django.db.models.functions import Concat
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@login_required
@require_POST
@csrf_exempt
def save_resume(request):
    user = request.user
    
    if request.method == 'POST':
        customer = Customer.objects.get(email=user.email)
        first_name = request.POST.get('first_name')
        surname = request.POST.get('surname')
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
        print(first_name)
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
            first_name=first_name,
            surname=surname,
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
     
@login_required 
def show_resumes(request):
    user = request.user
    resumes = Resume.objects.filter(customer=user)
    uploaded_resumes = Resume_Uploaded.objects.filter(customer=user)
    
    context = {
        'resumes': resumes,
        'uploaded_resumes': uploaded_resumes,
    }
    
    return render(request, 'show_resume.html', context)

     
@login_required    
def create_resume(request):
    return render(request, 'create_resume.html')

@login_required
def delete_resume(request, id):
    if request.method == "POST":
        resume = get_object_or_404(Resume, id=id)
        resume.delete()
        
        return redirect('show_resume')  
    return redirect('show_resume')  

@login_required
def delete_uploaded_resume(request, id):
    if request.method == "POST":
        resume = get_object_or_404(Resume_Uploaded, id=id)
        resume.delete()
        
        return redirect('show_resume')  
    return redirect('show_resume')  

@login_required
def edit_resume(request, id):
    resume = get_object_or_404(Resume, id=id)

    if request.method == 'POST':
        # Lista de todos los campos que se pueden actualizar
        fields = [
            'first_name', 'surname', 'id_card', 'birth_date', 'phone_number', 'resume_email', 'country', 'city',
            'expected_salary', 'professional_summary', 'company_name', 'position', 'start_date', 'end_date',
            'description', 'degree', 'institution', 'start_date_education', 'end_date_education',
            'description_education', 'skill_name', 'proficiency_level', 'language', 'fluency', 'project_name',
            'description_project', 'technologies_used', 'title', 'institution_certification', 'date_obtained',
            'reference_name', 'relationship', 'contact_info'
        ]

        for field in fields:
            value = request.POST.get(field)
            if value:  # Solo actualiza si el valor no está vacío
                setattr(resume, field, value)

        # Guarda los cambios en la base de datos
        resume.save()

        
        return redirect('show_resume') 
    context = {
        'resume': resume,
    }
    return render(request, 'edit_resume.html', context)


@login_required
def generate_pdf(request, resume_id):
    # Se obtienen los datos de la hoja de vida del modelo usando el `resume_id`
    resume = Resume.objects.get(id=resume_id)
    
    # Se configura la respuesta para enviar un archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="resume_{resume_id}.pdf"'
    
    # Se crea un canvas para el PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Resume of {resume.first_name}")
    p.drawString(100, 730, f"ID: {resume.id_card}")
    p.drawString(100, 710, f"Email: {resume.resume_email}")
    p.drawString(100, 690, f"Phone: {resume.phone_number}")

    p.showPage()
    p.save()

    return response

@login_required
@csrf_exempt
def select_resume(request):
    print("Entrando en select_resume")  # Verificar si la función se llama

    user = request.user
    try:
        customer = Customer.objects.get(email=user.email)
        print("Cliente encontrado:", customer)
    except Customer.DoesNotExist:
        print("No se encontró un cliente con el email proporcionado.")
        return JsonResponse({'error': 'No se encontró el cliente.'}, status=404)

    if request.method == "POST":
        print("Método POST recibido")  # Confirmar que se detecta el método POST
        
        resume_id = request.POST.get('resume_id')
        is_uploaded = request.POST.get('uploaded') == "True"
        print("resume_id obtenido:", resume_id)
        print("¿Es uploaded?:", is_uploaded)
        print("¿uploaded type?:", type(is_uploaded))

        if is_uploaded:
            resume_uploaded = Resume_Uploaded.objects.filter(id=resume_id, customer=customer).first()
            print("Resume Uploaded encontrado:", resume_uploaded)
            if resume_uploaded:
                customer.resume_used = None
                customer.resume_uploaded_used = resume_uploaded
                customer.save()
                print("CUSTOMER después de asignar resume_uploaded_used:", customer.resume_uploaded_used)
                # Agregar mensaje de éxito
                messages.success(request, "Hoja de vida subida seleccionada con éxito.")
        else:
            resume = Resume.objects.filter(id=resume_id, customer=customer).first()
            print("Resume encontrado:", resume)
            if resume:
                customer.resume_used = resume
                customer.resume_uploaded_used = None
                customer.save()
                print("CUSTOMER después de asignar resume_used:", customer.resume_used)
                # Agregar mensaje de éxito
                messages.success(request, "Hoja de vida seleccionada con éxito.")
        
        # Redirigir a `show_resume` en lugar de `select_resume`
        return redirect('show_resume')
    
    else:
        print("Método GET recibido") 
        resumes = list(chain(
            customer.resumes.all().annotate(is_uploaded=Value(False)), 
            customer.resumes_uploaded.all().annotate(is_uploaded=Value(True))
        ))
        print("Resumes obtenidos:", resumes)
        return render(request, 'select_resume.html', {'resumes': resumes})
  

@csrf_exempt
@login_required
def get_user_email(request):
    return JsonResponse({'email': request.user.email})

    
@csrf_exempt 
def save_applied_page(request):
    print("ENTROOOOOOOOOOO en save_applied_page")  # Verificar si la función se llama
    if request.method == 'POST':
        data = json.loads(request.body)
        customer_email = data.get('customer_email')
        name_page = data.get('name_page')
        url_page = data.get('url_page')

        # Intenta obtener el cliente
        try:
            customer = Customer.objects.get(email=customer_email)
            print("Cliente encontrado:", customer)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'No se encontró un cliente con el email proporcionado.'}, status=404)
            
        # Crea la página aplicada
        applied_page = Applied_pages.objects.create(
            customer=customer,
            name_page=name_page,
            url_page=url_page
        )
        print("Página aplicada guardada:", applied_page)
        return JsonResponse({'success': 'Página aplicada guardada', 'applied_page_id': applied_page.id})
    return JsonResponse({'error': 'Método no permitido.'}, status=405)


@login_required
def check_user_role(request):
    print("ENTROOOOOOOOOOO en check_user_role")  # Verificar si la función se llama
    # Verifica si el usuario es un superusuario (administrador)
    
    
    if request.user.is_superuser:
        role = 'admin'
        print("El usuario es un superusuario (administrador)")
    
    # Verifica si el usuario es el usuario específico
    elif request.user.username == 'admin@gmail.com':   
        role = 'specific_user'
        print("El usuario es el usuario específico")
    
    # Si no es ni admin ni el usuario específico, es un usuario regular
    else:
        role = 'regular_user'
        print("El usuario es un usuario regular")
    
    # Retorna el rol en formato JSON para que la extensión lo use
    return JsonResponse({'role': role})


#def admin_required(view_func):
#    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
#    return decorated_view_func

#@admin_required
def admin_dashboard(request):
    visited_pages = Applied_pages.objects.all()  
    return render(request, 'admin_dashboard.html', {'visited_pages': visited_pages})