from django.contrib import admin
from .models import configChromaGeneral, configChromaAV, DataChromaGeneral
# Register your models here.

admin.site.register(configChromaGeneral)
admin.site.register(configChromaAV)
admin.site.register(DataChromaGeneral)