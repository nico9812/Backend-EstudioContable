from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from .models import Vencimiento
from .serializer import VencimientoSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.utils import timezone
from django.conf import settings
from datetime import date
from django.contrib.auth import get_user_model

class VencimientosUsuarioView(APIView):
    def get(self, request, usuario_id):
        try:
            try:
                token = Token.objects.get(key=request.auth)
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            ahora = timezone.now()
            diferencia_segundos = (ahora - token.created).total_seconds()
            if diferencia_segundos > getattr(settings, 'TOKEN_EXPIRATION'):
                token.delete()
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            if token:
                user = token.user
                group = user.groups.all().first().id
                if user.id == usuario_id or group == 1:
                    vencimientos = Vencimiento.objects.filter(propietario__id=usuario_id,fecha__gte=date.today())
                    serializer = VencimientoSerializer(vencimientos, many=True)
                else:
                    return Response({"error": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class VencimientoContaViewSet(viewsets.ModelViewSet):
    queryset = Vencimiento.objects.filter(fecha__gte=date.today())
    serializer_class = VencimientoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        # Obtener el token de autenticación del encabezado de la solicitud
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        try:
            token = Token.objects.get(key=token)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        ahora = timezone.now()
        diferencia_segundos = (ahora - token.created).total_seconds()
        if diferencia_segundos > getattr(settings, 'TOKEN_EXPIRATION'):
            token.delete()
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if token:
            user = token.user
            group = user.groups.all().first().id
            if group != 1:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        return super().dispatch(request, *args, **kwargs)