from rest_framework import serializers
from .models import DocumentoPDF
from .models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'nombre')


class DocumentoPDFSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(
        source='categoria.nombre', read_only=True)

    class Meta:
        model = DocumentoPDF
        fields = ['id', 'nombre', 'archivo',
                  'propietario', 'categoria', 'fecha_creacion']
