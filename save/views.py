from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST,require_GET
import json
from .models import Resume

@csrf_exempt
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
    
@csrf_exempt
@require_GET
def get_data(request):
    try:
        resume_data = Resume.objects.all().values('name','email', 'phone')
        return JsonResponse({'resume_data':list(resume_data)})
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

