from django.urls import path
from .views import LoginEstudiante

urlpatterns = [
    path('login', LoginEstudiante.login, name='Inicio de sesion'),
    path('Registrar', LoginEstudiante.RegistrarEstudiante, name='Registrar un estudiante'),
]