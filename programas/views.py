from rest_framework import viewsets, status, permissions
from .models import Programa
from .serializers import ProgramaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.db.models import Q
from users.authentication import ExpiringTokenAuthentication
from users.permissions import IsContador, IsCliente, IsOwner

class ProgramaViewSet(viewsets.ModelViewSet):
    queryset = Programa.objects.all()
    serializer_class = ProgramaSerializer
    authentication_classes = [ExpiringTokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, IsContador, ]


"""     def handle_exception(self, exc):
        # Imprimir el error
        print("Error en la vista del programa:", exc)

        # Devolver una respuesta de error al cliente
        return Response(
            {"detail": "Ocurrió un error en el servidor."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
 """


class ProgramasUsuarioAPIView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        token = Token.objects.get(key=request.auth)
        user = token.user
        group = user.groups.all().first().id
        if user.id == user_id or group == 1:
            programas = Programa.objects.filter(usuario_id=user_id)
            serializer = ProgramaSerializer(programas, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)



class ProSearchAPIView(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, search, id, format=None):
        token = Token.objects.get(key=request.auth)
        user = token.user
        group = user.groups.all().first().id
        if group == 1 or user.id == id:
            if search is not None and search != '':
                programas = Programa.objects.filter(
                    Q(nombre__icontains=search,) |
                    Q(resolucion__icontains=search) |
                    Q(localidad__icontains=search) |
                    Q(estado__icontains=search) |
                    Q(dias__icontains=search) |
                    Q(profesional__icontains=search),
                    usuario__groups__id=2,
                    usuario__id=id
                )

                serializer = ProgramaSerializer(programas, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Por favor, proporcione una palabra clave para buscar."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Sin permisos."}, status=status.HTTP_401_UNAUTHORIZED)
