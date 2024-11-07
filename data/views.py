# Librerías estándar de Python 
import os
import json
import re  # type: ignore

# Librerías de terceros (requieren instalación con pip)
import PyPDF2  # type: ignore
from docx import Document  # type: ignore
import spacy  
import pdfplumber  
from dotenv import load_dotenv  
from groq import Groq  
from nltk.corpus import stopwords
import nltk 

# Librerías de Django
from django.http import HttpResponse, JsonResponse  
from django.views.decorators.csrf import csrf_exempt  
from django.core.files.storage import FileSystemStorage  
from django.conf import settings  
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.middleware.csrf import get_token

# Modelos de Django del proyecto
from .models import Resume
from resumes_manage.models import Resume_Uploaded
from access.models import Customer
# Configuración de la API de Groq
load_dotenv('api_keys.env')
groq_api_key = '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'
client = Groq(api_key=groq_api_key)

# Inicialización de NLTK y spaCy
nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))
nlp = spacy.load("es_core_news_sm")


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
    


def extract_text(file_path, file_type):
    """Extrae texto del archivo dependiendo de su tipo."""
    text = ""
    if file_type == 'pdf':
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    elif file_type == 'docx':
        doc = Document(file_path)
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    return text


# Cargar el modelo de spaCy en español
nlp = spacy.load("es_core_news_sm")

# Cargar stopwords de NLTK para español

nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))

# Lista básica de nombres comunes en español (puedes ampliarla)
common_names = ["Juan", "María", "Luis", "Carlos", "Ana", "Pedro", "Carmen", "Santiago", "Laura", "Manuel"]

def extract_key_information(text):
    """
    Extrae información clave del texto del archivo, incluyendo el nombre, apellido, edad, 
    profesión, experiencia, información de contacto, educación y habilidades.
    """
    extracted_data = {
        "name": None,
        "surname": None,
        "age": None,
        "profession": None,
        "experience": None,
        "contact_info": {
            "email": None,
            "phone": None
        },
        "education": None,
        "skills": None
    }
    warnings = []

    # Divide el texto en líneas para la búsqueda
    lines = text.split('\n')
    
    # Buscar nombre y apellido usando nombres comunes
    for line in lines:
        words = line.split()
        if len(words) > 1 and words[0] in common_names:
            extracted_data["name"] = words[0]
            extracted_data["surname"] = words[1]
            break

    # Buscar edad
    age_match = re.search(r"(\d{1,2})\s*(años|AÑOS|Años)", text, re.IGNORECASE)
    if age_match:
        extracted_data["age"] = age_match.group(1)
    else:
        warnings.append("No se detectó la edad.")

    # Buscar email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if email_match:
        extracted_data["contact_info"]["email"] = email_match.group(0)
    else:
        warnings.append("No se detectó el correo electrónico.")

    # Buscar teléfono
    phone_match = re.search(r"\b\d{10}\b", text)
    if phone_match:
        extracted_data["contact_info"]["phone"] = phone_match.group(0)
    else:
        warnings.append("No se detectó el número de teléfono.")

    # Detectar profesión y experiencia (palabras comunes asociadas a profesiones)
    profession_match = re.search(r"(ingeniero|doctor|abogado|profesor|financiero|director|analista|diseñador|arquitecto)", text, re.IGNORECASE)
    if profession_match:
        extracted_data["profession"] = profession_match.group(0)
    else:
        warnings.append("No se detectó la profesión.")
    
    experience_match = re.search(r"(\d+ años de experiencia|experiencia en)", text, re.IGNORECASE)
    if experience_match:
        extracted_data["experience"] = experience_match.group(0)
    else:
        warnings.append("No se detectó experiencia laboral.")

    # Buscar educación
    education_match = re.search(r"(licenciatura|maestría|doctorado|ingeniería|carrera en [\w\s]+)", text, re.IGNORECASE)
    if education_match:
        extracted_data["education"] = education_match.group(0)
    else:
        warnings.append("No se detectó información de educación.")
    
    # Buscar habilidades
    skills_match = re.search(r"(habilidades|competencias|conocimientos en [\w\s,]+)", text, re.IGNORECASE)
    if skills_match:
        extracted_data["skills"] = skills_match.group(0)
    else:
        warnings.append("No se detectaron habilidades.")

    return extracted_data, warnings

@csrf_exempt
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('uploaded_resume'):
        uploaded_file = request.FILES['uploaded_resume']
        file_type = 'pdf' if uploaded_file.name.endswith('.pdf') else 'docx' if uploaded_file.name.endswith('.docx') else None

        if not file_type:
            return JsonResponse({'error': 'Formato de archivo no soportado'}, status=400)
        
        # Guardar el archivo temporalmente
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'resumes_saved'))
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        # Procesar el archivo y extraer texto
        text_content = extract_text(file_path, file_type)
        
        # Extraer información clave y advertencias
        extracted_data, warnings = extract_key_information(text_content)

        # Guardar la información extraída en un archivo JSON
        json_path = os.path.join(settings.MEDIA_ROOT, 'resumes_saved', f"{uploaded_file.name}.json")
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(extracted_data, json_file, ensure_ascii=False, indent=4)

        # Responder al cliente con datos extraídos y advertencias
        return JsonResponse({'message': 'Archivo procesado y guardado en JSON correctamente', 'data': extracted_data, 'warnings': warnings})
    return JsonResponse({'error': 'No se subió ningún archivo'}, status=400)

def homepage(request):
    return HttpResponse("Bienvenido a la página principal de CV Manager")

