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
from resumes_manage.models import Resume
@login_required
@require_POST
def save_data(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')

        if not name or not email:
            return JsonResponse({'error': 'Faltan datos'}, status=400)
        
        Resume.objects.create(
            name=name,
            email=email,
            phone=phone
        )
        return JsonResponse({'message': 'Datos guardados correctamente'})
    except json.JSONDecodeError:
        return JsonResponse({'erros': 'Error en la decodificación JSON'}, status=400)
    


@login_required
@require_GET
def get_data(request):

    try:
        resume_data = Resume.objects.all().values('name','email', 'phone')
        return JsonResponse({'resume_data':list(resume_data)})
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)



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
        uploaded_file = request.FILES['uploaded_resume']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'resumes_saved'))
        filename = fs.save(uploaded_file.name, uploaded_file)  # Guarda el archivo
        file_url = fs.url(filename)
        return JsonResponse({'message': 'Archivo subido exitosamente'})
    return JsonResponse({'error': 'No se subió ningún archivo'}, status=400)
