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
        fields = '__all__'