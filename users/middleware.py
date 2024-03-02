from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponseBadRequest


class VencimientoToken:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == 'token':
                try:
                    token = Token.objects.get(key=auth[1])
                    ahora = timezone.now()
                    diferencia_segundos = (ahora - token.created).total_seconds()
                    if diferencia_segundos > getattr(settings, 'TOKEN_EXPIRATION'):
                        token.delete()
                        return HttpResponseBadRequest("Token expirado. Por favor, inicia sesión nuevamente.")
                except Token.DoesNotExist:
                    request.auth_token = None
        else:
            request.auth_token = None

        response = self.get_response(request)
        return response
