from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST,require_GET
import json
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from resumes_manage.models import Resume, Resume_Uploaded
from access.models import Customer
import os
from groq import Groq
from dotenv import load_dotenv
import pdfplumber

load_dotenv('api_keys.env')
groq_api_key = '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'
client = Groq(api_key=groq_api_key)

@csrf_exempt
@login_required
def strategy_function(request):
    print("ENTROOOOOOOOOOO AL ESTRATEGY FUNCTION")
    user = request.user
    customer = Customer.objects.get(email=user.email)
    print("CUSTOMER: ", customer.email)
    if customer.resume_used:
        print("RESUME: ", customer.resume_used.id)
        return match_inputs_info_resume(request)
    elif customer.resume_uploaded_used:
        print("RESUME SUBIDO: ", customer.resume_uploaded_used.id)
        return match_inputs_info_resume_uploaded(request)

@csrf_exempt
@login_required
def match_inputs_info_resume_uploaded(request):
    user = request.user
    customer = Customer.objects.get(email=user.email)
    resume = customer.resume_uploaded_used
    if request.method == 'POST':
        matched_dict = {}
        
        data = json.loads(request.body)
        labels = data['labels']
        print("LABELS: ",labels)

        prompt = f'''Recibirás una lista de labels de un formulario para aplicar a una oferta de empleo, empareja los términos de la Lista A con la información mejor relacionada del texto B. El resultado debe ser un diccionario en formato JSON donde cada término de la Lista A se asocie con el campo más adecuado del texto B.

        Lista A: {labels}

        Lista B: {resume.content}

        El diccionario JSON el cual deberá ser compatible para usar la función json.loads() en python, debe tener la siguiente estructura: "Término de A": "información correspondiente de B". Solo incluye en el resultado aquellos términos que tengan una relación clara y precisa entre la lista A y el texto B. Si algún término de la Lista A no tiene una correspondencia clara en el texto B, no lo incluyas en el diccionario. Utiliza únicamente los términos proporcionados en las listas y asegúrate de que las asociaciones sean precisas y significativas.

        Responde únicamente con el diccionario JSON generado.'''
        response = client.chat.completions.create(
        model="gemma2-9b-it",
        temperature=0,
        top_p=1,
        messages=[{
            "role": "user",
            "content": prompt
        }]
        )

        content = response.choices[0].message.content
        content = content.replace('`','')
        content = content.replace('json','')
        content = content.strip()
        try:
            matched_dict = json.loads(content)
        except json.JSONDecodeError as e:
            print("ERROR", e)
        
        print("DICCIONARIO: ",matched_dict)
        print("=========================================================")

            


        
        return JsonResponse({'success': 'Datos emparejados', 'matched_dict': matched_dict})

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

