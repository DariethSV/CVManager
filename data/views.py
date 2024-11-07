from django.http import HttpResponse # type: ignore
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.core.files.storage import FileSystemStorage # type: ignore
from django.conf import settings # type: ignore
from .models import Resume
import os
import json
import PyPDF2 # type: ignore
from docx import Document # type: ignore
import re
import spacy # type: ignore
from nltk.corpus import stopwords # type: ignore

# Cargar el modelo en español de spaCy
nlp = spacy.load("es_core_news_sm")

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
import nltk
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

