from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

UserModel = get_user_model()

def custom_validation(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data.pop('password').strip()
    passwordConfirm = data['passwordConfirm'].strip()
    errors = {}
    ##
    if not email or UserModel.objects.filter(email=email).exists():
        errors['email'] = ['Email no válido o ya está registrado.']

    # Validación de las contraseñas
    if password != passwordConfirm:
        errors['password'] = ['Las contraseñas no coinciden.']

    elif not password or len(password) < 8:
        errors['password'] = ['Elige otra contraseña, mínimo 8 caracteres.']

    # Validación del nombre de usuario
    if not username or UserModel.objects.filter(username=username).exists():
        errors['username'] = ['Nombre de usuario no válido o no disponible.']
    
    hashed_password = make_password(password)
    data['password'] = hashed_password    
    data.pop('passwordConfirm', None)

    if errors:
        raise serializers.ValidationError(errors)

    return data