from django.urls import path
from .views import MainOption

urlpatterns = [
    path("general/chat", MainOption.get_general_chat, name="chat general"),
    path("Asistente/chat", MainOption.get_response_AV, name="chat av"),
]