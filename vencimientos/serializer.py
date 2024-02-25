from rest_framework import serializers
from .models import Vencimiento

class VencimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vencimiento
        fields = ['id', 'nombre', 'fecha', 'alarma', 'propietario', 'is_active']
