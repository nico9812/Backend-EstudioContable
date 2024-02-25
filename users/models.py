from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    recovery_password = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
            group= Group.objects.filter(id=2).first()
            if group:
                if not self.groups.filter(id=group.id).exists():
                    self.groups.add(group)
                else:
                    raise ValidationError("Error al guardar el usuario")
        else:
            super().save(*args, **kwargs)

