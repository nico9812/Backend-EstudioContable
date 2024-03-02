from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .models import DocumentoPDF
from .serializers import DocumentoPDFSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.http import HttpResponse
from django.conf import settings
import os
from rest_framework.authtoken.models import Token
from .models import Categoria
from .serializers import CategoriaSerializer
from django.utils import timezone


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        # Obtener el token del usuario actual
        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Calcular la diferencia en segundos
        ahora = timezone.now()
        diferencia_segundos = (ahora - token.created).total_seconds()

        # Si la diferencia es mayor a 5 segundos, eliminar el token
        if diferencia_segundos > getattr(settings, 'TOKEN_EXPIRATION'):
            token.delete()
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return super().dispatch(request, *args, **kwargs)


class ProtectedMediaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):

        try:
            token = Token.objects.get(key=request.auth)
            ahora = timezone.now()
            diferencia_segundos = (ahora - token.created).total_seconds()
            if diferencia_segundos > getattr(settings, 'TOKEN_EXPIRATION'):
                token.delete()
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = token.user
        group = user.groups.all().first().id
        doc = DocumentoPDF.objects.get(id=id)

        if (user.id == doc.propietario.id or group == 1):
            # Construir la ruta completa al archivo de medios
            full_path = os.path.join(settings.MEDIA_ROOT, doc.archivo.path)
            if not os.path.exists(full_path):
                return Response("File not found", status=404)

            # Entregar el archivo de medios
            with open(full_path, 'rb') as file:
                response = HttpResponse(
                    headers={
                        'Content-Disposition': f'attachment; filename={os.path.basename(full_path)}'},
                    content_type='application/pdf',
                    status=status.HTTP_200_OK
                )
                response.content = file
                return response

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class DocumentoPDFViewSet(viewsets.ModelViewSet):
    queryset = DocumentoPDF.objects.all()
    serializer_class = DocumentoPDFSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        # Obtener el token del usuario actual
        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Calcular la diferencia en segundos
        ahora = timezone.now()
        diferencia_segundos = (ahora - token.created).total_seconds()

        # Si la diferencia es mayor a 5 segundos, eliminar el token
        if diferencia_segundos > getattr(settings, 'TOKEN_EXPIRATION'):
            token.delete()
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        if token:
            user = token.user
            group = user.groups.all().first().id
            if group != 1:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            

        return super().dispatch(request, *args, **kwargs)


class DocumentoPDFAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):

        try:
            token = Token.objects.get(key=request.auth)
            ahora = timezone.now()
            diferencia_segundos = (ahora - token.created).total_seconds()
            if diferencia_segundos > getattr(settings, 'TOKEN_EXPIRATION'):
                token.delete()
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = token.user
        group = user.groups.all().first().id

        if (user.id == id or group == 1):
            documentos_pdf = DocumentoPDF.objects.filter(
                propietario__id=id).order_by('-fecha_creacion')
            serializer = DocumentoPDFSerializer(documentos_pdf, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class DocumentosFiltrarCatView(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, categoria, id, format=None):

        try:
            token = Token.objects.get(key=request.auth)
        except:
            print(1)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        ahora = timezone.now()
        diferencia_segundos = (ahora - token.created).total_seconds()
        if diferencia_segundos > getattr(settings, 'TOKEN_EXPIRATION'):
            token.delete()
            print(2)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = token.user
        group = user.groups.all().first().id
        if group == 1 or user.id == id:
            if categoria is not None and categoria != '':

                if categoria == 'todas':
                    documentos_pdf = DocumentoPDF.objects.filter(
                        propietario__id=id)
                else:
                    id = int(id)
                    documentos_pdf = DocumentoPDF.objects.filter(
                        categoria__id=categoria, propietario__id=id)

                serializer = DocumentoPDFSerializer(documentos_pdf, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"mensaje": "Categoria no encontrada."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(3)
            return Response({"mensaje": "Sin permisos."}, status=status.HTTP_401_UNAUTHORIZED)
