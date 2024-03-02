from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

def delete_pdf_file(sender, instance, **kwargs):
    # Eliminar el archivo asociado al documento
    if instance.archivo:
        if os.path.isfile(instance.archivo.path):
            os.remove(instance.archivo.path)


def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("El archivo debe ser un PDF.")

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
    
class DocumentoPDF(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos_pdf/', validators=[validate_pdf])
    propietario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='documentos_pdf_propios')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
pre_delete.connect(delete_pdf_file, sender=DocumentoPDF)
