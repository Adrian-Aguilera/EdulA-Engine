from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class configChromaGeneral(models.Model):
    nameCollection = models.CharField(max_length=255)

    #funcion para validar que solo se pueda ingresar una vez
    def save(self, *args, **kwargs):
        if self.pk is None and configChromaGeneral.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de ConfigGeneral. Solo puedes modificar el existente.')
        super(configChromaGeneral, self).save(*args, **kwargs)

    def __str__(self):
        return self.nameCollection