from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
import re

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
    # elif not re.match(r'^[a-zA-Z0-9]+$', password): # Verifica que la contraseña sea alfanumérica
    #     errors['password'] = ['La contraseña debe ser alfanumérica.']

    # Validación del nombre de usuario
    if len(username) < 4:
        errors['username'] = ['El nombre de usuario debe contener 4 o mas caracteres']
    elif not username or UserModel.objects.filter(username=username).exists():
        errors['username'] = ['Nombre de usuario no válido o no disponible.']
    
    hashed_password = make_password(password)
    data['password'] = hashed_password    
    data.pop('passwordConfirm', None)

    if errors:
        raise serializers.ValidationError(errors)

    return data

def passwordpatch_validation(data,id):

    email = data.get('email', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    passwordConfirm = data.get('passwordConfirm', '').strip()
    errors = {}
    ##

    if email != '' and UserModel.objects.filter(email=email).exclude(id=id).exists():
        errors['email'] = ['Email no válido o ya está registrado.']

    # Validación de las contraseñas
    if password == '' or password == None:
        data.pop('passwordConfirm', None)
        data.pop('password', None)
    else:
        if password != passwordConfirm:
            errors['password'] = ['Las contraseñas no coinciden.']
        elif len(password) < 8:
            errors['password'] = ['Elige otra contraseña, mínimo 8 caracteres.']
        # elif not re.match(r'^[a-zA-Z0-9]+$', password): # Verifica que la contraseña sea alfanumérica
        #     errors['password'] = ['La contraseña debe ser alfanumérica.']
        data.pop('passwordConfirm', None)


    # Validación del nombre de usuario
    if len(username) < 4:
        errors['username'] = ['El nombre de usuario debe contener 4 o mas caracteres']
    elif username == '' or UserModel.objects.filter(username=username).exclude(id=id).exists():
        errors['username'] = ['Nombre de usuario no válido o no disponible.']

    if username == UserModel.objects.get(id=id).username:
        data.pop('username',None)

    if errors:
        raise serializers.ValidationError(errors)
    return data