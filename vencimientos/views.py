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

    def get(self, request, usuario_id, mes, anio):
        token = Token.objects.get(key=request.auth)
        if token:
            user = token.user
            group = user.groups.all().first().id
            if user.id == usuario_id or group == 1:
                if 1 <= mes <= 12 and len(str(anio)) == 4:
                    vencimientos = Vencimiento.objects.filter(
                        propietario__id=usuario_id,
                        fecha__month=mes,
                        fecha__year=anio
                    )
                    
                    serializer = VencimientoSerializer(vencimientos, many=True)
                else:
                    return Response({"error": "Mes o año proporcionados son inválidos"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data)

    def handle_exception(self, exc):
        # Imprimir el error
        print("Error en la vista del programa:", exc)

        # Devolver una respuesta de error al cliente
        return Response(
            {"detail": "Ocurrió un error en el servidor."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class VencimientoContaViewSet(viewsets.ModelViewSet):
    queryset = Vencimiento.objects.filter(fecha__gte=date.today())
    serializer_class = VencimientoSerializer
    authentication_classes = [ExpiringTokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, IsContador ]
