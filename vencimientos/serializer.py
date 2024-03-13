from rest_framework import serializers
from .models import Vencimiento

class VencimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vencimiento
        fields = ['id', 'nombre', 'fecha', 'alarma', 'propietario', 'is_active', 'mensualidad']


    # Esta es otra opcion de obtener las mensualidades No borres
        
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if instance.mensualidad:
    #         fecha = instance.fecha
    #         additional_data = []
    #         # Calcular el mes inicial
    #         mes = fecha.month + 1
    #         while mes < 13:
    #             nueva_fecha = fecha.replace(month=mes)
    #             additional_data.append({'nombre': representation['nombre'], 'fecha': nueva_fecha, 'alarma': representation['alarma'], 'propietario': representation['propietario'], 'is_active': representation['is_active'], 'mensualidad': representation['mensualidad']})
    #             mes += 1
    #         representation['mensualidades_adicionales'] = additional_data
    #     return representation