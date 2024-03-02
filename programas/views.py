from rest_framework import viewsets, status, permissions
from .models import Programa
from .serializers import ProgramaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.conf import settings
from django.db.models import Q

class ProgramaViewSet(viewsets.ModelViewSet):
    queryset = Programa.objects.all()
    serializer_class = ProgramaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        # Obtener el token de autenticación del encabezado de la solicitud
        try:
            token = Token.objects.get(key=token)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if token:
            user = token.user
            group = user.groups.all().first().id
            if group != 1:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().dispatch(request, *args, **kwargs)
    
    def handle_exception(self, exc):
        # Imprimir el error
        print("Error en la vista del programa:", exc)
        
        # Devolver una respuesta de error al cliente
        return Response(
            {"detail": "Ocurrió un error en el servidor."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
class ProgramasUsuarioAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            try:
                token = Token.objects.get(key=request.auth)
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            
            user = token.user
            group = user.groups.all().first().id
            if user.id == user_id or group == 1:
                programas = Programa.objects.filter(usuario_id=user_id)
                serializer = ProgramaSerializer(programas, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class ProSearchAPIView(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes =[TokenAuthentication]

    def get(self, request,search,id,format=None):
        try:
            token = Token.objects.get(key=request.auth)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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
                    usuario__id = id
                ) 

                serializer = ProgramaSerializer(programas, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"mensaje": "Por favor, proporcione una palabra clave para buscar."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje": "Sin permisos."}, status=status.HTTP_401_UNAUTHORIZED)
        
    def handle_exception(self, exc):
        # Imprimir el error
        print("Error en la vista del programa:", exc)
        
        # Devolver una respuesta de error al cliente
        return Response(
            {"detail": "Ocurrió un error en el servidor."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )