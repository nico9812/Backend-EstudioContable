from django.contrib.auth import get_user_model
from django.db import models

class Vencimiento(models.Model):
    nombre = models.CharField(max_length=255)
    fecha = models.DateField()
    alarma = models.BooleanField(default=False)
    propietario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='vencimientos')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre