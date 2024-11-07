from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json
from .models import Admin_Custom_User, Customer
from django.contrib.auth import authenticate, login

@csrf_exempt 
def register_user(request):
    if not Admin_Custom_User.objects.exists():
        admin = Admin_Custom_User.objects.create(
            email="darieth.s.v@gmail.com",
            name="CVManager Admin",
            password=make_password("1234cvmanager")
        )

    if request.method == 'POST':
        data = json.loads(request.body) #Carga lo enviado en la solicitud fetch del js de la extensión
        # Extraer datos enviados por la extensión
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Validaciones básicas
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required.'}, status=400)
        if  password != confirm_password:
            return JsonResponse({'error': 'The passwords are not the same.'}, status=400)

        # Verificar si el usuario ya existe
        if Customer.objects.filter(email=email).exists()  or Admin_Custom_User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'User with this email already exists.'}, status=400)

        # Crear el usuario
        user = Customer.objects.create(
            email=email,
            name=name,
            password=make_password(password)  # Asegúrate de guardar la contraseña cifrada
        )
        return JsonResponse({'message': 'User registered successfully.'}, status=201)

    return JsonResponse({'error': 'Invalid request method. Expected method: POST'}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request,username=email, password=password)

        if user is not None:
            login(request, user)
            if hasattr(user,"customer"):
                return JsonResponse({'message': f'Bienvenido {user.name}','customer':'si'})
            else:
                return  JsonResponse({'message': f'Bienvenido administrador {user.name}'})
        else:
            return JsonResponse({'error':'Email or password incorrects, please check it and try again'})



