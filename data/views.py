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
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')





@csrf_exempt
@login_required
def match_inputs_info(request):
    user = request.user
    customer = Customer.objects.get(email=user.email)
    resume = customer.resumes.first()
    if request.method == 'POST':
        data = json.loads(request.body)
        input_names = data['input_names']


        database_fields = ["first_name","surname","birth_date","email","phone_number","professional_summary","company_name","position","start_date","end_date","description""degree","institution","start_date_education","end_date_education","description_education","skill_name","proficiency_level","language","fluency","project_name","description_project","technologies_used","title","institution_certification","date_obtained","reference_name","relationship","contact_info"]

        matched_dict = {}
        matched_dict_update = {}

        input_embeddings = model.encode(input_names)
        field_embeddings = model.encode(database_fields)
        similarities = cosine_similarity(input_embeddings, field_embeddings)
        matched_indices = np.argmax(similarities, axis=1)
        matched_dict = {input_names[i]: database_fields[matched_indices[i]] for i in range(len(input_names))}

        for key,value in matched_dict.items():
            if key == "name":
                matched_dict_update[key] = resume.first_name
            elif "last_name" in key:
                matched_dict_update[key] = resume.surname
            else:
                matched_dict_update[key] = getattr(resume, value, None)
        print("MATCHED_DICT: ", matched_dict)
        print("MATCHED_DICT_UPDATE", matched_dict_update)
        return JsonResponse({'success': 'Datos emparejados', 'matched_dict': matched_dict_update})

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
def  upload_resume(request):
    if request.method == 'POST' and request.FILES.get('uploaded_resume'):
        user = request.user
        if not user.is_authenticated:
            return  JsonResponse({'error': 'User is not authenticated'}, status=401)

        uploaded_file = request.FILES['uploaded_resume']
        _ = Resume_Uploaded.objects.create(customer=user,file=uploaded_file)
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'resumes_saved'))
        filename = fs.save(uploaded_file.name, uploaded_file)  # Guarda el archivo
        file_url = fs.url(filename)
        return JsonResponse({'message': 'Archivo subido exitosamente'})
    return JsonResponse({'error': 'No se subió ningún archivo'}, status=400)
