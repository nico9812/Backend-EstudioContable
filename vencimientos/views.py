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
from users.authentication import ExpiringTokenAuthentication
from users.permissions import IsContador, IsCliente, IsOwner


class VencimientosUsuarioView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, usuario_id):
        token = Token.objects.get(key=request.auth)
        if token:
            user = token.user
            group = user.groups.all().first().id
            if user.id == usuario_id or group == 1:
                vencimientos = Vencimiento.objects.filter(
                    propietario__id=usuario_id, fecha__gte=date.today())
                serializer = VencimientoSerializer(vencimientos, many=True)
            else:
                return Response({"error": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data)


class VencimientoContaViewSet(viewsets.ModelViewSet):
    queryset = Vencimiento.objects.filter(fecha__gte=date.today())
    serializer_class = VencimientoSerializer
    authentication_classes = [ExpiringTokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, IsContador ]
