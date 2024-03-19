from rest_framework import serializers
from .models import Programa


class ProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programa
        fields = '__all__'


class ProgramaSerializerWithPropietarioName(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(
        source='usuario.username', read_only=True)

    class Meta:
        model = Programa
        fields = ['id', 'nombre', 'usuario_nombre']
