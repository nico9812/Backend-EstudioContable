import os
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DocumentoPDF
from .serializers import DocumentoPDFSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.http import HttpResponse
from django.conf import settings
from rest_framework.authtoken.models import Token
from .models import Categoria
from .serializers import CategoriaSerializer
from users.authentication import ExpiringTokenAuthentication
from users.permissions import IsContador, IsCliente, IsOwner


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated, IsContador, ]
    authentication_classes = [ExpiringTokenAuthentication]


class ProtectedMediaView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        token = Token.objects.get(key=request.auth)
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
        else:
            return Response({"mensaje": "Sin permisos."}, status=status.HTTP_401_UNAUTHORIZED)


class DocumentoPDFViewSet(viewsets.ModelViewSet):
    queryset = DocumentoPDF.objects.all()
    serializer_class = DocumentoPDFSerializer
    authentication_classes = [ExpiringTokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, IsContador]


class DocumentoPDFAPIView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):

        token = Token.objects.get(key=request.auth)
        user = token.user
        group = user.groups.all().first().id

        if (user.id == id or group == 1):
            documentos_pdf = DocumentoPDF.objects.filter(
                propietario__id=id).order_by('-fecha_creacion')
            serializer = DocumentoPDFSerializer(documentos_pdf, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"mensaje": "Sin permisos."}, status=status.HTTP_401_UNAUTHORIZED)


class DocumentosFiltrarCatView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, categoria, id, format=None):

        token = Token.objects.get(key=request.auth)
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
            return Response({"mensaje": "Sin permisos."}, status=status.HTTP_401_UNAUTHORIZED)
