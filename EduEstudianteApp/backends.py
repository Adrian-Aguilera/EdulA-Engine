from django.contrib.auth.backends import BaseBackend
from .models import PerfilEstudiante

class PerfilBackend(BaseBackend):
    @staticmethod
    def authenticate(self, request, carnet=None, password=None, **kwargs):
        try:
            perfil = PerfilEstudiante.objects.get(carnet=carnet)
            if perfil.check_password(password):
                return perfil
        except PerfilEstudiante.DoesNotExist:
            return None
    @staticmethod
    def get_user(self, user_id):
        try:
            return PerfilEstudiante.objects.get(pk=user_id)
        except PerfilEstudiante.DoesNotExist:
            return None