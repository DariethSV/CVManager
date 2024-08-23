from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Usuario

@csrf_exempt
@require_POST
def save_data(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return JsonResponse({'error': 'Faltan datos'}, status=400)
        
        Usuario.objects.create(
            name=name,
            email=email
        )
        return JsonResponse({'message': 'Datos guardados correctamente'})
    except json.JSONDecodeError:
        return JsonResponse({'erros': 'Error en la decodificación JSON'}, status=400)