@csrf_exempt
@login_required
def match_inputs_info_resume(request):
    user = request.user
    customer = Customer.objects.get(email=user.email)
    resume = customer.resumes.first()
    if request.method == 'POST':
        data = json.loads(request.body)
        labels = data['labels']
        print("LABELS: ",labels)

        database_fields = ["first_name","surname","birth_date","email","phone_number","professional_summary","company_name","position","start_date","end_date","description","degree","institution","start_date_education","end_date_education","description_education","skill_name","proficiency_level","language","fluency","project_name","description_project","technologies_used","title","institution_certification","date_obtained","reference_name","relationship","contact_info"]
        prompt = f'''Empareja los términos de la Lista A con los más relacionados de la Lista B. El resultado debe ser un diccionario en formato JSON donde cada término de la Lista A se asocie con el campo más adecuado de la Lista B.

        Lista A: {labels}

        Lista B: {database_fields}

        El diccionario JSON el cual deberá ser compatible para usar la función json.loads() en python, debe tener la siguiente estructura: "Término de A": "Término correspondiente de B". Solo incluye en el resultado aquellos términos que tengan una relación clara y precisa entre ambas listas. Si algún término de la Lista A no tiene una correspondencia clara en la Lista B, no lo incluyas en el diccionario. Utiliza únicamente los términos proporcionados en las listas y asegúrate de que las asociaciones sean precisas y significativas.

        Responde únicamente con el diccionario JSON generado.'''
        response = client.chat.completions.create(
        model="gemma2-9b-it",
        temperature=0,
        top_p=1,
        messages=[{
            "role": "user",
            "content": prompt
        }]
        )

        content = response.choices[0].message.content
        content = content.replace('`','')
        content = content.replace('json','')
        content = content.strip()
        try:
            matched_dict = json.loads(content)
            print(matched_dict)
        except json.JSONDecodeError as e:
            print("ERROR", e)
        matched_dict_update = {}
        inputs_not_filled = []
        for key, value in matched_dict.items():
            try:
                if(value):
                    matched_dict_update[key] = getattr(resume, value)
            except AttributeError:
                inputs_not_filled.append(key)
        
        print("DICCIONARIO: ",matched_dict_update)
        print("=========================================================")
        print("INPUTS NO COMPLETADOS: ",inputs_not_filled)

            


        
        return JsonResponse({'success': 'Datos emparejados', 'matched_dict': matched_dict_update, 'inputs_not_filled':inputs_not_filled})

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

    
    
    
@csrf_exempt
@login_required
@require_GET
def get_data(request):
    user = request.user
    customer = Customer.objects.get(email=user.email)
    # Obtener la primera hoja de vida relacionada con el cliente
    resume = customer.resumes.first()
    if resume:
        resume_data = {
            'first_name': resume.first_name,
            'surname': resume.surname,
            'birth_date': resume.birth_date,
            'email': resume.email,
            'phone_number': resume.phone_number,
            'professional_summary': resume.professional_summary,
            'company_name': resume.company_name,
            'position': resume.position,
            'start_date': resume.start_date,
            'end_date': resume.end_date,
            'description': resume.description,
            'degree': resume.degree,
            'institution': resume.institution,
            'start_date_education': resume.start_date_education,
            'end_date_education': resume.end_date_education,
            'description_education': resume.description_education,
            'skill_name': resume.skill_name,
            'proficiency_level': resume.proficiency_level,
            'language': resume.language,
            'fluency': resume.fluency,
            'project_name': resume.project_name,
            'description_project': resume.description_project,
            'technologies_used': resume.technologies_used,
            'title': resume.title,
            'institution_certification': resume.institution_certification,
            'date_obtained': resume.date_obtained,
            'reference_name': resume.reference_name,
            'relationship': resume.relationship,
            'contact_info': resume.contact_info,
        }
        return JsonResponse({'resume_data': resume_data})
    else:
        return JsonResponse({'error': 'No resume found'}, status=404)


def check_customer_resume(request):
    user = request.user
    if user.is_authenticated and hasattr(request.user, "customer"):
        has_resume = Resume.objects.filter(customer=user).exists()
        if has_resume:
            return JsonResponse({'has_resume': True})
        else:
            return JsonResponse({'has_resume': False})
    else:
        return JsonResponse({'error': 'User is not a customer'}, status=400)

@csrf_exempt
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('uploaded_resume'):
        user = request.user
        customer = Customer.objects.filter(email=user.email).first()
        if not user.is_authenticated:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)

        uploaded_file = request.FILES['uploaded_resume']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'resumes_saved'))
        filename = fs.save(uploaded_file.name, uploaded_file)  
        file_path = os.path.join(fs.location, filename)  

        # Extraer el contenido del PDF
        content = extract_content_pdf(file_path)
        print("CONTENIDO DEL PDF: ", content)
        resume_instance = Resume_Uploaded.objects.create(
            customer=customer,
            content=content,
            file=uploaded_file
        )

        return JsonResponse({'message': 'Archivo subido exitosamente', 'content': content})
    return JsonResponse({'error': 'No se subió ningún archivo'}, status=400)

def extract_content_pdf(file_path):
    content = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                content += page.extract_text() + "\n" 
    except Exception as e:
        return f"Error al extraer el contenido del PDF: {str(e)}"
    
    return content
    
