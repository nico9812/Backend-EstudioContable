from rest_framework import serializers
from .models import DocumentoPDF
from .models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'nombre')


class DocumentoPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoPDF
        fields = ['id', 'nombre', 'archivo',
                  'propietario', 'categoria', 'fecha_creacion']

class DocumentoPDFSerializerWithPropietarioName(serializers.ModelSerializer):
    propietario_nombre = serializers.CharField(
        source='propietario.username', read_only=True)

    class Meta:
        model = DocumentoPDF
        fields = ['id', 'nombre', 'archivo',
                  'propietario_nombre', 'categoria', 'fecha_creacion']
