from django.db import models
from django.contrib.auth import get_user_model

class Programa(models.Model):
    nombre = models.CharField(max_length=100)
    resolucion = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    dias = models.IntegerField()
    profesional = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre