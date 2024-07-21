from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class configChromaGeneral(models.Model):
    nameCollection = models.CharField(max_length=255, help_text='Ingresa el nombre de la colleccion para chat general')

    #funcion para validar que solo se pueda ingresar una vez
    def save(self, *args, **kwargs):
        if self.pk is None and configChromaGeneral.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de ConfigGeneral. Solo puedes modificar el existente.')
        super(configChromaGeneral, self).save(*args, **kwargs)

    def __str__(self):
        return self.nameCollection

class configChromaAV(models.Model):
    nameCollection = models.CharField(max_length=255, help_text='Ingresa el nombre de la colleccion para el asistente virtual')

    #funcion para validar que solo se pueda ingresar una vez
    def save(self, *args, **kwargs):
        if self.pk is None and configChromaGeneral.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de ConfigAV. Solo puedes modificar el existente.')
        super(configChromaGeneral, self).save(*args, **kwargs)

    def __str__(self):
        return self.nameCollection